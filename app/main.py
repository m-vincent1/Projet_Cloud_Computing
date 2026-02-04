"""
Application Flask principale - Plateforme de diffusion de contenu statique
"""
import os
import logging
from datetime import datetime
from flask import Flask, jsonify, render_template_string

from .config import get_config
from .services import ContentService

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Instance Flask
app = Flask(__name__)

# Charger la configuration
config = get_config()
app.config.from_object(config)

# Initialiser le service de contenu
content_service = ContentService(config)

# Heure de démarrage pour les health checks
START_TIME = datetime.utcnow()


# =============================================================================
# ENDPOINTS DE SANTÉ (Health Checks)
# =============================================================================

@app.route('/healthz', methods=['GET'])
def healthz():
    """
    Liveness probe - Vérifie si l'application est vivante.
    Kubernetes restart le pod si cet endpoint échoue.
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": (datetime.utcnow() - START_TIME).total_seconds()
    }), 200


@app.route('/readyz', methods=['GET'])
def readyz():
    """
    Readiness probe - Vérifie si l'application peut recevoir du trafic.
    Kubernetes retire le pod du load balancer si cet endpoint échoue.
    """
    # Vérifier si le service de contenu est prêt
    is_ready = True
    checks = {
        "service_initialized": content_service is not None
    }

    # En production, vérifier la connexion Blob
    if not getattr(config, 'USE_LOCAL_FILES', False):
        checks["blob_storage"] = content_service.is_blob_available()
        is_ready = is_ready and checks["blob_storage"]

    status = "ready" if is_ready else "not_ready"
    status_code = 200 if is_ready else 503

    return jsonify({
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }), status_code


# =============================================================================
# ENDPOINTS API REST
# =============================================================================

@app.route('/api/events', methods=['GET'])
def get_events():
    """
    Retourne la liste des événements.

    Returns:
        JSON contenant les événements avec clé 'items'
    """
    try:
        data = content_service.get_events()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({"error": "Internal server error", "items": []}), 500


@app.route('/api/news', methods=['GET'])
def get_news():
    """
    Retourne la liste des actualités.

    Returns:
        JSON contenant les actualités avec clé 'items'
    """
    try:
        data = content_service.get_news()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return jsonify({"error": "Internal server error", "items": []}), 500


@app.route('/api/faq', methods=['GET'])
def get_faq():
    """
    Retourne la FAQ.

    Returns:
        JSON contenant les questions/réponses avec clé 'items'
    """
    try:
        data = content_service.get_faq()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching FAQ: {e}")
        return jsonify({"error": "Internal server error", "items": []}), 500


# =============================================================================
# INTERFACE WEB MINIMALE
# =============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plateforme de Contenu</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #fff;
            padding: 2rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            text-align: center;
            margin-bottom: 2rem;
            font-size: 2.5rem;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .status {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .status-badge {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        .status-ok { background: #00c853; }
        .status-error { background: #ff5252; }
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card h2 {
            color: #00d4ff;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .card-content {
            max-height: 300px;
            overflow-y: auto;
        }
        .item {
            background: rgba(0,0,0,0.2);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }
        .item-title { font-weight: bold; color: #7b2cbf; }
        .item-date { font-size: 0.8rem; color: #888; }
        .loading { text-align: center; color: #888; }
        .error { color: #ff5252; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Plateforme de Contenu Cloud-Native</h1>

        <div class="status">
            <span class="status-badge status-ok" id="health-status">⏳ Vérification...</span>
        </div>

        <div class="cards">
            <div class="card">
                <h2>📅 Événements</h2>
                <div class="card-content" id="events-content">
                    <p class="loading">Chargement...</p>
                </div>
            </div>

            <div class="card">
                <h2>📰 Actualités</h2>
                <div class="card-content" id="news-content">
                    <p class="loading">Chargement...</p>
                </div>
            </div>

            <div class="card">
                <h2>❓ FAQ</h2>
                <div class="card-content" id="faq-content">
                    <p class="loading">Chargement...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function fetchData() {
            // Health check
            try {
                const health = await fetch('/healthz').then(r => r.json());
                document.getElementById('health-status').textContent =
                    '✅ ' + health.status + ' (uptime: ' + Math.round(health.uptime_seconds) + 's)';
            } catch (e) {
                document.getElementById('health-status').className = 'status-badge status-error';
                document.getElementById('health-status').textContent = '❌ Erreur santé';
            }

            // Events
            try {
                const events = await fetch('/api/events').then(r => r.json());
                renderItems('events-content', events.items, 'title', 'date', 'description');
            } catch (e) {
                document.getElementById('events-content').innerHTML = '<p class="error">Erreur de chargement</p>';
            }

            // News
            try {
                const news = await fetch('/api/news').then(r => r.json());
                renderItems('news-content', news.items, 'title', 'date', 'content');
            } catch (e) {
                document.getElementById('news-content').innerHTML = '<p class="error">Erreur de chargement</p>';
            }

            // FAQ
            try {
                const faq = await fetch('/api/faq').then(r => r.json());
                renderFaq('faq-content', faq.items);
            } catch (e) {
                document.getElementById('faq-content').innerHTML = '<p class="error">Erreur de chargement</p>';
            }
        }

        function renderItems(containerId, items, titleField, dateField, contentField) {
            const container = document.getElementById(containerId);
            if (!items || items.length === 0) {
                container.innerHTML = '<p class="loading">Aucun élément</p>';
                return;
            }
            container.innerHTML = items.map(item => `
                <div class="item">
                    <div class="item-title">${item[titleField] || 'Sans titre'}</div>
                    <div class="item-date">${item[dateField] || ''}</div>
                    <div>${item[contentField] || ''}</div>
                </div>
            `).join('');
        }

        function renderFaq(containerId, items) {
            const container = document.getElementById(containerId);
            if (!items || items.length === 0) {
                container.innerHTML = '<p class="loading">Aucune question</p>';
                return;
            }
            container.innerHTML = items.map(item => `
                <div class="item">
                    <div class="item-title">Q: ${item.question || ''}</div>
                    <div>R: ${item.answer || ''}</div>
                </div>
            `).join('');
        }

        fetchData();
        // Rafraîchir toutes les 60 secondes (même que le cache TTL)
        setInterval(fetchData, 60000);
    </script>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    """Interface web minimale pour visualiser les données"""
    return render_template_string(HTML_TEMPLATE)


# =============================================================================
# POINT D'ENTRÉE
# =============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
