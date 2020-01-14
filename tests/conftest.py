import os
import sys
import pytest
import sqlite3

from os.path import dirname

print(dirname(dirname(__file__)))
sys.path.insert(0, dirname(dirname(__file__)))


class TestDB:
    def __init__(self, app, db):
        self.app = app
        self.__db = db

    def init_data(self):
        from app.models import Survey, Observation

        with self.app.app_context():
            db = self.db
            for s in Survey.query.all():
                db.session.delete(s)
                db.session.commit()

            for s in Observation.query.all():
                db.session.delete(s)
                db.session.commit()

            db.session.add(Survey(id=1, name='Ian'))
            db.session.add(Survey(id=2, name='Mike'))
            db.session.add(Survey(id=3, name='Eric'))

            db.session.add(Observation(survey_id=1, value=1, frequency=3))
            db.session.add(Observation(survey_id=1, value=2, frequency=6))
            db.session.add(Observation(survey_id=1, value=3, frequency=4))
            db.session.add(Observation(survey_id=1, value=4, frequency=6))
            db.session.add(Observation(survey_id=1, value=5, frequency=3))
            db.session.add(Observation(survey_id=1, value=6, frequency=1))

            db.session.add(Observation(survey_id=2, value=1, frequency=4))
            db.session.add(Observation(survey_id=2, value=2, frequency=7))
            db.session.add(Observation(survey_id=2, value=3, frequency=6))
            db.session.add(Observation(survey_id=2, value=4, frequency=2))
            db.session.add(Observation(survey_id=2, value=5, frequency=3))

            db.session.commit()

    def clear_data(self):
        from app.models import Survey, Observation

        with self.app.app_context():
            db = self.db
            for s in Survey.query.all():
                db.session.delete(s)
                db.session.commit()

            for s in Observation.query.all():
                db.session.delete(s)
                db.session.commit()

    @property
    def db(self):
        return self.__db


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for test."""
    from app import create_app
    from app import db

    # create the app with common test config
    app = create_app('config.TestConfig')
    app.testing = True

    db.create_all(app=app)

    app.db = TestDB(app, db)

    yield app

    # close and remove the temporary database
    print('drop_all')
    db.drop_all(app=app)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
