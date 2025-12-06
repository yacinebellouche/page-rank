#!/bin/bash

# ============================================================================
# SCRIPT AUTOMATIQUE - TEST AVEC 2 WORKERS
# ============================================================================
# Ce script exécute TOUT automatiquement pour la configuration 2 workers:
# 1. Crée le cluster
# 2. Exécute RDD et DataFrame sur 100% des données
# 3. Génère les graphiques et comparaisons
# 4. Supprime le cluster IMMÉDIATEMENT
# ============================================================================

# Configuration - MODIFIER ICI
PROJECT_ID="votre-projet-id"  #Changer PROJECT_ID
REGION="europe-west1"
CLUSTER_NAME="pagerank-cluster-2w"
BUCKET_NAME="${PROJECT_ID}-pagerank-data"
NUM_WORKERS=2

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "============================================================================"
echo "🚀 TEST AUTOMATIQUE - CONFIGURATION ${NUM_WORKERS} WORKERS"
echo "============================================================================"
echo ""

# Vérifier que PROJECT_ID a été modifié
if [ "$PROJECT_ID" = "votre-project-id" ]; then
    echo -e "${RED}❌ ERREUR: Vous devez modifier PROJECT_ID dans ce script !${NC}"
    exit 1
fi

# Créer dossier pour les résultats
RESULTS_DIR="../results/config_${NUM_WORKERS}workers"
mkdir -p "$RESULTS_DIR"

# ============================================================================
# ÉTAPE 1: CRÉATION DU CLUSTER
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📋 ÉTAPE 1/5: Création du cluster Dataproc${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

TOTAL_VCPU=$((NUM_WORKERS * 4 + 4))
echo "Configuration:"
echo "  - Nom: $CLUSTER_NAME"
echo "  - Workers: $NUM_WORKERS"
echo "  - Total vCPU: $TOTAL_VCPU"
echo ""

# Créer le cluster avec arrêt immédiat après job
gcloud dataproc clusters create $CLUSTER_NAME \
    --region=$REGION \
    --zone=europe-west1-b \
    --master-machine-type=e2-standard-4 \
    --master-boot-disk-size=50GB \
    --num-workers=$NUM_WORKERS \
    --worker-machine-type=e2-standard-4 \
    --worker-boot-disk-size=50GB \
    --image-version=2.1-debian11 \
    --project=$PROJECT_ID \
    --bucket=$BUCKET_NAME \
    --max-idle=10m \
        --properties="spark:spark.executor.memory=12g,spark:spark.driver.memory=12g,spark:spark.executor.cores=3,spark:spark.sql.shuffle.partitions=200"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Échec de la création du cluster${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Cluster créé avec succès${NC}"
echo ""
sleep 10

# ============================================================================
# ÉTAPE 2: UPLOAD DES SCRIPTS
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📤 ÉTAPE 2/5: Upload des scripts vers GCS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

gsutil cp ../src/*.py gs://$BUCKET_NAME/scripts/
echo -e "${GREEN}✅ Scripts uploadés${NC}"
echo ""

# ============================================================================
# ÉTAPE 3: TESTS AVEC 100% DES DONNÉES
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📊 ÉTAPE 3/5: Tests avec 100% des données${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Fichier .bz2 - PySpark décompresse automatiquement
DATA_FULL="gs://$BUCKET_NAME/data/wikilinks_full.ttl.bz2"
echo ""

# Test RDD - 100%
echo -e "${RED}🔴 PageRank RDD (100%)...${NC}"
START_TIME=$(date +%s)

gcloud dataproc jobs submit pyspark gs://$BUCKET_NAME/scripts/pagerank_rdd.py \
    --cluster=$CLUSTER_NAME \
    --region=$REGION \
    --py-files=gs://$BUCKET_NAME/scripts/utils.py \
    -- $DATA_FULL 10 \
    > "$RESULTS_DIR/rdd_full.log" 2>&1

END_TIME=$(date +%s)
RDD_FULL_TIME=$((END_TIME - START_TIME))
echo -e "${GREEN}✅ RDD 100% terminé en ${RDD_FULL_TIME}s${NC}"
echo ""

sleep 5

# Test DataFrame - 100%
echo -e "${BLUE}🔵 PageRank DataFrame (100%)...${NC}"
START_TIME=$(date +%s)

gcloud dataproc jobs submit pyspark gs://$BUCKET_NAME/scripts/pagerank_dataframe.py \
    --cluster=$CLUSTER_NAME \
    --region=$REGION \
    --py-files=gs://$BUCKET_NAME/scripts/utils.py \
    -- $DATA_FULL 10 \
    > "$RESULTS_DIR/df_full.log" 2>&1

END_TIME=$(date +%s)
DF_FULL_TIME=$((END_TIME - START_TIME))
echo -e "${GREEN}✅ DataFrame 100% terminé en ${DF_FULL_TIME}s${NC}"
echo ""

# ============================================================================
# ÉTAPE 4: GÉNÉRATION DES RÉSULTATS ET GRAPHIQUES
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📈 ÉTAPE 4/5: Génération des résultats et comparaisons${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Extraire le centre de Wikipedia
echo "Extraction du centre de Wikipedia..."
WIKI_CENTER_RDD=$(grep -A 1 "CENTRE DE WIKIPEDIA" "$RESULTS_DIR/rdd_full.log" | tail -1 || echo "N/A")
WIKI_CENTER_DF=$(grep -A 1 "CENTRE DE WIKIPEDIA" "$RESULTS_DIR/df_full.log" | tail -1 || echo "N/A")

# Créer le fichier de résumé
cat > "$RESULTS_DIR/summary.txt" << EOF
============================================================================
RÉSULTATS - CONFIGURATION ${NUM_WORKERS} WORKERS
============================================================================
Date: $(date)
Projet: $PROJECT_ID
Cluster: $CLUSTER_NAME
Total vCPU: $TOTAL_VCPU

============================================================================
TEMPS D'EXÉCUTION (100% DES DONNÉES)
============================================================================

  RDD:       ${RDD_FULL_TIME}s
  DataFrame: ${DF_FULL_TIME}s
  Gagnant:   $([ $RDD_FULL_TIME -lt $DF_FULL_TIME ] && echo "RDD" || echo "DataFrame")
  Différence: $((RDD_FULL_TIME > DF_FULL_TIME ? RDD_FULL_TIME - DF_FULL_TIME : DF_FULL_TIME - RDD_FULL_TIME))s

============================================================================
CENTRE DE WIKIPEDIA
============================================================================
RDD:       $WIKI_CENTER_RDD
DataFrame: $WIKI_CENTER_DF

============================================================================
COMPARAISON RDD vs DataFrame
============================================================================

Pourcentage d'amélioration:
  $([ $RDD_FULL_TIME -lt $DF_FULL_TIME ] && echo "RDD plus rapide de $(echo "scale=2; ($DF_FULL_TIME - $RDD_FULL_TIME) * 100 / $DF_FULL_TIME" | bc)%" || echo "DataFrame plus rapide de $(echo "scale=2; ($RDD_FULL_TIME - $DF_FULL_TIME) * 100 / $RDD_FULL_TIME" | bc)%")

============================================================================
FICHIERS GÉNÉRÉS
============================================================================
  - rdd_full.log        : Log complet RDD 100%
  - df_full.log         : Log complet DataFrame 100%
  - summary.txt         : Ce fichier
  - comparison.csv      : Données pour graphiques

============================================================================
EOF

# Créer fichier CSV pour graphiques
cat > "$RESULTS_DIR/comparison.csv" << EOF
Type,Dataset,Time_seconds
RDD,100%,${RDD_FULL_TIME}
DataFrame,100%,${DF_FULL_TIME}
EOF

echo -e "${GREEN}✅ Fichiers de résultats créés:${NC}"
echo "  📄 $RESULTS_DIR/summary.txt"
echo "  📄 $RESULTS_DIR/comparison.csv"
echo "  📄 $RESULTS_DIR/rdd_full.log"
echo "  📄 $RESULTS_DIR/df_full.log"
echo ""

# Afficher le résumé
cat "$RESULTS_DIR/summary.txt"
echo ""

# ============================================================================
# SUPPRESSION IMMÉDIATE DU CLUSTER
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🧹 Suppression IMMÉDIATE du cluster${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${YELLOW}💰 Suppression du cluster pour économiser les coûts...${NC}"
gcloud dataproc clusters delete $CLUSTER_NAME \
    --region=$REGION \
    --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Cluster supprimé avec succès${NC}"
else
    echo -e "${RED}⚠️  Erreur lors de la suppression - Vérifiez manuellement!${NC}"
fi

echo ""
echo "============================================================================"
echo -e "${GREEN}✅ TEST TERMINÉ AVEC SUCCÈS - ${NUM_WORKERS} WORKERS${NC}"
echo "============================================================================"
echo ""
echo "📊 Résultats disponibles dans: $RESULTS_DIR/"
echo ""
echo "🎯 Prochaines étapes:"
echo "  1. Consultez summary.txt pour les résultats"
echo "  2. Utilisez comparison.csv pour créer des graphiques"
echo "  3. Lancez ./test_config_4workers.sh pour tester 4 workers"
echo ""
