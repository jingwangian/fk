from jsonschema import validate
from jsonschema import draft7_format_checker
from flask import Blueprint, request, jsonify

import logging
import jsonschema

from . import db
from .models import Survey, Observation
from .errors import response_400, response_404, response_500


bp = Blueprint(
    'stat',
    __name__,
    template_folder='./templates',
    url_prefix="/stat"
)

logger = logging.getLogger(__name__)

newStatSchema = {
    "type": "object",
    "properties": {
        "value": {"type": "number"},
        "frequency": {"type": "number"},
    },
    "required": ["value", "frequency"]
}


@bp.route('/<survey_id>', methods=('POST',))
def new_stat(survey_id):
    logger.info('Enter new_stat')
    survey = Survey.query.get(survey_id)
    if survey is None:
        return response_400('Invalid survey id')

    stat_json = request.get_json()

    try:
        validate(stat_json,
                 schema=newStatSchema,
                 format_checker=draft7_format_checker)

    except jsonschema.exceptions.ValidationError as e:
        return response_400(str(e))

    stat_value = stat_json["value"]

    result = Observation.query.filter_by(value=stat_value, survey_id=survey_id).first()

    if result:
        return response_400('value has already exits, please use put to update it')

    obs = Observation(survey=survey,
                      value=stat_json["value"],
                      frequency=stat_json["frequency"])

    try:
        db.session.add(obs)
        db.session.commit()
    except Exception as e:
        return response_500(f'Failed insert new stat:{str(e)}')
    return jsonify(obs.to_json())


@bp.route('')
def list_stats():
    logger.info('Enter list_stats')
    obs_list = Observation.query.all()

    return jsonify([obs.to_json() for obs in obs_list])


@bp.route('/<int:id>')
def get_stat(id):
    logger.info(f'Enter get_stat with id[{id}]')
    obs = Observation.query.get(id)
    if obs is None:
        return response_404('The stat is not exists')
    return jsonify(obs.to_json())


@bp.route('/<id>', methods=('DELETE',))
def delete_stat(id):
    logger.info(f'Enter delete_stat with id[{id}]')
    obs = Observation.query.get(id)
    if obs is None:
        return response_404('Invalid stat id')

    db.session.delete(obs)
    db.session.commit()
    return jsonify(obs.to_json())


@bp.route('/<int:id>', methods=('PUT',))
def update_stat(id):
    logger.info(f'Enter update_stat with id[{id}]')
    obs = Observation.query.get(id)
    if obs is None:
        return response_404('Invalid stat id')

    updated_stat = request.get_json()

    if updated_stat['value'] != obs.value:
        return response_400('Invalid value')

    obs.frequency = updated_stat['frequency']

    try:
        db.session.add(obs)
        db.session.commit()
    except Exception as e:
        return str(e)
    return jsonify(obs.to_json())
