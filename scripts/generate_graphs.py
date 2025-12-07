"""
Script de génération automatique de graphiques pour l'analyse PageRank
Génère tous les graphiques de comparaison à partir des fichiers CSV
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_comparison_graphs():
    """Génère tous les graphiques de comparaison"""
    
    # Vérifier que les dossiers de résultats existent
    results_dir = "../results"
    configs = [2, 4, 6]
    
    # Collecter toutes les données
    all_data = []
    
    for config in configs:
        csv_file = f"{results_dir}/config_{config}workers/comparison.csv"
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df['Config'] = f"{config} workers"
            df['NumWorkers'] = config
            all_data.append(df)
            print(f"✅ Données chargées pour {config} workers")
        else:
            print(f"⚠️  Fichier manquant: {csv_file}")
    
    if not all_data:
        print("❌ Aucune donnée trouvée. Lancez d'abord les scripts de test.")
        return
    
    # Combiner toutes les données
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Créer le dossier pour les graphiques
    graphs_dir = f"{results_dir}/graphs"
    os.makedirs(graphs_dir, exist_ok=True)
    
    print(f"\n📊 Génération des graphiques dans {graphs_dir}/...")
    
    # ========================================================================
    # GRAPHIQUE 1: Comparaison RDD vs DataFrame (100% données)
    # ========================================================================
    plt.figure(figsize=(12, 7))
    
    # Données pour 100%
    df_100 = combined_df[combined_df['Dataset'] == '100%'].sort_values('NumWorkers')
    configs_100 = df_100['Config'].unique()
    
    x = np.arange(len(configs_100))
    width = 0.35
    
    rdd_times_100 = [df_100[(df_100['Config'] == c) & (df_100['Type'] == 'RDD')]['Time_seconds'].values[0] 
                     for c in configs_100]
    df_times_100 = [df_100[(df_100['Config'] == c) & (df_100['Type'] == 'DataFrame')]['Time_seconds'].values[0] 
                    for c in configs_100]
    
    bars1 = plt.bar(x - width/2, rdd_times_100, width, label='RDD', color='#e74c3c', alpha=0.8, edgecolor='black')
    bars2 = plt.bar(x + width/2, df_times_100, width, label='DataFrame', color='#3498db', alpha=0.8, edgecolor='black')
    
    # Ajouter les valeurs sur les barres
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}s\n({int(height/60)}min)',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xlabel('Configuration', fontsize=13, fontweight='bold')
    plt.ylabel('Temps d\'exécution (secondes)', fontsize=13, fontweight='bold')
    plt.title('Comparaison RDD vs DataFrame - Dataset Complet (100%)', fontsize=15, fontweight='bold', pad=20)
    plt.xticks(x, configs_100, fontsize=11)
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/comparison_rdd_vs_dataframe.png", dpi=300, bbox_inches='tight')
    print(f"✅ Graphique 1 sauvegardé: comparison_rdd_vs_dataframe.png")
    plt.close()
    
    # ========================================================================
    # GRAPHIQUE 2: Scalabilité - Speedup
    # ========================================================================
    plt.figure(figsize=(12, 7))
    
    # Calculer le speedup (baseline = 2 workers)
    rdd_speedup = [rdd_times_100[0] / t for t in rdd_times_100]
    df_speedup = [df_times_100[0] / t for t in df_times_100]
    num_workers = [2, 4, 6]
    ideal_speedup = [1, 2, 3]
    
    plt.plot(num_workers, rdd_speedup, 'o-', label='RDD', color='#e74c3c', linewidth=3, markersize=12)
    plt.plot(num_workers, df_speedup, 's-', label='DataFrame', color='#3498db', linewidth=3, markersize=12)
    plt.plot(num_workers, ideal_speedup, '--', label='Speedup idéal (linéaire)', 
             color='#2ecc71', linewidth=2, alpha=0.7)
    
    # Ajouter les valeurs
    for i, (x, y) in enumerate(zip(num_workers, rdd_speedup)):
        plt.text(x, y + 0.1, f'{y:.2f}x', ha='center', fontsize=10, fontweight='bold', color='#e74c3c')
    for i, (x, y) in enumerate(zip(num_workers, df_speedup)):
        plt.text(x, y - 0.2, f'{y:.2f}x', ha='center', fontsize=10, fontweight='bold', color='#3498db')
    
    plt.xlabel('Nombre de Workers', fontsize=13, fontweight='bold')
    plt.ylabel('Speedup (par rapport à 2 workers)', fontsize=13, fontweight='bold')
    plt.title('Scalabilité - Facteur d\'Accélération', fontsize=15, fontweight='bold', pad=20)
    plt.xticks(num_workers, fontsize=11)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/scalability_speedup.png", dpi=300, bbox_inches='tight')
    print(f"✅ Graphique 2 sauvegardé: scalability_speedup.png")
    plt.close()
    
    # ========================================================================
    # GRAPHIQUE 3: Amélioration DataFrame vs RDD (en pourcentage)
    # ========================================================================
    plt.figure(figsize=(12, 7))
    
    improvements_100 = [(rdd - df) / rdd * 100 for rdd, df in zip(rdd_times_100, df_times_100)]
    
    colors = ['#27ae60' if imp > 0 else '#e74c3c' for imp in improvements_100]
    bars = plt.bar(num_workers, improvements_100, color=colors, alpha=0.8, edgecolor='black', width=0.6)
    
    # Ajouter les valeurs sur les barres
    for bar, imp in zip(bars, improvements_100):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{imp:.1f}%',
                ha='center', va='bottom' if height > 0 else 'top', 
                fontsize=12, fontweight='bold')
    
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
    plt.xlabel('Nombre de Workers', fontsize=13, fontweight='bold')
    plt.ylabel('Amélioration (%)', fontsize=13, fontweight='bold')
    plt.title('Amélioration de Performance: DataFrame vs RDD', fontsize=15, fontweight='bold', pad=20)
    plt.xticks(num_workers, fontsize=11)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/improvement_percentage.png", dpi=300, bbox_inches='tight')
    print(f"✅ Graphique 3 sauvegardé: improvement_percentage.png")
    plt.close()
    
    # ========================================================================
    # GRAPHIQUE 4: Évolution du temps d'exécution (lignes)
    # ========================================================================
    plt.figure(figsize=(12, 7))
    
    plt.plot(num_workers, rdd_times_100, 'o-', label='RDD', color='#e74c3c', 
             linewidth=3, markersize=12)
    plt.plot(num_workers, df_times_100, 's-', label='DataFrame', color='#3498db', 
             linewidth=3, markersize=12)
    
    # Ajouter les valeurs
    for x, y in zip(num_workers, rdd_times_100):
        plt.text(x, y + 100, f'{int(y)}s', ha='center', fontsize=10, 
                fontweight='bold', color='#e74c3c')
    for x, y in zip(num_workers, df_times_100):
        plt.text(x, y - 100, f'{int(y)}s', ha='center', fontsize=10, 
                fontweight='bold', color='#3498db')
    
    plt.xlabel('Nombre de Workers', fontsize=13, fontweight='bold')
    plt.ylabel('Temps d\'exécution (secondes)', fontsize=13, fontweight='bold')
    plt.title('Évolution du Temps d\'Exécution', fontsize=15, fontweight='bold', pad=20)
    plt.xticks(num_workers, fontsize=11)
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/execution_time_evolution.png", dpi=300, bbox_inches='tight')
    print(f"✅ Graphique 4 sauvegardé: execution_time_evolution.png")
    plt.close()
    
    print(f"\n{'='*70}")
    print(f"✅ TOUS LES GRAPHIQUES ONT ÉTÉ GÉNÉRÉS AVEC SUCCÈS!")
    print(f"{'='*70}")
    print(f"\n📁 Emplacement: {graphs_dir}/")
    print(f"\n📊 Graphiques créés:")
    print(f"  1. comparison_rdd_vs_dataframe.png - Comparaison barres")
    print(f"  2. scalability_speedup.png         - Scalabilité")
    print(f"  3. improvement_percentage.png      - Amélioration %")
    print(f"  4. execution_time_evolution.png    - Évolution temps")
    print(f"\n💡 Utilisez ces graphiques dans votre rapport!\n")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("📈 GÉNÉRATION AUTOMATIQUE DES GRAPHIQUES PAGERANK")
    print("="*70 + "\n")
    
    try:
        create_comparison_graphs()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
