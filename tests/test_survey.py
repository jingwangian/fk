import json
import pytest

from app.models import Survey


def test_list_surveys(app, client):
    response = client.get("/survey")

    assert response.status_code == 200


def test_new_survey(app, client):
    app.db.clear_data()
    # Create a validated survey
    response = client.post("/survey",
                           json={"name": "John"})
    assert response.status_code == 200

    # Create a validated survey
    response = client.post("/survey",
                           json={"name": "Mike"})
    assert response.status_code == 200

    # Create an invalid survey with lacking key 'name'
    response = client.post("/survey",
                           json={"noname": "Mike"})
    assert response.status_code == 400

    # Create an invalid survey with name is already exists
    response = client.post("/survey",
                           json={"name": "John"})
    assert response.status_code == 400

    response = client.get("/survey")
    assert len(response.get_json()) == 2


def test_get_survey(app, client):
    app.db.init_data()
    response = client.get("/survey/1")
    return_data = response.get_json()
    assert return_data['name'] == 'Ian'


def test_remove_survey(app, client):
    app.db.init_data()
    response = client.delete("/survey/1")
    assert response.status_code == 200

    response = client.get("/survey")
    assert len(response.get_json()) == 2

    response = client.delete("/survey/2")
    assert response.status_code == 200

    response = client.get("/survey")
    assert len(response.get_json()) == 1

    response = client.delete("/survey/20")
    assert response.status_code == 404
