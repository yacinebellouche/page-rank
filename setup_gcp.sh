#!/bin/bash

# Configuration - MODIFIER ICI
PROJECT_ID="votre-projet-id"  #Changer PROJECT_ID
REGION="europe-west1"
BUCKET_NAME="${PROJECT_ID}-pagerank-data"

echo "🚀 Configuration du projet Google Cloud PageRank..."
echo ""
echo "⚙️  Configuration:"
echo "   Projet: $PROJECT_ID"
echo "   Région: $REGION"
echo "   Bucket: $BUCKET_NAME"
echo ""

# Vérifier que PROJECT_ID a été modifié
if [ "$PROJECT_ID" = "votre-project-id" ]; then
    echo "❌ ERREUR: Vous devez modifier PROJECT_ID dans ce script !"
    echo "   Ouvrez setup_gcp.sh et remplacez 'votre-project-id' par votre vrai ID de projet"
    exit 1
fi

# Définir le projet
echo "📋 Configuration du projet GCP..."
gcloud config set project $PROJECT_ID

if [ $? -ne 0 ]; then
    echo "❌ Erreur: Impossible de définir le projet. Vérifiez que le projet existe."
    exit 1
fi

# Activer les APIs nécessaires
echo ""
echo "📡 Activation des APIs Google Cloud..."
gcloud services enable dataproc.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable compute.googleapis.com

if [ $? -eq 0 ]; then
    echo "✅ APIs activées avec succès"
else
    echo "⚠️  Certaines APIs n'ont pas pu être activées. Vérifiez manuellement."
fi

# Créer le bucket pour les données
echo ""
echo "🪣 Création du bucket Google Cloud Storage..."
gsutil mb -l $REGION gs://$BUCKET_NAME/ 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Bucket créé: gs://$BUCKET_NAME/"
else
    echo "ℹ️  Le bucket existe déjà ou ne peut pas être créé"
fi

# Créer les dossiers dans le bucket
echo ""
echo "📁 Création de la structure de dossiers..."
gsutil -q ls gs://$BUCKET_NAME/data/ 2>/dev/null || gsutil mkdir gs://$BUCKET_NAME/data/
gsutil -q ls gs://$BUCKET_NAME/scripts/ 2>/dev/null || gsutil mkdir gs://$BUCKET_NAME/scripts/
gsutil -q ls gs://$BUCKET_NAME/results/ 2>/dev/null || gsutil mkdir gs://$BUCKET_NAME/results/

echo "✅ Structure créée dans le bucket"

# Configurer les alertes de budget (optionnel)
echo ""
echo "💰 Configuration des alertes de budget..."
echo "⚠️  IMPORTANT: Configurez manuellement une alerte de budget dans la console GCP:"
echo "   1. Allez sur https://console.cloud.google.com/billing"
echo "   2. Créez un budget de 50€ par membre (150€ total)"
echo "   3. Activez les alertes à 50%, 80%, 100%"
echo ""

# Résumé
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Configuration terminée avec succès!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Modifiez PROJECT_ID dans TOUS les scripts:"
echo "      - data/download_data.sh"
echo "      - scripts/test_config_*workers.sh"
echo "      - scripts/compile_results.sh"
echo "      - scripts/cleanup.sh"
echo ""
echo "   2. Téléchargez les données:"
echo "      cd data && bash download_data.sh"
echo ""
echo "   3. Lancez les tests (chaque membre prend 1 config):"
echo "      cd scripts && bash test_config_2workers.sh"
echo "      cd scripts && bash test_config_4workers.sh"
echo "      cd scripts && bash test_config_6workers.sh"
echo ""
echo "   4. Compilez les résultats:"
echo "      cd scripts && bash compile_results.sh"
echo ""
