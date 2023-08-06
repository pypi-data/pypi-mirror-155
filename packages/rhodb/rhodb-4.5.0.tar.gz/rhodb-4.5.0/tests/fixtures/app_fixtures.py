from __future__ import print_function

import os
import pytest
import sys
from flask import Flask
from mock import patch

PY3 = sys.version_info[0] >= 3

__all__ = ["app", "db", "session", "Person", "rhodb"]


@pytest.fixture(scope='function')
def app(request):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    if hasattr(request.cls, 'database_name'):
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] =\
            'postgresql://postgres:@127.0.0.1/{0}'\
            .format(request.cls.database_name)

    if hasattr(request.cls, 'app_config'):
        app.config.update(request.cls.app_config)

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope='function')
def db(app, request):
    """Session-wide test database."""
    scenario = 'with-app'
    if 'scenario' in request.funcargnames:
        scenario = request.getfuncargvalue('scenario')

    if "rhodb.database" in sys.modules:
        del sys.modules['rhodb.database']

    if "rhodb.flask_sqlalchemy" in sys.modules:
        del sys.modules['rhodb.flask_sqlalchemy']

    if "rhodb.rhodb_sqlalchemy" in sys.modules:
        del sys.modules['rhodb.rhodb_sqlalchemy']

    if 'flask_sqlalchemy' in sys.modules:
        del sys.modules['flask_sqlalchemy']

    # Check if we're running a parametrized test

    # If the parametrized test is without-app, then set the database connection
    # uri
    if scenario == 'without-app':
        os.environ['SQLALCHEMY_DATABASE_URI'] =\
            'postgresql://postgres:@127.0.0.1/{0}'\
            .format(request.cls.database_name)
        os.environ['SQLALCHEMY_ECHO'] = 'False'
        os.environ['SQLALCHEMY_POOL_SIZE'] = '5'
        os.environ['SQLALCHEMY_POOL_TIMEOUT'] = '30'
        os.environ['SQLALCHEMY_POOL_RECYCLE'] = '-1'
        os.environ['SQLALCHEMY_MAX_OVERFLOW'] = '10'

    # Mock the import statement so that we that the db variable in
    # rhodb.database can be set to the proper SQLAlchemy instance
    orig_import = __import__

    def import_mock(name, *args, **kwargs):
        if name == 'flask_sqlalchemy' and scenario == 'without-app':
            raise ImportError('package not found')

        return orig_import(name, *args, **kwargs)

    import_obj = 'builtins.__import__' if PY3 else '__builtin__.__import__'
    with patch(import_obj, side_effect=import_mock):
        from rhodb.database import SQLAlchemy, create_database, drop_database
        _db = SQLAlchemy()

        try:
            drop_database(request.cls.database_name)
            create_database(request.cls.database_name)
        except Exception as e:
            pass

        if scenario == 'with-app':
            _db.init_app(app)
        if scenario == 'without-app':
            _db.init_session()

        def teardown():
            _db.session.rollback()
            _db.session.close()
            _db.session.bind.dispose()

        request.addfinalizer(teardown)
        return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""

    db.session.begin_nested()

    def teardown():
        db.session.rollback()
        db.session.close()
        db.session.bind.dispose()

    request.addfinalizer(teardown)
    return db.session


@pytest.fixture(scope='function',
                params=['postgres', 'sqlite', 'sqlite-mem', 'mysql'])
def rhodb(request):
    from rhodb.database import create_database, drop_database
    sqlite_db = '/tmp/{0}.db'.format(request.cls.database_name)

    try:
        if request.param in ['postgres', 'mysql']:
            drop_database(request.cls.database_name, request.param)
            create_database(request.cls.database_name, request.param)
        elif request.param == 'sqlite':
            os.remove(sqlite_db)

    except Exception as e:
        print(e)
        pass

    from rhodb.rhodb_sqlalchemy import SQLAlchemy

    os.environ['SQLALCHEMY_ECHO'] = 'False'
    if 'SQLALCHEMY_POOL_SIZE' in os.environ:
        del os.environ['SQLALCHEMY_POOL_SIZE']
    if 'SQLALCHEMY_POOL_TIMEOUT' in os.environ:
        del os.environ['SQLALCHEMY_POOL_TIMEOUT']
    if 'SQLALCHEMY_POOL_RECYCLE' in os.environ:
        del os.environ['SQLALCHEMY_POOL_RECYCLE']
    if 'SQLALCHEMY_MAX_OVERFLOW' in os.environ:
        del os.environ['SQLALCHEMY_MAX_OVERFLOW']

    if request.param == 'postgres':
        os.environ['SQLALCHEMY_DATABASE_URI'] =\
            'postgresql://postgres:@127.0.0.1/{0}'\
            .format(request.cls.database_name)
    elif request.param == 'sqlite':
        os.environ['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///{0}'.format(sqlite_db)
    elif request.param == 'sqlite-mem':
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    elif request.param == 'mysql':
        os.environ['SQLALCHEMY_DATABASE_URI'] =\
            'mysql://root@127.0.0.1/{0}'.format(request.cls.database_name)
    else:
        raise Exception('Driver {0} not supported'.format(request.param))

    _db = SQLAlchemy()
    _db.init_session()

    def teardown():
        _db.session.rollback()
        _db.session.close()
        _db.session.bind.dispose()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def Person(db, request):
    scenario = 'with-app'
    if 'scenario' in request.funcargnames:
        scenario = request.getfuncargvalue('scenario')

    orig_import = __import__

    def import_mock(name, *args, **kwargs):
        if name == 'flask_sqlalchemy' and scenario == 'without-app':
            raise ImportError('package not found')

        return orig_import(name, *args, **kwargs)

    import_obj = 'builtins.__import__' if PY3 else '__builtin__.__import__'
    with patch(import_obj, side_effect=import_mock):
        from rhodb.database import BaseWithIntPK, MutableDict, JSONEncodedDict

        class Person(BaseWithIntPK, db.Model):
            __tablename__ = 'person'

            given_name = db.Column(db.String(255))
            family_name = db.Column(db.String(255))
            custom_data = db.Column(MutableDict.as_mutable(JSONEncodedDict),
                                    default={})
            birth_date = db.Column(db.Interval)

            __serializable_columns__ = ['id', 'given_name', 'family_name',
                                        'birth_date']

            def __init__(self, given_name='Ricky', family_name='Bobby',
                         custom_data={'age': 30}):
                self.given_name = given_name
                self.family_name = family_name
                self.custom_data = custom_data

        db.create_all()

        return Person
