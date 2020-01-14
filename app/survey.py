from flask import Blueprint, request, jsonify

from . import db
from .models import Survey
from .errors import response_400, response_404, response_500

import logging

bp = Blueprint(
    'survey',
    __name__,
    template_folder='./templates',
    url_prefix="/survey"
)

logger = logging.getLogger(__name__)


@bp.route('')
def list_surveys():
    # survey_list = []
    logger.info('Enter list_surveys')
    surveys = Survey.query.all()
    survey_list = [s.to_json() for s in surveys]

    return jsonify(survey_list)


@bp.route('', methods=('POST',))
def new_survey():
    logger.info('Enter new_survey')
    survey_json = request.get_json()

    try:
        survey_name = survey_json["name"]
    except KeyError:
        return response_400('"name" is required')

    if Survey.query.filter_by(name=survey_name).first():
        return response_400(f'The name with "{survey_name}" is already existed')

    survey = Survey(name=survey_json["name"])

    try:
        db.session.add(survey)
        db.session.commit()
    except Exception:
        return response_500(f'Failed to create new survey:{survey}')

    # print(survey)
    return jsonify(survey.to_json())


@bp.route('/<id>')
def get_survey(id):
    logger.info('Enter get_survey')
    survey = Survey.query.get(id)
    if survey is None:
        return response_404('survey is not exists')

    return jsonify(survey.to_json())


@bp.route('/<id>', methods=('DELETE',))
def remove_survey(id):
    survey = Survey.query.get(id)
    if survey is None:
        return response_404('survey is not exists')

    db.session.delete(survey)
    db.session.commit()
    return jsonify(survey.to_json())
