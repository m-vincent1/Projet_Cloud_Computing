"""
Application Flask principale - Plateforme de diffusion de contenu statique
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, jsonify, render_template_string
from app.config import Config
from app.services.content_service import ContentService

# Configuration du logging structuré pour Azure Monitor (US-08)
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "logger": record.name
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.root.addHandler(handler)
logging.root.setLevel(logging.INFO)
# Supprimer le handler par défaut s'il existe pour éviter les doublons
logging.getLogger().handlers = [handler]
logger = logging.getLogger(__name__)

# Instance Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialisation du service de contenu (Azure + Cache)
content_service = ContentService(app.config)


# =============================================================================
# ENDPOINTS DE SANTÉ (Health Checks)
# =============================================================================

@app.route('/healthz', methods=['GET'])
def healthz():
    """Liveness probe"""
    return jsonify({"status": "healthy"}), 200


@app.route('/readyz', methods=['GET'])
def readyz():
    """Readiness probe"""
    is_ready = content_service.is_blob_available() if not app.config.get('USE_LOCAL_FILES') else True
    status = 200 if is_ready else 503
    return jsonify({
        "status": "ready" if is_ready else "not_ready",
        "azure_connection": "connected" if is_ready else "failed"
    }), status


@app.route('/health', methods=['GET'])
def health():
    """Alias pour compatibilité"""
    return jsonify({"status": "healthy"}), 200


# =============================================================================
# ENDPOINTS API REST
# =============================================================================

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(content_service.get_events()), 200


@app.route('/api/news', methods=['GET'])
def get_news():
    return jsonify(content_service.get_news()), 200


@app.route('/api/faq', methods=['GET'])
def get_faq():
    return jsonify(content_service.get_faq()), 200


# =============================================================================
# INTERFACE WEB MINIMALE
# =============================================================================
# ... (le template HTML reste identique, je le réutilise pour la concision) ...

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plateforme de Contenu (Azure Connected)</title>
    <style>
        body { font-family: sans-serif; padding: 2rem; background: #f0f2f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #1a73e8; }
        .item { border-bottom: 1px solid #eee; padding: 1rem 0; }
        .success { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Plateforme Cloud (Azure V2)</h1>
        <div id="status">Chargement...</div>
        <hr>
        <h2>Dernières News</h2>
        <div id="news"></div>
    </div>
    <script>
        fetch('/readyz')
            .then(r => r.json())
            .then(d => document.getElementById('status').innerHTML = 
                d.status === 'ready' ? '<span class="success">✅ Connecté à Azure Blob Storage</span>' : '❌ Erreur Connexion')
            .catch(() => document.getElementById('status').innerText = '❌ API Inaccessible');

        fetch('/api/news')
            .then(r => r.json())
            .then(d => {
                const html = d.items ? d.items.map(i => `<div class="item"><h3>${i.title}</h3><p>${i.content}</p></div>`).join('') : 'Aucune news';
                document.getElementById('news').innerHTML = html;
            });
    </script>
</body>
</html>"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
