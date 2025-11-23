# Résultats PageRank

Ce dossier contient tous les résultats générés par les tests PageRank.

---

## 📁 Structure Après Exécution

```
results/
├── config_2workers/
│   └── comparison.csv              # Résultats configuration 2 workers
│
├── config_4workers/
│   └── comparison.csv              # Résultats configuration 4 workers
│
├── config_6workers/
│   └── comparison.csv              # Résultats configuration 6 workers
│
├── graphs/
│   ├── comparison_all_configs.png      # Graphique comparatif complet
│   ├── execution_time_evolution.png    # Évolution temps d'exécution
│   └── summary_table.png               # Tableau récapitulatif
│
├── config_2workers_YYYYMMDD_HHMMSS.log # Log détaillé 2 workers
├── config_4workers_YYYYMMDD_HHMMSS.log # Log détaillé 4 workers
├── config_6workers_YYYYMMDD_HHMMSS.log # Log détaillé 6 workers
│
├── summary_YYYYMMDD_HHMMSS.txt         # Récapitulatif consolidé texte
│
└── performance_analysis.md             # Template d'analyse (à compléter)
```

---

## 📊 Fichiers Générés

### CSV de Comparaison

**Emplacement :** `config_Xworkers/comparison.csv`

**Format :**
```csv
Type,Dataset,Time_seconds,Time_formatted
RDD,10%,245,4m 5s
DataFrame,10%,198,3m 18s
RDD,100%,1823,30m 23s
DataFrame,100%,1456,24m 16s
```

**Utilisation :**
- Importer dans Excel/Google Sheets
- Créer tableaux pour rapport
- Calculer statistiques personnalisées

### Logs Détaillés

**Emplacement :** `config_Xworkers_YYYYMMDD_HHMMSS.log`

**Contenu :**
- Timestamps de toutes les opérations
- Commandes gcloud exécutées
- Outputs complets des jobs Spark
- Temps d'exécution de chaque étape
- Top 10 entités PageRank
- Récapitulatif final

**Utilisation :**
- Debugging en cas d'erreur
- Validation des résultats
- Extraction données détaillées
- Documentation méthodologie

### Graphiques PNG

**Emplacement :** `graphs/*.png`

**Résolution :** 300 DPI (haute qualité pour rapport)

#### 1. `comparison_all_configs.png`

Contient 4 sous-graphiques :
- **Top-left:** RDD vs DataFrame sur 10% données
- **Top-right:** RDD vs DataFrame sur 100% données
- **Bottom-left:** Speedup avec augmentation workers
- **Bottom-right:** Amélioration DataFrame vs RDD (%)

#### 2. `execution_time_evolution.png`

Graphique linéaire montrant :
- Évolution temps selon nombre de workers
- Lignes séparées : RDD 10%, DF 10%, RDD 100%, DF 100%
- Tendances de scalabilité

#### 3. `summary_table.png`

Tableau formaté avec :
- Configuration (2/4/6 workers)
- Temps RDD et DataFrame (10% et 100%)
- Amélioration en pourcentage
- Cellules colorées (vert = amélioration, rouge = régression)

**Utilisation :**
- Insérer directement dans rapport Word/PDF
- Présentation PowerPoint
- Documentation visuelle

### Récapitulatif Texte

**Emplacement :** `summary_YYYYMMDD_HHMMSS.txt`

**Contenu :**
- Configurations testées
- Extraits des récapitulatifs de chaque configuration
- Liste des graphiques générés
- Timestamp de génération

**Utilisation :**
- Vue d'ensemble rapide
- Vérification résultats
- Référence textuelle

---

## 🔄 Comment Générer les Résultats

### Méthode Automatique (Recommandée)

```bash
# Chaque membre lance SON test
cd scripts
bash test_config_2workers.sh    # Membre 1
bash test_config_4workers.sh    # Membre 2
bash test_config_6workers.sh    # Membre 3

# Un membre compile tous les résultats
bash compile_results.sh
```

Les fichiers sont automatiquement générés dans `results/`.

### Vérifier les Résultats

```bash
# Lister tous les fichiers générés
ls -lh results/

# Voir CSV d'une configuration
cat results/config_2workers/comparison.csv

# Voir récapitulatif d'un log
grep -A 20 "RÉCAPITULATIF" results/config_2workers_*.log

# Ouvrir graphiques (selon OS)
# Windows
start results/graphs/comparison_all_configs.png

# Mac
open results/graphs/comparison_all_configs.png

# Linux
xdg-open results/graphs/comparison_all_configs.png
```

---

## 📈 Analyser les Résultats

### Comparaison RDD vs DataFrame

**Questions à se poser :**

1. **Quelle approche est plus rapide ?**
   ```bash
   # Extraire temps d'exécution
   awk -F, 'NR>1 {print $1, $2, $3}' results/config_*/comparison.csv
   ```

2. **L'amélioration est-elle cohérente ?**
   - Comparer 10% vs 100%
   - Comparer 2 vs 4 vs 6 workers

3. **Quel est le gain moyen ?**
   ```python
   # Calculer amélioration moyenne
   import pandas as pd
   
   df = pd.read_csv('results/config_2workers/comparison.csv')
   for dataset in ['10%', '100%']:
       rdd = df[(df['Type']=='RDD') & (df['Dataset']==dataset)]['Time_seconds'].values[0]
       dframe = df[(df['Type']=='DataFrame') & (df['Dataset']==dataset)]['Time_seconds'].values[0]
       improvement = (rdd - dframe) / rdd * 100
       print(f"{dataset}: {improvement:.1f}% improvement")
   ```

### Analyse de Scalabilité

**Calculer le speedup :**

$$
Speedup(n) = \frac{T_{2workers}}{T_{n workers}}
$$

**Exemple :**
```python
import pandas as pd

# Charger tous les CSV
df2 = pd.read_csv('results/config_2workers/comparison.csv')
df4 = pd.read_csv('results/config_4workers/comparison.csv')
df6 = pd.read_csv('results/config_6workers/comparison.csv')

# Temps RDD sur 100%
t2 = df2[(df2['Type']=='RDD') & (df2['Dataset']=='100%')]['Time_seconds'].values[0]
t4 = df4[(df4['Type']=='RDD') & (df4['Dataset']=='100%')]['Time_seconds'].values[0]
t6 = df6[(df6['Type']=='RDD') & (df6['Dataset']=='100%')]['Time_seconds'].values[0]

# Speedup
speedup_4 = t2 / t4
speedup_6 = t2 / t6

print(f"Speedup 4 workers: {speedup_4:.2f}x (idéal: 2.0x)")
print(f"Speedup 6 workers: {speedup_6:.2f}x (idéal: 3.0x)")

# Efficacité parallèle
efficiency_4 = (speedup_4 / 2.0) * 100
efficiency_6 = (speedup_6 / 3.0) * 100

print(f"Efficacité 4 workers: {efficiency_4:.1f}%")
print(f"Efficacité 6 workers: {efficiency_6:.1f}%")
```

### Identifier le Centre de Wikipedia

**Extraire depuis les logs :**

```bash
# Chercher le top PageRank dans les logs
grep -A 1 "Top 10 entités par PageRank:" results/config_*workers_*.log | head -5

# OU chercher directement dans les outputs Spark
grep -A 15 "=== TOP 10 ENTITÉS ===" results/config_*workers_*.log
```

**Le centre de Wikipedia est l'entité avec le plus grand PageRank.**

---

## 📝 Utiliser pour le Rapport

### Tableaux de Résultats

**Copier depuis les CSV :**

| Configuration | Dataset | RDD (s) | DataFrame (s) | Gagnant | Amélioration |
|---------------|---------|---------|---------------|---------|--------------|
| 2 workers     | 10%     | [CSV]   | [CSV]         | ?       | Calculer     |
| 2 workers     | 100%    | [CSV]   | [CSV]         | ?       | Calculer     |
| ...           | ...     | ...     | ...           | ...     | ...          |

### Graphiques

**Insérer les PNG depuis `results/graphs/` :**

1. **Figure 1:** Comparaison RDD vs DataFrame (`comparison_all_configs.png`)
2. **Figure 2:** Évolution temps d'exécution (`execution_time_evolution.png`)
3. **Figure 3:** Tableau récapitulatif (`summary_table.png`)

**Légendes suggérées :**

- "Figure 1: Comparaison des performances RDD vs DataFrame pour toutes les configurations testées. Les graphiques montrent (a) temps d'exécution sur 10% données, (b) temps sur 100% données, (c) speedup selon nombre de workers, (d) amélioration DataFrame vs RDD en pourcentage."

- "Figure 2: Évolution du temps d'exécution selon le nombre de workers. Les lignes continues représentent les tests sur 10% des données, les lignes pointillées sur 100%. Rouge = RDD, Bleu = DataFrame."

- "Figure 3: Tableau récapitulatif des résultats. Les cellules vertes indiquent une amélioration DataFrame vs RDD, les cellules rouges une régression (peu probable avec optimisations appliquées)."

### Extraits de Logs

**Pour méthodologie :**

```bash
# Copier configuration Spark utilisée
grep -A 5 "Configuration Spark" results/config_2workers_*.log
```

**Pour validation :**

```bash
# Copier messages de succès
grep "SUCCESS" results/config_*workers_*.log
```

---

## 🎯 Interprétation des Résultats

### Si DataFrame est Plus Rapide (Attendu)

**Raisons probables :**
- Catalyst optimizer optimise le plan d'exécution
- Tungsten engine gère mieux la mémoire
- Optimisations automatiques (predicate pushdown, column pruning)

**Dans le rapport :**
> "Les résultats montrent que l'API DataFrame est systématiquement plus rapide 
> que l'API RDD, avec une amélioration moyenne de X%. Cette différence s'explique 
> principalement par les optimisations automatiques du Catalyst optimizer et 
> l'utilisation du Tungsten engine pour la gestion mémoire."

### Si RDD est Compétitif (Possible)

**Raisons probables :**
- Co-partitionnement manuel très efficace
- Cache bien placé
- Overhead Catalyst compensé par contrôle fin

**Dans le rapport :**
> "Bien que DataFrame bénéficie d'optimisations automatiques, l'API RDD avec 
> co-partitionnement manuel atteint des performances comparables, démontrant 
> l'importance d'une bonne compréhension du partitionnement Spark."

### Si Speedup est Sous-Linéaire (Attendu)

**Raisons probables :**
- Overhead de communication réseau
- Coordination entre workers
- Partie séquentielle de l'algorithme (Loi d'Amdahl)

**Dans le rapport :**
> "Le speedup observé est sous-linéaire (1.Xx pour 4 workers au lieu de 2.0x idéal), 
> ce qui s'explique par l'overhead de communication réseau et la coordination entre 
> workers. Cependant, l'amélioration reste significative et justifie l'utilisation 
> de configurations multi-workers pour des datasets volumineux."

---

## ✅ Checklist Résultats

**Avant compilation :**
- [ ] Au moins un fichier `config_*workers_*.log` existe
- [ ] Au moins un fichier `config_*/comparison.csv` existe
- [ ] Pas d'erreurs dans les logs

**Après compilation :**
- [ ] 3 fichiers PNG dans `results/graphs/`
- [ ] Fichier `summary_*.txt` créé
- [ ] Graphiques s'ouvrent correctement
- [ ] CSV contiennent données valides

**Pour le rapport :**
- [ ] Tableaux remplis avec données des CSV
- [ ] Graphiques PNG insérés
- [ ] Centre de Wikipedia identifié
- [ ] Interprétation rédigée
- [ ] Speedup calculé et analysé

---

## 🆘 En Cas de Problème

### Fichiers Manquants

**Si `config_*/comparison.csv` manque :**

```bash
# Vérifier que le script test a bien été exécuté
ls -lh results/config_*workers_*.log

# Relancer le script si nécessaire
cd scripts
bash test_config_2workers.sh
```

### Graphiques Non Générés

**Vérifier packages Python :**

```bash
python3 -m pip list | grep -E "(matplotlib|pandas)"

# Installer si manquant
python3 -m pip install matplotlib pandas numpy
```

**Relancer compilation :**

```bash
cd scripts
bash compile_results.sh
```

### Données Incohérentes

**Vérifier logs pour erreurs :**

```bash
grep -i "error\|failed\|exception" results/config_*workers_*.log
```

**Vérifier CSV :**

```bash
# Temps doivent être positifs et cohérents
cat results/config_*/comparison.csv
```

---

## 📚 Références

**Pour aller plus loin :**

- **GUIDE_RAPPORT.md** - Guide complet rédaction rapport
- **OPTIMISATIONS.md** - Détails optimisations techniques
- **README.md** - Vue d'ensemble projet

---

**Bon courage pour l'analyse ! 📊**
