# ✅ CHECKLIST - Vérification Avant Exécution

**Utilisez cette checklist pour éviter les erreurs courantes**

---

## 🔴 CRITIQUE - À FAIRE ABSOLUMENT

### 1. Modifier PROJECT_ID

- [ ] `setup_gcp.sh` - Ligne 4
- [ ] `data/download_simple.sh` - Ligne 4
- [ ] `scripts/test_config_2workers.sh` - Ligne 4
- [ ] `scripts/test_config_4workers.sh` - Ligne 4
- [ ] `scripts/test_config_6workers.sh` - Ligne 4
- [ ] `scripts/compile_results.sh` - Ligne 4
- [ ] `scripts/cleanup.sh` - Ligne 4

**Comment vérifier:**
```bash
grep -n "votre-project-id" *.sh data/*.sh scripts/*.sh

# Si cette commande retourne des résultats, vous avez oublié de modifier !
```

### 2. Configuration Google Cloud

- [ ] Compte Google Cloud créé
- [ ] Projet créé (noter l'ID exact)
- [ ] Facturation activée
- [ ] Alerte de budget configurée (50€ par membre)

**Vérifier:**
```bash
gcloud config list
# Doit afficher votre project ID
```

### 3. APIs Activées

- [ ] Dataproc API
- [ ] Storage API  
- [ ] Compute Engine API

**Vérifier:**
```bash
gcloud services list --enabled | grep -E "(dataproc|storage|compute)"
```

---

## 🟡 IMPORTANT - Recommandé

### 4. Quotas Vérifiés

- [ ] vCPU quota >= 32
- [ ] Disques persistants quota OK

**Vérifier:**
```bash
gcloud compute project-info describe --project=VOTRE-PROJECT-ID
```

### 5. Outils Installés

- [ ] Google Cloud SDK installé
- [ ] `gcloud` fonctionnel
- [ ] `gsutil` fonctionnel
- [ ] Bash disponible

**Vérifier:**
```bash
gcloud --version
gsutil --version
```

### 6. Structure de Projet

- [ ] Dossier `data/` existe
- [ ] Dossier `src/` existe
- [ ] Dossier `scripts/` existe
- [ ] Dossier `results/` existe

**Vérifier:**
```bash
ls -la
# Doit afficher data/, src/, scripts/, results/
```

---

## 🟢 OPTIONNEL - Conseils

### 7. Git Configuration

- [ ] Dépôt Git initialisé
- [ ] `.gitignore` configuré
- [ ] Commit initial effectué

**Faire:**
```bash
git init
git add .
git commit -m "Initial commit - PageRank project"
```

### 8. Documentation Lue

- [ ] `DEMARRAGE_RAPIDE.md` lu
- [ ] `INSTRUCTIONS.md` parcouru
- [ ] `README.md` consulté

### 9. Membres du Groupe

- [ ] Noms ajoutés dans `README.md`
- [ ] Emails ajoutés dans `README.md`
- [ ] Répartition des tâches effectuée

---

## 📋 AVANT CHAQUE EXÉCUTION

### Test avec 10% des Données

- [ ] Données 10% téléchargées et dans GCS
- [ ] Scripts uploadés vers GCS
- [ ] Cluster créé avec 2 workers (test)
- [ ] Job RDD exécuté avec succès
- [ ] Job DataFrame exécuté avec succès
- [ ] Cluster supprimé après test

### Test avec 100% des Données

- [ ] Test 10% réussi
- [ ] Temps d'exécution 10% acceptable
- [ ] Budget suffisant
- [ ] Cluster créé avec configuration souhaitée
- [ ] Jobs exécutés
- [ ] Résultats sauvegardés
- [ ] Cluster supprimé

---

## 🧹 APRÈS CHAQUE EXÉCUTION

### Nettoyage Immédiat

- [ ] Cluster Dataproc supprimé
- [ ] Logs sauvegardés localement
- [ ] Coûts vérifiés

**Commandes:**
```bash
# Vérifier qu'aucun cluster n'est actif
gcloud dataproc clusters list --region=europe-west1

# Vérifier les coûts
# https://console.cloud.google.com/billing
```

---

## 💰 SURVEILLANCE DES COÛTS

### Vérifications Régulières

- [ ] Budget alert configuré
- [ ] Coûts consultés toutes les 2h pendant les expériences
- [ ] Aucun cluster oublié actif

**Seuils d'alerte:**
- 🟢 < 20€: OK
- 🟡 20-40€: Attention
- 🔴 > 40€: STOP! Vérifier immédiatement

---

## 📊 AVANT LE RENDU

### Résultats Complets

- [ ] Centre de Wikipedia identifié
- [ ] Tableaux dans `README.md` remplis
- [ ] `results/performance_analysis.md` complété
- [ ] Graphiques créés
- [ ] Conclusions rédigées

### Documentation

- [ ] Noms des membres ajoutés
- [ ] URL du dépôt ajoutée
- [ ] README.md professionnel
- [ ] Code commenté

### Fichiers

- [ ] Tous les fichiers source (.py, .sh) présents
- [ ] Logs d'exécution sauvegardés
- [ ] `.gitignore` configuré (pas de gros fichiers)
- [ ] Git push effectué

### Nettoyage Final

- [ ] TOUS les clusters supprimés
- [ ] Bucket GCS nettoyé ou conservé selon besoin
- [ ] Coûts totaux < 50€ par membre
- [ ] Pas de ressources actives oubliées

---

## 🚨 ERREURS COURANTES À ÉVITER

### ❌ NE PAS FAIRE

1. ❌ Oublier de modifier `PROJECT_ID`
2. ❌ Lancer sur 100% sans tester 10% d'abord
3. ❌ Laisser des clusters actifs la nuit
4. ❌ Créer des clusters sans machines préemptibles
5. ❌ Ignorer les alertes de budget
6. ❌ Utiliser des machines trop puissantes (n1-highmem, etc.)
7. ❌ Créer plus de 6 workers (limite vCPU)
8. ❌ Oublier de sauvegarder les logs
9. ❌ Ne pas vérifier les coûts régulièrement
10. ❌ Pusher les gros fichiers de données dans Git

### ✅ À FAIRE

1. ✅ Toujours tester avec 10% d'abord
2. ✅ Utiliser des machines préemptibles
3. ✅ Supprimer les clusters immédiatement après usage
4. ✅ Configurer des alertes de budget
5. ✅ Sauvegarder tous les logs
6. ✅ Vérifier les coûts toutes les 2 heures
7. ✅ Respecter la limite de 32 vCPU
8. ✅ Utiliser `.gitignore` pour les gros fichiers
9. ✅ Documenter toutes les observations
10. ✅ Travailler en équipe de manière organisée

---

## 📞 EN CAS DE PROBLÈME

### Étape 1: Consulter la Documentation

1. Chercher dans `INSTRUCTIONS.md` section Dépannage
2. Consulter ce fichier (CHECKLIST.md)
3. Lire les messages d'erreur attentivement

### Étape 2: Vérifier les Bases

```bash
# Projet correct?
gcloud config list

# APIs activées?
gcloud services list --enabled

# Clusters actifs?
gcloud dataproc clusters list --region=europe-west1

# Budget OK?
# https://console.cloud.google.com/billing
```

### Étape 3: Actions Correctives

**Si cluster ne se crée pas:**
```bash
# Vérifier quotas
gcloud compute project-info describe --project=VOTRE-PROJECT-ID
```

**Si job échoue:**
```bash
# Voir les logs complets
gcloud dataproc jobs describe JOB-ID --region=europe-west1
```

**Si out of memory:**
```bash
# Utiliser config avec plus de workers
bash test_config_6workers.sh  # au lieu de test_config_2workers.sh
```

**Si coûts trop élevés:**
```bash
# ARRÊTER TOUT IMMÉDIATEMENT
bash scripts/cleanup.sh
```

---

## ✅ VALIDATION FINALE

Avant de dire "C'est terminé", vérifiez:

```bash
# Aucun cluster actif
gcloud dataproc clusters list --region=europe-west1
# Devrait retourner: Listed 0 items.

# Aucun job en cours
gcloud dataproc jobs list --region=europe-west1 --filter="status.state=RUNNING"
# Devrait retourner: Listed 0 items.

# Git à jour
git status
git push
```

---

**🎯 Utilisez cette checklist à chaque étape du projet!**

**📌 Imprimez ou gardez ce fichier ouvert pendant l'exécution**

---

*Dernière mise à jour: Novembre 2025*
