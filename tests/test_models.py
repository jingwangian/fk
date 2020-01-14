import pytest

from app.models import Survey, Observation
from app import db


class TestSurveyModel():
    def test_count(self, app):
        app.db.init_data()
        with app.app_context():
            survey = Survey.query.get_or_404(1)
            result = survey.count()
            assert result == 23

        with app.app_context():
            survey = Survey.query.get_or_404(2)
            result = survey.count()
            assert result == 22

        with app.app_context():
            survey = Survey.query.get_or_404(3)
            result = survey.count()
            assert result == 0

    def test_mean(self, app):
        app.db.init_data()

        with app.app_context():
            survey = Survey.query.get_or_404(1)
            result = survey.mean()
            assert result == 3.13

            survey = Survey.query.get_or_404(2)
            result = survey.mean()
            assert result == 2.68

            survey = Survey.query.get_or_404(3)
            result = survey.mean()
            assert result == 0

    def test_median(self, app):
        app.db.init_data()
        with app.app_context():
            survey = Survey.query.get_or_404(1)
            result = survey.median()
            assert result == 3.0

            survey = Survey.query.get_or_404(2)
            result = survey.median()
            assert result == 2.5

            survey = Survey.query.get_or_404(3)
            result = survey.median()
            assert result == 0

    def test_mode(self, app):
        app.db.init_data()
        with app.app_context():
            survey = Survey.query.get_or_404(1)
            result = survey.mode()
            assert result == [2.0, 4.0]

            survey = Survey.query.get_or_404(2)
            result = survey.mode()
            assert result == [2.0]

            survey = Survey.query.get_or_404(3)
            result = survey.mode()
            assert result == [0]


class TestObservation():
    def test_to_json(self):
        ob = Observation(id=100, survey_id=1, value=200, frequency=300)
        json_data = ob.to_json()

        assert json_data['id'] == 100
        assert json_data['survey_id'] == 1
        assert json_data['value'] == 200
        assert json_data['frequency'] == 300
