from __future__ import absolute_import

import os
from ast import literal_eval as make_tuple
from elasticsearch import RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from elasticsearch_dsl.connections import connections


class FlaskElasticsearch(object):

    EXTENSION_NAME = 'flask_elasticsearch'

    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        try:
            options = {
                'hosts': app.config['ES_ENDPOINT'],
                'http_auth': app.config.get('ES_HTTP_AUTH', None),
                'timeout': app.config.get('ES_TIMEOUT', 10),
                'use_ssl': app.config.get('ES_USE_SSL', True),
                'verify_certs': app.config.get('ES_VERIFY_CERTS', True),
                'ca_certs': app.config.get('ES_CA_CERTS', None),
                'client_cert': app.config.get('ES_CLIENT_CERT', None),
                'client_key': app.config.get('ES_CLIENT_KEY', None),
                'headers': app.config.get('ES_HEADERS', None),
                'es_user': app.config.get('ES_USER', None),
                'es_password': app.config.get('ES_PASSWORD', None),
                'aws_access_key_id': app.config.get('ES_AWS_ACCESS_KEY', None),
                'aws_secret_access_key':
                    app.config.get('ES_AWS_SECRET_KEY', None),
                'aws_region': app.config.get('ES_AWS_REGION', 'us-east-1')
            }
            options.update(**kwargs)

            self.client = ESClient(**options).create_connection()
        except Exception as e:
            self.client = None

        app.extensions[self.EXTENSION_NAME] = self
        self.app = app


class ESClient(object):
    """ Return an elasticsearch client.

    Arguments:
        hosts: Expects an array of strings with host information for
               the elasticsearch cluster connection. In form:
               ["es.end.point:port"]
        http_auth: Authentication details. Can be either a tuple with username/
                   password, an initialized AWS4Auth object, or None. If None,
                   this will check for ES_USER and ES_PASSWORD to create
                   an http auth connection. If either of those is None, this
                   attempts to create an AWS4Auth auth object, which requires
                   aws access/secret.
        use_ssl: Boolean
        verify_certs: Boolean
        verify_certs: Boolean
        ca_certs: Path to CA bundle. By default standard requests' bundle will
                  be used.
        client_cert: Path to the file containing the private key and the
                     certificate, or cert only if using client_key
        client_key: Path to the file containing the private key if using
                    separate cert and key files (client_cert will contain only
                    the cert)
        headers: Any custom http headers to be add to requests
        es_user: [Optional] Elasticsearch Username for http authentication
        es_password: [Optional] Elasticsearch Password for http authentication
        aws_access_key_id: [Optional] Access Key for authorized IAM user.
        aws_secret_access_key: [Optional] Secret Key for authorized IAM user.
        aws_region: [Optional] Region for connection (e.g. us-east-1)

    Currently only supports the RequestsHttpConnection Transport.
    http://elasticsearch-py.readthedocs.io/en/master/transports.html
    """
    def __init__(self, hosts=['localhost:9200'], http_auth=None, timeout=10,
                 use_ssl=True, verify_certs=True, ca_certs=None,
                 client_cert=None, client_key=None, headers=None,
                 es_user=None, es_password=None,
                 aws_access_key_id=None, aws_secret_access_key=None,
                 aws_region='us-east-1', **kwargs):
        super(ESClient, self).__init__()

        self.hosts = hosts
        self.http_auth = http_auth
        self.timeout = timeout
        self.use_ssl = use_ssl
        self.verify_certs = verify_certs
        self.ca_certs = ca_certs
        self.client_cert = client_cert
        self.client_key = client_key
        self.headers = headers
        self.es_user = es_user
        self.es_password = es_password
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

        self.auto_http_auth_kinds = ('aws4auth')

    def _get_http_auth(self):
        """ Convenience method to get various kinds of HTTP auth objects.

            Currently supports creating an AWS4Auth auth object.
        """
        if self.http_auth is None:
            # Check if username/password are set
            if self.es_user is not None and self.es_password is not None:
                self.http_auth = (self.es_user, self.es_password)
                return self.http_auth
            return None

        # If this isn't a string, pass it on as-is. Error will be thrown when
        # trying to establish connection if it isnt valid. Example of a valid
        # Non-string value: ('username', 'password')
        if not isinstance(self.http_auth, str):
            return self.http_auth

        # If it is a string but doesn't exist in our list of auth kinds we
        # can create automatically, return it unchanged.
        elif self.http_auth not in self.auto_http_auth_kinds:
            return self.http_auth

        # We should know how to create a connection object.
        elif self.http_auth in self.auto_http_auth_kinds:
            if self.http_auth.lower() == 'aws4auth'\
                    and self.aws_access_key_id is not None\
                    and self.aws_secret_access_key is not None\
                    and self.aws_region is not None:
                return AWS4Auth(
                    self.aws_access_key_id,
                    self.aws_secret_access_key,
                    self.aws_region,
                    'es'
                )

        return None

    @classmethod
    def from_env(cls, hosts_var='ES_ENDPOINT', http_auth_var='ES_HTTP_AUTH',
                 timeout_var='ES_TIMEOUT', use_ssl_var='ES_USE_SSL',
                 verify_certs_var='ES_VERIFY_CERTS', ca_certs_var='ES_CA_CERTS',
                 client_cert_var='ES_CLIENT_CERT',
                 client_key_var='ES_CLIENT_KEY', headers_var='ES_HEADERS',
                 es_user_var='ES_USER', es_password_var='ES_PASSWORD',
                 aws_access_key_id_var='ES_AWS_ACCESS_KEY',
                 aws_secret_access_key_var='ES_AWS_SECRET_KEY',
                 aws_region_var='ES_AWS_REGION', **kwargs):
        """ Alternate constructor for building an ESClient object from
        environment variables.  Particularly useful in combination with
        honcho/.env files.

        Each *_var argument corresponds to an argument in init.  If the
        variable is not in the enviroment, it will look in *args, **kwargs,
        and then finally fall back to the defaults in init if not present
        elsewhere.

        Typically this should be called as
            client = ESClient.from_env()
        assuming all required environment variables are set. In the event some
        are not, you can pass the specific keyword arguments you want to use
        for ESClient() directly to the from_env() method,  e.g.
            client = ESClient.from_env(http_auth='aws4auth')

        Args:
            hosts_var (str): Name of the environment variable corresponding
                to self.hosts. Environment variable should be in form of a
                string, using comma separated format if multiple hosts desired.
                e.g. ES_ENDPOINT=localhost:9200,other.host.here:9200
                NOTE: This will instantiate the same SSL/Cert settings for all
                hosts, so you can't mix :9200 and :443, for example.
            timeout_var (str): Name of the environment variable corresponding
                to self.timeout
            use_ssl_var (str): Name of the environment variable corresponding
                to self.use_ssl
            verify_certs_var (str): Name of the environment variable
                corresponding to self.verify_certs
            ca_certs_var (str): Name of the environment variable corresponding
                to self.ca_certs
            client_cert_var (str): Name of the environment variable
                corresponding to self.client_cert
            client_key_var (str): Name of the environment variable corresponding
                to self.client_key
            headers_var (str): Name of the environment variable corresponding
                to self.headers
            es_user_var: Name of the environment variable corresponding to the
                Elasticsearch Username for http authentication
            es_password_var: Name of the environment variable corresponding to the
                Elasticsearch Password for http authentication
            aws_access_key_id_var (str): Name of the environment variable
                corresponding to self.aws_access_key_id
            aws_secret_access_key_var (str): Name of the environment variable
                corresponding to self.aws_secret_access_key
            aws_region_var (str): Name of the environment variable corresponding
                to self.aws_region

        Returns: Initialized class instance.

        """

        def check_vars(var_name, kwarg_name, result_dict):
            """ Check if a variable is in the environment, if so update the
                dict of results to send to init.

            Args:
                var_name: e.g., 'ES_ENDPOINT'
                kwarg_name: the name of the kwarg expected by init.  E.g.
                    'hosts'
                result_dict (dict): a dict mapping kwargs to values in init

            Returns (dict): updated result_dict

            """
            var_val = os.environ.get(var_name, None)
            if var_val is not None:
                result_dict[kwarg_name] = var_val
            return result_dict

        result_dict = {}
        result_dict = check_vars(hosts_var, 'hosts', result_dict)
        if 'hosts' in result_dict:
            # Hosts is a 'special' variable because we allow a comma
            # separated string and need to turn into an array for ESClient()
            host_list = result_dict['hosts'].split(',')
            result_dict['hosts'] = [host.strip() for host in host_list]

        # Attempt to populate http_auth and es user/password if exist
        # After this block, we should have a valid http auth value of either
        # a provided tuple, e.g. ES_HTTP_AUTH=(\"username\", \"password\")
        # or a provided user/password, e.g. ES_USER=foo, ES_PASSWORD=bar
        # or `aws4auth`, which will require the AWS access keys as well.
        result_dict = check_vars(http_auth_var, 'http_auth', result_dict)
        result_dict = check_vars(es_user_var, 'es_user', result_dict)
        result_dict = check_vars(es_password_var, 'es_password', result_dict)
        if result_dict.get('es_user') and result_dict.get('es_password'):
            # Make a username/password tuple if they are set. This takes
            # precedence.
            result_dict['http_auth'] =\
                (result_dict.get('es_user'), result_dict.get('es_password'))
        elif result_dict.get('http_auth') is None:
            # Set to aws4auth as default if no http_auth is set
            result_dict['http_auth'] = 'aws4auth'
        elif result_dict.get('http_auth') != 'aws4auth':
            # If http_auth is set and it's not aws4auth, try to make it into
            # a valid tuple (e.g. ES_HTTP_AUTH=(\"username\", \"password\"))
            try:
                result_dict['http_auth'] = make_tuple(result_dict['http_auth'])
            except Exception as e:
                logger.error("Unable to form http_auth value ... {}".format(e))

        # use_ssl and verify_certs need to be boolean, so treat them specially
        result_dict = check_vars(use_ssl_var, 'use_ssl', result_dict)
        if 'use_ssl' in result_dict:
            result_dict['use_ssl'] = result_dict['use_ssl'].lower() == 'true'
        result_dict = check_vars(verify_certs_var, 'verify_certs', result_dict)
        if 'verify_certs' in result_dict:
            result_dict['verify_certs'] =\
                result_dict['verify_certs'].lower() == 'true'
        result_dict = check_vars(timeout_var, 'timeout', result_dict)
        if 'timeout' in result_dict:
            result_dict['timeout'] = int(result_dict['timeout'])

        kwarg_names = ['ca_certs', 'client_cert', 'client_key',
                       'headers', 'aws_access_key_id', 'aws_secret_access_key',
                       'aws_region']
        var_names = [x + '_var' for x in kwarg_names]
        for var, kwarg_name in zip(var_names, kwarg_names):
            result_dict = check_vars(eval(var), kwarg_name, result_dict)

        initialized_cls = cls(**kwargs)
        for k, v in result_dict.items():
            setattr(initialized_cls, k, v)

        return initialized_cls

    def create_connection(self, return_client=True):
        http_auth = self._get_http_auth()
        client = connections.create_connection(
            hosts=self.hosts,
            http_auth=http_auth,
            timeout=self.timeout,
            use_ssl=self.use_ssl,
            verify_certs=self.verify_certs,
            ca_certs=self.ca_certs,
            client_cert=self.client_cert,
            client_key=self.client_key,
            headers=self.headers,
            connection_class=RequestsHttpConnection
        )

        if return_client:
            return client
        return
