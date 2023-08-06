import os
import re
import sqlalchemy
from sqlalchemy import create_engine, event
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import scoped_session, sessionmaker, class_mapper, Query
from sqlalchemy.orm.exc import UnmappedClassError

from .compat import itervalues

_camelcase_re = re.compile(r'([A-Z]+)(?=[a-z0-9])')


def _make_table(db):
    def _make_table(*args, **kwargs):
        if len(args) > 1 and isinstance(args[1], db.Column):
            args = (args[0], db.metadata) + args[1:]
        info = kwargs.pop('info', None) or {}
        info.setdefault('bind_key', None)
        kwargs['info'] = info
        return sqlalchemy.Table(*args, **kwargs)
    return _make_table


def _include_sqlalchemy(obj):
    for module in sqlalchemy, sqlalchemy.orm:
        for key in module.__all__:
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))
    # Note: obj.Table does not attempt to be a SQLAlchemy Table class.
    obj.Table = _make_table(obj)
    obj.event = event


def _should_set_tablename(bases, d):
    """Check what values are set by a class and its bases to determine if a
    tablename should be automatically generated.
    The class and its bases are checked in order of precedence: the class
    itself then each base in the order they were given at class definition.
    Abstract classes do not generate a tablename, although they may have set
    or inherited a tablename elsewhere.
    If a class defines a tablename or table, a new one will not be generated.
    Otherwise, if the class defines a primary key, a new name will be generated.
    This supports:
    * Joined table inheritance without explicitly naming sub-models.
    * Single table inheritance.
    * Inheriting from mixins or abstract models.
    :param bases: base classes of new class
    :param d: new class dict
    :return: True if tablename should be set
    """

    if '__tablename__' in d or '__table__' in d or '__abstract__' in d:
        return False

    if any(v.primary_key for v in itervalues(d) if isinstance(v, sqlalchemy.Column)):
        return True

    for base in bases:
        if hasattr(base, '__tablename__') or hasattr(base, '__table__'):
            return False

        for name in dir(base):
            attr = getattr(base, name)

            if isinstance(attr, sqlalchemy.Column) and attr.primary_key:
                return True


class _BoundDeclarativeMeta(DeclarativeMeta):

    def __new__(cls, name, bases, d):
        if _should_set_tablename(bases, d):
            def _join(match):
                word = match.group()
                if len(word) > 1:
                    return ('_%s_%s' % (word[:-1], word[-1])).lower()
                return '_' + word.lower()
            d['__tablename__'] = _camelcase_re.sub(_join, name).lstrip('_')

        return DeclarativeMeta.__new__(cls, name, bases, d)

    def __init__(self, name, bases, d):
        bind_key = d.pop('__bind_key__', None)
        DeclarativeMeta.__init__(self, name, bases, d)
        if bind_key is not None:
            self.__table__.info['bind_key'] = bind_key


class _QueryProperty(object):

    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = class_mapper(type)
            if mapper:
                return type.query_class(mapper, session=self.sa.session())
        except UnmappedClassError:  # pragma: no cover
            return None  # pragma: no cover


class Model(object):

    query_class = Query
    query = None


class SQLAlchemy(object):
    """ This class is used to integrate SQLAlchemy outside of Flask
    applications.

    :param use_native_unicode: True or False. Used to tell the underlying
                               driver if it should use native unicode.
    :param session_options: Any options to pass when creating a session through
                            :func:`sqlalchemy.orm.sessionmaker` and
                            :func:`sqlalchemy.orm.scoped_session`.
    :param metadata: Any metadata to pass to
                     :func:`sqlalchemy.ext.declarative_base`.
    """

    def __init__(self, use_native_unicode=True, session_options=None,
                 metadata=None, database_uri=None, engine_options=None):
        self.use_native_unicode = use_native_unicode
        self.Model = self.make_declarative_base(metadata=metadata)
        self.engine = None
        self.session = None
        self.init_session(database_uri, session_options, engine_options)
        _include_sqlalchemy(self)

    @property
    def metadata(self):
        """ Returns the metadata """
        return self.Model.metadata

    def init_session(self, database_uri=None, session_options=None,
                     engine_options=None):
        if self.session:
            self.session.remove()
        self.engine = self.create_engine(engine_options, database_uri)
        self.session = self.create_scoped_session(session_options)

    def create_engine(self, options=None, database_uri=None):
        """ Creates a new engine with the given options and returns it.

        :param options: Subset of options to be passed to ``create_engine``
        """

        db_uri = database_uri if database_uri is not None\
            else os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite://')

        info = make_url(db_uri)
        if options is None:
            options = {}
        self.apply_engine_options(options)
        self.apply_driver_hacks(info, options)

        return create_engine(info, **options)

    def make_declarative_base(self, metadata=None):
        base = declarative_base(cls=Model, name='Model',
                                metadata=metadata,
                                metaclass=_BoundDeclarativeMeta)
        base.query = _QueryProperty(self)
        return base

    def create_scoped_session(self, options=None):
        """ Creates a new scoped session.

        :param options: Subset of options to be passed to ``sessionmaker`` and
                        ``scoped_session``.
        """
        if options is None:
            options = {}

        scopefunc = None
        if 'scopefunc' in options:
            scopefunc = options['scopefunc']
            del options['scopefunc']

        session_factory = sessionmaker(bind=self.engine, **options)
        Session = scoped_session(session_factory, scopefunc=scopefunc)
        return Session

    def apply_engine_options(self, options):
        def isint(val):
            try:
                int(val)
                return True
            except:
                return False

        def _setdefault(optionkey, envkey):
            value = os.environ.get(envkey, None)
            if value is not None:
                if value.lower() == 'true':
                    options[optionkey] = True
                elif value.lower() == 'false':
                    options[optionkey] = False
                elif isint(value):
                    options[optionkey] = int(value)
                else:
                    options[optionkey] = value

        _setdefault('echo', 'SQLALCHEMY_ECHO')
        _setdefault('pool_size', 'SQLALCHEMY_POOL_SIZE')
        _setdefault('pool_timeout', 'SQLALCHEMY_POOL_TIMEOUT')
        _setdefault('pool_recycle', 'SQLALCHEMY_POOL_RECYCLE')
        _setdefault('max_overflow', 'SQLALCHEMY_MAX_OVERFLOW')

    def apply_driver_hacks(self, info, options):
        """This method is called before engine creation and used to inject
        driver specific hacks into the options.

        :param info: The URI info.
        :param options: dictionary of keyword arguments that will then be used
        to call the :func:`sqlalchemy.create_engine` function.
        The default implementation provides some saner defaults for things
        like pool sizes for MySQL and sqlite.
        """
        # This method was copied directly from Flask-SQLAlchemy
        if info.drivername.startswith('mysql'):
            info.query.setdefault('charset', 'utf8')
            if info.drivername != 'mysql+gaerdbms':
                options.setdefault('pool_size', 10)
                options.setdefault('pool_recycle', 7200)
        elif info.drivername == 'sqlite':
            pool_size = options.get('pool_size')
            detected_in_memory = False
            # we go to memory and the pool size was explicitly set to 0
            # which is fail.  Let the user know that
            if info.database in (None, '', ':memory:'):
                detected_in_memory = True
                from sqlalchemy.pool import StaticPool
                options['poolclass'] = StaticPool
                if 'connect_args' not in options:
                    options['connect_args'] = {}
                options['connect_args']['check_same_thread'] = False

                if pool_size == 0:
                    raise RuntimeError('SQLite in memory database with an '
                                       'empty queue not possible due to data '
                                       'loss.')
            # if pool size is None or explicitly set to 0 we assume the
            # user did not want a queue for this sqlite connection and
            # hook in the null pool.
            elif not pool_size:
                from sqlalchemy.pool import NullPool
                options['poolclass'] = NullPool

            # if it's not an in memory database we make the path absolute.
            if not detected_in_memory:
                info.database = info.database

        if not self.use_native_unicode:
            options['use_native_unicode'] = False

    def create_all(self):
        self.metadata.create_all(self.engine)

    def drop_all(self):
        self.metadata.drop_all(self.engine)
