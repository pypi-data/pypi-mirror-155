from arango import ArangoClient


class FlaskArangoDB(object):

    EXTENSION_NAME = 'flask_arangodb'

    def __init__(self, app=None, **kwargs):
        self.app = app
        self.arango = None

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        try:
            options = {
                'protocol': 'http',
                'host': app.config['ARANGO_HOST'],
                'port': app.config['ARANGO_PORT'],
                'db_name': app.config['ARANGO_DB'],
                'username': app.config['ARANGO_USERNAME'],
                'password': app.config['ARANGO_PASSWORD']
            }
            options.update(**kwargs)
            self.arango = ArangoDB(**options)

        except Exception as e:
            self.arango = None
            raise Exception('Unable to initialize ArangoDB ... {}'.format(e))

        app.extensions[self.EXTENSION_NAME] = self
        self.app = app

    @property
    def client(self):
        if self.arango is not None:
            return self.arango.client
        return None

    @property
    def db(self):
        if self.arango is not None:
            return self.arango.db
        return None


class ArangoDB(object):

    def __init__(self, host, port, db_name, username=None,
                 password=None, protocol='http'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self.protocol = protocol
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = ArangoClient(
                protocol=self.protocol,
                host=self.host,
                port=self.port
            )
        return self._client

    @property
    def db(self):
        if self.client:
            return self.client.db(name=self.db_name,
                                  username=self.username,
                                  password=self.password)
