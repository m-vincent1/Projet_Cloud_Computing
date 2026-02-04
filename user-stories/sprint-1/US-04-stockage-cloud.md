# US #4 : Stockage Cloud

## 📋 Informations générales

| Champ | Valeur |
|-------|--------|
| **ID** | US-04 |
| **Sprint** | Sprint 1 |
| **Responsable** | Partenaire B (Ingénieur Docker) |
| **Priorité** | Haute |
| **Statut** | 🟢 Terminé |

---

## 🎯 User Story

**En tant que** équipe éditoriale,  
**Je veux** stocker les fichiers de contenu (événements, actualités, FAQ) dans Azure Blob Storage,  
**Afin de** centraliser et sécuriser les données tout en permettant leur mise à jour facile.

---

## 📝 Description

Configurer le compte Azure Blob Storage, créer les conteneurs nécessaires, et uploader les fichiers de test au format JSON/YAML.

---

## ✅ Critères d'acceptation

- [x] Compte Azure Storage créé sur Azure for Students
- [x] Conteneur blob créé pour les fichiers de contenu
- [x] Fichiers de test créés :
  - [x] `events.json` ou `events.yaml`
  - [x] `news.json` ou `news.yaml`
  - [x] `faq.json` ou `faq.yaml`
- [x] Chaîne de connexion sécurisée générée
- [x] Connexion testée depuis l'application locale

---

## 🔧 Tâches techniques

1. [x] Créer un compte Azure Storage :
   - Nom : `cloudprojectmatrou`
   - Tier : Standard
   - Redondance : LRS
2. [x] Créer un conteneur blob : `content`
3. [x] Créer les fichiers de test :
   - [x] `events.json`
   - [x] `news.json`
   - [x] `faq.json`
4. [x] Uploader les fichiers via Azure Portal ou CLI
5. [x] Récupérer la chaîne de connexion (Access Keys)
6. [x] Stocker la chaîne de connexion de manière sécurisée :
   - En local : fichier `.env` (non versionné) - `.env.example` créé
   - En prod : Kubernetes Secret
7. [x] Tester la connexion depuis l'application

---

## 📦 Livrables

- Compte Azure Blob Storage configuré
- Fichiers de contenu uploadés
- Chaîne de connexion sécurisée prête à l'emploi
- Fichier `.env.example` (template sans valeurs sensibles)

---

## 🔗 Dépendances

- **Bloqué par** : Aucune (peut commencer en parallèle de US #1)
- **Bloque** : US #1 (pour les tests réels), US #8 (Managed Identity)

---

## 📁 Structure des fichiers de contenu

### events.json
```json
{
  "items": [
    {
      "id": 1,
      "title": "Conférence Cloud Computing",
      "date": "2026-03-15",
      "location": "Paris",
      "description": "Introduction aux services Azure"
    },
    {
      "id": 2,
      "title": "Workshop Kubernetes",
      "date": "2026-04-10",
      "location": "Lyon",
      "description": "Déploiement d'applications sur AKS"
    }
  ]
}
```

### news.json
```json
{
  "items": [
    {
      "id": 1,
      "title": "Nouvelle version de la plateforme",
      "date": "2026-02-01",
      "content": "Lancement de la v2.0 avec de nouvelles fonctionnalités"
    },
    {
      "id": 2,
      "title": "Partenariat stratégique",
      "date": "2026-02-10",
      "content": "Annonce d'un nouveau partenariat avec Microsoft"
    }
  ]
}
```

### faq.json
```json
{
  "items": [
    {
      "id": 1,
      "question": "Comment accéder à la plateforme ?",
      "answer": "Rendez-vous sur le portail web ou utilisez l'API REST."
    },
    {
      "id": 2,
      "question": "Quels formats de données sont supportés ?",
      "answer": "La plateforme supporte JSON et YAML."
    }
  ]
}
```

---

## 📚 Ressources

- [Azure Portal](https://portal.azure.com/)
- [Azure CLI - Blob Storage](https://docs.microsoft.com/en-us/cli/azure/storage/blob)
- [Azure for Students](https://azure.microsoft.com/en-us/free/students/)

---

## 🔐 Sécurité

> ⚠️ **IMPORTANT** : La chaîne de connexion ne doit JAMAIS être versionnée dans Git !

- Ajouter `.env` au `.gitignore`
- Utiliser des variables d'environnement
- En production, préférer Managed Identity (voir US #8)
