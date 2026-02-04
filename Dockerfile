FROM python:3.11-slim

# Métadonnées
LABEL maintainer="equipe-cloud"
LABEL description="Content Platform - Static Content Delivery"
LABEL version="1.0"

# Variables d'environnement pour optimiser Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.main:app \
    FLASK_ENV=production

# Créer utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash appuser

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires et nettoyer le cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python en premier (optimisation des layers)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser data/ ./data/

# Changer vers l'utilisateur non-root
USER appuser

# Exposer le port de l'application
EXPOSE 5000

# Health check pour vérifier que l'application répond
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Commande de démarrage avec Gunicorn pour la production
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
