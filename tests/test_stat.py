import json
import pytest
from app.models import Survey, Observation


# class TestObservation:


def test_new_stat(app, client):
    app.db.init_data()
    # Create new obversation with validate survey id
    response = client.post('/stat/3',
                           json={"value": 1, "frequency": 13})
    assert response.status_code == 200

    # Create new obversation with validate survey id
    response = client.post('/stat/3',
                           json={"value": 2, "frequency": 10})
    assert response.status_code == 200

    with app.app_context():
        obs = Observation.query.filter_by(survey_id=3).all()
        assert len(obs) == 2
        assert obs[0].value == 1
        assert obs[0].frequency == 13


def test_new_stat_with_invadate_content(app, client):
    app.db.init_data()
    # Create new obversation with invalidate survey id
    response = client.post('/stat/20',
                           json={"value": 61, "frequency": 15})
    assert response.status_code == 400

    # Create new obversation with existing value
    response = client.post('/stat/1',
                           json={"value": 1, "frequency": 10})
    assert response.status_code == 400

    # Create new obversation lack "value"
    response = client.post('/stat/1',
                           json={"lack_value": 1, "frequency": 10})
    assert response.status_code == 400

    # Create new obversation lack "frequency"
    response = client.post('/stat/1',
                           json={"value": 1, "no-frequency": 10})
    assert response.status_code == 400

    # Create new obversation with invalidate format of value
    response = client.post('/stat/1',
                           json={"value": "invalid-format", "frequency": 10})
    assert response.status_code == 400


def test_list_stats(app, client):
    app.db.init_data()

    response = client.get('/stat')
    assert response.status_code == 200
    assert len(response.get_json()) == 11

    # clear all data and test again
    app.db.clear_data()
    response = client.get('/stat')
    assert response.status_code == 200
    assert len(response.get_json()) == 0


def test_get_stat(app, client):
    app.db.init_data()

    # Get with validate obversation id
    response = client.get('/stat/1')
    assert response.status_code == 200

    return_data = response.get_json()
    assert return_data['value'] == 1
    assert return_data['frequency'] == 3

    # Get with invalid obversation id
    response = client.get('/stat/100')
    assert response.status_code == 404


def test_get_invalid_stat(app, client):
    response = client.get('/stat/100')
    assert response.status_code == 404


def test_delete_stat(app, client):
    app.db.init_data()

    # delete with validate obversation id
    response = client.delete('/stat/1')
    assert response.status_code == 200

    response = client.get('/stat/1')
    assert response.status_code == 404

    response = client.get('/stat')
    assert response.status_code == 200
    assert len(response.get_json()) == 10

    # delete with invalid id
    response = client.delete('/stat/100')
    assert response.status_code == 404


def test_update_stat(app, client):
    app.db.init_data()

    # update with validate obversation id
    response = client.put('/stat/1',
                          json=dict(value=1, frequency=1001))
    assert response.status_code == 200

    # Check updated obversation
    response = client.get('/stat/1')
    return_data = response.get_json()
    assert return_data['value'] == 1
    assert return_data['frequency'] == 1001


def test_update_stat_with_invalidate_content(app, client):
    app.db.init_data()
    # update with invalid obversation id
    response = client.put('/stat/100', json=dict(value=1, frequency=10))
    assert response.status_code == 404

    # update with validate obversation id but incorrect value
    response = client.put('/stat/1', json=dict(value=10, frequency=10))
    assert response.status_code == 400
