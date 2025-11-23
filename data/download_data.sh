#!/bin/bash

# Configuration - MODIFIER ICI
PROJECT_ID="votre-project-id"  # ⚠️ À MODIFIER OBLIGATOIREMENT
BUCKET_NAME="${PROJECT_ID}-pagerank-data"

# URLs des données
DATA_URL="https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01/wikilinks_lang=en.ttl.bz2"

echo "📥 Téléchargement et préparation des données Wikipedia..."
echo ""

# Vérifier que PROJECT_ID a été modifié
if [ "$PROJECT_ID" = "votre-project-id" ]; then
    echo "❌ ERREUR: Vous devez modifier PROJECT_ID dans ce script !"
    exit 1
fi

# Vérifier si wget est installé
if ! command -v wget &> /dev/null; then
    echo "❌ wget n'est pas installé. Installez-le avec:"
    echo "   Windows: choco install wget (avec Chocolatey)"
    echo "   Linux: sudo apt install wget"
    exit 1
fi

# Vérifier si bzip2 est installé
if ! command -v bunzip2 &> /dev/null; then
    echo "❌ bzip2 n'est pas installé. Installez-le avec:"
    echo "   Windows: choco install bzip2"
    echo "   Linux: sudo apt install bzip2"
    exit 1
fi

# Télécharger les données complètes
echo "📦 Téléchargement des données Wikipedia (1.8 GB compressé)..."
echo "   URL: $DATA_URL"
echo "   Cela peut prendre plusieurs minutes..."
echo ""

wget -c -O wikilinks_full.ttl.bz2 "$DATA_URL"

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du téléchargement"
    exit 1
fi

echo "✅ Téléchargement terminé"
echo ""

# Décompresser
echo "📦 Décompression des données..."
bunzip2 -k wikilinks_full.ttl.bz2

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de la décompression"
    exit 1
fi

echo "✅ Décompression terminée"
echo ""

# Créer échantillon de 10% pour les tests
echo "✂️  Création d'un échantillon de 10% pour les tests initiaux..."
TOTAL_LINES=$(wc -l < wikilinks_full.ttl)
SAMPLE_LINES=$((TOTAL_LINES / 10))

echo "   Total de lignes: $TOTAL_LINES"
echo "   Échantillon (10%): $SAMPLE_LINES lignes"

head -n $SAMPLE_LINES wikilinks_full.ttl > wikilinks_10percent.ttl

echo "✅ Échantillon créé: wikilinks_10percent.ttl"
echo ""

# Uploader vers Google Cloud Storage
echo "☁️  Upload vers Google Cloud Storage..."
echo "   Destination: gs://$BUCKET_NAME/data/"
echo ""

echo "   Upload de l'échantillon 10%..."
gsutil cp wikilinks_10percent.ttl gs://$BUCKET_NAME/data/

echo "   Upload des données complètes..."
gsutil cp wikilinks_full.ttl gs://$BUCKET_NAME/data/

if [ $? -eq 0 ]; then
    echo "✅ Upload terminé"
else
    echo "❌ Erreur lors de l'upload"
    exit 1
fi

echo ""

# Vérifier les fichiers uploadés
echo "📊 Vérification des fichiers dans GCS..."
gsutil ls -lh gs://$BUCKET_NAME/data/

echo ""

# Nettoyage local (optionnel)
read -p "🧹 Supprimer les fichiers locaux pour libérer de l'espace ? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    rm wikilinks_full.ttl wikilinks_10percent.ttl wikilinks_full.ttl.bz2
    echo "✅ Fichiers locaux supprimés"
else
    echo "📦 Fichiers locaux conservés"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Préparation des données terminée!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Fichiers disponibles dans GCS:"
echo "   - gs://$BUCKET_NAME/data/wikilinks_10percent.ttl"
echo "   - gs://$BUCKET_NAME/data/wikilinks_full.ttl"
echo ""
echo "📝 Prochaine étape:"
echo "   cd ../scripts && bash run_experiments.sh"
echo ""
