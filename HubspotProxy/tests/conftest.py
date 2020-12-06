import pytest

from mongoengine import signals
from mongoengine.connection import disconnect

from HubspotProxy.app import create_app
from HubspotProxy.config.database import db


def ensure_indexes(sender, document, **kwargs):
    document.ensure_indexes()


signals.pre_init.connect(ensure_indexes)


class Db(object):
    def __init__(self, application):
        self.application = application

    def clean(self):
        dtb = db.connection[self.application.config['MONGODB_SETTINGS']['DB']]
        if (self.application.config['MONGODB_SETTINGS']['USERNAME'] and
                self.application.config['MONGODB_SETTINGS']['PASSWORD']):
            dtb.authenticate(
                self.application.config['MONGODB_SETTINGS']['USERNAME'],
                self.application.config['MONGODB_SETTINGS']['PASSWORD']
            )

        for name in dtb.collection_names():
            if not name.startswith('system'):
                dtb.drop_collection(name)


@pytest.fixture(scope="session")
def app(request):
    disconnect('default')
    app = create_app('Testing')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(request, app):
    db = Db(application=app)
    yield db
    db.clean()
