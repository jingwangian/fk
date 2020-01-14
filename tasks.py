from invoke import task

from main import start_server, app
from app import db
from app.models import Survey, Observation


def add_mock_data():
    client = app.test_client()

    client.post("/survey", json={"name": "Ian"})
    client.post("/survey", json={"name": "Mike"})
    client.post("/survey", json={"name": "Eric"})

    client.post('/stat/1', json={"value": 1, "frequency": 3})
    client.post('/stat/1', json={"value": 2, "frequency": 6})
    client.post('/stat/1', json={"value": 3, "frequency": 4})
    client.post('/stat/1', json={"value": 4, "frequency": 6})
    client.post('/stat/1', json={"value": 5, "frequency": 3})
    client.post('/stat/1', json={"value": 6, "frequency": 1})

    client.post('/stat/2', json={"value": 1, "frequency": 4})
    client.post('/stat/2', json={"value": 2, "frequency": 7})
    client.post('/stat/2', json={"value": 3, "frequency": 6})
    client.post('/stat/2', json={"value": 4, "frequency": 2})
    client.post('/stat/2', json={"value": 5, "frequency": 3})
    return 'ok'


def clear_mock_data():
    with app.app_context():
        for s in Survey.query.all():
            db.session.delete(s)
            db.session.commit()

        for s in Observation.query.all():
            db.session.delete(s)
            db.session.commit()


@task()
def add(c):
    """add mock data"""
    add_mock_data()


@task()
def clear(c):
    """clear mock data"""
    clear_mock_data()
