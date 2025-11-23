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
    # GRAPHIQUE 1: Comparaison RDD vs DataFrame par configuration
    # ========================================================================
    plt.figure(figsize=(14, 8))
    
    # Données pour 10%
    df_10 = combined_df[combined_df['Dataset'] == '10%']
    configs_10 = df_10['Config'].unique()
    
    x = np.arange(len(configs_10))
    width = 0.35
    
    rdd_times_10 = [df_10[(df_10['Config'] == c) & (df_10['Type'] == 'RDD')]['Time_seconds'].values[0] 
                    for c in configs_10]
    df_times_10 = [df_10[(df_10['Config'] == c) & (df_10['Type'] == 'DataFrame')]['Time_seconds'].values[0] 
                   for c in configs_10]
    
    plt.subplot(2, 2, 1)
    plt.bar(x - width/2, rdd_times_10, width, label='RDD', color='#e74c3c', alpha=0.8)
    plt.bar(x + width/2, df_times_10, width, label='DataFrame', color='#3498db', alpha=0.8)
    plt.xlabel('Configuration', fontsize=12)
    plt.ylabel('Temps (secondes)', fontsize=12)
    plt.title('Comparaison RDD vs DataFrame - 10% des données', fontsize=14, fontweight='bold')
    plt.xticks(x, configs_10, rotation=0)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Données pour 100%
    df_100 = combined_df[combined_df['Dataset'] == '100%']
    configs_100 = df_100['Config'].unique()
    
    rdd_times_100 = [df_100[(df_100['Config'] == c) & (df_100['Type'] == 'RDD')]['Time_seconds'].values[0] 
                     for c in configs_100]
    df_times_100 = [df_100[(df_100['Config'] == c) & (df_100['Type'] == 'DataFrame')]['Time_seconds'].values[0] 
                    for c in configs_100]
    
    plt.subplot(2, 2, 2)
    plt.bar(x - width/2, rdd_times_100, width, label='RDD', color='#e74c3c', alpha=0.8)
    plt.bar(x + width/2, df_times_100, width, label='DataFrame', color='#3498db', alpha=0.8)
    plt.xlabel('Configuration', fontsize=12)
    plt.ylabel('Temps (secondes)', fontsize=12)
    plt.title('Comparaison RDD vs DataFrame - 100% des données', fontsize=14, fontweight='bold')
    plt.xticks(x, configs_100, rotation=0)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # ========================================================================
    # GRAPHIQUE 2: Speedup avec l'augmentation des workers
    # ========================================================================
    if len(rdd_times_100) >= 2:
        plt.subplot(2, 2, 3)
        
        # Calculer le speedup (baseline = 2 workers)
        rdd_speedup = [rdd_times_100[0] / t for t in rdd_times_100]
        df_speedup = [df_times_100[0] / t for t in df_times_100]
        ideal_speedup = [1, 2, 3] if len(configs_100) == 3 else [1, 2]
        
        plt.plot(range(len(configs_100)), rdd_speedup, 'o-', label='RDD', color='#e74c3c', linewidth=2, markersize=8)
        plt.plot(range(len(configs_100)), df_speedup, 's-', label='DataFrame', color='#3498db', linewidth=2, markersize=8)
        plt.plot(range(len(configs_100)), ideal_speedup[:len(configs_100)], '--', 
                 label='Speedup idéal', color='#2ecc71', linewidth=2)
        
        plt.xlabel('Configuration', fontsize=12)
        plt.ylabel('Speedup', fontsize=12)
        plt.title('Scalabilité - Speedup vs Configuration', fontsize=14, fontweight='bold')
        plt.xticks(range(len(configs_100)), configs_100, rotation=0)
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    # ========================================================================
    # GRAPHIQUE 3: Amélioration DataFrame vs RDD (en pourcentage)
    # ========================================================================
    plt.subplot(2, 2, 4)
    
    improvements_10 = [(rdd - df) / rdd * 100 for rdd, df in zip(rdd_times_10, df_times_10)]
    improvements_100 = [(rdd - df) / rdd * 100 for rdd, df in zip(rdd_times_100, df_times_100)]
    
    x = np.arange(len(configs_10))
    width = 0.35
    
    colors_10 = ['#27ae60' if imp > 0 else '#e74c3c' for imp in improvements_10]
    colors_100 = ['#27ae60' if imp > 0 else '#e74c3c' for imp in improvements_100]
    
    bars1 = plt.bar(x - width/2, improvements_10, width, label='10% données', color=colors_10, alpha=0.8)
    bars2 = plt.bar(x + width/2, improvements_100, width, label='100% données', color=colors_100, alpha=0.8)
    
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.xlabel('Configuration', fontsize=12)
    plt.ylabel('Amélioration (%)', fontsize=12)
    plt.title('Amélioration DataFrame vs RDD', fontsize=14, fontweight='bold')
    plt.xticks(x, configs_10, rotation=0)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Ajouter les valeurs sur les barres
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom' if height > 0 else 'top', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/comparison_all_configs.png", dpi=300, bbox_inches='tight')
    print(f"✅ Graphique 1 sauvegardé: comparison_all_configs.png")
    plt.close()
    
    # ========================================================================
    # GRAPHIQUE 4: Temps d'exécution détaillé (ligne)
    # ========================================================================
    plt.figure(figsize=(12, 6))
    
    for dataset, marker, linestyle in [('10%', 'o', '-'), ('100%', 's', '--')]:
        df_subset = combined_df[combined_df['Dataset'] == dataset]
        
        for impl_type, color in [('RDD', '#e74c3c'), ('DataFrame', '#3498db')]:
            data = df_subset[df_subset['Type'] == impl_type]
            configs_sorted = sorted(data['Config'].unique(), key=lambda x: int(x.split()[0]))
            times = [data[data['Config'] == c]['Time_seconds'].values[0] for c in configs_sorted]
            
            label = f"{impl_type} - {dataset}"
            plt.plot(range(len(configs_sorted)), times, marker=marker, linestyle=linestyle,
                    label=label, color=color, linewidth=2, markersize=8)
    
    plt.xlabel('Configuration', fontsize=12)
    plt.ylabel('Temps d\'exécution (secondes)', fontsize=12)
    plt.title('Évolution du Temps d\'Exécution - Toutes Configurations', fontsize=14, fontweight='bold')
    plt.xticks(range(len(configs_sorted)), configs_sorted, rotation=0)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{graphs_dir}/execution_time_evolution.png", dpi=300, bbox_inches='tight')
    print(f"✅ Graphique 2 sauvegardé: execution_time_evolution.png")
    plt.close()
    
    # ========================================================================
    # GRAPHIQUE 5: Tableau récapitulatif
    # ========================================================================
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('tight')
    ax.axis('off')
    
    # Créer le tableau de données
    table_data = [['Configuration', 'RDD 10%', 'DF 10%', 'Gain 10%', 'RDD 100%', 'DF 100%', 'Gain 100%']]
    
    for i, config in enumerate(configs_10):
        rdd_10 = f"{rdd_times_10[i]:.0f}s"
        df_10 = f"{df_times_10[i]:.0f}s"
        gain_10 = f"{improvements_10[i]:+.1f}%"
        rdd_100 = f"{rdd_times_100[i]:.0f}s" if i < len(rdd_times_100) else "N/A"
        df_100 = f"{df_times_100[i]:.0f}s" if i < len(df_times_100) else "N/A"
        gain_100 = f"{improvements_100[i]:+.1f}%" if i < len(improvements_100) else "N/A"
        
        table_data.append([config, rdd_10, df_10, gain_10, rdd_100, df_100, gain_100])
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.15, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Styliser l'en-tête
    for i in range(7):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Colorer les cellules de gain
    for i in range(1, len(table_data)):
        for j in [3, 6]:  # Colonnes de gain
            if table_data[i][j] != "N/A":
                gain = float(table_data[i][j].replace('%', '').replace('+', ''))
                color = '#d5f4e6' if gain > 0 else '#fadbd8'
                table[(i, j)].set_facecolor(color)
    
    plt.title('Tableau Récapitulatif - RDD vs DataFrame', fontsize=16, fontweight='bold', pad=20)
    plt.savefig(f"{graphs_dir}/summary_table.png", dpi=300, bbox_inches='tight')
    print(f"✅ Graphique 3 sauvegardé: summary_table.png")
    plt.close()
    
    print(f"\n{'='*70}")
    print(f"✅ TOUS LES GRAPHIQUES ONT ÉTÉ GÉNÉRÉS AVEC SUCCÈS!")
    print(f"{'='*70}")
    print(f"\n📁 Emplacement: {graphs_dir}/")
    print(f"\n📊 Graphiques créés:")
    print(f"  1. comparison_all_configs.png  - Comparaisons complètes")
    print(f"  2. execution_time_evolution.png - Évolution des temps")
    print(f"  3. summary_table.png           - Tableau récapitulatif")
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
