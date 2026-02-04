# 📋 User Stories - Projet Cloud & DevOps

## Plateforme de diffusion de contenu statique cloud-native

Ce dossier contient toutes les user stories du projet, organisées par sprint.

---

## 🎯 Vue d'ensemble

| Sprint | Objectif | User Stories |
|--------|----------|--------------|
| **Sprint 1** | Développement & Conteneurisation | US #1, #2, #3, #4 |
| **Sprint 2** | Automatisation & Kubernetes | US #5, #6, #7, #8 |

---

## 👥 Répartition des rôles

### Partenaire A : Développeur Flask & Spécialiste CI/CD
- **Sprint 1** : US #1 (Lecture données), US #2 (Qualité & Santé)
- **Sprint 2** : US #5 (Pipeline GitHub Actions), US #6 (Smoke Tests)
- **Rapport** : Stratégie Git, tests unitaires, logique de cache

### Partenaire B : Ingénieur Docker & Architecte Kubernetes
- **Sprint 1** : US #3 (Dockerfile), US #4 (Stockage Cloud)
- **Sprint 2** : US #7 (Déploiement AKS), US #8 (Observabilité & Sécurité)
- **Rapport** : Choix AKS, sécurité Docker, gestion ressources K8s

---

## 📁 Structure des fichiers

```
user-stories/
├── README.md                    # Ce fichier
├── sprint-1/
│   ├── US-01-lecture-donnees.md
│   ├── US-02-qualite-sante.md
│   ├── US-03-dockerfile.md
│   └── US-04-stockage-cloud.md
└── sprint-2/
    ├── US-05-pipeline-cicd.md
    ├── US-06-smoke-tests.md
    ├── US-07-deploiement-aks.md
    └── US-08-observabilite-securite.md
```

---

## ✅ Ordre de réalisation imposé par le TP

1. Architecture & repo
2. Flask local
3. Tests Flask
4. Docker
5. CI (sans AKS)
6. AKS
7. Monitoring & sécurité
8. Démo & rapport

> ⚠️ **Règle d'or** : On ne déploie jamais ce qui n'est pas testé !
