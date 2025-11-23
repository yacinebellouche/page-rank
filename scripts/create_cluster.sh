#!/bin/bash

# Configuration - MODIFIER ICI
PROJECT_ID="votre-project-id"  # ⚠️ À MODIFIER OBLIGATOIREMENT
REGION="europe-west1"
ZONE="europe-west1-b"
CLUSTER_NAME="pagerank-cluster"
BUCKET_NAME="${PROJECT_ID}-pagerank-data"

# Paramètres du cluster (passés en argument)
NUM_WORKERS=${1:-2}  # Par défaut: 2 workers

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Création du cluster Dataproc pour PageRank"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Vérifier que PROJECT_ID a été modifié
if [ "$PROJECT_ID" = "votre-project-id" ]; then
    echo "❌ ERREUR: Vous devez modifier PROJECT_ID dans ce script !"
    exit 1
fi

# Configuration affichée
TOTAL_VCPU=$((NUM_WORKERS * 4 + 4))

echo "⚙️  Configuration du cluster:"
echo "   Nom: $CLUSTER_NAME"
echo "   Projet: $PROJECT_ID"
echo "   Région: $REGION"
echo "   Zone: $ZONE"
echo ""
echo "💻 Matériel:"
echo "   Master: e2-standard-4 (4 vCPU, 16 GB RAM)"
echo "   Workers réguliers: $NUM_WORKERS × e2-standard-4"
echo "   Workers préemptibles: $NUM_WORKERS × e2-standard-4"
echo "   Total vCPU: $TOTAL_VCPU (limite: 32)"
echo ""
echo "💰 Optimisations de coûts:"
echo "   ✅ Machines préemptibles (80% d'économie)"
echo "   ✅ Arrêt automatique après 60s d'inactivité (minimum GCP)"
echo "   ✅ Région europe-west1 (optimale pour coûts)"
echo ""

# Vérifier la limite de vCPU
if [ $TOTAL_VCPU -gt 32 ]; then
    echo "❌ ERREUR: Total vCPU ($TOTAL_VCPU) dépasse la limite de 32 !"
    echo "   Réduisez le nombre de workers."
    exit 1
fi

echo "⏳ Création du cluster en cours..."
echo ""

# Créer le cluster avec machines préemptibles
gcloud dataproc clusters create $CLUSTER_NAME \
    --region=$REGION \
    --zone=$ZONE \
    --master-machine-type=e2-standard-4 \
    --master-boot-disk-type=pd-standard \
    --master-boot-disk-size=50GB \
    --num-workers=$NUM_WORKERS \
    --worker-machine-type=e2-standard-4 \
    --worker-boot-disk-type=pd-standard \
    --worker-boot-disk-size=50GB \
    --num-preemptible-workers=$NUM_WORKERS \
    --image-version=2.1-debian11 \
    --project=$PROJECT_ID \
    --bucket=$BUCKET_NAME \
    --enable-component-gateway \
    --max-idle=60s \
    --properties="spark:spark.executor.memory=10g,spark:spark.driver.memory=10g,spark:spark.executor.cores=3,spark:spark.sql.shuffle.partitions=200" \
    --initialization-actions=gs://goog-dataproc-initialization-actions-${REGION}/python/pip-install.sh \
    --metadata='PIP_PACKAGES=google-cloud-storage'

# Vérifier si la création a réussi
if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ Cluster créé avec succès!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📊 Résumé:"
    echo "   Nom: $CLUSTER_NAME"
    echo "   Workers: $NUM_WORKERS réguliers + $NUM_WORKERS préemptibles"
    echo "   Total vCPU: $TOTAL_VCPU / 32"
    echo "   Bucket: gs://$BUCKET_NAME/"
    echo ""
    echo "🌐 Interfaces Web (Component Gateway):"
    echo "   Consultez: https://console.cloud.google.com/dataproc/clusters/$CLUSTER_NAME?project=$PROJECT_ID&region=$REGION"
    echo ""
    echo "⚠️  N'oubliez pas de SUPPRIMER le cluster après utilisation!"
    echo "   Commande: gcloud dataproc clusters delete $CLUSTER_NAME --region=$REGION"
    echo ""
else
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "❌ Erreur lors de la création du cluster"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🔍 Vérifications à faire:"
    echo "   1. Vérifiez vos quotas: gcloud compute project-info describe --project=$PROJECT_ID"
    echo "   2. Vérifiez que les APIs sont activées"
    echo "   3. Vérifiez que vous avez les permissions nécessaires"
    echo ""
    exit 1
fi
