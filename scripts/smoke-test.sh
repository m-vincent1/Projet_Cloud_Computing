#!/bin/bash
# =============================================================================
# Smoke Tests - Plateforme de Contenu Cloud-Native
# =============================================================================
# US #6 - Vérifie que l'application fonctionne après déploiement
# Usage: ./scripts/smoke-test.sh [URL]
# Exemple: ./scripts/smoke-test.sh http://localhost:5000
#          ./scripts/smoke-test.sh https://mon-app.azurewebsites.net
# =============================================================================

set -e

# Configuration
APP_URL=${1:-"http://localhost:5000"}
MAX_RETRIES=${2:-10}
RETRY_INTERVAL=${3:-5}
FAILED_TESTS=0
PASSED_TESTS=0

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Fonctions utilitaires
# =============================================================================

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Fonction pour tester un endpoint
test_endpoint() {
    local endpoint=$1
    local expected_status=${2:-200}
    local description=${3:-"Testing $endpoint"}
    
    echo -n "  Testing $endpoint... "
    
    # Faire la requête et récupérer le code HTTP
    local response
    response=$(curl -s -o /tmp/response_body.txt -w "%{http_code}" "$APP_URL$endpoint" 2>/dev/null || echo "000")
    
    if [ "$response" -eq "$expected_status" ]; then
        log_success "HTTP $response"
        ((PASSED_TESTS++))
        return 0
    else
        log_error "HTTP $response (attendu: $expected_status)"
        ((FAILED_TESTS++))
        return 1
    fi
}

# Fonction pour tester qu'un endpoint retourne du JSON valide
test_json_response() {
    local endpoint=$1
    local required_key=${2:-""}
    
    echo -n "  Testing JSON $endpoint... "
    
    local response
    response=$(curl -s "$APP_URL$endpoint" 2>/dev/null)
    
    # Vérifier que c'est du JSON valide
    if echo "$response" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
        # Si une clé est requise, vérifier sa présence
        if [ -n "$required_key" ]; then
            if echo "$response" | python3 -c "import sys, json; d=json.load(sys.stdin); assert '$required_key' in d" 2>/dev/null; then
                log_success "JSON valide avec clé '$required_key'"
                ((PASSED_TESTS++))
                return 0
            else
                log_error "Clé '$required_key' manquante"
                ((FAILED_TESTS++))
                return 1
            fi
        else
            log_success "JSON valide"
            ((PASSED_TESTS++))
            return 0
        fi
    else
        log_error "JSON invalide"
        ((FAILED_TESTS++))
        return 1
    fi
}

# =============================================================================
# Script principal
# =============================================================================

echo ""
echo "=========================================="
echo "🔍 SMOKE TESTS - Plateforme de Contenu"
echo "=========================================="
echo ""
log_info "URL cible: $APP_URL"
log_info "Max tentatives: $MAX_RETRIES"
log_info "Intervalle: ${RETRY_INTERVAL}s"
echo ""

# -----------------------------------------------------------------------------
# Étape 1: Attendre que l'application soit prête
# -----------------------------------------------------------------------------
echo "📡 Étape 1: Vérification de la disponibilité..."
echo ""

for i in $(seq 1 $MAX_RETRIES); do
    if curl -s "$APP_URL/healthz" > /dev/null 2>&1; then
        log_success "Application disponible après $i tentative(s)"
        break
    fi
    
    if [ $i -eq $MAX_RETRIES ]; then
        log_error "Application non disponible après $MAX_RETRIES tentatives"
        echo ""
        echo "=========================================="
        echo "❌ SMOKE TESTS ÉCHOUÉS"
        echo "=========================================="
        exit 1
    fi
    
    log_warning "Tentative $i/$MAX_RETRIES - Nouvelle tentative dans ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

echo ""

# -----------------------------------------------------------------------------
# Étape 2: Tests des endpoints de santé (Health Checks)
# -----------------------------------------------------------------------------
echo "❤️  Étape 2: Tests de santé (Health Checks)..."
echo ""

test_endpoint "/healthz" 200 "Liveness probe"
test_json_response "/healthz" "status"

test_endpoint "/readyz" 200 "Readiness probe"
test_json_response "/readyz" "status"

test_endpoint "/health" 200 "Health endpoint"

echo ""

# -----------------------------------------------------------------------------
# Étape 3: Tests des endpoints API
# -----------------------------------------------------------------------------
echo "🔌 Étape 3: Tests des endpoints API..."
echo ""

test_endpoint "/api/events" 200 "API Events"
test_json_response "/api/events" "items"

test_endpoint "/api/news" 200 "API News"
test_json_response "/api/news" "items"

test_endpoint "/api/faq" 200 "API FAQ"
test_json_response "/api/faq" "items"

echo ""

# -----------------------------------------------------------------------------
# Étape 4: Test de l'interface web
# -----------------------------------------------------------------------------
echo "🌐 Étape 4: Test de l'interface web..."
echo ""

test_endpoint "/" 200 "Page d'accueil"

echo ""

# -----------------------------------------------------------------------------
# Résumé des résultats
# -----------------------------------------------------------------------------
echo "=========================================="
echo "📊 RÉSUMÉ DES TESTS"
echo "=========================================="
echo ""
echo -e "  Tests réussis:  ${GREEN}$PASSED_TESTS${NC}"
echo -e "  Tests échoués:  ${RED}$FAILED_TESTS${NC}"
echo -e "  Total:          $((PASSED_TESTS + FAILED_TESTS))"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo "=========================================="
    log_success "TOUS LES SMOKE TESTS PASSENT ! 🎉"
    echo "=========================================="
    exit 0
else
    echo "=========================================="
    log_error "CERTAINS TESTS ONT ÉCHOUÉ"
    echo "=========================================="
    exit 1
fi
