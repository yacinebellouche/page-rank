"""
Implémentation PageRank avec PySpark DataFrame
Optimisé avec partitionnement intelligent et Catalyst optimizer
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, lit, explode, collect_list, size
import sys
import time
from utils import (
    parser_ligne_ttl,
    afficher_progression,
    mesurer_temps
)

def pagerank_dataframe(fichier_input, iterations=10, damping=0.85, num_partitions=200):
    """
    Calcul du PageRank avec PySpark DataFrame
    
    OPTIMISATIONS CLÉS:
    1. Repartitionnement par clé (source)
    2. Cache des DataFrames qui ne changent pas
    3. Utilisation de Catalyst optimizer
    4. Adaptive Query Execution
    
    Args:
        fichier_input: Chemin GCS vers les données TTL
        iterations: Nombre d'itérations PageRank
        damping: Facteur de damping (0.85 par défaut)
        num_partitions: Nombre de partitions
    
    Returns:
        Tuple (top_page, total_pages)
    """
    
    # Créer SparkSession avec optimisations
    spark = SparkSession.builder \
        .appName("PageRank-DataFrame") \
        .config("spark.sql.shuffle.partitions", str(num_partitions)) \
        .config("spark.default.parallelism", str(num_partitions)) \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.adaptive.skewJoin.enabled", "true") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    print("\n" + "="*80)
    print("🔵 PageRank avec PySpark DataFrame")
    print("="*80)
    print(f"📁 Fichier d'entrée: {fichier_input}")
    print(f"🔄 Itérations: {iterations}")
    print(f"📉 Damping factor: {damping}")
    print(f"📦 Partitions: {num_partitions}")
    print(f"⚡ Adaptive Query Execution: Activé")
    print("="*80 + "\n")
    
    # Étape 1: Charger et parser les données
    print("📖 Étape 1/5: Chargement et parsing des données...")
    debut_chargement = time.time()
    
    # Charger via RDD puis convertir en DataFrame
    lignes_rdd = spark.sparkContext.textFile(fichier_input)
    liens_rdd = lignes_rdd.map(parser_ligne_ttl).filter(lambda x: x is not None)
    
    fin_chargement = time.time()
    print(f"   ✅ Parsing effectué en {fin_chargement - debut_chargement:.2f} secondes\n")
    
    # Étape 2: Construire le graphe de liens (DataFrame)
    print("🔗 Étape 2/5: Construction du graphe de liens (DataFrame)...")
    debut_graphe = time.time()
    
    # Créer DataFrame des liens
    df_liens_bruts = spark.createDataFrame(liens_rdd, ["source", "destination"])
    
    # Grouper les destinations par source
    # OPTIMISATION: Repartitionner et cacher
    df_liens = df_liens_bruts.groupBy("source") \
        .agg(collect_list("destination").alias("destinations")) \
        .repartition(num_partitions, "source") \
        .cache()  # ⭐ CACHE: Le graphe ne change jamais
    
    # Forcer l'évaluation du cache
    num_pages = df_liens.count()
    
    fin_graphe = time.time()
    print(f"   ✅ Graphe construit en {fin_graphe - debut_graphe:.2f} secondes")
    
    # Statistiques
    print(f"\n📊 Statistiques du graphe:")
    print("-" * 60)
    print(f"   Pages avec liens sortants: {num_pages:,}")
    
    # Calculer le nombre moyen de liens
    avg_links = df_liens.agg(_sum(size("destinations")).alias("total")).collect()[0]["total"] / num_pages
    print(f"   Liens sortants - Moyenne: {avg_links:.2f}")
    print("-" * 60 + "\n")
    
    # Étape 3: Initialiser les rangs PageRank
    print("⚖️  Étape 3/5: Initialisation des rangs PageRank...")
    
    # OPTIMISATION: Repartitionner de la même manière que les liens
    df_rangs = df_liens.select("source").distinct() \
        .withColumn("rank", lit(1.0)) \
        .repartition(num_partitions, "source")
    
    print(f"   ✅ {num_pages:,} pages initialisées avec rang = 1.0\n")
    
    # Étape 4: Itérations PageRank
    print("🔄 Étape 4/5: Calcul PageRank (itérations)...")
    print("-" * 80)
    
    debut_iterations = time.time()
    
    for iteration in range(iterations):
        # Afficher la progression
        afficher_progression(iteration + 1, iterations)
        
        # OPTIMISATION: Join sans shuffle (même clé de partition)
        df_joint = df_liens.join(df_rangs, "source")
        
        # Calculer les contributions
        # Chaque page distribue son rang également à toutes ses destinations
        df_contributions = df_joint.select(
            explode("destinations").alias("destination"),
            (col("rank") / size("destinations")).alias("contribution")
        )
        
        # Agréger les contributions et appliquer la formule PageRank
        # PageRank(p) = (1-d) + d * Σ(PR(in)/outlinks(in))
        df_rangs = df_contributions.groupBy("destination") \
            .agg(_sum("contribution").alias("rank_sum")) \
            .select(
                col("destination").alias("source"),
                (lit(damping) * col("rank_sum") + lit(1 - damping)).alias("rank")
            ) \
            .repartition(num_partitions, "source")  # Maintenir le partitionnement
    
    fin_iterations = time.time()
    temps_iterations = fin_iterations - debut_iterations
    
    print("-" * 80)
    print(f"✅ {iterations} itérations terminées en {temps_iterations:.2f} secondes")
    print(f"   Temps moyen par itération: {temps_iterations/iterations:.2f} secondes\n")
    
    # Étape 5: Résultats finaux
    print("📊 Étape 5/5: Calcul des résultats finaux...")
    
    # Cache pour les résultats finaux
    df_rangs_final = df_rangs.cache()
    total_pages = df_rangs_final.count()
    
    print(f"   ✅ Total de pages analysées: {total_pages:,}\n")
    
    # Afficher le top 20
    print("=" * 80)
    print("🏆 Top 20 pages par PageRank")
    print("=" * 80 + "\n")
    
    top_pages_df = df_rangs_final.orderBy(col("rank").desc()).limit(20)
    top_pages_df.show(20, truncate=False)
    
    # Récupérer le top 1
    top_page = df_rangs_final.orderBy(col("rank").desc()).first()
    top_page_tuple = (top_page['source'], top_page['rank'])
    
    print("\n" + "=" * 80 + "\n")
    
    # Sauvegarder les résultats dans GCS (format Parquet)
    output_path = fichier_input.replace('/data/', '/results/').replace('.ttl', '_dataframe_results')
    print(f"💾 Sauvegarde des résultats dans: {output_path}")
    
    try:
        df_rangs_final.write.mode("overwrite").parquet(output_path)
        print("   ✅ Résultats sauvegardés (format Parquet)\n")
    except Exception as e:
        print(f"   ⚠️  Erreur lors de la sauvegarde: {e}\n")
    
    # Sauvegarder aussi le top 100 en CSV pour lecture facile
    output_csv = output_path + "_top100.csv"
    try:
        df_rangs_final.orderBy(col("rank").desc()).limit(100) \
            .write.mode("overwrite").csv(output_csv, header=True)
        print(f"💾 Top 100 sauvegardé en CSV: {output_csv}\n")
    except Exception as e:
        print(f"   ⚠️  Erreur lors de la sauvegarde CSV: {e}\n")
    
    # Arrêter Spark
    spark.stop()
    
    return top_page_tuple, total_pages

@mesurer_temps
def executer_pagerank_dataframe(fichier_input, iterations=10):
    """
    Wrapper avec mesure de temps pour l'exécution complète
    
    Args:
        fichier_input: Chemin GCS vers les données
        iterations: Nombre d'itérations
    
    Returns:
        Tuple (top_page, total_pages)
    """
    return pagerank_dataframe(fichier_input, iterations)

def main():
    """Fonction principale"""
    
    if len(sys.argv) < 2:
        print("❌ Usage: spark-submit pagerank_dataframe.py <gs://bucket/data/fichier.ttl> [iterations]")
        print("\nExemple:")
        print("  spark-submit pagerank_dataframe.py gs://mon-bucket/data/wikilinks_10percent.ttl 10")
        sys.exit(1)
    
    fichier = sys.argv[1]
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    # Vérifier que le fichier est dans GCS
    if not fichier.startswith('gs://'):
        print("⚠️  Attention: Le fichier devrait être dans Google Cloud Storage (gs://...)")
    
    print("\n" + "🚀" * 40)
    print("DÉMARRAGE DU CALCUL PAGERANK - IMPLÉMENTATION DATAFRAME")
    print("🚀" * 40 + "\n")
    
    # Exécuter PageRank
    resultat, temps_total = executer_pagerank_dataframe(fichier, iterations)
    top_page, total_pages = resultat
    
    # Afficher le résumé final
    print("\n" + "=" * 80)
    print("🎯 RÉSUMÉ FINAL - PAGERANK DATAFRAME")
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
