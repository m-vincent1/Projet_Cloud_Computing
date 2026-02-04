"""
Configuration pytest et fixtures pour les tests
"""
import os
import sys
import pytest

# Ajouter le répertoire app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configurer l'environnement de test AVANT d'importer l'app
os.environ['FLASK_ENV'] = 'testing'
os.environ['USE_LOCAL_FILES'] = 'True'
os.environ['LOCAL_DATA_PATH'] = 'tests/data'


@pytest.fixture
def app():
    """Crée une instance de l'application pour les tests"""
    from app.main import app as flask_app

    # Configuration de test
    flask_app.config['TESTING'] = True
    flask_app.config['USE_LOCAL_FILES'] = True
    flask_app.config['LOCAL_DATA_PATH'] = 'tests/data'

    yield flask_app


@pytest.fixture
def client(app):
    """Crée un client de test Flask"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Crée un runner CLI pour les tests"""
    return app.test_cli_runner()
