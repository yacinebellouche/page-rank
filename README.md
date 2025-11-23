# PageRank - Analyse de Performance PySpark

**Membres du groupe:** [VOTRE NOM 1, VOTRE NOM 2, VOTRE NOM 3]

## 📊 Objectif

Comparer les performances entre **PySpark DataFrame** et **PySpark RDD** pour le calcul du PageRank sur les données Wikipedia DBpedia.

## 🚀 Démarrage Rapide

### Travail en équipe - Exécution parallèle

Chaque membre de l'équipe peut tester une configuration différente **en parallèle** sur son propre compte GCP :

```bash
# Membre 1 - Teste la configuration 2 workers
cd scripts
bash test_config_2workers.sh

# Membre 2 - Teste la configuration 4 workers  
cd scripts
bash test_config_4workers.sh

# Membre 3 - Teste la configuration 6 workers
cd scripts
bash test_config_6workers.sh
```

**Avantages :**
- ✅ **Exécution parallèle** : 3 personnes = 3x plus rapide
- ✅ **Scripts automatisés** : Création cluster → Tests → Suppression automatique
- ✅ **Budget optimisé** : Clusters supprimés immédiatement après les tests
- ✅ **Résultats CSV** : Génération automatique pour comparaison

### Agrégation des résultats

Une fois que tous les membres ont terminé leurs tests :

```bash
# Compiler tous les résultats et générer les graphiques
cd scripts
bash compile_results.sh
```

Cela génère :
- 📊 Graphiques de comparaison PNG
- 📄 Fichier récapitulatif texte  
- 📈 Tableaux CSV consolidés

---

## 🎯 Résultats Principaux

### 🏆 Entité avec le plus grand PageRank

**Centre de Wikipedia:** `[À COMPLÉTER APRÈS EXÉCUTION]`

**PageRank:** `[À COMPLÉTER]`

---

## 📈 Comparaison des Performances

### Résultats avec 10% des données

| Configuration | RDD (secondes) | DataFrame (secondes) | Gagnant | Amélioration |
|---------------|----------------|----------------------|---------|--------------|
| 2 nœuds       | -              | -                    | -       | -            |
| 4 nœuds       | -              | -                    | -       | -            |
| 6 nœuds       | -              | -                    | -       | -            |

### Résultats avec 100% des données

| Configuration | RDD (secondes) | DataFrame (secondes) | Gagnant | Amélioration |
|---------------|----------------|----------------------|---------|--------------|
| 2 nœuds       | -              | -                    | -       | -            |
| 4 nœuds       | -              | -                    | -       | -            |
| 6 nœuds       | -              | -                    | -       | -            |

---

## 🛠️ Configuration Matérielle

- **Type de machine:** `e2-standard-4` (4 vCPU, 16 GB RAM) - Série E2 économique
- **Région:** `europe-west1` (Belgique - optimise coûts et latence)
- **Machines préemptibles:** OUI ✅ (économie de **80%** sur les coûts)
- **Arrêt automatique:** 60 secondes d'inactivité (suppression rapide)

### Configurations testées

| Configuration | Master | Workers | Workers préemptibles | Total vCPU | Limite respectée |
|---------------|--------|---------|----------------------|------------|------------------|
| 2 nœuds       | 4 vCPU | 2×4 vCPU| 2×4 vCPU             | 12 vCPU    | ✅ < 32 vCPU     |
| 4 nœuds       | 4 vCPU | 4×4 vCPU| 4×4 vCPU             | 20 vCPU    | ✅ < 32 vCPU     |
| 6 nœuds       | 4 vCPU | 6×4 vCPU| 6×4 vCPU             | 28 vCPU    | ✅ < 32 vCPU     |

---

## 💰 Optimisation des Coûts

### Stratégies appliquées

1. ✅ **Machines préemptibles** - Économie de 80%
2. ✅ **Arrêt automatique** - Pas de coûts inutiles
3. ✅ **Test progressif** - Validation avec 10% avant 100%
4. ✅ **Stockage régional** - Pas de coûts multi-régions
5. ✅ **Monitoring budget** - Alertes à 40€ par membre

### Estimation des coûts

| Ressource | Quantité | Durée estimée | Coût unitaire | Coût total |
|-----------|----------|---------------|---------------|------------|
| 2 workers préemptibles | 2 | 30 min | $0.04/h | ~$0.50 |
| 4 workers préemptibles | 4 | 20 min | $0.04/h | ~$0.80 |
| 6 workers préemptibles | 6 | 15 min | $0.04/h | ~$1.20 |
| Storage GCS | 2 GB | 1 mois | $0.020/GB | ~$0.05 |
| **TOTAL estimé** | - | ~2h | - | **~10-15€** |

**Budget restant pour ajustements:** ~35-40€ par personne ✅

---

## 🚀 Installation et Exécution

### Prérequis

1. **Google Cloud SDK** installé
   ```bash
   # Windows (PowerShell)
   # Télécharger depuis: https://cloud.google.com/sdk/docs/install
   ```

2. **Compte Google Cloud** avec facturation activée

3. **Projet GCP** créé

### ⚙️ Configuration Initiale

**IMPORTANT:** Avant toute exécution, modifiez la variable `PROJECT_ID` dans TOUS les scripts :
- `setup_gcp.sh`
- `data/download_data.sh`
- `scripts/create_cluster.sh`
- `scripts/run_experiments.sh`
- `scripts/cleanup.sh`

```bash
# Remplacer partout:
PROJECT_ID="votre-project-id"  # PAR EXEMPLE: PROJECT_ID="pagerank-m2-2025"
```

### 📋 Étapes d'Exécution

#### Étape 1: Authentification et configuration GCP

```bash
# S'authentifier
gcloud auth login

# Définir le projet
gcloud config set project VOTRE-PROJECT-ID

# Configurer l'environnement
bash setup_gcp.sh
```

#### Étape 2: Télécharger et préparer les données

```bash
cd data
bash download_data.sh
cd ..
```

⚠️ **Attention:** Le téléchargement complet fait ~1.8 GB. Le script crée automatiquement un échantillon de 10% pour les tests.

#### Étape 3: Exécuter les expériences

```bash
cd scripts
bash run_experiments.sh
```

Le script va :
1. Créer un cluster avec 2 workers
2. Tester RDD et DataFrame avec 10% des données
3. Demander confirmation pour tester avec 100%
4. Supprimer le cluster
5. Répéter pour 4 et 6 workers

#### Étape 4: Analyser les résultats

Les logs sont sauvegardés dans `results/` :
- `rdd_2workers_10pct.log`
- `df_2workers_10pct.log`
- `rdd_2workers_full.log`
- etc.

Consultez aussi `results/performance_analysis.md` pour l'analyse détaillée.

#### Étape 5: Nettoyage

```bash
# Supprimer toutes les ressources
bash cleanup.sh
```

---

## 🔧 Optimisations Techniques

### 1. Partitionnement Intelligent

**Objectif:** Éviter le shuffle réseau (coûteux en performance)

#### Dans RDD (`src/pagerank_rdd.py`)

```python
# Co-partitionnement des données
liens = liens_bruts.groupByKey() \
    .mapValues(list) \
    .partitionBy(200)  # ← Partitionnement par clé (source)
    .cache()  # ← Cache pour éviter recalcul

rangs = liens.map(lambda x: (x[0], 1.0)) \
    .partitionBy(200)  # ← MÊME partitionnement
```

**Bénéfice:** Lors du `.join()`, les données sont déjà co-localisées → pas de shuffle !

#### Dans DataFrame (`src/pagerank_dataframe.py`)

```python
# Repartitionnement et cache
df_liens = df_liens_bruts.groupBy("source") \
    .agg(collect_list("destination").alias("destinations")) \
    .repartition(200, "source")  # ← Partitionnement par source
    .cache()  # ← Cache

df_rangs = df_rangs.repartition(200, "source")  # ← MÊME clé de partition
```

### 2. Cache Stratégique

```python
# Cache des données qui NE CHANGENT PAS entre itérations
liens.cache()  # Le graphe de liens est constant
df_liens.cache()
```

**Bénéfice:** Évite de relire et reparser les données à chaque itération.

### 3. Configuration Spark Optimale

```python
spark = SparkSession.builder \
    .appName("PageRank") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.sql.adaptive.enabled", "true")  # ← Optimisation adaptative
    .config("spark.executor.memory", "10g")  # ← Mémoire suffisante
    .config("spark.executor.cores", "3")  # ← Parallélisme
    .getOrCreate()
```

### 4. Algorithme PageRank

**Paramètres:**
- **Itérations:** 10 (convergence généralement atteinte)
- **Damping factor:** 0.85 (standard académique)
- **Formule:** `PageRank(p) = 0.85 × Σ(PR(in)/outlinks(in)) + 0.15`

---

## 📚 Structure du Projet

```
page-rank/
├── README.md                          # Ce fichier
├── INSTRUCTIONS.md                    # Guide détaillé pas-à-pas
├── DEMARRAGE_RAPIDE.md                # Guide de démarrage rapide
├── requirements.txt                   # Dépendances Python
├── setup_gcp.sh                       # Configuration Google Cloud
├── .gitignore                         # Fichiers à ignorer
│
├── data/
│   └── download_data.sh               # Téléchargement données Wikipedia
│
├── src/
│   ├── utils.py                       # Fonctions utilitaires
│   ├── pagerank_rdd.py                # Implémentation RDD
│   └── pagerank_dataframe.py          # Implémentation DataFrame
│
├── scripts/
│   ├── create_cluster.sh              # Création cluster Dataproc
│   ├── test_config_2workers.sh        # ✨ Test automatisé 2 workers
│   ├── test_config_4workers.sh        # ✨ Test automatisé 4 workers
│   ├── test_config_6workers.sh        # ✨ Test automatisé 6 workers
│   ├── compile_results.sh             # ✨ Agrégation et graphiques
│   ├── generate_graphs.py             # ✨ Génération graphiques Python
│   └── cleanup.sh                     # Nettoyage ressources
│
└── results/
    ├── config_2workers/               # Résultats configuration 2 workers
    ├── config_4workers/               # Résultats configuration 4 workers
    ├── config_6workers/               # Résultats configuration 6 workers
    ├── graphs/                        # ✨ Graphiques de comparaison PNG
    ├── performance_analysis.md        # Analyse détaillée
    └── *.log                          # Logs d'exécution
```

### ✨ Nouveaux scripts automatisés

Les scripts `test_config_*workers.sh` effectuent **automatiquement** :
1. ✅ Création du cluster Dataproc avec la configuration spécifiée
2. ✅ Upload des scripts Python vers Cloud Storage
3. ✅ Exécution RDD sur 10% des données
4. ✅ Exécution DataFrame sur 10% des données
5. ✅ Exécution RDD sur 100% des données
6. ✅ Exécution DataFrame sur 100% des données
7. ✅ **Suppression immédiate du cluster** (économie de coûts!)
8. ✅ Génération d'un fichier CSV de comparaison
9. ✅ Sauvegarde des logs détaillés

Le script `compile_results.sh` permet ensuite de :
- 📊 Générer des graphiques de comparaison
- 📈 Créer un récapitulatif consolidé
- 🎯 Afficher les améliorations DataFrame vs RDD

---

## 🔍 Observations et Analyses

### Partitionnement des Données

**Stratégie utilisée:** Partitionnement par clé (source) avec co-partitionnement

**Référence:** Article NSDI sur l'optimisation du shuffle dans les systèmes distribués

**Résultats:**
- ✅ Shuffle évité lors des joins
- ✅ Données co-localisées sur les mêmes workers
- ✅ Performances améliorées de [À COMPLÉTER]%

### Convergence

- **Critère de convergence:** Nombre fixe d'itérations (10)
- **Convergence observée:** [À COMPLÉTER]
- **Stabilité des résultats:** [À COMPLÉTER]

### Scalabilité

**Question:** Le speedup est-il linéaire avec l'ajout de workers ?

**Hypothèse:** Speedup sous-linéaire dû à :
- Overhead de communication réseau
- Temps de setup du cluster
- Partie séquentielle (loi d'Amdahl)

**Résultats:** [À COMPLÉTER APRÈS EXÉCUTION]

---

## 🎓 Conclusions

### RDD vs DataFrame

**[À COMPLÉTER APRÈS ANALYSE]**

Points attendus :
- Performance relative
- Facilité d'utilisation
- Optimisations du Catalyst (DataFrame)
- Contrôle bas-niveau (RDD)

### Impact de la scalabilité

**[À COMPLÉTER APRÈS ANALYSE]**

Points à analyser :
- Speedup observé vs théorique
- Bottlenecks identifiés
- Recommandations pour production

### Recommandations

**[À COMPLÉTER APRÈS ANALYSE]**

---

## 📖 Références

- **Données:** [DBpedia Wikilinks](https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01/)
- **Article PageRank original:** Brin & Page, 1998
- **Apache Spark Documentation:** [spark.apache.org](https://spark.apache.org/docs/latest/)
- **Google Cloud Dataproc:** [cloud.google.com/dataproc](https://cloud.google.com/dataproc)

---

## ⚠️ Notes Importantes

1. **Budget:** Surveillez régulièrement vos coûts dans la console GCP
2. **Clusters:** Toujours supprimer les clusters après utilisation
3. **Données:** Les données complètes font 1.8 GB - testez avec 10% d'abord
4. **vCPU Limit:** Respect strict de la limite de 32 vCPU totaux
5. **Région:** Utilisez `europe-west1` pour optimiser les coûts

---

## 🆘 Dépannage

### Le cluster ne se crée pas

```bash
# Vérifier les quotas
gcloud compute project-info describe --project=VOTRE-PROJECT-ID

# Augmenter les quotas si nécessaire (console GCP)
```

### Erreur "Permission denied"

```bash
# Activer les APIs nécessaires
gcloud services enable dataproc.googleapis.com
gcloud services enable storage.googleapis.com
```

### Coûts trop élevés

```bash
# Lister tous les clusters actifs
gcloud dataproc clusters list --region=europe-west1

# Supprimer immédiatement
gcloud dataproc clusters delete NOM-CLUSTER --region=europe-west1
```

---

## 📧 Contact

**Membres du groupe:**
- [NOM 1] - [email]
- [NOM 2] - [email]
- [NOM 3] - [email]

**Cours:** Large Scale Data Management  
**Enseignant:** Pascal Molli  
**Année:** 2025-2026

---

**Date de rendu:** [À COMPLÉTER]  
**URL du dépôt:** `https://github.com/yacinebellouche/page-rank`