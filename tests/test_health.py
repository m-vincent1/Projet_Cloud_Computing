"""
Tests de santé (Health Checks) - US #2

Ces tests vérifient que les endpoints /healthz et /readyz
fonctionnent correctement pour Kubernetes.
"""
import json


class TestHealthz:
    """Tests pour l'endpoint /healthz (liveness probe)"""

    def test_healthz_returns_200(self, client):
        """Vérifie que /healthz retourne HTTP 200"""
        response = client.get('/healthz')
        assert response.status_code == 200

    def test_healthz_returns_json(self, client):
        """Vérifie que /healthz retourne du JSON valide"""
        response = client.get('/healthz')
        assert response.content_type == 'application/json'

        # Vérifie que c'est du JSON valide
        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_healthz_has_status_field(self, client):
        """Vérifie que /healthz contient un champ 'status'"""
        response = client.get('/healthz')
        data = json.loads(response.data)

        assert 'status' in data
        assert data['status'] == 'healthy'


class TestReadyz:
    """Tests pour l'endpoint /readyz (readiness probe)"""

    def test_readyz_returns_200(self, client):
        """Vérifie que /readyz retourne HTTP 200"""
        response = client.get('/readyz')
        assert response.status_code == 200

    def test_readyz_returns_json(self, client):
        """Vérifie que /readyz retourne du JSON valide"""
        response = client.get('/readyz')
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_readyz_has_status_field(self, client):
        """Vérifie que /readyz contient un champ 'status'"""
        response = client.get('/readyz')
        data = json.loads(response.data)

        assert 'status' in data
        assert data['status'] in ['ready', 'not_ready']

    def test_readyz_has_azure_connection(self, client):
        """Vérifie que /readyz contient l'état de la connexion Azure"""
        response = client.get('/readyz')
        data = json.loads(response.data)

        assert 'azure_connection' in data
        assert data['azure_connection'] in ['connected', 'failed']
