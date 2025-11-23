# Scripts PageRank - Guide d'Utilisation

Ce dossier contient tous les scripts nécessaires pour exécuter le projet PageRank.

---

## 📋 Scripts Disponibles

### ✨ Scripts Automatisés (Recommandés)

Ces scripts font **TOUT automatiquement** : création cluster → tests → suppression → résultats.

#### `test_config_2workers.sh`
**Usage :** Configuration avec 2 workers (recommandé pour débutant)
```bash
bash test_config_2workers.sh
```

**Ce qu'il fait :**
- Demande PROJECT_ID (ou utilise variable d'environnement)
- Crée cluster Dataproc avec 2 workers préemptibles
- Upload scripts Python vers Cloud Storage
- Exécute RDD et DataFrame sur 10% des données
- Exécute RDD et DataFrame sur 100% des données
- **Supprime le cluster immédiatement** (économie!)
- Génère CSV de comparaison dans `results/config_2workers/`
- Sauvegarde log détaillé avec timestamp

**Durée :** ~20 minutes  
**Coût :** ~3€

#### `test_config_4workers.sh`
**Usage :** Configuration avec 4 workers
```bash
bash test_config_4workers.sh
```

Identique à `test_config_2workers.sh` mais avec 4 workers.

**Durée :** ~25 minutes  
**Coût :** ~4€

#### `test_config_6workers.sh`
**Usage :** Configuration avec 6 workers (configuration maximale)
```bash
bash test_config_6workers.sh
```

Identique mais avec 6 workers (limite avant quota 32 vCPU).

**Durée :** ~30 minutes  
**Coût :** ~5€

#### `compile_results.sh`
**Usage :** Compiler tous les résultats et générer les graphiques
```bash
bash compile_results.sh
```

**Ce qu'il fait :**
- Recherche tous les fichiers de résultats (config_*workers_*.log)
- Génère graphiques de comparaison (Python/matplotlib)
- Crée récapitulatif texte consolidé
- Affiche aperçu des améliorations DataFrame vs RDD

**Prérequis :** Au moins un fichier de résultats doit exister.

**Génère :**
- `results/graphs/comparison_all_configs.png`
- `results/graphs/execution_time_evolution.png`
- `results/graphs/summary_table.png`
- `results/summary_YYYYMMDD_HHMMSS.txt`

---

### ⚙️ Scripts Utilitaires

#### `create_cluster.sh`
**Usage :** Créer un cluster Dataproc manuellement
```bash
bash create_cluster.sh NUM_WORKERS
```

**Paramètres :**
- `NUM_WORKERS` : Nombre de workers (2, 4, ou 6)

**Exemple :**
```bash
bash create_cluster.sh 4  # Crée cluster avec 4 workers
```

**Note :** Les scripts `test_config_*workers.sh` appellent ce script automatiquement.

#### `cleanup.sh`
**Usage :** Nettoyer toutes les ressources GCP manuellement
```bash
bash cleanup.sh
```

**Ce qu'il fait :**
- Supprime tous les clusters Dataproc dans la région
- Supprime le bucket Cloud Storage
- Affiche résumé des ressources supprimées

**Attention :** Utilisez avec précaution - supprime TOUTES les ressources du projet!

#### `generate_graphs.py`
**Usage :** Script Python pour générer les graphiques (appelé par compile_results.sh)
```bash
python3 generate_graphs.py
```

**Prérequis :**
- Python 3
- matplotlib, pandas, numpy installés
- Fichiers CSV dans `results/config_*workers/comparison.csv`

**Note :** Normalement, utilisez `compile_results.sh` qui appelle ce script automatiquement.

---

## 🔄 Workflow Recommandé

### Scénario 1 : Travail en Équipe (Recommandé)

**3 membres = 3 configurations en parallèle**

```bash
# Membre 1 (sur son compte GCP)
cd scripts
bash test_config_2workers.sh

# Membre 2 (sur son compte GCP)  
cd scripts
bash test_config_4workers.sh

# Membre 3 (sur son compte GCP)
cd scripts
bash test_config_6workers.sh

# Ensuite, un membre compile tous les résultats
bash compile_results.sh
```

**Avantages :**
- ⚡ Temps divisé par 3
- 💰 Coûts répartis
- 🔄 Résultats obtenus en ~30 min au lieu de 1h30

### Scénario 2 : Travail Solo

**Une seule personne teste toutes les configurations**

```bash
cd scripts

# Test 1 : 2 workers
bash test_config_2workers.sh
# Attendre fin (~20 min)

# Test 2 : 4 workers
bash test_config_4workers.sh
# Attendre fin (~25 min)

# Test 3 : 6 workers
bash test_config_6workers.sh
# Attendre fin (~30 min)

# Compilation
bash compile_results.sh
```

**Durée totale :** ~1h30 + compilation  
**Coût total :** ~12€

---

## 💡 Configuration PROJECT_ID

### Méthode 1 : Variable d'Environnement (Recommandée)

```bash
# Définir une fois au début de la session
export PROJECT_ID=votre-project-id-gcp

# Ensuite tous les scripts l'utilisent automatiquement
bash test_config_2workers.sh  # Pas besoin de saisir PROJECT_ID
```

### Méthode 2 : Saisie Interactive

```bash
# Si PROJECT_ID n'est pas défini, le script demande :
bash test_config_2workers.sh

# Affiche :
# "PROJECT_ID n'est pas défini. Entrez votre PROJECT_ID:"
# [Vous tapez : votre-project-id-gcp]
```

### Méthode 3 : Modifier Directement dans les Scripts

Ouvrir le script et modifier la ligne :
```bash
PROJECT_ID="${PROJECT_ID:-votre-project-id}"
```

Remplacer `votre-project-id` par votre vrai PROJECT_ID.

---

## 📊 Résultats Générés

### Structure après exécution complète :

```
results/
├── config_2workers/
│   └── comparison.csv                     # Résultats 2 workers
├── config_4workers/
│   └── comparison.csv                     # Résultats 4 workers
├── config_6workers/
│   └── comparison.csv                     # Résultats 6 workers
│
├── graphs/
│   ├── comparison_all_configs.png         # Graphique principal
│   ├── execution_time_evolution.png       # Évolution temps
│   └── summary_table.png                  # Tableau récapitulatif
│
├── config_2workers_20240315_143022.log    # Log détaillé 2 workers
├── config_4workers_20240315_150145.log    # Log détaillé 4 workers
├── config_6workers_20240315_153308.log    # Log détaillé 6 workers
│
└── summary_20240315_160000.txt            # Récapitulatif consolidé
```

### Contenu des CSV (example)

`results/config_2workers/comparison.csv` :
```csv
Type,Dataset,Time_seconds,Time_formatted
RDD,10%,245,4m 5s
DataFrame,10%,198,3m 18s
RDD,100%,1823,30m 23s
DataFrame,100%,1456,24m 16s
```

---

## 🔧 Dépannage

### Problème : "gcloud: command not found"

**Solution :** Installer Google Cloud SDK
```bash
# Windows (PowerShell)
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe

# Linux/Mac
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Problème : "Permission denied" lors de l'exécution

**Solution :** Rendre le script exécutable
```bash
chmod +x test_config_2workers.sh
chmod +x test_config_4workers.sh
chmod +x test_config_6workers.sh
chmod +x compile_results.sh
```

### Problème : "Quota exceeded" lors création cluster

**Cause :** Limite de 32 vCPU par projet dépassée.

**Solutions :**
1. Supprimer clusters existants :
   ```bash
   gcloud dataproc clusters list --region=europe-west1
   gcloud dataproc clusters delete CLUSTER_NAME --region=europe-west1
   ```

2. Demander augmentation quota (processus long, non recommandé)

3. Utiliser configuration plus petite (2 workers au lieu de 6)

### Problème : Cluster créé mais job échoue

**Débug :**
```bash
# Voir les logs du job
gcloud dataproc jobs list --region=europe-west1

# Détails d'un job spécifique
gcloud dataproc jobs describe JOB_ID --region=europe-west1

# Logs YARN (dans GCP Console)
# Dataproc → Clusters → [Cluster Name] → Web Interfaces → YARN ResourceManager
```

### Problème : Graphiques ne se génèrent pas

**Vérifications :**
```bash
# Vérifier packages Python
python3 -m pip list | grep -E "(matplotlib|pandas|numpy)"

# Installer si manquant
python3 -m pip install matplotlib pandas numpy

# Vérifier que CSV existent
ls -la ../results/config_*workers/comparison.csv
```

### Problème : Coûts inattendus

**Vérifications :**
```bash
# Lister tous les clusters (doivent être supprimés après tests)
gcloud dataproc clusters list --region=europe-west1

# Vérifier bucket Cloud Storage (ne devrait contenir que données)
gsutil du -sh gs://PROJECT_ID-pagerank-data/

# Voir estimation coûts dans GCP Console
# Billing → Reports → Filter by Service (Dataproc, Compute Engine)
```

---

## ⏱️ Estimations Temps et Coûts

| Configuration | Setup | RDD 10% | DF 10% | RDD 100% | DF 100% | Cleanup | Total | Coût |
|---------------|-------|---------|--------|----------|---------|---------|-------|------|
| 2 workers     | 3 min | 4 min   | 3 min  | 30 min   | 24 min  | 1 min   | ~20 min | ~3€ |
| 4 workers     | 3 min | 2.5 min | 2 min  | 17 min   | 13 min  | 1 min   | ~25 min | ~4€ |
| 6 workers     | 3 min | 1.5 min | 1.5 min| 12 min   | 9 min   | 1 min   | ~30 min | ~5€ |

**Total si 3 configurations :** ~12€ et 75 minutes (en séquentiel)  
**Total si parallèle (3 membres) :** ~12€ et 30 minutes

---

## ✅ Checklist Avant Lancement

- [ ] Google Cloud SDK installé (`gcloud --version`)
- [ ] Authentifié à GCP (`gcloud auth list`)
- [ ] PROJECT_ID correctement défini
- [ ] Données téléchargées (`data/download_data.sh` exécuté)
- [ ] Quota vCPU vérifié (< 32 vCPU disponibles)
- [ ] Alerte budget configurée dans GCP Console
- [ ] Script exécutable (`chmod +x` si nécessaire)

---

## 📚 Documentation Associée

- **DEMARRAGE_RAPIDE.md** - Vue d'ensemble rapide
- **INSTRUCTIONS.md** - Guide détaillé pas-à-pas
- **RECAPITULATIF.md** - Récapitulatif complet du projet
- **GUIDE_RAPPORT.md** - Guide pour rédiger le rapport final
- **OPTIMISATIONS.md** - Détails techniques optimisations

---

**Bon courage ! 🚀**
