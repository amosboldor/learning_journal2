"""Test for the Learning Journal."""


import unittest
import transaction

from pyramid import testing

from learning_journal.models import Entries, get_tm_session
from learning_journal.models.meta import Base

from datetime import datetime


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance."""
    settings = {'sqlalchemy.url': 'postgres://Sera@localhost:5432/test_learning_journal'}
    config = testing.setUp(settings=settings)
    config.include('learning_journal.models')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def db_session(configuration, request):
    """Create session for interacting with test db."""
    SessionFactory = configuration.registory['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate fake HTTP requst."""
    return testing.DummyRequest(dbsession=db_session)

@pytest.fixture
def add_models(dummy_request):
    """Add model instances to db."""
    for entry in ENTRIES:
        row = Entries(title=entry['title'], title1=entry['title1'], create_date=entry['create_date'], body=entry['body'])
        dummy_request.dbsession.add(row)


ENTRIES = [
    {'title': 'Week 2', 'title1': 'Day 5', 'create_date': datetime.strptime('December 18, 2016', '%B %d, %Y'), 'body': 'Cherries are rotten'},
    {'title': 'Week 3', 'title1': 'Day 1', 'create_date': datetime.strptime('December 19, 2016', '%B %d, %Y'), 'body': 'Apples are rotten'},
    {'title': 'Week 3', 'title1': 'Day 2', 'create_date': datetime.strptime('December 20, 2016', '%B %d, %Y'), 'body': 'Oranges are rotten'},
    {'title': 'Week 3', 'title1': 'Day 3', 'create_date': datetime.strptime('December 21, 2016', '%B %d, %Y'), 'body': 'Kiwis are rotten'},
    {'title': 'Week 3', 'title1': 'Day 4', 'create_date': datetime.strptime('December 22, 2016', '%B %d, %Y'), 'body': 'Mangos are rotten'},
    {'title': 'Week 3', 'title1': 'Day 5', 'create_date': datetime.strptime('December 23, 2016', '%B %d, %Y'), 'body': 'Pomogranets are rotten'}
]


#`````````````` unit test```````````````


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestMyViewSuccessCondition(BaseTest):

    def setUp(self):
        super(TestMyViewSuccessCondition, self).setUp()
        self.init_database()

        from .models import Entries

        model = Entries(name='one', value=55)
        self.session.add(model)

    def test_passing_view(self):
        from .views.default import my_view
        info = my_view(dummy_request(self.session))
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'learning_journal')


class TestMyViewFailureCondition(BaseTest):

    def test_failing_view(self):
        from .views.default import my_view
        info = my_view(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)
