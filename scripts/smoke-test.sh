#!/bin/bash
# =============================================================================
# Smoke Tests - Plateforme de Contenu Cloud-Native
# =============================================================================
# US #6 - Vérifie que l'application fonctionne après déploiement
# Usage: ./scripts/smoke-test.sh [URL]
# =============================================================================

APP_URL=${1:-"http://localhost:5000"}
MAX_RETRIES=${2:-10}
RETRY_INTERVAL=${3:-5}

echo ""
echo "=========================================="
echo "🔍 SMOKE TESTS - Plateforme de Contenu"
echo "=========================================="
echo ""
echo "ℹ️  URL cible: $APP_URL"
echo "ℹ️  Max tentatives: $MAX_RETRIES"
echo "ℹ️  Intervalle: ${RETRY_INTERVAL}s"
echo ""

# -----------------------------------------------------------------------------
# Étape 1: Attendre que l'application soit prête
# -----------------------------------------------------------------------------
echo "📡 Étape 1: Vérification de la disponibilité..."
echo ""

READY=false
for i in $(seq 1 $MAX_RETRIES); do
    if curl -sf "$APP_URL/healthz" > /dev/null 2>&1; then
        echo "✅ Application disponible après $i tentative(s)"
        READY=true
        break
    fi
    
    if [ $i -eq $MAX_RETRIES ]; then
        echo "❌ Application non disponible après $MAX_RETRIES tentatives"
        exit 1
    fi
    
    echo "⚠️  Tentative $i/$MAX_RETRIES - Nouvelle tentative dans ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

if [ "$READY" = false ]; then
    echo "❌ Application non disponible"
    exit 1
fi

echo ""

# -----------------------------------------------------------------------------
# Fonction de test simple
# -----------------------------------------------------------------------------
PASSED=0
FAILED=0

test_url() {
    local url=$1
    local name=$2
    
    echo -n "  Testing $name... "
    if curl -sf "$APP_URL$url" > /dev/null 2>&1; then
        echo "✅ OK"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FAILED"
        FAILED=$((FAILED + 1))
    fi
}

# Test spécial pour /readyz qui peut retourner 503 si Azure n'est pas configuré
test_readyz() {
    echo -n "  Testing /readyz... "
    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL/readyz" 2>/dev/null)
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "503" ]; then
        echo "✅ OK (HTTP $http_code)"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FAILED (HTTP $http_code)"
        FAILED=$((FAILED + 1))
    fi
}

# -----------------------------------------------------------------------------
# Étape 2: Tests des endpoints de santé
# -----------------------------------------------------------------------------
echo "❤️  Étape 2: Tests de santé (Health Checks)..."
echo ""

test_url "/healthz" "/healthz"
test_readyz
test_url "/health" "/health"

echo ""

# -----------------------------------------------------------------------------
# Étape 3: Tests des endpoints API
# -----------------------------------------------------------------------------
echo "🔌 Étape 3: Tests des endpoints API..."
echo ""

test_url "/api/events" "/api/events"
test_url "/api/news" "/api/news"
test_url "/api/faq" "/api/faq"

echo ""

# -----------------------------------------------------------------------------
# Étape 4: Test de l'interface web
# -----------------------------------------------------------------------------
echo "🌐 Étape 4: Test de l'interface web..."
echo ""

test_url "/" "Page d'accueil"

echo ""

# -----------------------------------------------------------------------------
# Résumé
# -----------------------------------------------------------------------------
echo "=========================================="
echo "📊 RÉSUMÉ DES TESTS"
echo "=========================================="
echo ""
echo "  Tests réussis:  $PASSED"
echo "  Tests échoués:  $FAILED"
echo "  Total:          $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "=========================================="
    echo "✅ TOUS LES SMOKE TESTS PASSENT ! 🎉"
    echo "=========================================="
    exit 0
else
    echo "=========================================="
    echo "❌ CERTAINS TESTS ONT ÉCHOUÉ"
    echo "=========================================="
    exit 1
fi
