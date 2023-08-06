from __future__ import absolute_import

import os
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
            self.client = ESClient(**kwargs).create_connection()
        except Exception as e:
            self.client = None

        app.extensions[self.EXTENSION_NAME] = self
        self.app = app


class ESClient(object):
    """ Return an elasticsearch client.

    Arguments:
        hosts: Expects an array of objects with host information for
               the elasticsearch cluster connection. In form:
               [{'host': es_endpoint, 'port': 443}]
        http_auth: Authentication details. If None, this will attempt to create
                   an AWS4Auth auth object, which requires aws access/secret
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
        aws_access_key_id: Access Key for authorized IAM user.
        aws_secret_access_key: Secret Key for authorized IAM user.
        aws_region: Region for connection (e.g. us-east-1)

    Currently only supports the RequestsHttpConnection Transport.
    http://elasticsearch-py.readthedocs.io/en/master/transports.html
    """
    def __init__(self, hosts=['localhost'], http_auth=None, timeout=10,
                 use_ssl=True, verify_certs=True, ca_certs=None,
                 client_cert=None, client_key=None, headers=None,
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
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

        self.auto_http_auth_kinds = ('aws4auth')

    def _get_http_auth(self):
        """ Convenience method to get various kinds of HTTP auth objects.

            Currently supports creating an AWS4Auth auth object.
        """
        if self.http_auth is None:
            return None

        # If this isn't a string, pass it on as-is. Error will be thrown when
        # trying to establish connection if it isnt valid.
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
    def from_env(cls, hosts_var='ES_ENDPOINT', port=443,
                 timeout_var='ES_TIMEOUT', use_ssl_var='ES_USE_SSL',
                 verify_certs_var='ES_VERIFY_CERTS', ca_certs_var='ES_CA_CERTS',
                 client_cert_var='ES_CLIENT_CERT',
                 client_key_var='ES_CLIENT_KEY', headers_var='ES_HEADERS',
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
        client = ESClient.from_env(http_ath='aws4auth')

        Args:
            hosts_var (str): Name of the environment variable corresponding
                to self.hosts
            port (str): Name of the environment variable corresponding
                to self.port
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
            result_dict['hosts'] = [{'host': result_dict['hosts'],
                                     'port': port}]

        kwarg_names = ['timeout', 'use_ssl', 'verify_certs', 'ca_certs',
                       'client_cert', 'client_key', 'headers',
                       'aws_access_key_id', 'aws_secret_access_key',
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
