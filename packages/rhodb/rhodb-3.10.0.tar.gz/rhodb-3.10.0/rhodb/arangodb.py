from arango import ArangoClient

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    try:
        from flask import _request_ctx_stack as stack
    except:
        pass


class FlaskArangoDB(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def connect(self):
        self.arango = ArangoDB(
            protocol='http',
            host=self.app.config['ARANGO_HOST'],
            port=self.app.config['ARANGO_PORT'],
            db_name=self.app.config['ARANGO_DB'],
            username=self.app.config['ARANGO_USERNAME'],
            password=self.app.config['ARANGO_PASSWORD']
        )
        return self.arango.client

    @property
    def client(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'arango_client'):
                ctx.arango_client = self.connect()
            return ctx.arango_client

    @property
    def db(self):
        if self.client:
            db_name = self.app.config['ARANGO_DB']
            return self.client.db(name=db_name)


class ArangoDB(object):

    def __init__(self, protocol, host, port, db_name, username=None,
                 password=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = ArangoClient(
                protocol='http',
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                enable_logging=True
            )
        return self._client

    @property
    def db(self):
        if self.client:
            return self.client.db(name=self.db_name)
