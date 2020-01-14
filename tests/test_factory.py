import pytest
from app import create_app


def test_config(app):
    """Test create_app without passing test config."""

    assert 'test.db' in app.config['SQLALCHEMY_DATABASE_URI']
