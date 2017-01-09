import pytest
import transaction
from pyramid import testing
from gerrypy.models.mymodel import Tract, District, Edge
from gerrypy.models.meta import Base
# from learning_journal.models.mymodel import Entry
# from learning_journal.models.meta import Base
import sys


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.
    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.
    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://julienawilson:postword!!@localhost:5432/gerrypy_test'
    })
    config.include("gerrypy.models")
    config.include("gerrypy.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.
    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


# ------DB Tests--------

def test_database_has_tracts(db_session):
    """Test that database has contents."""
    assert db_session.query(Tract).count() == 1249


def test_database_has_edges(db_session):
    """Test that database has contents."""
    assert db_session.query(Edge).count() == 15948


# def test_database_has_edges(db_session):
#     """Test that database has contents."""
#     assert db_session.query(Edge).count() == 15948

#     entry1 = Entry(title='test_title1', body='test_body1', creation_date='test_date1')
#     entry2 = Entry(title='test_title2', body='test_body2', creation_date='test_date2')
#     entry3 = Entry(title='test_title3', body='test_body3', creation_date='test_date3')
#     entry4 = Entry(title='test_title4', body='test_body4', creation_date='test_date4')
#     for entry in (entry1, entry2, entry3, entry4):
#         db_session.add(entry)
#     assert db_session.query(Entry).count() == 4


# def test_entry_attributes(db_session):
#     """Test that new attributes are entered correctly."""
#     entry1 = Entry(title='test_title1', body='Testing123', creation_date='test_date1')
#     db_session.add(entry1)
#     test_row = db_session.query(Entry).first()
#     assert test_row.body == 'Testing123'