# US #2 : Qualité et Santé

## 📋 Informations générales

| Champ | Valeur |
|-------|--------|
| **ID** | US-02 |
| **Sprint** | Sprint 1 |
| **Responsable** | Partenaire A (Développeur Flask) |
| **Priorité** | Haute |
| **Statut** | 🔴 À faire |

---

## 🎯 User Story

**En tant que** opérateur de la plateforme,  
**Je veux** vérifier l'état de santé de l'application et optimiser les performances,  
**Afin de** garantir la disponibilité du service et réduire la charge sur Azure Blob Storage.

---

## 📝 Description

Implémenter un système de cache mémoire avec TTL (60 secondes) pour optimiser les performances, ainsi que les endpoints de vérification de santé requis par Kubernetes.

---

## ✅ Critères d'acceptation

### Cache mémoire
- [ ] Les données sont mises en cache pendant 60 secondes
- [ ] Après expiration du TTL, les données sont rechargées depuis Blob Storage
- [ ] Le cache réduit significativement les appels à Azure

### Health checks
- [ ] L'endpoint `GET /healthz` retourne HTTP 200
- [ ] L'endpoint `GET /readyz` retourne HTTP 200
- [ ] Les réponses sont au format JSON valide
- [ ] Un champ indique l'état du service (ex: `{"status": "healthy"}`)

### Tests
- [ ] Les tests pytest passent en local
- [ ] Les tests sont indépendants de l'environnement Azure
- [ ] Les tests sont reproductibles

---

## 🔧 Tâches techniques

1. [ ] Implémenter le cache mémoire avec TTL :
   - [ ] Utiliser `cachetools` ou implémentation manuelle
   - [ ] Configurer TTL à 60 secondes
2. [ ] Créer l'endpoint `/healthz` (liveness probe)
3. [ ] Créer l'endpoint `/readyz` (readiness probe)
4. [ ] Écrire les tests pytest :
   - [ ] `test_healthz()` - vérifie HTTP 200 et JSON valide
   - [ ] `test_readyz()` - vérifie HTTP 200 et JSON valide
   - [ ] `test_api_events()` - vérifie la structure de réponse
   - [ ] `test_api_news()` - vérifie la structure de réponse
   - [ ] `test_api_faq()` - vérifie la structure de réponse
5. [ ] Configurer les mocks pour les tests (indépendance Azure)

---

## 📦 Livrables

- Cache mémoire fonctionnel avec TTL de 60s
- Endpoints `/healthz` et `/readyz`
- Script pytest validant les codes HTTP 200
- Fichier `tests/test_health.py`
- Fichier `tests/test_api.py`

---

## 🔗 Dépendances

- **Bloqué par** : US #1 (Lecture des données)
- **Bloque** : US #5 (Pipeline CI/CD), US #6 (Smoke Tests)

---

## 📚 Ressources

### Différence Liveness vs Readiness

| Probe | Objectif | Endpoint |
|-------|----------|----------|
| **Liveness** | L'application est-elle vivante ? (sinon restart) | `/healthz` |
| **Readiness** | L'application peut-elle recevoir du trafic ? | `/readyz` |

- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [pytest Documentation](https://docs.pytest.org/)
- [cachetools](https://cachetools.readthedocs.io/)
