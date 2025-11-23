# 🚀 DÉMARRAGE RAPIDE - Projet PageRank

**LISEZ CE FICHIER EN PREMIER !**

---

## ⚡ Démarrage Rapide avec Scripts Automatisés

### ✨ NOUVEAU : Scripts automatisés par configuration

Chaque membre de l'équipe peut lancer **un script unique** qui fait TOUT automatiquement :
- Création du cluster ✅
- Exécution des tests ✅  
- Suppression immédiate du cluster ✅
- Génération des résultats CSV ✅

### Étape 1: Configuration Initiale (une fois)

```bash
# S'authentifier à Google Cloud
gcloud auth login

# Télécharger les données (une fois)
cd data
bash download_data.sh
cd ..

# Exécuter le setup
bash setup_gcp.sh
```

### Étape 2: Lancer UN test (choisir selon assignation)

**Chaque membre de l'équipe lance UN SEUL des scripts suivants :**

```bash
cd scripts

# Membre 1 - Configuration 2 workers (recommandé pour débutant)
bash test_config_2workers.sh

# OU Membre 2 - Configuration 4 workers
bash test_config_4workers.sh

# OU Membre 3 - Configuration 6 workers
bash test_config_6workers.sh
```

**Le script vous demandera votre PROJECT_ID** (ou définissez `export PROJECT_ID=votre-projet`)

**Ce qui se passe automatiquement :**
```
1. ✅ Création cluster (avec VMs préemptibles = 80% économie)
2. ✅ Tests RDD et DataFrame sur 10% données
3. ✅ Tests RDD et DataFrame sur 100% données  
4. ✅ Suppression IMMÉDIATE du cluster (économie!)
5. ✅ Génération CSV de comparaison
6. ✅ Sauvegarde logs détaillés
```

**Durée estimée :** 15-30 minutes

**Coût estimé :** 3-5€ par configuration

### Étape 3: Partager les résultats

Après l'exécution, partagez ces fichiers avec l'équipe :

```bash
# Fichier CSV (petit)
results/config_Xworkers/comparison.csv

# Log détaillé (pour référence)
results/config_Xworkers_YYYYMMDD_HHMMSS.log
```

### Étape 4: Compilation finale (un seul membre)

Une fois que TOUS les membres ont partagé leurs résultats :

```bash
cd scripts
bash compile_results.sh
```

Cela génère :
- 📊 **Graphiques PNG** dans `results/graphs/`
- 📄 **Récapitulatif texte** dans `results/summary_*.txt`
- 📈 **Comparaisons visuelles** RDD vs DataFrame

---

## 🎯 Workflow en Équipe - Recommandé

```
┌──────────────────────────────────────────────────────────────┐
│                 PHASE 1: Configuration (5 min)               │
├──────────────────────────────────────────────────────────────┤
│  Chaque membre:                                              │
│  1. gcloud auth login                                        │
│  2. cd data && bash download_data.sh                         │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│            PHASE 2: Exécution Parallèle (20-30 min)          │
├──────────────────────────────────────────────────────────────┤
│  Membre 1: bash test_config_2workers.sh                      │
│  Membre 2: bash test_config_4workers.sh                      │
│  Membre 3: bash test_config_6workers.sh                      │
│                                                              │
│  ⚡ Les 3 tests tournent EN PARALLÈLE sur comptes séparés    │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│              PHASE 3: Partage Résultats (5 min)              │
├──────────────────────────────────────────────────────────────┤
│  Chaque membre partage:                                      │
│  - results/config_Xworkers/comparison.csv                    │
│  - results/config_Xworkers_*.log                             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│           PHASE 4: Compilation Finale (5 min)                │
├──────────────────────────────────────────────────────────────┤
│  Un membre: bash compile_results.sh                          │
│  Résultat: Graphiques + tableaux consolidés                  │
└──────────────────────────────────────────────────────────────┘
```

**Temps total : ~40 minutes** (au lieu de 2+ heures en séquentiel!)

---

## 📚 Documentation Complète

Pour les instructions détaillées, consultez :

- **[INSTRUCTIONS.md](INSTRUCTIONS.md)** - Guide complet pas-à-pas
- **[README.md](README.md)** - Vue d'ensemble et résultats

---

## ✅ Checklist Rapide

**Avant de commencer:**
- [ ] Compte Google Cloud créé
- [ ] Facturation activée
- [ ] Alerte de budget configurée (50€ par membre)
- [ ] Google Cloud SDK installé
- [ ] PROJECT_ID modifié dans TOUS les scripts

**Pendant l'exécution:**
- [ ] Tester avec 10% des données d'abord
- [ ] Vérifier les coûts régulièrement
- [ ] Sauvegarder les logs

**Après l'exécution:**
- [ ] Remplir les tableaux dans README.md
- [ ] Compléter results/performance_analysis.md
- [ ] Supprimer les clusters (cleanup.sh)
- [ ] Vérifier que tous les clusters sont supprimés

---

## 🎯 Objectif du Projet

Comparer les performances de **PySpark RDD** vs **PySpark DataFrame** pour le calcul du PageRank sur les données Wikipedia (DBpedia).

### Configurations Testées

- 2 nœuds (12 vCPU total)
- 4 nœuds (20 vCPU total)  
- 6 nœuds (28 vCPU total)

### Résultat Attendu

Identifier le **centre de Wikipedia** (page avec le plus grand PageRank).

---

## 💰 Budget et Coûts

**Budget total:** 150€ (50€ par membre)

**Coût estimé du projet:** 10-15€

**Optimisations appliquées:**
- ✅ Machines préemptibles (80% d'économie)
- ✅ Arrêt automatique des clusters
- ✅ Test progressif (10% avant 100%)
- ✅ Région optimale (europe-west1)

---

## 🔧 Structure du Projet

```
page-rank/
├── README.md                    # Vue d'ensemble et résultats
├── INSTRUCTIONS.md              # Guide détaillé
├── DEMARRAGE_RAPIDE.md         # Ce fichier
├── requirements.txt             # Dépendances Python
├── setup_gcp.sh                # Configuration GCP initiale
├── .gitignore                  # Fichiers à ignorer
│
├── data/
│   └── download_data.sh        # Téléchargement données Wikipedia
│
├── src/
│   ├── utils.py                # Fonctions utilitaires
│   ├── pagerank_rdd.py         # Implémentation RDD
│   └── pagerank_dataframe.py   # Implémentation DataFrame
│
├── scripts/
│   ├── create_cluster.sh       # Création cluster Dataproc
│   ├── run_experiments.sh      # Exécution des expériences
│   └── cleanup.sh              # Nettoyage ressources
│
└── results/
    ├── performance_analysis.md # Analyse détaillée
    └── *.log                   # Logs d'exécution
```

---

## 🆘 Problèmes Fréquents

### Le cluster ne se crée pas

```bash
# Vérifier les quotas
gcloud compute project-info describe --project=VOTRE-PROJECT-ID
```

### Permission denied

```bash
# Activer les APIs
gcloud services enable dataproc.googleapis.com
gcloud services enable storage.googleapis.com
```

### Out of memory

```bash
# Augmenter le nombre de workers
bash create_cluster.sh 6  # au lieu de 2
```

### Coûts trop élevés

```bash
# Supprimer TOUS les clusters immédiatement
bash cleanup.sh
```

---

## 📊 Optimisations Techniques Implémentées

### 1. Partitionnement Intelligent

**RDD:**
```python
liens = liens.partitionBy(200).cache()
rangs = rangs.partitionBy(200)
# → Pas de shuffle lors du join!
```

**DataFrame:**
```python
df_liens = df_liens.repartition(200, "source").cache()
df_rangs = df_rangs.repartition(200, "source")
# → Co-partitionnement optimisé
```

### 2. Cache Stratégique

```python
liens.cache()  # Le graphe ne change jamais
```

### 3. Configuration Spark Optimale

- Adaptive Query Execution activé
- 200 partitions de shuffle
- Mémoire executor: 10 GB
- Serializer: Kryo

---

## 🎓 Points Clés du Projet

### Ce qui est demandé

1. ✅ Comparaison RDD vs DataFrame
2. ✅ Tests sur 3 configurations (2/4/6 workers)
3. ✅ Éviter le shuffle (partitionnement intelligent)
4. ✅ Identifier le centre de Wikipedia
5. ✅ Analyse de performance et scalabilité

### Ce qui est fourni

1. ✅ Code complet et optimisé
2. ✅ Scripts d'automatisation
3. ✅ Documentation détaillée
4. ✅ Templates d'analyse
5. ✅ Optimisations de coûts

### Ce que vous devez faire

1. ✅ Modifier PROJECT_ID dans les scripts
2. ✅ Exécuter les expériences
3. ✅ Remplir les tableaux de résultats
4. ✅ Analyser et conclure
5. ✅ Ajouter vos noms au README.md

---

## 🚀 Prochaines Étapes

1. **Lisez INSTRUCTIONS.md** pour le guide complet
2. **Modifiez PROJECT_ID** dans tous les scripts
3. **Configurez votre alerte de budget** (IMPORTANT!)
4. **Testez avec 10%** avant de lancer sur 100%
5. **Nettoyez toujours** après utilisation

---

## 📧 Informations de Rendu

**À rendre:**
- URL du dépôt GitHub/GitLab
- Noms des 3 membres du groupe

**Contenu attendu:**
- Code source complet
- README.md avec résultats
- Centre de Wikipedia identifié
- Analyse comparative RDD vs DataFrame

---

**BON COURAGE! 🎉**

N'oubliez pas: L'objectif est d'apprendre, pas de dépenser tout le budget. Testez progressivement!
