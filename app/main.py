"""
Application Flask principale - Plateforme de diffusion de contenu statique
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, jsonify, render_template_string

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Instance Flask
app = Flask(__name__)

# Configuration
USE_LOCAL_FILES = os.getenv('USE_LOCAL_FILES', 'True').lower() == 'true'
LOCAL_DATA_PATH = os.getenv('LOCAL_DATA_PATH', 'data')
CACHE_TTL = int(os.getenv('CACHE_TTL', '60'))

# Cache simple en mémoire
_cache = {}
_cache_timestamps = {}

# Heure de démarrage pour les health checks
START_TIME = datetime.utcnow()


def get_cached_data(filename):
    """Récupère les données avec cache TTL"""
    now = datetime.utcnow()
    
    # Vérifier si le cache est valide
    if filename in _cache and filename in _cache_timestamps:
        age = (now - _cache_timestamps[filename]).total_seconds()
        if age < CACHE_TTL:
            logger.debug(f"Cache hit for {filename}")
            return _cache[filename]
    
    # Charger depuis le fichier
    logger.debug(f"Cache miss for {filename}, loading...")
    filepath = os.path.join(LOCAL_DATA_PATH, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        _cache[filename] = data
        _cache_timestamps[filename] = now
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return {"items": [], "error": f"File not found: {filename}"}
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {filepath}: {e}")
        return {"items": [], "error": f"Invalid JSON in {filename}"}


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
    """
    return jsonify({
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "service_initialized": True
        }
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Alias pour la compatibilité avec le Dockerfile HEALTHCHECK"""
    return jsonify({"status": "healthy"}), 200


# =============================================================================
# ENDPOINTS API REST
# =============================================================================

@app.route('/api/events', methods=['GET'])
def get_events():
    """Retourne la liste des événements."""
    try:
        data = get_cached_data('events.json')
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({"error": "Internal server error", "items": []}), 500


@app.route('/api/news', methods=['GET'])
def get_news():
    """Retourne la liste des actualités."""
    try:
        data = get_cached_data('news.json')
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return jsonify({"error": "Internal server error", "items": []}), 500


@app.route('/api/faq', methods=['GET'])
def get_faq():
    """Retourne la FAQ."""
    try:
        data = get_cached_data('faq.json')
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
            background: #00c853;
        }
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
        }
        .item {
            background: rgba(0,0,0,0.2);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }
        .item-title { font-weight: bold; color: #7b2cbf; }
        .item-date { font-size: 0.8rem; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Plateforme de Contenu Cloud-Native</h1>
        <div class="status">
            <span class="status-badge" id="health-status">⏳ Vérification...</span>
        </div>
        <div class="cards">
            <div class="card">
                <h2>📅 Événements</h2>
                <div id="events-content"><p>Chargement...</p></div>
            </div>
            <div class="card">
                <h2>📰 Actualités</h2>
                <div id="news-content"><p>Chargement...</p></div>
            </div>
            <div class="card">
                <h2>❓ FAQ</h2>
                <div id="faq-content"><p>Chargement...</p></div>
            </div>
        </div>
    </div>
    <script>
        async function fetchData() {
            try {
                const health = await fetch('/healthz').then(r => r.json());
                document.getElementById('health-status').textContent =
                    '✅ ' + health.status + ' (uptime: ' + Math.round(health.uptime_seconds) + 's)';
            } catch (e) {
                document.getElementById('health-status').textContent = '❌ Erreur';
            }
            try {
                const events = await fetch('/api/events').then(r => r.json());
                document.getElementById('events-content').innerHTML = events.items.map(e =>
                    '<div class="item"><div class="item-title">' + e.title + '</div><div class="item-date">' + e.date + '</div><div>' + (e.description || '') + '</div></div>'
                ).join('');
            } catch (e) {}
            try {
                const news = await fetch('/api/news').then(r => r.json());
                document.getElementById('news-content').innerHTML = news.items.map(n =>
                    '<div class="item"><div class="item-title">' + n.title + '</div><div class="item-date">' + n.date + '</div><div>' + (n.content || '') + '</div></div>'
                ).join('');
            } catch (e) {}
            try {
                const faq = await fetch('/api/faq').then(r => r.json());
                document.getElementById('faq-content').innerHTML = faq.items.map(f =>
                    '<div class="item"><div class="item-title">Q: ' + f.question + '</div><div>R: ' + f.answer + '</div></div>'
                ).join('');
            } catch (e) {}
        }
        fetchData();
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
