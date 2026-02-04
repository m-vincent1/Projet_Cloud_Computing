# US #6 : Smoke Tests

## 📋 Informations générales

| Champ | Valeur |
|-------|--------|
| **ID** | US-06 |
| **Sprint** | Sprint 2 |
| **Responsable** | Partenaire A (Spécialiste CI/CD) |
| **Priorité** | Moyenne |
| **Statut** | 🔴 À faire |

---

## 🎯 User Story

**En tant que** équipe DevOps,  
**Je veux** vérifier automatiquement que l'application fonctionne après chaque déploiement,  
**Afin de** détecter immédiatement les régressions en production.

---

## 📝 Description

Ajouter une étape de smoke test dans le pipeline CI/CD qui vérifie que l'API répond correctement sur AKS après le déploiement.

---

## ✅ Critères d'acceptation

- [ ] Un smoke test s'exécute après le déploiement sur AKS
- [ ] Le test vérifie que `/healthz` retourne HTTP 200
- [ ] Le test vérifie que `/readyz` retourne HTTP 200
- [ ] Le test vérifie qu'au moins un endpoint API répond
- [ ] Le pipeline passe au "Vert" uniquement si l'app est en ligne
- [ ] Le pipeline échoue si les tests ne passent pas

---

## 🔧 Tâches techniques

1. [ ] Créer un script de smoke test :
   - [ ] `scripts/smoke-test.sh` (bash)
   - [ ] ou `tests/smoke_test.py` (Python)
2. [ ] Configurer le test pour utiliser l'URL de prod
3. [ ] Ajouter l'étape au workflow GitHub Actions :
   ```yaml
   - name: Smoke test
     run: ./scripts/smoke-test.sh ${{ env.APP_URL }}
   ```
4. [ ] Configurer un timeout raisonnable
5. [ ] Attendre que le déploiement soit prêt avant de tester

---

## 📦 Livrables

- Script de smoke test
- Étape de test dans le pipeline
- Pipeline qui passe au "Vert" uniquement si l'app est en ligne

---

## 🔗 Dépendances

- **Bloqué par** : US #5 (Pipeline), US #7 (Déploiement AKS)
- **Bloque** : Aucune (fin du cycle CI/CD)

---

## 📝 Exemple de script smoke-test.sh

```bash
#!/bin/bash
set -e

APP_URL=${1:-"http://localhost:5000"}
MAX_RETRIES=10
RETRY_INTERVAL=10

echo "🔍 Running smoke tests against: $APP_URL"

# Fonction pour tester un endpoint
test_endpoint() {
    local endpoint=$1
    local expected_status=${2:-200}
    
    echo "Testing $endpoint..."
    
    status=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL$endpoint" || echo "000")
    
    if [ "$status" -eq "$expected_status" ]; then
        echo "✅ $endpoint returned $status"
        return 0
    else
        echo "❌ $endpoint returned $status (expected $expected_status)"
        return 1
    fi
}

# Attendre que l'app soit prête
echo "⏳ Waiting for application to be ready..."
for i in $(seq 1 $MAX_RETRIES); do
    if curl -s "$APP_URL/healthz" > /dev/null 2>&1; then
        echo "✅ Application is responding"
        break
    fi
    
    if [ $i -eq $MAX_RETRIES ]; then
        echo "❌ Application not responding after $MAX_RETRIES attempts"
        exit 1
    fi
    
    echo "Attempt $i/$MAX_RETRIES - Retrying in ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

# Exécuter les tests
echo ""
echo "🧪 Running endpoint tests..."
echo "=========================="

test_endpoint "/healthz" 200
test_endpoint "/readyz" 200
test_endpoint "/api/events" 200
test_endpoint "/api/news" 200
test_endpoint "/api/faq" 200

echo ""
echo "=========================="
echo "✅ All smoke tests passed!"
```

---

## 📝 Intégration dans le workflow

```yaml
  smoke-test:
    needs: deploy
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Wait for deployment to stabilize
        run: sleep 30
        
      - name: Run smoke tests
        run: |
          chmod +x ./scripts/smoke-test.sh
          ./scripts/smoke-test.sh ${{ secrets.APP_URL }}
```

---

## 📚 Ressources

- [Smoke Testing Best Practices](https://martinfowler.com/bliki/SmokeTest.html)
- [curl Documentation](https://curl.se/docs/)
