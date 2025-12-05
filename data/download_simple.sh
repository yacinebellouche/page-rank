#!/bin/bash

# Configuration
PROJECT_ID="page-rank-479014"
BUCKET_NAME="${PROJECT_ID}-pagerank-data"
DATA_URL="https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01/wikilinks_lang=en.ttl.bz2"

echo "========================================================================="
echo "📥 TÉLÉCHARGEMENT OPTIMISÉ - WIKIPEDIA DATA (Version .bz2)"
echo "========================================================================="
echo ""
echo "⚙️  Configuration:"
echo "   Projet: $PROJECT_ID"
echo "   Bucket: gs://$BUCKET_NAME"
echo "   Format: Fichiers compressés .bz2 (PySpark les décompresse automatiquement)"
echo ""
echo "💡 AVANTAGES:"
echo "   ✅ Pas de décompression locale (économise 10 GB d'espace)"
echo "   ✅ Upload plus rapide (1.8 GB vs 11 GB)"
echo "   ✅ PySpark décompresse à la volée lors de la lecture"
echo ""

# Nettoyer les anciens fichiers si existants
echo "🧹 Nettoyage des fichiers temporaires..."
rm -f wikilinks_full.ttl.bz2 wikilinks_full.ttl 2>/dev/null
echo "✅ Nettoyage terminé"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📥 ÉTAPE 1/3: Téléchargement du fichier compressé"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 Téléchargement de 1.8 GB compressé..."
echo "   Source: DBpedia Wikilinks 2022.12.01"
echo ""

wget -q --show-progress -O wikilinks_full.ttl.bz2 "$DATA_URL"

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du téléchargement"
    exit 1
fi

echo ""
echo "✅ Téléchargement terminé"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "☁️  ÉTAPE 2/3: Upload vers Google Cloud Storage"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📤 Upload du fichier complet compressé..."

gsutil cp wikilinks_full.ttl.bz2 gs://$BUCKET_NAME/data/

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'upload vers GCS"
    exit 1
fi

echo "✅ Fichier complet uploadé: gs://$BUCKET_NAME/data/wikilinks_full.ttl.bz2"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🗑️  ÉTAPE 3/3: Nettoyage des fichiers locaux"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

rm -f wikilinks_full.ttl.bz2

echo "✅ Fichiers locaux supprimés (espace libéré)"
echo ""

echo "========================================================================="
echo "✅ TÉLÉCHARGEMENT ET UPLOAD TERMINÉS AVEC SUCCÈS!"
echo "========================================================================="
echo ""
echo "📊 Fichier créé dans GCS:"
echo "   ✅ gs://$BUCKET_NAME/data/wikilinks_full.ttl.bz2 (~1.8 GB)"
echo ""
echo "💾 Stockage total utilisé: ~1.8 GB compressé"
echo "💰 Coût estimé: ~0.04€/mois"
echo ""
echo "💡 NOTE TECHNIQUE:"
echo "   - PySpark décompresse automatiquement les fichiers .bz2"
echo "   - Pas besoin de décompression manuelle"
echo "   - Économise 10 GB d'espace disque"
echo ""
echo "📝 Prochaine étape:"
echo "   cd ../scripts"
echo "   bash test_config_2workers.sh  # Ou 4/6 selon votre assignation"
echo ""
