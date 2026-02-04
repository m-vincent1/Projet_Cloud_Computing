# US #3 : Standardisation Docker

## 📋 Informations générales

| Champ | Valeur |
|-------|--------|
| **ID** | US-03 |
| **Sprint** | Sprint 1 |
| **Responsable** | Partenaire B (Ingénieur Docker) |
| **Priorité** | Haute |
| **Statut** | 🔴 À faire |

---

## 🎯 User Story

**En tant que** équipe DevOps,  
**Je veux** conteneuriser l'application Flask dans une image Docker optimisée,  
**Afin de** garantir la portabilité, la sécurité et la reproductibilité des déploiements.

---

## 📝 Description

Créer un Dockerfile optimisé respectant les bonnes pratiques de sécurité et de performance : image slim, utilisateur non-root, pas de dépendances inutiles.

---

## ✅ Critères d'acceptation

- [ ] Le Dockerfile utilise une image de base slim (ex: `python:3.11-slim`)
- [ ] L'application s'exécute avec un utilisateur non-root
- [ ] Aucune dépendance inutile n'est incluse
- [ ] L'image se build sans erreur
- [ ] Le conteneur démarre et l'application répond correctement
- [ ] La taille de l'image est optimisée (< 200 MB idéalement)

---

## 🔧 Tâches techniques

1. [ ] Créer le Dockerfile avec multi-stage build (optionnel mais recommandé)
2. [ ] Utiliser une image de base slim (`python:3.11-slim`)
3. [ ] Créer un utilisateur non-root :
   ```dockerfile
   RUN useradd --create-home --shell /bin/bash appuser
   USER appuser
   ```
4. [ ] Optimiser les layers Docker (ordre des COPY)
5. [ ] Configurer le `.dockerignore`
6. [ ] Tester le build local :
   ```bash
   docker build -t content-platform:local .
   docker run -p 5000:5000 content-platform:local
   ```
7. [ ] Vérifier que l'application répond sur `http://localhost:5000`

---

## 📦 Livrables

- Fichier `Dockerfile` optimisé
- Fichier `.dockerignore`
- Image Docker fonctionnelle testée localement
- Documentation des commandes de build/run

---

## 🔗 Dépendances

- **Bloqué par** : US #1 (Lecture des données)
- **Bloque** : US #5 (Pipeline CI/CD), US #7 (Déploiement AKS)

---

## 📚 Questions à traiter (Rapport)

### 1. Comment réduire la taille de l'image ?
- Utiliser une image de base slim
- Multi-stage build
- Installer uniquement les dépendances de production
- Nettoyer les caches (`apt-get clean`, `pip cache purge`)

### 2. Pourquoi l'image Docker est-elle un paquet binaire d'application ?
- Elle contient tout le nécessaire pour exécuter l'application
- Elle est auto-suffisante et portable
- Elle garantit la reproductibilité entre environnements

### 3. Pourquoi le conteneur doit être stateless ?
- Facilite la scalabilité horizontale
- Permet le rolling update sans perte de données
- Les données persistantes sont stockées dans Azure Blob Storage

---

## 📝 Exemple de Dockerfile

```dockerfile
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="equipe-cloud"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Créer utilisateur non-root
RUN useradd --create-home --shell /bin/bash appuser

# Répertoire de travail
WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY --chown=appuser:appuser . .

# Changer vers l'utilisateur non-root
USER appuser

# Exposer le port
EXPOSE 5000

# Commande de démarrage
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
```
