# US #7 : Déploiement AKS

## 📋 Informations générales

| Champ | Valeur |
|-------|--------|
| **ID** | US-07 |
| **Sprint** | Sprint 2 |
| **Responsable** | Partenaire B (Architecte Kubernetes) |
| **Priorité** | Haute |
| **Statut** | 🟢 Livré (En attente déploiement) |

---

## 🎯 User Story

**En tant que** équipe d'exploitation,  
**Je veux** déployer l'application sur Azure Kubernetes Service (AKS),  
**Afin de** garantir la scalabilité, la haute disponibilité et la gestion automatisée de l'infrastructure.

---

## 📝 Description

Écrire les manifests Kubernetes nécessaires pour déployer l'application sur AKS, avec gestion des ressources, probes de santé et rolling updates.

---

## ✅ Critères d'acceptation

- [ ] Namespace dédié créé
- [ ] Deployment configuré avec :
  - [ ] Replicas : 2 minimum
  - [ ] Resources requests/limits
  - [ ] Liveness et readiness probes
  - [ ] Rolling update strategy
- [ ] Service de type LoadBalancer ou ClusterIP
- [ ] Ingress NGINX configuré
- [ ] ConfigMap pour les variables d'environnement
- [ ] Secret pour la chaîne de connexion Azure
- [ ] Application accessible via IP publique

---

## 🔧 Tâches techniques

1. [ ] Créer le cluster AKS :
   ```bash
   az aks create --resource-group myRG --name myAKS --node-count 2 --enable-managed-identity
   ```
2. [x] Créer les manifests Kubernetes :
   - [x] `k8s/namespace.yaml`
   - [x] `k8s/configmap.yaml`
   - [x] `k8s/secret.yaml`
   - [x] `k8s/deployment.yaml`
   - [x] `k8s/service.yaml`
   - [x] `k8s/ingress.yaml`
3. [ ] Installer NGINX Ingress Controller
4. [ ] Appliquer les manifests :
   ```bash
   kubectl apply -f k8s/
   ```
5. [ ] Vérifier le déploiement :
   ```bash
   kubectl get pods -n content-platform
   kubectl get svc -n content-platform
   ```

---

## 📦 Livrables

- Manifests YAML dans le dossier `k8s/`
- Application accessible via une IP publique
- Documentation des commandes de déploiement

---

## 🔗 Dépendances

- **Bloqué par** : US #3 (Dockerfile), US #5 (Pipeline CI/CD)
- **Bloque** : US #6 (Smoke Tests), US #8 (Observabilité)

---

## 📁 Structure des manifests

### k8s/namespace.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: content-platform
  labels:
    app: content-platform
```

### k8s/configmap.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: content-platform
data:
  FLASK_ENV: "production"
  CACHE_TTL: "60"
  BLOB_CONTAINER: "content"
```

### k8s/secret.yaml
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: azure-storage-secret
  namespace: content-platform
type: Opaque
stringData:
  AZURE_STORAGE_CONNECTION_STRING: "<votre-connection-string>"
```

### k8s/deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: content-platform
  namespace: content-platform
spec:
  replicas: 2
  selector:
    matchLabels:
      app: content-platform
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: content-platform
    spec:
      containers:
        - name: app
          image: ghcr.io/votre-org/projet_cloud_computing:latest
          ports:
            - containerPort: 5000
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: azure-storage-secret
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /readyz
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 10
```

### k8s/service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: content-platform-svc
  namespace: content-platform
spec:
  selector:
    app: content-platform
  ports:
    - port: 80
      targetPort: 5000
  type: ClusterIP
```

### k8s/ingress.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: content-platform-ingress
  namespace: content-platform
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: content-platform-svc
                port:
                  number: 80
```

---

## 📚 Questions à traiter (Rapport)

### 1. Rôle de chaque ressource Kubernetes ?

| Ressource | Rôle |
|-----------|------|
| **Namespace** | Isolation logique des ressources |
| **Deployment** | Gestion du cycle de vie des pods |
| **Service** | Exposition et load balancing interne |
| **Ingress** | Routage HTTP externe |
| **ConfigMap** | Configuration non sensible |
| **Secret** | Données sensibles chiffrées |

### 2. Différence entre readiness et liveness ?

| Probe | Question | Action si échec |
|-------|----------|-----------------|
| **Liveness** | L'app est-elle vivante ? | Restart du pod |
| **Readiness** | L'app peut-elle recevoir du trafic ? | Retrait du load balancer |

### 3. Impact des resources sur la scalabilité ?
- **Requests** : Minimum garanti, utilisé pour le scheduling
- **Limits** : Maximum autorisé, protection contre les fuites mémoire
- Permet au scheduler de placer efficacement les pods
- Facilite l'auto-scaling (HPA)
