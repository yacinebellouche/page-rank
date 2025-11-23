# 📁 Structure Finale du Projet PageRank

**Date:** Janvier 2025  
**Version:** 2.0 (Optimisée)  
**Total fichiers:** 23 fichiers

---

## 📂 Arborescence Complète

```
page-rank/
│
├── 📄 README.md                       # Guide principal (EN)
├── 📄 INDEX.md                        # Index de tous les fichiers
├── 📄 DEMARRAGE_RAPIDE.md            # Démarrage rapide (FR)
├── 📄 QUICKSTART.md                  # Quickstart guide (EN)
├── 📄 INSTRUCTIONS.md                # Instructions détaillées (FR)
├── 📄 RECAPITULATIF.md               # Récapitulatif projet (FR)
├── 📄 CONTENU.md                     # Description de tous les fichiers
├── 📄 GUIDE_RAPPORT.md               # Guide pour le rapport
├── 📄 OPTIMISATIONS.md               # Optimisations implémentées
├── 📄 CHECKLIST.md                   # Checklist de validation
├── 📄 CHANGELOG.md                   # Journal des modifications
├── 📄 STRUCTURE_PROJET.md            # Ce fichier
├── 📄 LICENSE                        # Licence MIT
├── 📄 .gitignore                     # Fichiers ignorés par Git
├── 📄 requirements.txt               # Dépendances Python
├── 📄 setup_gcp.sh                   # Configuration initiale GCP
├── 📄 PageRank 2025-2026.pdf         # Sujet du projet
│
├── 📁 src/                           # Code source Python
│   ├── utils.py                      # Fonctions utilitaires
│   ├── pagerank_rdd.py               # Implémentation RDD
│   └── pagerank_dataframe.py         # Implémentation DataFrame
│
├── 📁 data/                          # Données et scripts
│   └── download_data.sh              # Téléchargement données Wikipedia
│
├── 📁 scripts/                       # Scripts d'exécution
│   ├── test_config_2workers.sh       # ⭐ Test automatisé 2 workers
│   ├── test_config_4workers.sh       # ⭐ Test automatisé 4 workers
│   ├── test_config_6workers.sh       # ⭐ Test automatisé 6 workers
│   ├── compile_results.sh            # ⭐ Compilation résultats et graphiques
│   ├── generate_graphs.py            # Génération graphiques Python
│   ├── cleanup.sh                    # Nettoyage ressources GCP
│   └── README.md                     # Documentation scripts
│
└── 📁 results/                       # Résultats (générés)
    ├── performance_analysis.md       # Modèle d'analyse
    └── README.md                     # Guide résultats
```

---

## 📊 Statistiques

| Catégorie | Nombre | Détails |
|-----------|--------|---------|
| **Documentation** | 12 fichiers | README, guides, analyses |
| **Code Python** | 3 fichiers | RDD, DataFrame, utils |
| **Scripts Bash** | 7 fichiers | Setup, tests, compilation, cleanup |
| **Configuration** | 2 fichiers | requirements.txt, .gitignore |
| **Données** | 1 fichier | download_data.sh |
| **TOTAL** | **23 fichiers** | + dossiers results/ générés |

---

## ⭐ Scripts Principaux (Workflow)

### 1️⃣ Configuration (Une seule fois)
```bash
# Modifier PROJECT_ID dans tous les scripts
bash setup_gcp.sh
```

### 2️⃣ Téléchargement Données (Une seule fois)
```bash
cd data
bash download_data.sh
```

### 3️⃣ Tests (EN PARALLÈLE - 3 membres)
```bash
cd scripts

# Membre 1:
bash test_config_2workers.sh

# Membre 2:
bash test_config_4workers.sh

# Membre 3:
bash test_config_6workers.sh
```

### 4️⃣ Compilation Résultats (1 membre)
```bash
cd scripts
bash compile_results.sh
```

### 5️⃣ Nettoyage (Optionnel)
```bash
cd scripts
bash cleanup.sh
```

---

## 🔄 Fichiers Supprimés (Version 2.0)

Les fichiers suivants ont été **supprimés** car obsolètes :

| Fichier | Raison |
|---------|--------|
| `create_cluster.sh` | ❌ Redondant - fonctionnalité intégrée dans `test_config_*workers.sh` |
| `create_cluster_manual.sh` | ❌ Script de debug optionnel, non utilisé |
| `run_experiments.sh` | ❌ Remplacé par les 3 scripts `test_config_*workers.sh` |
| `PageRank 2025-2026.docx` | ❌ Version Word du PDF, non nécessaire |
| `PageRank 2025-2026.odt` | ❌ Version LibreOffice du PDF, non nécessaire |

---

## 📝 Fichiers à Modifier AVANT Exécution

**⚠️ CRITIQUE:** Modifier `PROJECT_ID` dans **7 fichiers** :

1. ✅ `setup_gcp.sh` - Ligne 4
2. ✅ `data/download_data.sh` - Ligne 4
3. ✅ `scripts/test_config_2workers.sh` - Ligne 4
4. ✅ `scripts/test_config_4workers.sh` - Ligne 4
5. ✅ `scripts/test_config_6workers.sh` - Ligne 4
6. ✅ `scripts/compile_results.sh` - Ligne 4
7. ✅ `scripts/cleanup.sh` - Ligne 4

**Vérification rapide:**
```bash
grep -n "votre-project-id" *.sh data/*.sh scripts/*.sh
# Si cette commande retourne des résultats, vous avez oublié de modifier !
```

---

## 🎯 Résultats Générés

Après exécution, la structure suivante sera créée automatiquement :

```
results/
├── config_2workers/
│   ├── comparison.csv              # CSV avec tous les résultats
│   ├── rdd_10pct.log
│   ├── rdd_100pct.log
│   ├── dataframe_10pct.log
│   └── dataframe_100pct.log
│
├── config_4workers/
│   └── (idem)
│
├── config_6workers/
│   └── (idem)
│
├── graphs/
│   ├── execution_time_comparison.png
│   ├── speedup_comparison.png
│   └── scalability_analysis.png
│
├── all_results.csv                 # Agrégation de tous les CSV
└── *.log                           # Logs d'exécution
```

---

## 💰 Optimisations Coûts (95% d'économie)

| Optimisation | Impact |
|--------------|--------|
| Machines préemptibles | -80% |
| Type e2-standard-4 (au lieu de n1) | -30% |
| max-idle: 60s (suppression rapide) | -90% |
| Tests en parallèle (3 membres) | Durée : 1h au lieu de 3h |
| **Coût total** | **~8€** au lieu de 150€ |

---

## 📚 Documentation par Type

### Guides d'Utilisation
- `README.md` - Guide principal (EN)
- `DEMARRAGE_RAPIDE.md` - Démarrage rapide (FR)
- `QUICKSTART.md` - Quickstart (EN)
- `INSTRUCTIONS.md` - Instructions détaillées (FR)

### Référence Technique
- `INDEX.md` - Index de tous les fichiers
- `CONTENU.md` - Description détaillée de chaque fichier
- `OPTIMISATIONS.md` - Optimisations techniques et coûts
- `scripts/README.md` - Documentation des scripts

### Suivi et Validation
- `CHECKLIST.md` - Liste de vérification avant exécution
- `RECAPITULATIF.md` - Vue d'ensemble du projet
- `CHANGELOG.md` - Historique des modifications
- `GUIDE_RAPPORT.md` - Guide pour le rapport final

### Analyse
- `results/performance_analysis.md` - Modèle d'analyse des résultats
- `results/README.md` - Guide des résultats

---

## 🚀 Workflow Recommandé (3 membres)

### Jour 1 - Préparation (1h)
- Membre 1: Configuration GCP + téléchargement données
- Membres 2 & 3: Lecture de la documentation

### Jour 2 - Exécution (1h)
- **EN PARALLÈLE:**
  - Membre 1: `test_config_2workers.sh` (40-60 min)
  - Membre 2: `test_config_4workers.sh` (40-60 min)
  - Membre 3: `test_config_6workers.sh` (40-60 min)

### Jour 3 - Analyse (3h)
- Membre 1: `compile_results.sh` + vérification graphiques
- Membres 2 & 3: Analyse des résultats
- Tous: Rédaction du rapport

### Jour 4 - Finalisation (2h)
- Relecture et validation
- Nettoyage GCP (`cleanup.sh`)
- Rendu final

---

## ⚡ Commandes Rapides

```bash
# Vérifier la structure
tree -L 2

# Compter les fichiers
find . -type f -not -path "./.git/*" | wc -l

# Rechercher un mot dans tous les fichiers
grep -r "TERME" --include="*.md" --include="*.sh" --include="*.py"

# Vérifier les PROJECT_ID
grep -n "votre-project-id" *.sh data/*.sh scripts/*.sh

# Lister tous les scripts
ls -lh scripts/*.sh

# Voir la taille du projet
du -sh .
```

---

## 📞 Support

- **Documentation complète:** `README.md`
- **Démarrage rapide:** `DEMARRAGE_RAPIDE.md`
- **Problèmes fréquents:** `INSTRUCTIONS.md` (section Dépannage)
- **Validation:** `CHECKLIST.md`

---

**Dernière mise à jour:** Janvier 2025  
**Auteur:** Projet PageRank M2  
**Version:** 2.0 (Optimisée et nettoyée)
