"""
Tests fonctionnels des endpoints API - US #1 & US #2

Ces tests vérifient que les endpoints /api/events, /api/news et /api/faq
fonctionnent correctement et retournent des données valides.
"""
import json


class TestApiEvents:
    """Tests pour l'endpoint /api/events"""

    def test_events_returns_200(self, client):
        """Vérifie que /api/events retourne HTTP 200"""
        response = client.get('/api/events')
        assert response.status_code == 200

    def test_events_returns_json(self, client):
        """Vérifie que /api/events retourne du JSON valide"""
        response = client.get('/api/events')
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_events_has_items_key(self, client):
        """Vérifie que /api/events contient une clé 'items'"""
        response = client.get('/api/events')
        data = json.loads(response.data)

        assert 'items' in data
        assert isinstance(data['items'], list)

    def test_events_items_structure(self, client):
        """Vérifie la structure des événements"""
        response = client.get('/api/events')
        data = json.loads(response.data)

        if len(data['items']) > 0:
            event = data['items'][0]
            # Vérifie les champs attendus
            assert 'id' in event
            assert 'title' in event


class TestApiNews:
    """Tests pour l'endpoint /api/news"""

    def test_news_returns_200(self, client):
        """Vérifie que /api/news retourne HTTP 200"""
        response = client.get('/api/news')
        assert response.status_code == 200

    def test_news_returns_json(self, client):
        """Vérifie que /api/news retourne du JSON valide"""
        response = client.get('/api/news')
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_news_has_items_key(self, client):
        """Vérifie que /api/news contient une clé 'items'"""
        response = client.get('/api/news')
        data = json.loads(response.data)

        assert 'items' in data
        assert isinstance(data['items'], list)

    def test_news_items_structure(self, client):
        """Vérifie la structure des actualités"""
        response = client.get('/api/news')
        data = json.loads(response.data)

        if len(data['items']) > 0:
            news = data['items'][0]
            assert 'id' in news
            assert 'title' in news


class TestApiFaq:
    """Tests pour l'endpoint /api/faq"""

    def test_faq_returns_200(self, client):
        """Vérifie que /api/faq retourne HTTP 200"""
        response = client.get('/api/faq')
        assert response.status_code == 200

    def test_faq_returns_json(self, client):
        """Vérifie que /api/faq retourne du JSON valide"""
        response = client.get('/api/faq')
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_faq_has_items_key(self, client):
        """Vérifie que /api/faq contient une clé 'items'"""
        response = client.get('/api/faq')
        data = json.loads(response.data)

        assert 'items' in data
        assert isinstance(data['items'], list)

    def test_faq_items_structure(self, client):
        """Vérifie la structure de la FAQ"""
        response = client.get('/api/faq')
        data = json.loads(response.data)

        if len(data['items']) > 0:
            faq = data['items'][0]
            assert 'id' in faq
            assert 'question' in faq
            assert 'answer' in faq


class TestIndexPage:
    """Tests pour la page d'accueil"""

    def test_index_returns_200(self, client):
        """Vérifie que / retourne HTTP 200"""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_returns_html(self, client):
        """Vérifie que / retourne du HTML"""
        response = client.get('/')
        assert 'text/html' in response.content_type
