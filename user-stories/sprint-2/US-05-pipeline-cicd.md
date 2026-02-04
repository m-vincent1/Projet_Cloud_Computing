# US #5 : Pipeline GitHub Actions

## 📋 Informations générales

| Champ | Valeur |
|-------|--------|
| **ID** | US-05 |
| **Sprint** | Sprint 2 |
| **Responsable** | Partenaire A (Spécialiste CI/CD) |
| **Priorité** | Haute |
| **Statut** | 🔴 À faire |

---

## 🎯 User Story

**En tant que** développeur,  
**Je veux** automatiser le build et le déploiement de l'application à chaque push sur `main`,  
**Afin de** garantir une intégration continue fiable et réduire les erreurs manuelles.

---

## 📝 Description

Créer un workflow GitHub Actions qui automatise le lint, les tests, le build Docker et le push vers GitHub Container Registry (GHCR).

---

## ✅ Critères d'acceptation

- [ ] Le workflow se déclenche à chaque push sur `main`
- [ ] Étape 1 : Lint du code Python (flake8 ou ruff)
- [ ] Étape 2 : Exécution des tests pytest
- [ ] Étape 3 : Build de l'image Docker
- [ ] Étape 4 : Push de l'image vers GHCR
- [ ] Étape 5 : Déploiement sur AKS (voir US #7)
- [ ] Les secrets sont gérés via GitHub Secrets
- [ ] Le pipeline affiche un statut vert si tout passe

---

## 🔧 Tâches techniques

1. [ ] Créer le fichier `.github/workflows/main.yml`
2. [ ] Configurer le déclencheur sur push `main`
3. [ ] Ajouter le job de lint et tests :
   - [ ] Setup Python
   - [ ] Install dependencies
   - [ ] Run flake8/ruff
   - [ ] Run pytest
4. [ ] Ajouter le job de build Docker :
   - [ ] Login to GHCR
   - [ ] Build image
   - [ ] Tag avec le SHA du commit
   - [ ] Push to GHCR
5. [ ] Configurer les GitHub Secrets :
   - [ ] `AZURE_CREDENTIALS` (pour AKS)
   - [ ] `AZURE_STORAGE_CONNECTION_STRING`
6. [ ] Documenter le pipeline dans le README

---

## 📦 Livrables

- Fichier `.github/workflows/main.yml`
- Secrets configurés dans GitHub
- Documentation du pipeline

---

## 🔗 Dépendances

- **Bloqué par** : US #2 (Tests), US #3 (Dockerfile)
- **Bloque** : US #6 (Smoke Tests), US #7 (Déploiement AKS)

---

## 📝 Exemple de workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest flake8
          
      - name: Lint with flake8
        run: flake8 app/ --max-line-length=120
        
      - name: Run tests
        run: pytest tests/ -v

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      
    steps:
      - uses: actions/checkout@v4
      
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

---

## 📚 Questions à traiter (Rapport)

### 1. Pourquoi GHCR plutôt qu'Azure Container Registry ?
- Intégré nativement avec GitHub Actions
- Gratuit avec le compte GitHub
- Permissions gérées via `GITHUB_TOKEN`
- Pas de configuration Azure supplémentaire

### 2. Comment gérer les secrets dans le pipeline ?
- Utiliser GitHub Secrets (`Settings > Secrets and variables > Actions`)
- Ne jamais hardcoder les secrets dans le code
- Utiliser `${{ secrets.NOM_SECRET }}` dans le workflow
- Limiter les permissions au minimum nécessaire

### 3. Quelle stratégie de rollback ?
- Taguer chaque image avec le SHA du commit
- En cas de problème, redéployer la version précédente
- Utiliser `kubectl rollout undo deployment/app-deployment`
- Conserver les N dernières images dans GHCR
