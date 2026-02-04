# US #1 : Lecture des données

## 📋 Informations générales

| Champ | Valeur |
|-------|--------|
| **ID** | US-01 |
| **Sprint** | Sprint 1 |
| **Responsable** | Partenaire A (Développeur Flask) |
| **Priorité** | Haute |
| **Statut** | 🔴 À faire |

---

## 🎯 User Story

**En tant que** consommateur de l'API (site web, app mobile, partenaire),  
**Je veux** accéder aux données d'événements, actualités et FAQ via des endpoints REST,  
**Afin de** pouvoir afficher dynamiquement du contenu statique sur ma plateforme.

---

## 📝 Description

Créer l'application Flask qui lit les fichiers JSON/YAML depuis Azure Blob Storage et expose les données via une API REST.

---

## ✅ Critères d'acceptation

- [ ] L'application Flask démarre sans erreur
- [ ] Les fichiers JSON/YAML sont lus depuis Azure Blob Storage
- [ ] L'endpoint `GET /api/events` retourne les événements (HTTP 200, JSON valide)
- [ ] L'endpoint `GET /api/news` retourne les actualités (HTTP 200, JSON valide)
- [ ] L'endpoint `GET /api/faq` retourne la FAQ (HTTP 200, JSON valide)
- [ ] La structure de réponse est stable (clé `items` contenant une liste)
- [ ] Une interface web minimale permet de visualiser les données

---

## 🔧 Tâches techniques

1. [ ] Initialiser le projet Flask (`app/__init__.py`, `app/main.py`)
2. [ ] Configurer la connexion Azure Blob Storage (SDK `azure-storage-blob`)
3. [ ] Créer le service de lecture des fichiers (`app/services/blob_service.py`)
4. [ ] Implémenter les routes API :
   - [ ] `/api/events`
   - [ ] `/api/news`
   - [ ] `/api/faq`
5. [ ] Gérer le parsing JSON et YAML
6. [ ] Créer une page HTML minimale pour visualiser les données
7. [ ] Documenter les endpoints dans le README

---

## 📦 Livrables

- Code Python avec les routes `/api/events`, `/api/news`, `/api/faq`
- Fichier `requirements.txt` avec les dépendances
- Documentation des endpoints

---

## 🔗 Dépendances

- **Bloqué par** : Aucune
- **Bloque** : US #2 (Qualité et Santé), US #3 (Dockerfile)

---

## 📚 Ressources

- [Azure Blob Storage SDK Python](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
