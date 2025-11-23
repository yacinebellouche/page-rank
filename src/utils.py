"""
Utilitaires pour le traitement des données Wikilinks et PageRank
Optimisé pour éviter le shuffle et maximiser les performances
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
import re
import time
from functools import wraps

def creer_spark_session(app_name, num_partitions=200):
    """
    Créer une session Spark optimisée pour PageRank
    
    Args:
        app_name: Nom de l'application
        num_partitions: Nombre de partitions (défaut: 200)
    
    Returns:
        SparkSession configurée
    """
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.shuffle.partitions", str(num_partitions)) \
        .config("spark.default.parallelism", str(num_partitions)) \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .getOrCreate()

def parser_ligne_ttl(ligne):
    """
    Parser une ligne TTL pour extraire source et destination
    
    Format attendu:
    <http://dbpedia.org/resource/Source> <http://dbpedia.org/ontology/wikiPageWikiLink> <http://dbpedia.org/resource/Destination> .
    
    Args:
        ligne: Ligne TTL à parser
    
    Returns:
        Tuple (source, destination) ou None si parsing échoue
    """
    try:
        # Extraire les URIs entre < >
        pattern = r'<http://dbpedia\.org/resource/([^>]+)>'
        matches = re.findall(pattern, ligne)
        
        if len(matches) >= 2:
            source = matches[0]
            destination = matches[1]
            # Décoder les caractères URL encodés
            source = source.replace('_', ' ')
            destination = destination.replace('_', ' ')
            return (source, destination)
    except Exception as e:
        pass
    
    return None

def calculer_contributions(urls, rank):
    """
    Calculer les contributions PageRank pour une page
    
    Args:
        urls: Liste des URLs sortantes
        rank: PageRank actuel de la page
    
    Yields:
        Tuples (url_destination, contribution)
    """
    num_urls = len(urls)
    if num_urls > 0:
        contribution = rank / num_urls
        for url in urls:
            yield (url, contribution)

def afficher_top_pagerank(pagerank_rdd, top_n=20):
    """
    Afficher les top N pages par PageRank (pour RDD)
    
    Args:
        pagerank_rdd: RDD de (page, rank)
        top_n: Nombre de résultats à afficher
    
    Returns:
        Tuple (page, rank) du top 1, ou None
    """
    print(f"\n{'='*80}")
    print(f"🏆 Top {top_n} pages par PageRank")
    print(f"{'='*80}")
    
    # Récupérer le top N
    top_pages = pagerank_rdd.takeOrdered(top_n, key=lambda x: -x[1])
    
    # Afficher avec formatage
    for i, (page, rank) in enumerate(top_pages, 1):
        # Tronquer le nom de page si trop long
        page_display = page[:60] + "..." if len(page) > 60 else page
        print(f"{i:2d}. {page_display:63s} | PageRank: {rank:.8f}")
    
    print(f"{'='*80}\n")
    
    return top_pages[0] if top_pages else None

def mesurer_temps(fonction):
    """
    Décorateur pour mesurer le temps d'exécution d'une fonction
    
    Args:
        fonction: Fonction à décorer
    
    Returns:
        Wrapper qui retourne (résultat_fonction, temps_execution)
    """
    @wraps(fonction)
    def wrapper(*args, **kwargs):
        print(f"\n⏱️  Début du chronomètre...")
        debut = time.time()
        
        resultat = fonction(*args, **kwargs)
        
        fin = time.time()
        temps_execution = fin - debut
        
        # Affichage formaté
        minutes = int(temps_execution // 60)
        secondes = temps_execution % 60
        
        print(f"\n{'='*80}")
        if minutes > 0:
            print(f"⏱️  Temps d'exécution: {minutes} min {secondes:.2f} sec ({temps_execution:.2f} sec)")
        else:
            print(f"⏱️  Temps d'exécution: {temps_execution:.2f} secondes")
        print(f"{'='*80}\n")
        
        return resultat, temps_execution
    
    return wrapper

def afficher_statistiques_graphe(liens_rdd):
    """
    Afficher des statistiques sur le graphe de liens
    
    Args:
        liens_rdd: RDD de (source, [destinations])
    """
    print("\n📊 Statistiques du graphe:")
    print("-" * 60)
    
    # Nombre de pages avec liens sortants
    num_pages = liens_rdd.count()
    print(f"   Pages avec liens sortants: {num_pages:,}")
    
    # Statistiques sur le nombre de liens
    liens_stats = liens_rdd.map(lambda x: len(x[1])).stats()
    print(f"   Liens sortants - Moyenne: {liens_stats.mean():.2f}")
    print(f"   Liens sortants - Min: {liens_stats.min()}")
    print(f"   Liens sortants - Max: {liens_stats.max()}")
    print(f"   Liens sortants - Total: {liens_stats.sum():,}")
    
    print("-" * 60 + "\n")

def sauvegarder_resultats_texte(pagerank_rdd, fichier_output, top_n=100):
    """
    Sauvegarder les résultats dans un fichier texte lisible
    
    Args:
        pagerank_rdd: RDD de (page, rank)
        fichier_output: Chemin du fichier de sortie
        top_n: Nombre de top résultats à sauvegarder
    """
    top_pages = pagerank_rdd.takeOrdered(top_n, key=lambda x: -x[1])
    
    # Créer le contenu
    contenu = []
    contenu.append("=" * 80)
    contenu.append(f"Top {top_n} Pages par PageRank")
    contenu.append("=" * 80)
    contenu.append("")
    
    for i, (page, rank) in enumerate(top_pages, 1):
        contenu.append(f"{i:3d}. {page:60s} | {rank:.8f}")
    
    contenu.append("")
    contenu.append("=" * 80)
    
    # Écrire dans le fichier
    with open(fichier_output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(contenu))
    
    print(f"💾 Top {top_n} résultats sauvegardés dans: {fichier_output}")

def verifier_convergence(rangs_precedents, rangs_actuels, seuil=0.001):
    """
    Vérifier si PageRank a convergé
    
    Args:
        rangs_precedents: RDD des rangs de l'itération précédente
        rangs_actuels: RDD des rangs actuels
        seuil: Seuil de convergence (différence moyenne acceptable)
    
    Returns:
        True si convergé, False sinon
    """
    # Joindre les deux RDDs et calculer la différence
    differences = rangs_precedents.join(rangs_actuels) \
        .map(lambda x: abs(x[1][0] - x[1][1]))
    
    # Calculer la différence moyenne
    diff_moyenne = differences.mean()
    
    return diff_moyenne < seuil, diff_moyenne

def afficher_progression(iteration, total_iterations, message=""):
    """
    Afficher une barre de progression pour les itérations
    
    Args:
        iteration: Numéro d'itération actuelle (commence à 1)
        total_iterations: Nombre total d'itérations
        message: Message additionnel à afficher
    """
    pourcentage = (iteration / total_iterations) * 100
    barre_longueur = 40
    progres = int((iteration / total_iterations) * barre_longueur)
    barre = "█" * progres + "░" * (barre_longueur - progres)
    
    print(f"Itération {iteration:2d}/{total_iterations} [{barre}] {pourcentage:5.1f}% {message}")
