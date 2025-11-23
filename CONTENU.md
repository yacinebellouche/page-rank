# 📦 CONTENU DU PROJET - PageRank

**Vue d'ensemble de tous les fichiers du projet**

---

## 📁 Structure Complète

```
page-rank/
│
├── 📘 Documentation
│   ├── README.md                    ⭐ Vue d'ensemble + Résultats
│   ├── DEMARRAGE_RAPIDE.md          🚀 Guide 5 minutes
│   ├── INSTRUCTIONS.md              📖 Guide complet pas-à-pas
│   ├── CHECKLIST.md                 ✅ Liste de vérification
│   ├── OPTIMISATIONS.md             🔧 Détails techniques
│   └── CONTENU.md                   📦 Ce fichier
│
├── ⚙️ Configuration
│   ├── .gitignore                   🚫 Fichiers à ignorer
│   ├── requirements.txt             📦 Dépendances Python
│   └── setup_gcp.sh                 🔧 Configuration Google Cloud
│
├── 📊 data/
│   └── download_data.sh             📥 Téléchargement Wikipedia
│
├── 💻 src/
│   ├── utils.py                     🛠️ Fonctions utilitaires
│   ├── pagerank_rdd.py              🔴 Implémentation RDD
│   └── pagerank_dataframe.py        🔵 Implémentation DataFrame
│
├── 🎬 scripts/
│   ├── test_config_2workers.sh      ✨ Test automatisé 2 workers
│   ├── test_config_4workers.sh      ✨ Test automatisé 4 workers
│   ├── test_config_6workers.sh      ✨ Test automatisé 6 workers
│   ├── compile_results.sh           ✨ Compilation résultats
│   ├── generate_graphs.py           📊 Génération graphiques
│   └── cleanup.sh                   🧹 Nettoyage ressources
│
└── 📈 results/
    ├── performance_analysis.md      📊 Analyse détaillée
    └── *.log                        📝 Logs d'exécution (générés)
```

---

## 📘 Documentation (7 fichiers)

### 1. README.md ⭐
**Ce qu'il contient:**
- Objectif du projet
- Tableaux de résultats (à remplir)
- Configuration matérielle
- Instructions d'exécution
- Optimisations techniques
- Centre de Wikipedia (résultat principal)

**Quand le consulter:**
- Pour comprendre le projet
- Pour voir les résultats
- Pour le rendu final

### 2. DEMARRAGE_RAPIDE.md 🚀
**Ce qu'il contient:**
- Démarrage en 5 minutes
- Commandes essentielles
- Checklist rapide
- Structure du projet

**Quand le consulter:**
- Première fois que vous voyez le projet
- Pour démarrer rapidement

### 3. INSTRUCTIONS.md 📖
**Ce qu'il contient:**
- Guide complet pas-à-pas
- Installation des prérequis
- Configuration détaillée
- Exécution étape par étape
- Dépannage complet

**Quand le consulter:**
- Pour suivre le projet de A à Z
- En cas de problème
- Pour comprendre chaque étape

### 4. CHECKLIST.md ✅
**Ce qu'il contient:**
- Liste de vérification avant exécution
- Erreurs courantes à éviter
- Validation finale
- Actions critiques

**Quand le consulter:**
- Avant chaque exécution
- Pour éviter les erreurs
- Avant le rendu

### 5. OPTIMISATIONS.md 🔧
**Ce qu'il contient:**
- Détails de toutes les optimisations
- Explications techniques
- Gains mesurés
- Références académiques

**Quand le consulter:**
- Pour comprendre le code
- Pour rédiger l'analyse
- Pour répondre aux questions techniques

### 6. CONTENU.md 📦
**Ce qu'il contient:**
- Ce fichier
- Vue d'ensemble de tous les fichiers
- Rôle de chaque fichier

**Quand le consulter:**
- Pour naviguer dans le projet
- Pour comprendre l'organisation

### 7. PageRank 2025-2026.pdf 📄
**Ce qu'il contient:**
- Énoncé du projet (fourni par l'enseignant)

---

## ⚙️ Configuration (3 fichiers)

### .gitignore 🚫
**Ce qu'il fait:**
- Ignore les gros fichiers de données
- Ignore les logs
- Ignore les fichiers Python compilés

**Ne pas modifier sauf:**
- Pour ajouter d'autres fichiers à ignorer

### requirements.txt 📦
**Ce qu'il contient:**
```
pyspark==3.5.0
google-cloud-storage==2.10.0
google-cloud-dataproc==5.4.3
```

**Quand l'utiliser:**
- Installé automatiquement sur Dataproc
- Pas besoin d'installation locale

### setup_gcp.sh 🔧
**Ce qu'il fait:**
1. Active les APIs Google Cloud
2. Crée le bucket GCS
3. Configure l'environnement

**À modifier:**
- `PROJECT_ID` (ligne 4) ⚠️ OBLIGATOIRE

**Quand l'exécuter:**
- Une seule fois au début

---

## 📊 Données (1 dossier, 1 script)

### data/download_data.sh 📥
**Ce qu'il fait:**
1. Télécharge wikilinks (1.8 GB)
2. Décompresse
3. Crée échantillon 10%
4. Upload vers GCS

**À modifier:**
- `PROJECT_ID` (ligne 4) ⚠️ OBLIGATOIRE

**Durée:**
- Téléchargement: 5-30 minutes
- Décompression: 2-5 minutes
- Upload: 5-10 minutes

**Sortie:**
- `gs://BUCKET/data/wikilinks_10percent.ttl`
- `gs://BUCKET/data/wikilinks_full.ttl`

---

## 💻 Code Source (3 fichiers Python)

### src/utils.py 🛠️
**Ce qu'il contient:**
- `parser_ligne_ttl()` - Parser TTL
- `calculer_contributions()` - Contributions PageRank
- `afficher_top_pagerank()` - Affichage résultats
- `mesurer_temps()` - Décorateur timing
- `afficher_progression()` - Barre de progression

**Lignes de code:** ~200

**Utilisé par:**
- `pagerank_rdd.py`
- `pagerank_dataframe.py`

### src/pagerank_rdd.py 🔴
**Ce qu'il fait:**
- Implémentation PageRank avec RDD
- Co-partitionnement optimisé
- Cache stratégique
- Mesure de temps

**Lignes de code:** ~180

**Optimisations clés:**
- `.partitionBy(200)` - Évite shuffle
- `.cache()` - Évite recalcul
- Kryo serializer

**Sortie:**
- Résultats dans GCS
- Top 20 pages affichées
- Temps d'exécution

### src/pagerank_dataframe.py 🔵
**Ce qu'il fait:**
- Implémentation PageRank avec DataFrame
- Repartitionnement par clé
- Adaptive Query Execution
- Mesure de temps

**Lignes de code:** ~200

**Optimisations clés:**
- `.repartition(200, "source")` - Partitionnement
- `.cache()` - Cache
- Catalyst optimizer
- Format Parquet

**Sortie:**
- Résultats en Parquet
- Top 100 en CSV
- Temps d'exécution

---

## 🎬 Scripts d'Exécution (6 scripts)

### scripts/test_config_2workers.sh ✨
**Ce qu'il fait:**
- Crée cluster avec 2 workers (machines préemptibles e2-standard-4)
- Exécute RDD et DataFrame (10% + 100%)
- Supprime cluster automatiquement (max-idle: 60s)
- Génère results/config_2workers/comparison.csv

**À modifier:**
- `PROJECT_ID` (ligne 4) ⚠️ OBLIGATOIRE

**Usage:**
```bash
bash test_config_2workers.sh
```

**Durée:** 40-60 minutes

### scripts/test_config_4workers.sh ✨
**Identique mais avec 4 workers**

### scripts/test_config_6workers.sh ✨
**Identique mais avec 6 workers**

### scripts/compile_results.sh ✨
**Ce qu'il fait:**
- Agrège tous les CSV (results/config_*/comparison.csv)
- Génère 3 graphiques PNG dans results/graphs/:
  - execution_time_comparison.png
  - speedup_comparison.png
  - scalability_analysis.png

**Usage:**
```bash
bash compile_results.sh
```

**Durée:** < 1 minute

### scripts/generate_graphs.py 🐍
**Script Python appelé par compile_results.sh**
- Utilise matplotlib pour générer les graphiques

### scripts/cleanup.sh 🧹
**Ce qu'il fait:**
- Supprime tous les clusters orphelins
- Liste les ressources actives
- Propose de supprimer le bucket

**À modifier:**
- `PROJECT_ID` (ligne 4) ⚠️ OBLIGATOIRE

**Usage:**
```bash
bash cleanup.sh
```

**Quand l'exécuter:**
- Après CHAQUE session de travail
- En cas d'urgence (coûts trop élevés)
- Avant le rendu final

---

## 📈 Résultats (1 dossier)

### results/performance_analysis.md 📊
**Ce qu'il contient:**
- Tableaux de résultats détaillés
- Analyse comparative RDD vs DataFrame
- Analyse de scalabilité
- Observations et conclusions

**À remplir:**
- Après chaque expérience
- Avec les données des logs

### results/*.log 📝
**Fichiers générés:**
- `rdd_2workers_10pct.log`
- `rdd_2workers_full.log`
- `rdd_4workers_10pct.log`
- `rdd_4workers_full.log`
- `rdd_6workers_10pct.log`
- `rdd_6workers_full.log`
- `df_2workers_10pct.log`
- `df_2workers_full.log`
- `df_4workers_10pct.log`
- `df_4workers_full.log`
- `df_6workers_10pct.log`
- `df_6workers_full.log`

**Contenu:**
- Sortie complète de chaque job
- Temps d'exécution
- Statistiques
- Top 20 pages
- Erreurs éventuelles

---

## 🎯 Workflow Complet

### Phase 1: Configuration (30 minutes)
1. Lire `DEMARRAGE_RAPIDE.md`
2. Modifier `PROJECT_ID` dans les 7 scripts
3. Exécuter `setup_gcp.sh`
4. Exécuter `data/download_data.sh`

### Phase 2: Exécution (40-60 min par config, EN PARALLÈLE)
1. Consulter `CHECKLIST.md`
2. Chaque membre exécute 1 config:
   - Membre 1: `scripts/test_config_2workers.sh`
   - Membre 2: `scripts/test_config_4workers.sh`
   - Membre 3: `scripts/test_config_6workers.sh`
3. Surveiller les logs
4. Sauvegarder les résultats

### Phase 3: Compilation (< 1 minute)
1. Exécuter `scripts/compile_results.sh`
2. Vérifier les CSV et graphiques générés dans `results/`

### Phase 4: Analyse (2-3 heures)
1. Analyser les CSV et graphiques
2. Remplir les tableaux dans `README.md`
3. Compléter `results/performance_analysis.md`

### Phase 5: Nettoyage (10 minutes)
1. Exécuter `scripts/cleanup.sh` si nécessaire
2. Vérifier les coûts
3. Valider avec `CHECKLIST.md`

### Phase 5: Rendu (30 minutes)
1. Ajouter vos noms dans `README.md`
2. Vérifier que tout est rempli
3. Git commit et push
4. Soumettre l'URL du dépôt

---

## 📝 Fichiers à Modifier OBLIGATOIREMENT

### Avant l'Exécution

**⚠️ CRITIQUE:**
1. `setup_gcp.sh` - Ligne 4 - `PROJECT_ID`
2. `data/download_data.sh` - Ligne 4 - `PROJECT_ID`
3. `scripts/test_config_2workers.sh` - Ligne 4 - `PROJECT_ID`
4. `scripts/test_config_4workers.sh` - Ligne 4 - `PROJECT_ID`
5. `scripts/test_config_6workers.sh` - Ligne 4 - `PROJECT_ID`
6. `scripts/compile_results.sh` - Ligne 4 - `PROJECT_ID`
7. `scripts/cleanup.sh` - Ligne 4 - `PROJECT_ID`

### Après l'Exécution

**Pour le rendu:**
1. `README.md` - Noms des membres (ligne 3)
2. `README.md` - Tableaux de résultats
3. `results/performance_analysis.md` - Toutes les sections `[À COMPLÉTER]`

---

## 🚫 Fichiers à NE PAS Modifier

**Code source (sauf si bug):**
- `src/utils.py`
- `src/pagerank_rdd.py`
- `src/pagerank_dataframe.py`

**Configuration (sauf PROJECT_ID):**
- `.gitignore`
- `requirements.txt`

**Documentation:**
- `DEMARRAGE_RAPIDE.md`
- `INSTRUCTIONS.md`
- `CHECKLIST.md`
- `OPTIMISATIONS.md`
- `CONTENU.md`

---

## 📊 Taille des Fichiers

| Fichier | Taille | Type |
|---------|--------|------|
| `README.md` | ~15 KB | Documentation |
| `INSTRUCTIONS.md` | ~20 KB | Guide |
| `OPTIMISATIONS.md` | ~12 KB | Technique |
| `src/*.py` | ~8 KB chacun | Code Python |
| `scripts/*.sh` | ~3 KB chacun | Scripts Bash |
| `results/*.log` | 10-100 KB | Logs (générés) |
| **Total (sans données)** | **~100 KB** | |

**Données:**
- `wikilinks_10percent.ttl` - ~200 MB
- `wikilinks_full.ttl` - ~2 GB
- **→ Stockées dans GCS, PAS dans Git** ✅

---

## ✅ Validation Finale du Contenu

Avant le rendu, vérifiez que vous avez:

### Documentation
- [x] `README.md` complet avec vos noms
- [x] Tous les tableaux remplis
- [x] Centre de Wikipedia identifié

### Code
- [x] Tous les fichiers `.py` présents
- [x] Tous les scripts `.sh` présents
- [x] `PROJECT_ID` modifié partout

### Résultats
- [x] Logs sauvegardés dans `results/`
- [x] `performance_analysis.md` complété
- [x] Graphiques créés (ou liens)

### Nettoyage
- [x] Clusters supprimés
- [x] Gros fichiers ignorés par Git
- [x] Dépôt Git à jour

---

**🎯 Ce projet contient TOUT ce dont vous avez besoin pour réussir!**

**📚 Lisez la documentation dans l'ordre:**
1. `DEMARRAGE_RAPIDE.md` (5 min)
2. `INSTRUCTIONS.md` (en suivant les étapes)
3. `CHECKLIST.md` (avant chaque action)
4. `OPTIMISATIONS.md` (pour l'analyse)

**🚀 Bon courage!**
