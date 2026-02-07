# 🚀 Plateforme de Diffusion de Contenu Statique Cloud-Native

## 📖 Description du Projet

Ce projet a été réalisé dans le cadre du module **Cloud Computing** en Master 2. Nous avons développé une plateforme de diffusion de contenu statique utilisant les technologies cloud-native.

**Auteurs :**
- **Roulem BAITICHE** - Partenaire A (Application Flask & CI/CD)
- **Mathis VINCENT** - Partenaire B (Docker, Azure & Kubernetes)

---

## 🎯 Objectifs du Projet

Nous devions créer une application cloud-native complète avec :
- Une API REST pour servir du contenu statique (événements, actualités, FAQ)
- Une intégration avec Azure Blob Storage
- Un pipeline CI/CD automatisé
- Un déploiement sur Azure Kubernetes Service (AKS)

---

## 👥 Répartition du Travail

### Roulem (Partenaire A) - Développeur Flask & CI/CD

#### Sprint 1
**US #1 - Lecture des données**
> J'ai développé l'application Flask principale avec les endpoints REST `/api/events`, `/api/news` et `/api/faq`. J'ai implémenté un système de cache en mémoire avec TTL de 60 secondes pour optimiser les performances.

**US #2 - Qualité et Santé**
> J'ai créé les endpoints de health check `/healthz` et `/readyz` pour Kubernetes. J'ai également écrit 21 tests unitaires avec pytest pour garantir la qualité du code.

#### Sprint 2
**US #5 - Pipeline CI/CD**
> J'ai mis en place le pipeline GitHub Actions complet qui automatise le lint (flake8), les tests (pytest), le build de l'image Docker et le push vers GitHub Container Registry (GHCR).

**US #6 - Smoke Tests**
> J'ai développé un script de smoke tests qui vérifie automatiquement que tous les endpoints de l'application répondent correctement après chaque déploiement.

---

### Mathis (Partenaire B) - Spécialiste Docker, Azure & Kubernetes

#### Sprint 1
**US #3 - Dockerfile**
> J'ai créé le Dockerfile optimisé avec une image `python:3.11-slim`, un utilisateur non-root pour la sécurité, et un health check intégré.

**US #4 - Stockage Cloud**
> J'ai configuré Azure Blob Storage pour stocker les fichiers de contenu (events.json, news.json, faq.json) et j'ai développé le ContentService pour lire ces données.

#### Sprint 2
**US #7 - Déploiement AKS**
> J'ai créé les manifestes Kubernetes (Deployment, Service, ConfigMap, Secret, Ingress) pour déployer l'application sur Azure Kubernetes Service.

**US #8 - Observabilité & Sécurité**
> J'ai implémenté le logging structuré en JSON pour Azure Monitor et configuré les alertes de sécurité.

---

## 🛠️ Technologies Utilisées

| Technologie | Utilisation |
|-------------|-------------|
| **Python 3.11** | Langage principal |
| **Flask** | Framework web |
| **Azure Blob Storage** | Stockage des données |
| **Docker** | Conteneurisation |
| **GitHub Actions** | CI/CD |
| **GitHub Container Registry** | Stockage des images Docker |
| **Azure Kubernetes Service** | Orchestration |
| **pytest** | Tests unitaires |

---

## 📂 Structure du Projet

```
Projet_Cloud_Computing/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration (Azure, Cache)
│   ├── main.py                # Application Flask principale
│   ├── requirements.txt       # Dépendances Python
│   └── services/
│       └── content_service.py # Service de lecture Azure/Local
├── data/                      # Données locales de développement
│   ├── events.json
│   ├── news.json
│   └── faq.json
├── tests/                     # Tests unitaires
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_health.py
│   └── data/
├── k8s/                       # Manifestes Kubernetes
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── ingress.yaml
├── scripts/
│   └── smoke-test.sh          # Tests post-déploiement
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline CI/CD
├── Dockerfile                 # Image Docker optimisée
├── .dockerignore
├── .env.example               # Template de configuration
└── README.md
```

---

## 🚀 Comment Lancer le Projet

### Prérequis
- Python 3.11+
- Docker (optionnel)
- Compte Azure (pour le déploiement)

### Installation locale

```bash
# Cloner le repo
git clone https://github.com/m-vincent1/Projet_Cloud_Computing.git
cd Projet_Cloud_Computing

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r app/requirements.txt

# Lancer l'application
FLASK_ENV=development USE_LOCAL_FILES=True LOCAL_DATA_PATH=data flask --app app.main run --port 5001
```

### Accès à l'application
- **Interface web** : http://localhost:5001
- **Health check** : http://localhost:5001/healthz
- **API Events** : http://localhost:5001/api/events
- **API News** : http://localhost:5001/api/news
- **API FAQ** : http://localhost:5001/api/faq

### Lancer les tests

```bash
# Tests unitaires
pytest tests/ -v

# Smoke tests
./scripts/smoke-test.sh http://localhost:5001
```

### Build Docker

```bash
docker build -t content-platform .
docker run -p 5000:5000 -e USE_LOCAL_FILES=True content-platform
```

---

## ⚙️ Pipeline CI/CD

Notre pipeline GitHub Actions s'exécute automatiquement à chaque push sur `main` :

1. **🧪 Lint & Tests** - Vérifie la qualité du code (flake8) et exécute les 21 tests
2. **🐳 Build & Push Docker** - Construit l'image et la pousse sur GHCR
3. **🔥 Smoke Tests** - Vérifie que l'application fonctionne dans le conteneur

---

## 📊 Résultats

| Métrique | Valeur |
|----------|--------|
| Tests unitaires | 21 passed ✅ |
| Smoke tests | 7 passed ✅ |
| Couverture de code | Rapport disponible |
| Pipeline CI/CD | ✅ Fonctionnel |
| Image Docker | ghcr.io/m-vincent1/projet_cloud_computing |

---

## 🔗 Liens Utiles

- **Repository GitHub** : https://github.com/m-vincent1/Projet_Cloud_Computing
- **GitHub Actions** : https://github.com/m-vincent1/Projet_Cloud_Computing/actions
- **Image Docker** : https://github.com/m-vincent1/Projet_Cloud_Computing/pkgs/container/projet_cloud_computing

---

## 📝 Licence

Projet réalisé dans le cadre du Master 2 - Module Cloud Computing.

**© 2026 Roulem BAITICHE & Mathis VINCENT**