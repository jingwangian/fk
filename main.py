#!/usr/bin/env python3
import os
import logging

from logging.handlers import RotatingFileHandler
from flask import render_template
from app import create_app
from app.models import Survey

env = os.environ.get('FLASK_ENV', 'development')

logger = logging.getLogger(__name__)

print(f'start to call create_app, env={env}')
app = create_app('config.%sConfig' % env.capitalize())
print(f"SQLALCHEMY_DATABASE_URI = {app.config['SQLALCHEMY_DATABASE_URI']}")


@app.route('/')
@app.route('/index')
def index():
    surveys = Survey.query.all()
    if not surveys:
        surveys = []

    return render_template('index.html', surveys=surveys)


@app.route('/results/<int:id>')
def results(id):
    survey = Survey.query.get_or_404(id)

    results = {
        "count": survey.count(),
        "mean": survey.mean(),
        "median": survey.median(),
        "mode": ', '.join([str(x) for x in survey.mode()]),
    }

    return render_template('result.html', survey_id=id, results=results)


def log_configurer():
    # Check log dir or create it
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    root = logging.getLogger()
    h = RotatingFileHandler('logs/websever.log', 'a', 1024 * 1024 * 2, 10)
    f = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s: %(message)s')
    h.setLevel(logging.INFO)
    h.setFormatter(f)
    root.addHandler(h)
    root.setLevel(logging.INFO)


log_configurer()


def start_server():
    logger.info('starting app')
    app.run(debug=True)


if __name__ == '__main__':
    start_server()
