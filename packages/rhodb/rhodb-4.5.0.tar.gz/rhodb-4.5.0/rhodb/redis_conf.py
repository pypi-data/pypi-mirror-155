from __future__ import print_function

import os
import logging
import re

from collections import namedtuple
from redis import __version__ as redis_version, StrictRedis, ConnectionPool
from redis.sentinel import Sentinel

from .compat import urlparse, iteritems

logger = logging.getLogger(__name__)


SentinelConfig =\
    namedtuple('SentinelConfig', ['hosts', 'options', 'service_name'])

redis_pattern = re.compile(r'2\.\d+\.\d+')


class FlaskRedis(object):

    EXTENSION_NAME = 'flask_redis'

    def __init__(self, app=None, using_sentinel=False, **kwargs):
        if app is not None:
            self.init_app(app, using_sentinel, **kwargs)

    def init_app(self, app, using_sentinel=False, **kwargs):
        redis_url = app.config.get('REDIS_URL', None)

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        if using_sentinel:
            if redis_url is None:
                self.master = None
                self.slave = None
            else:
                sentinel = SentinelRedisConnector(redis_url)
                self.master = sentinel.get_master_connection()
                self.slave = sentinel.get_slave_connection()
        else:
            if redis_url is None:
                self.master = None
            else:
                rc = RedisConnector(redis_url, **kwargs)
                self.master = rc.get_connection()
        app.extensions[self.EXTENSION_NAME] = self
        self.app = app


class SentinelRedisConnector(object):

    def __init__(self, sentinel_url):
        self.sentinel_config = self._parse_url(sentinel_url)
        options = self.sentinel_config.options
        if (redis_pattern.match(redis_version)):
            options = {
                'password': self.sentinel_config.options.get('password', None),
                'socket_timeout':
                    self.sentinel_config.options.get('socket_timeout', None),
                'min_other_sentinels':
                    self.sentinel_config.options.get('min_other_sentinels', 0),
            }

        self.sentinel = Sentinel(self.sentinel_config.hosts, **options)

    def _parse_url(self, sentinel_url):
        if sentinel_url is None:
            raise ValueError('Invalid conneciton url: {}'.format(sentinel_url))

        url = urlparse.urlparse(sentinel_url)
        if url.scheme != 'redis+sentinel':
            raise ValueError('Unsupported scheme: {}'.format(url.scheme))

        path_parts = url.path.split('/')
        if len(path_parts) < 3:
            raise ValueError("Invalid path: {0}. Must be of the form "
                             "/cluster-name/db-number".format(url.path))

        sentinel_option_types = {
            'min_other_sentinels': int,
            'socket_timeout': float
        }
        connection_options = {
            'db': int(path_parts[2])
        }

        if '@' in url.netloc:
            auth, hostspec = url.netloc.split('@', 1)

            if ':' in auth:
                _, password = auth.split(':', 1)
                connection_options['password'] = password
        else:
            hostspec = url.netloc

        hosts = self._parse_hosts(hostspec)

        for name, value in iteritems(urlparse.parse_qs(url.query)):
            if name not in sentinel_option_types:
                continue

            if len(value) > 1:
                raise ValueError('Multiple values specified for {}'
                                 .format(name))

            _type = sentinel_option_types[name]
            connection_options[name] = _type(value[0])

        return SentinelConfig(hosts, connection_options, path_parts[1])

    def _parse_hosts(self, hostspec):
        hosts = []
        for hp in hostspec.split(','):
            if ':' in hp:
                host, port = hp.split(':', 1)
                port = int(port)
            else:
                host = hp
                port = 26379  # default sentinel port

            hosts.append((host, port))

        return hosts

    def get_master_connection(self):
        return self.sentinel.master_for(self.sentinel_config.service_name,
                                        **self.sentinel_config.options)

    def get_slave_connection(self):
        return self.sentinel.slave_for(self.sentinel_config.service_name,
                                       **self.sentinel_config.options)


class RedisConnector(object):

    def __init__(self, redis_url: str = None, max_connections: int = None,
                 **connection_options):
        if redis_url is None:
            redis_url = os.environ.get('REDIS_URL', None)

        if redis_url is not None:
            url_bits = urlparse.urlparse(redis_url)
            options = {
                'host': url_bits.hostname,
                'port': int(url_bits.port),
                'db': url_bits.path.strip('/'),
                'password': url_bits.password
            }
        else:
            options = {}
            logger.warning("Initializing Redis without `redis_url` and without "
                           "`REDIS_URL` in the environment ...")

        options.update(connection_options)
        self.connection_options = options

        # In ~v2.9.1 the StrictRedis does not respect max_connections when
        # creating it's connection pool so we create it manually first.
        if max_connections is not None and redis_pattern.match(redis_version):
            connection_pool = self._create_connection_pool(max_connections)
            self.connection_options['connection_pool'] = connection_pool
        else:
            self.connection_options['max_connections'] = max_connections

    def _create_connection_pool(self, max_connections):
            options = {
                'max_connections': max_connections
            }
            options.update(self.connection_options)
            return ConnectionPool(**options)

    def get_connection(self):
        return StrictRedis(**self.connection_options)


def scan_keys(redis_conn: StrictRedis, pattern: str):
    """ Returns a list of all the keys matching a given pattern
    """

    result = []
    cur, keys = redis_conn.scan(cursor=0, match=pattern, count=2)
    result.extend(keys)
    while cur != 0:
        cur, keys = redis_conn.scan(cursor=cur, match=pattern, count=2)
        result.extend(keys)

    return result
