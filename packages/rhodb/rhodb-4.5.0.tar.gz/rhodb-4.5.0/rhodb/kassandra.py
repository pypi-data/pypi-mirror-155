import datetime
import json
import logging
import os
import ssl
import uuid

from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection, ValidationError, columns
from cassandra.cqlengine.models import Model
from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy

from .utils import stringify_dates

logger = logging.getLogger(__name__)


FLASK_EXTENSION_NAME = 'cassandra'


class CassandraDBCOnfig(object):

    hosts = None
    keyspace = None
    username = None
    password = None
    consistency_level = 'ALL'
    ssl_options = None


class FlaskCassandra(object):

    def __init__(self, app=None):
        logger.warning("Cassandra support will be deprecated in the next "
                       "major release...")
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        ssl_options = None
        if app.config.get('CASSANDRA_ENABLE_SSL', False):
            ssl_options = {
                'ssl_version': ssl.PROTOCOL_TLSv1,
                'ca_certs': app.config.get('CASSANDRA_SSL_CERT', None),
                'keyfile': app.config.get('CASSANDRA_USER_KEY', None),
                'certfile': app.config.get('CASSANDRA_USER_CERT', None)
            }

        cs = Cassandra(
            hosts=app.config.get('CASSANDRA_HOSTS', None),
            port=app.config.get('CASSANDRA_PORT', 9042),
            keyspace=app.config.get('CASSANDRA_KEYSPACE', None),
            username=app.config.get('CASSANDRA_USERNAME', None),
            password=app.config.get('CASSANDRA_PASSWORD', None),
            consistency_level=\
                app.config.get('CASSANDRA_CONSISTENCY_LEVEL', 'QUORUM'),
            ssl_options=ssl_options,
            local_region=app.config.get('CASSANDRA_LOCAL_REGION', None),
            remote_hosts=\
                app.config.get('CASSANDRA_REMOTE_HOSTS', 0)
        )

        session = cs.connect()

        # Store the extension in the app
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions[FLASK_EXTENSION_NAME] = cs
        self.app = app


class Cassandra(object):

    def __init__(self, hosts, port=9042, keyspace=None, username=None,
                 password=None, consistency_level=None, ssl_options=None,
                 local_region=None, remote_hosts=0):
        logger.warning("Cassandra support will be deprecated in the next "
                       "major release...")
        self.hosts = hosts
        self.port = port
        self.keyspace = keyspace
        self.username = username
        self.password = password
        self.consistency_level = consistency_level
        self.ssl_options = ssl_options
        self.local_region = local_region
        self.session = None

        # number of hosts in remote dc to connect to, default 0
        self.remote_hosts = remote_hosts

    def connect(self):
        # The cassandra uwsgi integration states that we should close any
        # existing connections before we open a new one. See:
        # https://datastax.github.io/python-driver/cqlengine/third_party.html#uwsgi
        # So, we try to close any existing connection first.
        self._disconnect()

        # Setup a session if is not already available
        if connection.session is None:
            kwargs = {}
            if self.username and self.password:
                kwargs['auth_provider'] = PlainTextAuthProvider(
                    username=self.username,
                    password=self.password
                )

            if self.ssl_options:
                kwargs['ssl_options'] = self.ssl_options

            if self.local_region:
                kwargs['load_balancing_policy'] = TokenAwarePolicy(
                    DCAwareRoundRobinPolicy(
                        self.local_region,
                        used_hosts_per_remote_dc=self.remote_hosts)
                )

            consistency = ConsistencyLevel.name_to_value.get(
                self.consistency_level, ConsistencyLevel.ALL)
            connection.setup(self.hosts, self.keyspace, consistency, **kwargs)
            logger.info("Opened connection to Cassandra cluster.")

            self.session = connection.session
        return connection.session

    def disconnect(self):
        self._disconnect()
        logger.info("Closed connection to Cassandra cluster.")

    def _disconnect(self):
        if connection.cluster is not None:
            connection.cluster.shutdown()
        if connection.session is not None:
            connection.session.shutdown()


class CassandraModel(Model):
    __abstract__ = True

    def to_dict(self):
        """ Converts a cassandra model to a dict.

        If `__serializable_columns__` is defined, then it uses the list of
        columns specified in this variable to create the dict.

        If `__unserializable_columns__`, it will use the list of defined columns
        from the model minus the list in `__unserializable_columns__` to
        create the dict.

        If neither `__serializable_columns__` nor `__unserializable_columns__`
        is specified, the it simply uses the list of defined columns in the
        model to create the dict.
        """
        if hasattr(self, '__serializable_columns__'):
            cols = self.__serializable_columns__
        elif hasattr(self, '__unserializable_columns__'):
            cols = [col for col in self._defined_columns.keys()
                    if col not in self.__unserializable_columns__]
        else:
            cols = self._defined_columns.keys()

        def _getattr(k):
            v = getattr(self, k)
            if isinstance(v, uuid.UUID):
                return str(v)
            else:
                return stringify_dates(v)

        retval = {k: _getattr(k) for k in cols}
        return retval

    def validate(self):
        # Some of the messages in the Cassandra validation errors are UGLY, so
        # let's replace them here
        try:
            super(CassandraModel, self).validate()
        except ValidationError as e:
            if 'None values are not allowed' in e.message:
                raise ValidationError(
                    e.message.replace('- None values are not allowed',
                                      'is required'))
            elif 'is shorter than 1 characters' in e.message:
                raise ValidationError(
                    e.message.replace('shorter than 1 characters', 'required'))
            else:
                raise

    @classmethod
    def get_by_pk(cls, pks):
        """ Get objects by primary key.

        Args:
            pks: Dict mapping pk field to list of values. Example:
                {
                    field_1: [val1, val2],
                    field_2: [val3, val4]
                }
        """

        q = cls.objects()
        for key, values in pks.iteritems():
            field = getattr(cls, key)
            q = q.filter(field.in_(values))

        return q.all()


class TextJSON(columns.Column):
    """
    Stores a UTF-8 encoded string
    """
    db_type = 'text'

    def to_python(self, value):
        try:
            if type(value) == dict:
                return value
            return json.loads(value)
        except ValueError:
            raise ValidationError("{0} {1} is not valid JSON"
                                  .format(self.column_name, value))

    def to_database(self, value):
        """
        Converts python value into database value
        """
        val = value
        if val is None and self.has_default:
            val = self.get_default()
        if type(val) != dict:
            raise ValidationError("{0} {1} can't be converted to JSON value"
                                  .format(self.column_name, value))
        return json.dumps(val)
