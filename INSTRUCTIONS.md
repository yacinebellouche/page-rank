# 📖 INSTRUCTIONS COMPLÈTES - Projet PageRank

**Guide pas-à-pas pour l'exécution du projet**

Ce guide vous accompagne de A à Z pour réaliser le projet PageRank sur Google Cloud Platform.

---

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Configuration Initiale](#configuration-initiale)
3. [Préparation des Données](#préparation-des-données)
4. [Exécution des Expériences](#exécution-des-expériences)
5. [Analyse des Résultats](#analyse-des-résultats)
6. [Nettoyage](#nettoyage)
7. [Dépannage](#dépannage)

---

## 1. Prérequis

### ✅ Checklist Avant de Commencer

- [ ] Compte Google avec accès à Google Cloud Platform
- [ ] Carte bancaire pour activer la facturation (ou crédits gratuits)
- [ ] Google Cloud SDK installé sur votre machine
- [ ] Git installé (pour cloner le dépôt)
- [ ] Bash/Shell disponible (Windows: Git Bash ou WSL)

### 📥 Installation de Google Cloud SDK

#### Windows

```powershell
# Télécharger depuis:
# https://cloud.google.com/sdk/docs/install

# Ou avec Chocolatey:
choco install gcloudsdk
```

#### Linux / macOS

```bash
# Suivre les instructions sur:
# https://cloud.google.com/sdk/docs/install
```

### ✅ Vérifier l'Installation

```bash
# Vérifier que gcloud est installé
gcloud --version

# Devrait afficher quelque chose comme:
# Google Cloud SDK 450.0.0
# ...
```

---

## 2. Configuration Initiale

### Étape 2.1: Créer un Projet Google Cloud

1. Allez sur https://console.cloud.google.com/
2. Cliquez sur "Sélectionner un projet" → "Nouveau projet"
3. Nommez votre projet (exemple: `pagerank-m2-2025`)
4. Notez l'**ID du projet** (différent du nom, ex: `pagerank-m2-2025-123456`)

### Étape 2.2: Activer la Facturation

1. Dans la console GCP, allez dans "Facturation"
2. Associez votre projet à un compte de facturation
3. ⚠️ **IMPORTANT:** Configurez une alerte de budget !

**Configurer une alerte de budget:**

```
Navigation: Facturation → Budgets et alertes → Créer un budget

Paramètres:
- Nom: "Budget PageRank"
- Montant: 50 EUR (ou USD) par membre
- Alertes: 50%, 80%, 100%
- Email: votre-email@etudiant.fr
```

### Étape 2.3: Authentification

```bash
# S'authentifier avec votre compte Google
gcloud auth login

# Suivre les instructions dans le navigateur
```

### Étape 2.4: Configurer le Projet

```bash
# Définir votre projet par défaut
gcloud config set project VOTRE-PROJECT-ID

# Exemple:
# gcloud config set project pagerank-m2-2025

# Vérifier
gcloud config list
```

### Étape 2.5: Modifier les Scripts

**CRUCIAL:** Avant d'exécuter quoi que ce soit, vous DEVEZ modifier la variable `PROJECT_ID` dans **TOUS** les fichiers suivants :

```bash
# Fichiers à modifier:
1. setup_gcp.sh
2. data/download_data.sh  
3. scripts/test_config_2workers.sh (ou 4/6 workers)
4. scripts/compile_results.sh
5. scripts/cleanup.sh# Dans chaque fichier, remplacer:
PROJECT_ID="votre-project-id"

# Par (exemple):
PROJECT_ID="pagerank-m2-2025"
```

**💡 Astuce:** Utilisez un éditeur de texte avec fonction "Rechercher et Remplacer" pour modifier tous les fichiers d'un coup.

### Étape 2.6: Exécuter le Script de Configuration

```bash
# Rendre le script exécutable
chmod +x setup_gcp.sh

# Exécuter
bash setup_gcp.sh
```

Ce script va:
- ✅ Activer les APIs nécessaires (Dataproc, Storage, Compute)
- ✅ Créer un bucket Google Cloud Storage
- ✅ Créer la structure de dossiers dans le bucket

**Sortie attendue:**
```
🚀 Configuration du projet Google Cloud PageRank...
📡 Activation des APIs...
✅ APIs activées avec succès
🪣 Création du bucket Google Cloud Storage...
✅ Bucket créé: gs://pagerank-m2-2025-pagerank-data/
✅ Configuration terminée avec succès!
```

---

## 3. Préparation des Données

### Étape 3.1: Télécharger les Données Wikipedia

```bash
# Aller dans le dossier data
cd data

# Rendre le script exécutable
chmod +x download_data.sh

# Exécuter le téléchargement
bash download_data.sh
```

**⚠️ Attention:**
- Le téléchargement fait ~1.8 GB
- Durée: 5-30 minutes selon votre connexion
- Le script crée automatiquement un échantillon de 10%

**Ce que fait le script:**
1. Télécharge `wikilinks_lang=en.ttl.bz2` (1.8 GB)
2. Décompresse le fichier
3. Crée un échantillon de 10% pour les tests
4. Upload les deux fichiers vers Google Cloud Storage
5. (Optionnel) Supprime les fichiers locaux pour libérer l'espace

**Sortie attendue:**
```
📥 Téléchargement des données Wikipedia...
✅ Téléchargement terminé
📦 Décompression...
✅ Décompression terminée
✂️  Création d'un échantillon de 10%...
✅ Échantillon créé
☁️  Upload vers Google Cloud Storage...
✅ Upload terminé
```

### Étape 3.2: Vérifier les Données

```bash
# Vérifier que les fichiers sont bien dans GCS
gsutil ls -lh gs://VOTRE-PROJECT-ID-pagerank-data/data/

# Devrait afficher:
# wikilinks_10percent.ttl  (~XXX MB)
# wikilinks_full.ttl       (~XXX GB)
```

---

## 4. Exécution des Expériences

### Étape 4.1: Préparer l'Exécution

```bash
# Retourner au dossier principal
cd ..

# Aller dans le dossier scripts
cd scripts

# Rendre les scripts exécutables
chmod +x *.sh
```

### Étape 4.2: Stratégie d'Exécution Recommandée

**🎯 Approche Progressive (RECOMMANDÉE):**

```bash
# Phase 1: Test avec 10% sur petite configuration
# Objectif: Valider que tout fonctionne

# Phase 2: Si Phase 1 OK, tester les autres configurations avec 10%
# Objectif: Comparer les performances

# Phase 3: Si tout OK, tester avec 100% des données
# Objectif: Résultats finaux
```

### Étape 4.3: Exécution Automatisée (Toutes les Configurations)

```bash
# Chaque membre de l'équipe lance UNE configuration:
Membre 1: bash test_config_2workers.sh
Membre 2: bash test_config_4workers.sh
Membre 3: bash test_config_6workers.sh
```

**⚠️ Durée par configuration:** 40-60 minutes

**Ce que fait chaque script:**

1. ✅ Crée le cluster Dataproc avec N workers
2. ✅ Exécute PageRank RDD avec 10% des données
3. ✅ Exécute PageRank DataFrame avec 10% des données
4. ✅ Exécute PageRank RDD avec 100% des données
5. ✅ Exécute PageRank DataFrame avec 100% des données
6. ✅ Supprime le cluster automatiquement (max-idle: 60s)
7. ✅ Génère results/config_Nworkers/comparison.csv

**Logs sauvegardés:**
- `results/config_2workers/rdd_10pct.log`
- `results/df_2workers_10pct.log`
- `results/rdd_4workers_10pct.log`
- `results/df_4workers_10pct.log`
- etc.

### Étape 4.4: Exécution Manuelle (Configuration par Configuration)

Si vous préférez contrôler chaque étape:

```bash
# CONFIGURATION 1: 2 workers (DÉCONSEILLÉ - Utiliser test_config_2workers.sh)
# Les scripts test_config_*workers.sh font ceci automatiquement

# Si vraiment vous voulez le faire manuellement:
# Créer le cluster avec gcloud dataproc clusters create...
# (voir le contenu de test_config_2workers.sh pour la commande complète)

# Étape 2: Uploader les scripts
gsutil cp ../src/*.py gs://VOTRE-PROJECT-ID-pagerank-data/scripts/

# Étape 3: Tester RDD (10%)
gcloud dataproc jobs submit pyspark \
  gs://VOTRE-PROJECT-ID-pagerank-data/scripts/pagerank_rdd.py \
  --cluster=pagerank-cluster-2workers \
  --region=europe-west1 \
  --py-files=gs://VOTRE-PROJECT-ID-pagerank-data/scripts/utils.py \
  -- gs://VOTRE-PROJECT-ID-pagerank-data/data/wikilinks_10percent.ttl 10

# Étape 4: Tester DataFrame (10%)
gcloud dataproc jobs submit pyspark \
  gs://VOTRE-PROJECT-ID-pagerank-data/scripts/pagerank_dataframe.py \
  --cluster=pagerank-cluster-2workers \
  --region=europe-west1 \
  --py-files=gs://VOTRE-PROJECT-ID-pagerank-data/scripts/utils.py \
  -- gs://VOTRE-PROJECT-ID-pagerank-data/data/wikilinks_10percent.ttl 10

# Étape 5: Supprimer le cluster
gcloud dataproc clusters delete pagerank-cluster --region=europe-west1

# Répéter pour 4 et 6 workers...
```

### Étape 4.5: Suivre l'Exécution

**Dans la Console GCP:**

1. Allez sur https://console.cloud.google.com/dataproc
2. Sélectionnez votre projet
3. Cliquez sur "Clusters" → Voir votre cluster
4. Cliquez sur "Tâches" → Voir les jobs en cours

**En ligne de commande:**

```bash
# Lister les clusters actifs
gcloud dataproc clusters list --region=europe-west1

# Lister les jobs en cours
gcloud dataproc jobs list --region=europe-west1 --filter="status.state=RUNNING"

# Voir les logs d'un job spécifique
gcloud dataproc jobs wait JOB-ID --region=europe-west1
```

---

## 5. Analyse des Résultats

### Étape 5.1: Récupérer les Logs

Les logs sont déjà sauvegardés localement dans `results/` pendant l'exécution.

Pour télécharger les résultats depuis GCS:

```bash
# Télécharger tous les résultats
gsutil -m cp -r gs://VOTRE-PROJECT-ID-pagerank-data/results/ ../results/gcs/
```

### Étape 5.2: Extraire les Informations Clés

#### Trouver le Centre de Wikipedia

```bash
# Dans les logs RDD (exemple)
grep "CENTRE DE WIKIPEDIA" ../results/rdd_6workers_full.log

# Dans les logs DataFrame
grep "CENTRE DE WIKIPEDIA" ../results/df_6workers_full.log
```

#### Extraire les Temps d'Exécution

```bash
# Pour tous les logs
grep "Temps d'exécution:" ../results/*.log

# Exemple de sortie:
# rdd_2workers_10pct.log:⏱️  Temps d'exécution: 45.23 secondes
# df_2workers_10pct.log:⏱️  Temps d'exécution: 38.67 secondes
```

### Étape 5.3: Compléter les Tableaux

**Dans README.md:**

Remplacez les `-` par vos résultats réels.

**Dans results/performance_analysis.md:**

Remplissez tous les champs `[À COMPLÉTER]` avec vos observations.

### Étape 5.4: Créer des Graphiques

**Outils recommandés:**
- Excel / Google Sheets
- Python (matplotlib/seaborn)
- R (ggplot2)

**Graphiques à créer:**
1. Temps d'exécution vs Nombre de workers (RDD vs DF)
2. Speedup vs Configuration
3. Temps par phase (chargement, itérations, sauvegarde)

---

## 6. Nettoyage

### ⚠️ IMPORTANT: Toujours Nettoyer Après Usage!

```bash
# Exécuter le script de nettoyage
cd scripts
bash cleanup.sh
```

**Le script va:**
1. ✅ Supprimer tous les clusters Dataproc actifs
2. ❓ Demander si vous voulez supprimer le bucket GCS
3. ✅ Annuler les jobs en cours
4. ✅ Afficher un résumé

**Vérifications manuelles recommandées:**

```bash
# Vérifier qu'aucun cluster n'est actif
gcloud dataproc clusters list --region=europe-west1

# Vérifier les coûts
# https://console.cloud.google.com/billing
```

---

## 7. Dépannage

### Problème 1: Le Cluster ne se Crée Pas

**Erreur:** `Quota exceeded` ou `Insufficient resources`

**Solution:**

```bash
# Vérifier vos quotas
gcloud compute project-info describe --project=VOTRE-PROJECT-ID

# Demander une augmentation de quota:
# https://console.cloud.google.com/iam-admin/quotas
```

### Problème 2: Permission Denied

**Erreur:** `Permission denied` lors de l'exécution

**Solution:**

```bash
# Activer les APIs
gcloud services enable dataproc.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable compute.googleapis.com

# Vérifier les rôles IAM
# Console → IAM & Admin → IAM
# Votre compte doit avoir les rôles:
# - Dataproc Editor
# - Storage Admin
```

### Problème 3: Job Échoue avec Out of Memory

**Erreur:** `OutOfMemoryError` dans les logs

**Solution:**

```bash
# Option 1: Réduire les données (tester avec 10% d'abord)

# Option 2: Utiliser une configuration avec plus de workers
bash test_config_6workers.sh  # au lieu de test_config_2workers.sh

# Option 3: Si vraiment nécessaire, modifier les scripts test_config_*workers.sh
# pour augmenter la mémoire:
--properties="spark:spark.executor.memory=12g,spark:spark.driver.memory=12g"
```

### Problème 4: Téléchargement des Données Échoue

**Erreur:** Timeout ou connexion interrompue

**Solution:**

```bash
# Option 1: Utiliser wget avec reprise
wget -c -O wikilinks_full.ttl.bz2 [URL]

# Option 2: Télécharger manuellement depuis:
# https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01/

# Puis uploader vers GCS:
gsutil cp wikilinks_full.ttl.bz2 gs://VOTRE-BUCKET/data/
```

### Problème 5: Coûts Trop Élevés

**Symptôme:** Budget dépassé

**Actions immédiates:**

```bash
# 1. Supprimer TOUS les clusters
gcloud dataproc clusters list --region=europe-west1
gcloud dataproc clusters delete NOM-CLUSTER --region=europe-west1

# 2. Vérifier les ressources actives
gcloud compute instances list

# 3. Consulter les coûts
# https://console.cloud.google.com/billing
```

**Prévention:**
- Toujours tester avec 10% d'abord
- Utiliser des machines préemptibles
- Activer les alertes de budget
- Supprimer les clusters après chaque utilisation

---

## 📊 Checklist Finale

Avant de rendre le projet, vérifiez que vous avez:

### Code et Documentation

- [ ] Tous les scripts sont dans le dépôt Git
- [ ] README.md complété avec vos noms et résultats
- [ ] results/performance_analysis.md rempli
- [ ] Logs d'exécution sauvegardés
- [ ] Graphiques créés

### Résultats

- [ ] Centre de Wikipedia identifié
- [ ] Tableaux de performance remplis
- [ ] Comparaison RDD vs DataFrame effectuée
- [ ] Analyse de scalabilité complétée
- [ ] Conclusions rédigées

### Nettoyage

- [ ] Tous les clusters supprimés
- [ ] Coûts vérifiés et dans le budget
- [ ] Bucket GCS nettoyé (ou conservé si nécessaire)

### Rendu

- [ ] URL du dépôt Git prête
- [ ] Noms des 3 membres du groupe indiqués
- [ ] README.md professionnel et complet

---

## 💡 Conseils Supplémentaires

### Travail en Équipe

- **Membre 1:** Configuration GCP et préparation des données
- **Membre 2:** Exécution des expériences et collecte des logs
- **Membre 3:** Analyse des résultats et rédaction

### Timing Recommandé

- **Jour 1:** Configuration et test avec 10% (2-3h)
- **Jour 2:** Expériences complètes (3-4h)
- **Jour 3:** Analyse et rédaction (2-3h)

### Points d'Attention

1. ⚠️ **Budget:** Surveillez constamment vos coûts
2. ⚠️ **Quotas:** Vérifiez la limite de 32 vCPU
3. ⚠️ **Temps:** Les jobs avec 100% peuvent prendre 30+ minutes
4. ⚠️ **Nettoyage:** TOUJOURS supprimer les ressources après usage

---

## 📧 Support

En cas de problème:

1. Consultez d'abord cette documentation
2. Vérifiez la section [Dépannage](#dépannage)
3. Consultez la documentation Google Cloud
4. Contactez l'enseignant: Pascal Molli

---

**Bon courage pour le projet! 🚀**

**N'oubliez pas:** L'objectif est d'apprendre, pas de dépenser tout le budget. Testez progressivement!
