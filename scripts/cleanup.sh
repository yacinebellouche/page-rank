#!/bin/bash

# Configuration - MODIFIER ICI
PROJECT_ID="votre-project-id"  # ⚠️ À MODIFIER OBLIGATOIREMENT
REGION="europe-west1"
CLUSTER_NAME="pagerank-cluster"
BUCKET_NAME="${PROJECT_ID}-pagerank-data"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧹 Nettoyage des ressources Google Cloud PageRank"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Vérifier que PROJECT_ID a été modifié
if [ "$PROJECT_ID" = "votre-project-id" ]; then
    echo "❌ ERREUR: Vous devez modifier PROJECT_ID dans ce script !"
    exit 1
fi

# Définir le projet
gcloud config set project $PROJECT_ID

echo "🔍 Recherche des ressources à nettoyer..."
echo ""

# 1. Supprimer le cluster Dataproc s'il existe
echo "1️⃣  Vérification des clusters Dataproc..."

CLUSTER_EXISTS=$(gcloud dataproc clusters list --region=$REGION --filter="clusterName:$CLUSTER_NAME" --format="value(clusterName)" 2>/dev/null)

if [ -n "$CLUSTER_EXISTS" ]; then
    echo "   ⚠️  Cluster trouvé: $CLUSTER_NAME"
    echo "   🗑️  Suppression en cours..."
    
    gcloud dataproc clusters delete $CLUSTER_NAME \
        --region=$REGION \
        --quiet
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Cluster supprimé"
    else
        echo "   ❌ Erreur lors de la suppression du cluster"
    fi
else
    echo "   ✅ Aucun cluster à supprimer"
fi

echo ""

# 2. Lister tous les clusters (pour vérification)
echo "2️⃣  Vérification de tous les clusters dans le projet..."
ALL_CLUSTERS=$(gcloud dataproc clusters list --region=$REGION --format="value(clusterName)" 2>/dev/null)

if [ -n "$ALL_CLUSTERS" ]; then
    echo "   ⚠️  Clusters actifs trouvés:"
    for cluster in $ALL_CLUSTERS; do
        echo "      - $cluster"
    done
    echo ""
    read -p "   ❓ Supprimer TOUS ces clusters ? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        for cluster in $ALL_CLUSTERS; do
            echo "   🗑️  Suppression de $cluster..."
            gcloud dataproc clusters delete $cluster --region=$REGION --quiet
        done
        echo "   ✅ Tous les clusters supprimés"
    fi
else
    echo "   ✅ Aucun cluster actif"
fi

echo ""

# 3. Option: supprimer le bucket GCS
echo "3️⃣  Gestion du bucket Google Cloud Storage..."
echo "   Bucket: gs://$BUCKET_NAME/"
echo ""

BUCKET_EXISTS=$(gsutil ls | grep "gs://$BUCKET_NAME/" 2>/dev/null)

if [ -n "$BUCKET_EXISTS" ]; then
    # Afficher la taille du bucket
    echo "   📊 Contenu du bucket:"
    gsutil du -sh gs://$BUCKET_NAME/
    echo ""
    
    echo "   ⚠️  ATTENTION: Cela supprimera TOUTES les données!"
    echo "      - Données Wikipedia téléchargées"
    echo "      - Résultats des expériences"
    echo "      - Scripts uploadés"
    echo ""
    
    read -p "   ❓ Supprimer le bucket GCS ? (o/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        echo "   🗑️  Suppression du bucket en cours..."
        gsutil -m rm -r gs://$BUCKET_NAME/
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Bucket supprimé"
        else
            echo "   ❌ Erreur lors de la suppression du bucket"
        fi
    else
        echo "   📦 Bucket conservé"
        echo ""
        echo "   💡 Pour supprimer manuellement plus tard:"
        echo "      gsutil -m rm -r gs://$BUCKET_NAME/"
    fi
else
    echo "   ✅ Bucket n'existe pas ou déjà supprimé"
fi

echo ""

# 4. Vérifier les jobs Dataproc en cours
echo "4️⃣  Vérification des jobs Dataproc..."

RUNNING_JOBS=$(gcloud dataproc jobs list --region=$REGION --filter="status.state=RUNNING" --format="value(reference.jobId)" 2>/dev/null)

if [ -n "$RUNNING_JOBS" ]; then
    echo "   ⚠️  Jobs en cours d'exécution:"
    for job in $RUNNING_JOBS; do
        echo "      - $job"
    done
    echo ""
    read -p "   ❓ Annuler ces jobs ? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        for job in $RUNNING_JOBS; do
            echo "   🛑 Annulation de $job..."
            gcloud dataproc jobs kill $job --region=$REGION
        done
        echo "   ✅ Jobs annulés"
    fi
else
    echo "   ✅ Aucun job en cours"
fi

echo ""

# 5. Résumé et estimation des coûts économisés
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Nettoyage terminé!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Vérifications finales recommandées:"
echo ""
echo "   1. Clusters Dataproc:"
echo "      gcloud dataproc clusters list --region=$REGION"
echo ""
echo "   2. Buckets GCS:"
echo "      gsutil ls | grep pagerank"
echo ""
echo "   3. Coûts accumulés:"
echo "      https://console.cloud.google.com/billing"
echo ""
echo "💰 Ressources libérées = économies réalisées!"
echo ""
echo "📝 Notes:"
echo "   - Les données locales dans results/ sont conservées"
echo "   - Les scripts sources dans src/ sont conservés"
echo "   - Seules les ressources GCP ont été nettoyées"
echo ""
