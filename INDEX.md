# 📑 INDEX - Navigation Rapide Projet PageRank

Ce fichier vous guide vers la bonne documentation selon votre besoin.

---

## 🎯 Je Veux...

### Démarrer Rapidement

➜ **DEMARRAGE_RAPIDE.md** ou **QUICKSTART.md** (English)
- 3 commandes pour tout faire
- Workflow en équipe
- Temps: 40 minutes

### Comprendre le Projet

➜ **README.md**
- Vue d'ensemble complète
- Objectifs et résultats
- Configuration matérielle

➜ **RECAPITULATIF.md**
- Résumé complet
- Structure fichiers
- Workflow détaillé

### Exécuter les Tests

➜ **scripts/README.md**
- Guide utilisation scripts
- test_config_*workers.sh
- compile_results.sh

➜ **CHECKLIST.md**
- Vérifications avant lancement
- Éviter erreurs coûteuses

### Instructions Détaillées

➜ **INSTRUCTIONS.md**
- Guide pas-à-pas complet
- Troubleshooting
- Configuration GCP

### Rédiger le Rapport

➜ **GUIDE_RAPPORT.md** ⭐
- Structure recommandée
- Exemples de rédaction
- Formules mathématiques
- Interprétation résultats

### Comprendre le Code

➜ **OPTIMISATIONS.md**
- Co-partitionnement
- Cache stratégique
- Catalyst optimizer
- Détails techniques

➜ Commentaires dans le code source :
- `src/utils.py`
- `src/pagerank_rdd.py`
- `src/pagerank_dataframe.py`

### Analyser les Résultats

➜ **results/README.md**
- Format fichiers générés
- Calculs de speedup
- Extraction données
- Interprétation graphiques

### Comprendre la Structure

➜ **CONTENU.md**
- Liste complète fichiers
- Description chaque composant
- Statistiques projet

---

## 📁 Par Type de Fichier

### 📖 Documentation (9 fichiers)

| Fichier | Contenu | Quand le lire |
|---------|---------|---------------|
| **INDEX.md** | Ce fichier - navigation | En premier |
| **QUICKSTART.md** | Démarrage rapide (English) | Pour vue rapide |
| **DEMARRAGE_RAPIDE.md** | Démarrage rapide (French) | ⭐ Commencer ici |
| **README.md** | Documentation principale | Vue d'ensemble |
| **RECAPITULATIF.md** | Récapitulatif complet | Workflow complet |
| **INSTRUCTIONS.md** | Guide détaillé | Si problème |
| **GUIDE_RAPPORT.md** | Guide rédaction rapport | ⭐ Pour rapport |
| **CHECKLIST.md** | Vérifications pré-lancement | Avant tests |
| **OPTIMISATIONS.md** | Détails techniques | Comprendre code |
| **CONTENU.md** | Structure projet | Organisation |

### 💻 Code Source (3 fichiers)

| Fichier | Description | Lignes |
|---------|-------------|--------|
| **src/utils.py** | Fonctions utilitaires | ~120 |
| **src/pagerank_rdd.py** | PageRank RDD | ~150 |
| **src/pagerank_dataframe.py** | PageRank DataFrame | ~140 |

### 🔧 Scripts (8 fichiers)

| Fichier | Type | Description |
|---------|------|-------------|
| **test_config_2workers.sh** | ⭐ AUTO | Test automatisé 2 workers |
| **test_config_4workers.sh** | ⭐ AUTO | Test automatisé 4 workers |
| **test_config_6workers.sh** | ⭐ AUTO | Test automatisé 6 workers |
| **compile_results.sh** | ⭐ AUTO | Compilation résultats |
| **generate_graphs.py** | Python | Génération graphiques |
| **create_cluster.sh** | Utilitaire | Création cluster |
| **cleanup.sh** | Utilitaire | Nettoyage |
| **scripts/README.md** | Doc | Guide scripts |

### 📊 Données et Résultats

| Dossier | Contenu |
|---------|---------|
| **data/** | Données Wikipedia DBpedia |
| **results/** | Résultats, logs, graphiques |
| **results/graphs/** | Graphiques PNG haute qualité |
| **results/config_*workers/** | CSV par configuration |

---

## 🚀 Parcours Recommandés

### Parcours 1 : Débutant - Démarrage Rapide

```
1. INDEX.md (ce fichier)
   ↓
2. DEMARRAGE_RAPIDE.md
   ↓
3. CHECKLIST.md
   ↓
4. Exécuter: bash test_config_Xworkers.sh
   ↓
5. GUIDE_RAPPORT.md
```

**Temps total :** ~1 heure (lecture + exécution)

### Parcours 2 : Complet - Compréhension Détaillée

```
1. INDEX.md
   ↓
2. README.md
   ↓
3. RECAPITULATIF.md
   ↓
4. INSTRUCTIONS.md
   ↓
5. OPTIMISATIONS.md
   ↓
6. Code source (src/*.py)
   ↓
7. Exécuter: bash test_config_Xworkers.sh
   ↓
8. results/README.md
   ↓
9. GUIDE_RAPPORT.md
```

**Temps total :** ~3 heures (lecture complète + exécution + analyse)

### Parcours 3 : Technique - Focus Code

```
1. OPTIMISATIONS.md
   ↓
2. src/utils.py
   ↓
3. src/pagerank_rdd.py
   ↓
4. src/pagerank_dataframe.py
   ↓
5. scripts/test_config_2workers.sh (lire le code)
   ↓
6. Exécuter et analyser logs
```

**Temps total :** ~2 heures

### Parcours 4 : Rapport - Rédaction

```
1. Résultats déjà générés (CSV, logs, PNG)
   ↓
2. results/README.md (analyser résultats)
   ↓
3. GUIDE_RAPPORT.md (structure)
   ↓
4. Extraire données des CSV
   ↓
5. Insérer graphiques PNG
   ↓
6. Calculer speedup/efficacité
   ↓
7. Rédiger analyse et conclusion
```

**Temps total :** ~3-4 heures (rédaction rapport complet)

---

## 🎓 Par Rôle dans l'Équipe

### Membre Exécutant les Tests

**Lire dans l'ordre :**

1. DEMARRAGE_RAPIDE.md
2. CHECKLIST.md
3. scripts/README.md (section correspondant à votre config)

**Exécuter :**
```bash
cd scripts
bash test_config_Xworkers.sh  # X = 2, 4, ou 6 selon assignation
```

**Partager :**
- `results/config_Xworkers/comparison.csv`
- `results/config_Xworkers_*.log`

### Membre Compilant les Résultats

**Lire dans l'ordre :**

1. scripts/README.md (section compile_results.sh)
2. results/README.md

**Exécuter :**
```bash
cd scripts
bash compile_results.sh
```

**Vérifier :**
- Graphiques générés dans `results/graphs/`
- Récapitulatif texte créé
- Tous les CSV présents

### Membre Rédigeant le Rapport

**Lire dans l'ordre :**

1. GUIDE_RAPPORT.md (⭐ principal)
2. results/README.md (analyser résultats)
3. OPTIMISATIONS.md (pour section méthodologie)
4. README.md (pour introduction/contexte)

**Utiliser :**
- Graphiques PNG depuis `results/graphs/`
- Données CSV depuis `results/config_*/`
- Logs pour extraits techniques

---

## 📋 Checklist Complète Projet

### Avant de Commencer

- [ ] Lu INDEX.md (ce fichier)
- [ ] Lu DEMARRAGE_RAPIDE.md
- [ ] Lu CHECKLIST.md
- [ ] GCP configuré (compte, facturation, SDK)

### Exécution Tests

- [ ] Données téléchargées (`bash data/download_data.sh`)
- [ ] Script test lancé selon assignation
- [ ] Résultats générés (CSV + logs)
- [ ] Cluster automatiquement supprimé

### Compilation

- [ ] Tous les CSV reçus (3 configurations)
- [ ] Script compile_results.sh exécuté
- [ ] Graphiques PNG vérifiés
- [ ] Récapitulatif texte créé

### Rapport

- [ ] Lu GUIDE_RAPPORT.md
- [ ] Structure rapport définie
- [ ] Tableaux remplis
- [ ] Graphiques insérés
- [ ] Analyse rédigée
- [ ] Conclusion écrite

---

## 🔍 Recherche Rapide

### Par Mot-Clé

| Vous cherchez... | Consultez... |
|------------------|--------------|
| Commandes à exécuter | DEMARRAGE_RAPIDE.md, scripts/README.md |
| Coûts et budget | README.md, RECAPITULATIF.md |
| Optimisations techniques | OPTIMISATIONS.md, code source |
| Structure rapport | GUIDE_RAPPORT.md |
| Troubleshooting | INSTRUCTIONS.md, scripts/README.md |
| Résultats et graphiques | results/README.md |
| Workflow équipe | RECAPITULATIF.md, DEMARRAGE_RAPIDE.md |
| Configuration GCP | INSTRUCTIONS.md, setup_gcp.sh |
| Formules mathématiques | GUIDE_RAPPORT.md |
| Speedup et scalabilité | GUIDE_RAPPORT.md, results/README.md |

### Par Question

| Question | Réponse dans... |
|----------|-----------------|
| Comment démarrer rapidement ? | DEMARRAGE_RAPIDE.md |
| Combien ça coûte ? | README.md (10-15€) |
| Combien de temps ? | RECAPITULATIF.md (~40 min en parallèle) |
| Quels fichiers modifier ? | CHECKLIST.md (PROJECT_ID) |
| Comment analyser résultats ? | results/README.md |
| Comment rédiger rapport ? | GUIDE_RAPPORT.md |
| Pourquoi DataFrame plus rapide ? | OPTIMISATIONS.md |
| Comment calculer speedup ? | GUIDE_RAPPORT.md, results/README.md |
| Que faire si erreur ? | INSTRUCTIONS.md (section Troubleshooting) |
| Comment partager résultats ? | RECAPITULATIF.md (workflow) |

---

## 🌟 Top 3 Fichiers à Lire Absolument

### 🥇 DEMARRAGE_RAPIDE.md
**Pourquoi :** Tout ce qu'il faut pour commencer en 5 minutes.  
**Quand :** Au début du projet.

### 🥈 GUIDE_RAPPORT.md
**Pourquoi :** Structure complète avec exemples pour rédiger le rapport final.  
**Quand :** Après obtention des résultats.

### 🥉 scripts/README.md
**Pourquoi :** Guide précis des scripts automatisés.  
**Quand :** Avant de lancer les tests.

---

## 💡 Conseil Final

**Pour gagner du temps :**

1. ⭐ Commencez par **DEMARRAGE_RAPIDE.md**
2. ⭐ Vérifiez **CHECKLIST.md** avant de lancer
3. ⭐ Lancez **test_config_Xworkers.sh** (automatique!)
4. ⭐ Compilez avec **compile_results.sh**
5. ⭐ Suivez **GUIDE_RAPPORT.md** pour rédiger

**Temps total : ~40 minutes tests + 3-4h rapport = 4-5h projet complet**

Au lieu de :
- ❌ Lire toute la doc (~2h)
- ❌ Comprendre tout le code (~2h)
- ❌ Configuration manuelle (~1h)
- ❌ Tests séquentiels (~2h)
- ❌ Compilation manuelle (~1h)
- ❌ Rédaction sans guide (~5h)

**Total traditionnel : ~13h** 😰

**Total avec ce projet : ~5h** 🚀

**Économie : 8 heures = 61%!**

---

**Navigation rapide, exécution efficace, résultats garantis ! 🎯**
