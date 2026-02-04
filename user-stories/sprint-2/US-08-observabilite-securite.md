# US #8 : Observabilité & Sécurité

## 📋 Informations générales

| Champ | Valeur |
|-------|--------|
| **ID** | US-08 |
| **Sprint** | Sprint 2 |
| **Responsable** | Partenaire B (Architecte Kubernetes) |
| **Priorité** | Moyenne |
| **Statut** | 🔴 À faire |

---

## 🎯 User Story

**En tant que** équipe SRE (Site Reliability Engineering),  
**Je veux** surveiller l'application et sécuriser l'accès aux données,  
**Afin de** garantir la disponibilité du service et protéger les données sensibles.

---

## 📝 Description

Configurer Azure Monitor pour le monitoring basique (CPU, mémoire, disponibilité), mettre en place des alertes, et sécuriser l'accès au Blob Storage (idéalement via Managed Identity).

---

## ✅ Critères d'acceptation

### Observabilité
- [ ] Métriques CPU et mémoire visibles dans Azure Monitor
- [ ] Disponibilité du service monitorée
- [ ] Logs applicatifs niveau INFO configurés
- [ ] 1 alerte configurée (ex : erreurs 5xx > 10/min)
- [ ] Dashboard basique créé

### Sécurité
- [ ] Secrets non exposés dans le code
- [ ] Accès Blob via Secret Kubernetes (minimum)
- [ ] Image Docker non-root (vérifié US #3)
- [ ] **Bonus** : Accès Blob via Managed Identity

---

## 🔧 Tâches techniques

### Observabilité

1. [ ] Activer Azure Monitor pour AKS :
   ```bash
   az aks enable-addons --resource-group myRG --name myAKS --addons monitoring
   ```
2. [ ] Configurer les logs applicatifs :
   - [ ] Niveau INFO dans l'app Flask
   - [ ] Format JSON pour parsing facile
3. [ ] Créer une alerte pour les erreurs 5xx :
   - Azure Portal > Alerts > New alert rule
   - Condition : HTTP 5xx count > 10 sur 5 min
4. [ ] Créer un dashboard basique :
   - CPU usage
   - Memory usage
   - Request count
   - Error rate

### Sécurité

5. [ ] Vérifier que `.env` est dans `.gitignore`
6. [ ] Vérifier que les secrets sont dans Kubernetes Secrets
7. [ ] **Bonus** - Configurer Managed Identity :
   ```bash
   # Activer Managed Identity sur AKS
   az aks update --resource-group myRG --name myAKS --enable-managed-identity
   
   # Attribuer le rôle au Storage
   az role assignment create --role "Storage Blob Data Reader" \
     --assignee <managed-identity-client-id> \
     --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage>
   ```

---

## 📦 Livrables

- Monitoring Azure configuré
- Alerte 5xx fonctionnelle
- Rapport de monitoring
- Accès sécurisé au Blob Storage (sans mot de passe en clair si Managed Identity)

---

## 🔗 Dépendances

- **Bloqué par** : US #7 (Déploiement AKS)
- **Bloque** : Aucune (dernière US technique)

---

## 📊 Métriques à surveiller

| Métrique | Objectif | Seuil d'alerte |
|----------|----------|----------------|
| CPU Usage | < 80% | > 90% pendant 5 min |
| Memory Usage | < 80% | > 90% pendant 5 min |
| Request Latency (p99) | < 500ms | > 1s pendant 1 min |
| Error Rate (5xx) | < 1% | > 5% pendant 1 min |
| Pod Restarts | 0 | > 3 en 10 min |

---

## 📚 Questions à traiter (Rapport)

### 1. Quelles métriques sont réellement utiles ?

**Métriques essentielles :**
- **CPU/Mémoire** : Détection des fuites et dimensionnement
- **Latence** : Expérience utilisateur
- **Taux d'erreur** : Fiabilité du service
- **Disponibilité** : SLA

**Métriques secondaires :**
- Nombre de requêtes par endpoint
- Temps de réponse du cache vs Blob Storage
- Nombre de pods actifs

### 2. Pourquoi éviter une journalisation excessive ?

- **Coût** : Azure Monitor facture au volume de données
- **Performance** : I/O disque, latence réseau
- **Bruit** : Difficile de trouver les vraies erreurs
- **RGPD** : Risque de logger des données personnelles

**Bonne pratique** : Logger en INFO en prod, DEBUG seulement en dev.

### 3. Comment limiter les coûts Azure Monitor ?

- Utiliser le **Free Tier** (5 GB ingestion/mois)
- **Filtrer les logs** : seulement WARNING+ en prod
- **Échantillonnage** : ne pas logger 100% des requêtes
- **Rétention courte** : 30 jours au lieu de 90
- **Alertes intelligentes** : éviter les faux positifs

---

## 🔐 Sécurité - Questions à traiter (Rapport)

### 1. Pourquoi ne pas stocker de secrets dans Git ?

- Git conserve tout l'historique (même après suppression)
- Dépôts forkés/clonés héritent des secrets
- Bots scannent GitHub en permanence
- Une fuite = compromission de tous les services

### 2. Avantages Managed Identity vs clé statique ?

| Critère | Clé statique | Managed Identity |
|---------|--------------|------------------|
| Rotation | Manuelle | Automatique |
| Stockage | Secret K8s | Aucun |
| Risque de fuite | Élevé | Quasi-nul |
| Configuration | Simple | Plus complexe |

### 3. Risques de fuite dans les logs ?

- Connection strings dans les stack traces
- Tokens dans les URLs loggées
- Données utilisateur sensibles
- Headers d'authentification

**Mitigation** :
- Sanitiser les logs avant écriture
- Ne jamais logger les secrets
- Utiliser des placeholders : `***REDACTED***`

---

## 📝 Configuration logging Flask

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# Configuration
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.root.addHandler(handler)
logging.root.setLevel(logging.INFO)
```
