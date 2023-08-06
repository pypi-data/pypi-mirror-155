#
# In this file, we're putting all database related
# code that multiple applications will need.  E.g.
# the db initialization, helper functions, and
# base classes for models.
#
import contextlib
import datetime
import json
import logging
import os
import sys
import uuid

from dateutil.parser import parse as dtparse

from itertools import chain

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.engine.url import make_url
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.types import TypeDecorator, TEXT

from .compat import str_types, iteritems
from .utils import stringify_dates

try:
    # This will throw an exception if Flask-SQLAlchemy is not in the
    # environment.
    from .flask_sqlalchemy import SQLAlchemy
except:
    # Flask-SQLAlchemy is not in the environment, then simply use our
    # own wrapper for SQLAlchemy
    from .rhodb_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)


class Base(object):
    added_datetime = Column(DateTime, default=func.now())
    changed_datetime = Column(
        DateTime,
        default=func.now(),
        onupdate=func.current_timestamp()
    )

    def update_columns(self, **kwargs):
        """ Allows you to overwrite values from an unpacked dictionary
            like cls.update_columns(foo=10, bar="kyle")
        """
        for field, field_value in iteritems(kwargs):
            if hasattr(self, field):
                setattr(self, field, field_value)

    @classmethod
    def pk_exists(cls, pks, pk='id'):
        """ Given a list of pimary keys, returns True or False, depending
            on if each pk exists in the database or not.
        """
        field = getattr(cls, pk)
        query = cls.query.with_entities(field).filter(field.in_(pks))
        found_set = set(result[0] for result in query)
        return [(pk in found_set) for pk in pks]

    @classmethod
    def get_by_pk(cls, pks, pk='id'):
        """ Get objects by primary key. Can return either a list or
            a single instance depending on if it is passed a list or not
            as input.
        """
        field = getattr(cls, pk)
        if isinstance(pks, list):
            result = cls.query.filter(field.in_(pks)).all()
        else:
            result = cls.query.filter(field == pks).one()
        return result

    @classmethod
    def _column_type(cls, kls, field):
        """ Returns the python type for a particular model column/field.
        """
        try:
            return getattr(kls, field).property.columns[0].type.python_type
        except NotImplementedError:
            logger.info("Couldn't get property type on field {0}.{1}"
                        .format(kls, field))
        except Exception as e:  # pragma: no cover
            logger.exception(e)  # pragma: no cover
            return None  # pragma: no cover

    @classmethod
    def _column_is_timedelta(cls, kls, field):
        if cls._column_type(kls, field) == datetime.timedelta:
            return True
        return False

    @staticmethod
    def _parse_datetime(datetime_string):
        """ Takes a string, returns a datetime.datetime instance
        """
        return dtparse(datetime_string)

    @classmethod
    def transform_datetime_fields(cls, d):
        """ Takes a dictionary and returns a copy of it in which
            datetime fields are appropriate python objects, instead
            of e.g. ints or floats or strings. Alters d in place.
        """
        for field, field_value in iteritems(d):
            if field_value is None:
                continue
            if 'datetime' in field:
                field_value = cls._parse_datetime(field_value)
            elif cls._column_is_timedelta(cls, field):
                field_value = datetime.timedelta(
                    seconds=field_value
                )
            d[field] = field_value

    @classmethod
    def from_dict(cls, d, transform_datetimes=True):
        """ Create an instance of the model from a dictionary. If
            `transform_datetimes` is True and a field looks like a
            datetime, we'll try to transform it as such. This is
            useful for
        """
        entity = cls()
        cls.transform_datetime_fields(d)
        for field, field_value in iteritems(d):
            if field_value is not None:
                try:
                    setattr(entity, field, field_value)
                except NotImplementedError:  # pragma: no cover
                    logger.info("Couldn't set attribute {0} on object {1} to "
                                "{2}".format(field, entity, field_value))   # pragma: no cover
                except Exception as e:  # pragma: no cover
                    logger.exception(e)  # pragma: no cover
        return entity

    @classmethod
    def equality_filter(cls, *args, **kwargs):
        """ Can be passed dictionaries and kwargs to
            do a filter on this class. So, you can, e.g. do
            Race.equality_filter(track_id='rir', series_id='W')
        """
        q = cls.query

        def f(q, x):
            for k, v in iteritems(x):
                q = q.filter(getattr(cls, k) == v)
            return q

        for arg in args:
            q = f(q, arg)
        q = f(q, kwargs)
        return q

    def duplicate(self, **overloads):
        """ Creates a copy of an instance of a model, excluding
            all columns that are primary keys. Will apply overloads
            after making the duplicate. Does not commit.
        """
        duplicate = self.__class__()
        primary_keys = set(self._primary_key_columns)
        for col in self._columns:
            if col not in primary_keys:
                setattr(duplicate, col, getattr(self, col))

        for col, value in iteritems(overloads):
            setattr(duplicate, col, value)

        return duplicate

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        return '<{0} instance>'.format(self.__class__.__name__)

    @staticmethod
    def stringify_dates(x):
        return stringify_dates(x)

    @staticmethod
    def id_dammit(object_or_id):
        """ Get the id of an object
        """
        if hasattr(object_or_id, 'id'):
            return object_or_id.id
        return object_or_id

    @classmethod
    def instance_dammit(cls, object_or_id, pk='id'):
        """ Get an object
        """
        if isinstance(object_or_id, cls):
            return object_or_id
        return cls.query.filter(getattr(cls, pk) == object_or_id).one()

    @property
    def _primary_key_columns(self):
        """ Get a list of all the columns that are part of the
            primary key for this object.
        """
        return [
            a.key for a in
            self.__mapper__.primary_key
            if isinstance(a, Column)
        ]

    @property
    def _columns(self):
        """ Get all the columns that are defined for this model
        """
        return [
            a.key for a in
            self.__mapper__.attrs
            if isinstance(a, ColumnProperty)
        ]

    def to_dict(self, string_dates=True, extra_columns=None):
        """ Returns a representation of this instances as a
            regular python dictionary.  Generally used for
            serializing to JSON. Only serializes those fields
            referred to in the __serializable_columns__ attribute.
        """
        if hasattr(self, '__serializable_columns__'):
            cols = self.__serializable_columns__
        elif hasattr(self, '__unserializable_columns__'):
            cols = [
                col for col in self._columns
                if col not in self.__unserializable_columns__
            ]
        else:
            raise NotImplementedError

        if not extra_columns:
            extra_columns = []

        def getattr_plus(k):
            v = getattr(self, k)
            if isinstance(v, uuid.UUID):
                v = str(v)
            elif string_dates:
                v = self.stringify_dates(v)
            return v

        retval = dict(
            (k, getattr_plus(k))
            for k in chain(cols, extra_columns)
        )
        return retval


class BaseWithIntPK(Base):
    id = Column(Integer, primary_key=True)


# The following two classes are used to implement the
# recipe shown here:
# http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/mutable.html
# for mutable JSON/dictionary columns.
#
# Looks like Postgresql's JSON type is not yet supported by SQLA.
#
class JSONEncodedDict(TypeDecorator):
    """ Represents an immutable structure as a json-encoded string.
    """

    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionaries to MutableDict.

        :param key: The dictionary key.
        :param value: The dictionary value.
        """

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


def run_db_commands(cmds, database, dialect):
    if dialect == 'postgres':
        import psycopg2
        conn = psycopg2.connect(database=database,
                                host='127.0.0.1',
                                user='postgres')
        conn.autocommit = True
    elif dialect == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host='127.0.0.1',
                               user='root',
                               db=database,
                               autocommit=True)
    else:
        raise Exception('Dialect {0} not supported.'.format(dialect))

    if isinstance(cmds, str_types):
        cmds = [cmds]

    cur = conn.cursor()
    for cmd in cmds:
        cur.execute(cmd)
    cur.close()
    conn.close()


def run_postgres_commands(cmds, database='postgres'):
    """ Run Postgres commands with autocommit

    :param cmds: List of commands.
    :param database: Defaults to postgres.
    """
    return run_db_commands(cmds, database, 'postgres')


def run_mysql_commands(cmds, database='mysql'):
    """ Run MySQL commands with autocommit.

    :param: cmds: List of commands.
    :param database: Defaults to mysql.
    """
    return run_db_commands(cmds, database, 'mysql')


def create_tables(db):
    """ Creates all tables in the database based on the SQLAlchemy models
    """
    db.create_all()


def drop_tables(db):
    """ Drops all the tables from the database
    """
    db.drop_all()


def reload_tables(db):
    """ Re-creates all tables in the database
    """
    drop_tables(db)
    create_tables(db)


def create_database(dbname, dialect='postgres'):
    """ Creates a Postgres database using psycopg2.

    :param dbname: The name of the database.
    """
    run_db_commands('CREATE DATABASE {0}'.format(dbname), dialect, dialect)


def enable_hstore_extension(dbname):
    """ Enables the hstore extension on the given database.

    :param dbname: The name of the database.
    """
    run_postgres_commands('CREATE EXTENSION IF NOT EXISTS hstore', dbname)


def disable_hstore_extension(dbname, cascade=False):
    """ Disables the hstore extension on the given database.

    :param dbname: The name of the database.
    :param cascade: Whether to auto drop objects that depend on HSTORE
    """

    sql = 'DROP EXTENSION IF EXISTS hstore'
    if cascade:
        sql += ' CASCADE'

    run_postgres_commands(sql, dbname)


def drop_database(dbname, dialect='postgres'):
    """ Drops a Postgres database using psycopg2.

    :param dbname: The name of the database.
    """
    run_db_commands('DROP DATABASE IF EXISTS {0}'.format(dbname),
                    dialect,
                    dialect)


def clear_all_tables(db):
    """ Clears all tables in the database """

    with contextlib.closing(db.engine.connect()) as con:
        trans = con.begin()
        for table in reversed(db.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()
