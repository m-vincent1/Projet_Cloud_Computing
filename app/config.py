"""
Configuration de l'application Flask
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()


class Config:
    """Configuration de base"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Azure Blob Storage
    AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING', '')
    BLOB_CONTAINER_NAME = os.getenv('BLOB_CONTAINER_NAME', 'content')

    # Cache TTL (en secondes)
    CACHE_TTL = int(os.getenv('CACHE_TTL', '60'))

    # Fichiers de contenu dans le Blob
    EVENTS_FILE = os.getenv('EVENTS_FILE', 'events.json')
    NEWS_FILE = os.getenv('NEWS_FILE', 'news.json')
    FAQ_FILE = os.getenv('FAQ_FILE', 'faq.json')


class DevelopmentConfig(Config):
    """Configuration pour le développement local"""
    DEBUG = True
    # En dev, on peut utiliser des fichiers locaux
    USE_LOCAL_FILES = os.getenv('USE_LOCAL_FILES', 'True').lower() == 'true'
    LOCAL_DATA_PATH = os.getenv('LOCAL_DATA_PATH', 'data')


class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    USE_LOCAL_FILES = False


class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    USE_LOCAL_FILES = True
    LOCAL_DATA_PATH = 'tests/data'
    CACHE_TTL = 1  # Cache court pour les tests


# Sélection de la configuration selon l'environnement
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Retourne la configuration selon FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
