"""
Implémentation PageRank avec PySpark RDD
Optimisé pour éviter le shuffle avec partitionnement intelligent et cache
"""

from pyspark import SparkContext
from pyspark.sql import SparkSession
import sys
import time
from utils import (
    parser_ligne_ttl, 
    calculer_contributions, 
    afficher_top_pagerank,
    afficher_statistiques_graphe,
    afficher_progression,
    mesurer_temps
)

def pagerank_rdd(fichier_input, iterations=10, damping=0.85, num_partitions=200):
    """
    Calcul du PageRank avec PySpark RDD
    
    OPTIMISATIONS CLÉS:
    1. Co-partitionnement des RDDs (liens et rangs)
    2. Cache des données qui ne changent pas
    3. Évite le shuffle lors des joins
    
    Args:
        fichier_input: Chemin GCS vers les données TTL
        iterations: Nombre d'itérations PageRank
        damping: Facteur de damping (0.85 par défaut)
        num_partitions: Nombre de partitions pour le partitionnement
    
    Returns:
        Tuple (top_page, total_pages, rangs_final_rdd)
    """
    
    # Créer SparkSession
    spark = SparkSession.builder \
        .appName("PageRank-RDD") \
        .config("spark.sql.shuffle.partitions", str(num_partitions)) \
        .config("spark.default.parallelism", str(num_partitions)) \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .getOrCreate()
    
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    
    print("\n" + "="*80)
    print("🔴 PageRank avec PySpark RDD")
    print("="*80)
    print(f"📁 Fichier d'entrée: {fichier_input}")
    print(f"🔄 Itérations: {iterations}")
    print(f"📉 Damping factor: {damping}")
    print(f"📦 Partitions: {num_partitions}")
    print("="*80 + "\n")
    
    # Étape 1: Charger et parser les données
    print("📖 Étape 1/5: Chargement et parsing des données...")
    debut_chargement = time.time()
    
    lignes = sc.textFile(fichier_input)
    
    # Parser les lignes TTL
    liens_bruts = lignes.map(parser_ligne_ttl).filter(lambda x: x is not None)
    
    fin_chargement = time.time()
    print(f"   ✅ Parsing effectué en {fin_chargement - debut_chargement:.2f} secondes\n")
    
    # Étape 2: Construire le graphe de liens
    print("🔗 Étape 2/5: Construction du graphe de liens...")
    debut_graphe = time.time()
    
    # Grouper par source pour avoir (source, [dest1, dest2, ...])
    # OPTIMISATION: Utiliser partitionBy pour co-localiser les données
    liens = liens_bruts.groupByKey() \
        .mapValues(list) \
        .partitionBy(num_partitions) \
        .cache()  # ⭐ CACHE: Le graphe ne change jamais
    
    # Forcer l'évaluation du cache
    num_liens = liens.count()
    
    fin_graphe = time.time()
    print(f"   ✅ Graphe construit en {fin_graphe - debut_graphe:.2f} secondes")
    
    # Afficher les statistiques
    afficher_statistiques_graphe(liens)
    
    # Étape 3: Initialiser les rangs PageRank
    print("⚖️  Étape 3/5: Initialisation des rangs PageRank...")
    
    # OPTIMISATION: Partitionner de la même manière que les liens
    rangs = liens.map(lambda x: (x[0], 1.0)) \
        .partitionBy(num_partitions)
    
    print(f"   ✅ {num_liens:,} pages initialisées avec rang = 1.0\n")
    
    # Étape 4: Itérations PageRank
    print("🔄 Étape 4/5: Calcul PageRank (itérations)...")
    print("-" * 80)
    
    debut_iterations = time.time()
    
    for iteration in range(iterations):
        # Afficher la progression
        afficher_progression(iteration + 1, iterations)
        
        # OPTIMISATION: Join sans shuffle car même partitionnement
        # liens et rangs sont partitionnés de la même manière (par clé)
        contributions_rdd = liens.join(rangs) \
            .flatMap(lambda url_ranks: calculer_contributions(url_ranks[1][0], url_ranks[1][1]))
        
        # Calculer les nouveaux rangs avec la formule PageRank
        # PageRank(p) = (1-d) + d * Σ(PR(in)/outlinks(in))
        rangs = contributions_rdd.reduceByKey(lambda x, y: x + y) \
            .mapValues(lambda rank: damping * rank + (1 - damping)) \
            .partitionBy(num_partitions)  # Maintenir le partitionnement
    
    fin_iterations = time.time()
    temps_iterations = fin_iterations - debut_iterations
    
    print("-" * 80)
    print(f"✅ {iterations} itérations terminées en {temps_iterations:.2f} secondes")
    print(f"   Temps moyen par itération: {temps_iterations/iterations:.2f} secondes\n")
    
    # Étape 5: Résultats finaux
    print("📊 Étape 5/5: Calcul des résultats finaux...")
    
    # Cache pour les résultats finaux
    rangs_final = rangs.cache()
    total_pages = rangs_final.count()
    
    print(f"   ✅ Total de pages analysées: {total_pages:,}\n")
    
    # Afficher le top 20
    top_page = afficher_top_pagerank(rangs_final, top_n=20)
    
    # Sauvegarder les résultats dans GCS
    output_path = fichier_input.replace('/data/', '/results/').replace('.ttl', '_rdd_results')
    print(f"💾 Sauvegarde des résultats dans: {output_path}")
    
    try:
        rangs_final.saveAsTextFile(output_path)
        print("   ✅ Résultats sauvegardés\n")
    except Exception as e:
        print(f"   ⚠️  Erreur lors de la sauvegarde: {e}\n")
    
    # Arrêter Spark
    spark.stop()
    
    return top_page, total_pages, rangs_final

@mesurer_temps
def executer_pagerank_rdd(fichier_input, iterations=10):
    """
    Wrapper avec mesure de temps pour l'exécution complète
    
    Args:
        fichier_input: Chemin GCS vers les données
        iterations: Nombre d'itérations
    
    Returns:
        Tuple (top_page, total_pages, rangs_final)
    """
    return pagerank_rdd(fichier_input, iterations)

def main():
    """Fonction principale"""
    
    if len(sys.argv) < 2:
        print("❌ Usage: spark-submit pagerank_rdd.py <gs://bucket/data/fichier.ttl> [iterations]")
        print("\nExemple:")
        print("  spark-submit pagerank_rdd.py gs://mon-bucket/data/wikilinks_10percent.ttl 10")
        sys.exit(1)
    
    fichier = sys.argv[1]
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    # Vérifier que le fichier est dans GCS
    if not fichier.startswith('gs://'):
        print("⚠️  Attention: Le fichier devrait être dans Google Cloud Storage (gs://...)")
    
    print("\n" + "🚀" * 40)
    print("DÉMARRAGE DU CALCUL PAGERANK - IMPLÉMENTATION RDD")
    print("🚀" * 40 + "\n")
    
    # Exécuter PageRank
    resultat, temps_total = executer_pagerank_rdd(fichier, iterations)
    top_page, total_pages, _ = resultat
    
    # Afficher le résumé final
    print("\n" + "=" * 80)
    print("🎯 RÉSUMÉ FINAL - PAGERANK RDD")
    print("=" * 80)
    
    if top_page:
        print(f"🏆 CENTRE DE WIKIPEDIA:")
        print(f"   Page: {top_page[0]}")
        print(f"   PageRank: {top_page[1]:.8f}")
    
    print(f"\n📊 STATISTIQUES:")
    print(f"   Total de pages: {total_pages:,}")
    print(f"   Itérations: {iterations}")
    print(f"   Temps total: {temps_total:.2f} secondes")
    print(f"   Temps par itération: {temps_total/iterations:.2f} secondes")
    
    print("\n" + "=" * 80)
    print("✅ CALCUL TERMINÉ AVEC SUCCÈS")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
