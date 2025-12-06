#!/bin/bash

################################################################################
# Script de compilation des résultats pour PageRank
# Agrège tous les logs et génère les graphiques de comparaison
################################################################################

set -e

RESULTS_DIR="../results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "========================================================================="
echo "📊 COMPILATION DES RÉSULTATS - PAGERANK"
echo "========================================================================="
echo ""

# Vérifier si Python et les packages nécessaires sont installés
echo "🔍 Vérification des dépendances..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Installation requise."
    exit 1
fi

# Installer les packages nécessaires si manquants
echo "📦 Installation des packages Python (matplotlib, pandas)..."
python3 -m pip install --quiet matplotlib pandas numpy 2>/dev/null || {
    echo "⚠️  Installation des packages échouée, vérifiez pip"
}

echo ""
echo "========================================================================="
echo "📂 RECHERCHE DES FICHIERS DE RÉSULTATS"
echo "========================================================================="
echo ""

# Compter les fichiers de résultats disponibles
found_2workers=0
found_4workers=0
found_6workers=0

if ls $RESULTS_DIR/config_2workers_*.log 1> /dev/null 2>&1; then
    latest_2=$(ls -t $RESULTS_DIR/config_2workers_*.log | head -1)
    echo "✅ Configuration 2 workers: $latest_2"
    found_2workers=1
fi

if ls $RESULTS_DIR/config_4workers_*.log 1> /dev/null 2>&1; then
    latest_4=$(ls -t $RESULTS_DIR/config_4workers_*.log | head -1)
    echo "✅ Configuration 4 workers: $latest_4"
    found_4workers=1
fi

if ls $RESULTS_DIR/config_6workers_*.log 1> /dev/null 2>&1; then
    latest_6=$(ls -t $RESULTS_DIR/config_6workers_*.log | head -1)
    echo "✅ Configuration 6 workers: $latest_6"
    found_6workers=1
fi

total_found=$((found_2workers + found_4workers + found_6workers))

if [ $total_found -eq 0 ]; then
    echo ""
    echo "❌ AUCUN FICHIER DE RÉSULTATS TROUVÉ!"
    echo ""
    echo "Lancez d'abord les scripts de test:"
    echo "  - bash scripts/test_config_2workers.sh"
    echo "  - bash scripts/test_config_4workers.sh"
    echo "  - bash scripts/test_config_6workers.sh"
    echo ""
    exit 1
fi

echo ""
echo "📊 Résultats trouvés: $total_found/3 configurations"
echo ""

# Créer un dossier pour les graphiques
GRAPHS_DIR="$RESULTS_DIR/graphs"
mkdir -p "$GRAPHS_DIR"

echo "========================================================================="
echo "📈 GÉNÉRATION DES GRAPHIQUES"
echo "========================================================================="
echo ""

cd scripts
python3 generate_graphs.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================================================="
    echo "✅ COMPILATION TERMINÉE AVEC SUCCÈS!"
    echo "========================================================================="
    echo ""
    echo "📁 Résultats compilés dans: $GRAPHS_DIR/"
    echo ""
    echo "📊 Fichiers générés:"
    ls -lh "$GRAPHS_DIR"/*.png 2>/dev/null | awk '{print "  - " $9 " (" $5 ")"}'
    echo ""
    echo "💡 Conseil: Ouvrez les images PNG pour voir les comparaisons!"
    echo ""
else
    echo ""
    echo "❌ Erreur lors de la génération des graphiques"
    echo ""
    exit 1
fi

# Créer un fichier récapitulatif texte
SUMMARY_FILE="$RESULTS_DIR/summary_${TIMESTAMP}.txt"

echo "Création du récapitulatif texte..."
cat > "$SUMMARY_FILE" << EOF
========================================================================
RÉCAPITULATIF DES RÉSULTATS PAGERANK
Généré le: $(date)
========================================================================

CONFIGURATIONS TESTÉES:
EOF

if [ $found_2workers -eq 1 ]; then
    echo "  ✅ 2 workers" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
    echo "--- Extrait 2 workers ---" >> "$SUMMARY_FILE"
    grep -A 20 "RÉCAPITULATIF" "$latest_2" >> "$SUMMARY_FILE" 2>/dev/null || echo "Données non disponibles" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
fi

if [ $found_4workers -eq 1 ]; then
    echo "  ✅ 4 workers" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
    echo "--- Extrait 4 workers ---" >> "$SUMMARY_FILE"
    grep -A 20 "RÉCAPITULATIF" "$latest_4" >> "$SUMMARY_FILE" 2>/dev/null || echo "Données non disponibles" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
fi

if [ $found_6workers -eq 1 ]; then
    echo "  ✅ 6 workers" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
    echo "--- Extrait 6 workers ---" >> "$SUMMARY_FILE"
    grep -A 20 "RÉCAPITULATIF" "$latest_6" >> "$SUMMARY_FILE" 2>/dev/null || echo "Données non disponibles" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
fi

cat >> "$SUMMARY_FILE" << EOF

========================================================================
GRAPHIQUES GÉNÉRÉS:
========================================================================
EOF

ls "$GRAPHS_DIR"/*.png >> "$SUMMARY_FILE" 2>/dev/null

echo ""
echo "📄 Récapitulatif texte créé: $SUMMARY_FILE"
echo ""

# Afficher un aperçu des améliorations DataFrame vs RDD
echo "========================================================================="
echo "🎯 APERÇU RAPIDE - AMÉLIORATION DATAFRAME vs RDD"
echo "========================================================================="
echo ""

for config in 2 4 6; do
    csv_file="$RESULTS_DIR/config_${config}workers/comparison.csv"
    if [ -f "$csv_file" ]; then
        echo "Configuration: $config workers"
        echo "-------------------------"
        
        # Extraire et calculer les améliorations
        python3 -c "
import pandas as pd
import sys

try:
    df = pd.read_csv('$csv_file')
    
    for dataset in ['10%', '100%']:
        rdd_time = df[(df['Type'] == 'RDD') & (df['Dataset'] == dataset)]['Time_seconds'].values
        df_time = df[(df['Type'] == 'DataFrame') & (df['Dataset'] == dataset)]['Time_seconds'].values
        
        if len(rdd_time) > 0 and len(df_time) > 0:
            improvement = (rdd_time[0] - df_time[0]) / rdd_time[0] * 100
            symbol = '✅' if improvement > 0 else '⚠️ '
            print(f'{dataset:5s}: RDD {rdd_time[0]:6.1f}s | DataFrame {df_time[0]:6.1f}s | {symbol} {improvement:+5.1f}%')
except Exception as e:
    print(f'Erreur: {e}', file=sys.stderr)
"
        echo ""
    fi
done

echo "========================================================================="
echo "🎉 TOUS LES RÉSULTATS ONT ÉTÉ COMPILÉS!"
echo "========================================================================="
echo ""
echo "📂 Emplacements importants:"
echo "  - Graphiques: $GRAPHS_DIR/"
echo "  - Récapitulatif: $SUMMARY_FILE"
echo "  - Logs détaillés: $RESULTS_DIR/config_*workers_*.log"
echo ""
echo "💡 Prochaines étapes suggérées:"
echo "  1. Ouvrir les graphiques PNG dans $GRAPHS_DIR/"
echo "  2. Lire le récapitulatif: cat $SUMMARY_FILE"
echo "  3. Intégrer les résultats dans votre rapport"
echo ""
