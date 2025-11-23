# 📊 Analyse de Performance PageRank - Détaillée

**Date de l'expérience:** [À COMPLÉTER]  
**Membres du groupe:** [NOM 1, NOM 2, NOM 3]  
**Cours:** Large Scale Data Management - Pascal Molli  
**Année:** 2025-2026

---

## 🎯 Objectif de l'Expérience

Comparer les performances de deux implémentations PySpark pour le calcul du PageRank :
- **RDD (Resilient Distributed Datasets)** - API bas niveau
- **DataFrame** - API haut niveau avec Catalyst optimizer

## 📊 Résultats Finaux

### 🏆 Centre de Wikipedia

**Page avec le plus grand PageRank:** `[À COMPLÉTER APRÈS EXÉCUTION]`

**Valeur du PageRank:** `[À COMPLÉTER]`

**Interprétation:** Cette page représente le "centre" de Wikipedia, c'est-à-dire la page la plus importante selon l'algorithme PageRank, qui prend en compte non seulement le nombre de liens entrants mais aussi l'importance des pages qui pointent vers elle.

---

## 📈 Résultats Détaillés

### Configuration 1: 2 Workers (12 vCPU total)

#### Test avec 10% des données

| Métrique | RDD | DataFrame | Différence | Gagnant |
|----------|-----|-----------|------------|---------|
| Temps d'exécution (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps par itération (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Pages analysées | [X] | [X] | - | - |
| Temps de chargement (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps des itérations (sec) | [X] | [X] | [X]% | [RDD/DF] |

#### Test avec 100% des données

| Métrique | RDD | DataFrame | Différence | Gagnant |
|----------|-----|-----------|------------|---------|
| Temps d'exécution (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps par itération (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Pages analysées | [X] | [X] | - | - |
| Temps de chargement (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps des itérations (sec) | [X] | [X] | [X]% | [RDD/DF] |

**Observations:**
- [À COMPLÉTER]

---

### Configuration 2: 4 Workers (20 vCPU total)

#### Test avec 10% des données

| Métrique | RDD | DataFrame | Différence | Gagnant |
|----------|-----|-----------|------------|---------|
| Temps d'exécution (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps par itération (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Pages analysées | [X] | [X] | - | - |
| Temps de chargement (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps des itérations (sec) | [X] | [X] | [X]% | [RDD/DF] |

#### Test avec 100% des données

| Métrique | RDD | DataFrame | Différence | Gagnant |
|----------|-----|-----------|------------|---------|
| Temps d'exécution (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps par itération (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Pages analysées | [X] | [X] | - | - |
| Temps de chargement (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps des itérations (sec) | [X] | [X] | [X]% | [RDD/DF] |

**Observations:**
- [À COMPLÉTER]

---

### Configuration 3: 6 Workers (28 vCPU total)

#### Test avec 10% des données

| Métrique | RDD | DataFrame | Différence | Gagnant |
|----------|-----|-----------|------------|---------|
| Temps d'exécution (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps par itération (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Pages analysées | [X] | [X] | - | - |
| Temps de chargement (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps des itérations (sec) | [X] | [X] | [X]% | [RDD/DF] |

#### Test avec 100% des données

| Métrique | RDD | DataFrame | Différence | Gagnant |
|----------|-----|-----------|------------|---------|
| Temps d'exécution (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps par itération (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Pages analysées | [X] | [X] | - | - |
| Temps de chargement (sec) | [X] | [X] | [X]% | [RDD/DF] |
| Temps des itérations (sec) | [X] | [X] | [X]% | [RDD/DF] |

**Observations:**
- [À COMPLÉTER]

---

## 📊 Analyse Comparative

### Graphique de Speedup

```
[INSÉRER ICI UN GRAPHIQUE MONTRANT:]
- Axe X: Nombre de workers (2, 4, 6)
- Axe Y: Temps d'exécution (secondes)
- Deux courbes: RDD et DataFrame
```

### Speedup vs Configuration

| Configuration | Speedup RDD (vs 2 workers) | Speedup DF (vs 2 workers) |
|---------------|---------------------------|--------------------------|
| 2 workers     | 1.00x (baseline)          | 1.00x (baseline)         |
| 4 workers     | [X]x                      | [X]x                     |
| 6 workers     | [X]x                      | [X]x                     |

**Speedup théorique vs observé:**
- Théorique (2→4 workers): 2.00x
- Observé RDD: [X]x
- Observé DataFrame: [X]x

---

## 🔍 Analyse Approfondie

### 1. Partitionnement des Données

**Stratégie implémentée:**
- Partitionnement par clé (source) avec 200 partitions
- Co-partitionnement des RDDs (liens et rangs)
- Cache stratégique des données statiques

**Impact du partitionnement:**
- ✅ Shuffle évité lors des joins
- ✅ Données co-localisées sur les mêmes workers
- ✅ [À COMPLÉTER: pourcentage d'amélioration observé]

**Référence:** Article NSDI sur l'optimisation du shuffle

### 2. Convergence de l'Algorithme

**Paramètres:**
- Nombre d'itérations: 10
- Facteur de damping: 0.85
- Critère d'arrêt: Nombre fixe d'itérations

**Observations:**
- Convergence atteinte à l'itération: [À COMPLÉTER]
- Stabilité des résultats: [OUI/NON]
- Variation du PageRank entre dernières itérations: [X]%

### 3. Scalabilité Horizontale

**Question:** Le speedup est-il linéaire avec l'ajout de workers ?

**Hypothèse initiale:**
- Speedup sous-linéaire attendu en raison de:
  - Overhead de communication réseau
  - Temps de setup et coordination
  - Partie séquentielle (loi d'Amdahl)
  - Coût du partitionnement

**Résultats observés:**

Pour RDD:
- 2→4 workers: speedup de [X]x (théorique: 2.00x) → [sous/sur-linéaire]
- 4→6 workers: speedup de [X]x (théorique: 1.50x) → [sous/sur-linéaire]

Pour DataFrame:
- 2→4 workers: speedup de [X]x (théorique: 2.00x) → [sous/sur-linéaire]
- 4→6 workers: speedup de [X]x (théorique: 1.50x) → [sous/sur-linéaire]

**Efficacité parallèle:**
- Avec 6 workers: [X]% (100% = linéaire parfait)

### 4. Bottlenecks Identifiés

**Analyse des logs:**

1. **Chargement des données:**
   - Temps: [X]% du temps total
   - Impact: [FAIBLE/MOYEN/ÉLEVÉ]

2. **Parsing TTL:**
   - Temps: [X]% du temps total
   - Impact: [FAIBLE/MOYEN/ÉLEVÉ]

3. **Itérations PageRank:**
   - Temps: [X]% du temps total
   - Impact: [FAIBLE/MOYEN/ÉLEVÉ]

4. **Sauvegarde des résultats:**
   - Temps: [X]% du temps total
   - Impact: [FAIBLE/MOYEN/ÉLEVÉ]

**Bottleneck principal:** [À IDENTIFIER]

---

## 🎓 Conclusions

### RDD vs DataFrame

**Gagnant global:** [RDD / DataFrame / Ex-aequo]

**Points forts de RDD:**
- [À COMPLÉTER]
- Exemple: Contrôle bas niveau, optimisations manuelles

**Points forts de DataFrame:**
- [À COMPLÉTER]
- Exemple: Catalyst optimizer, API déclarative

**Cas d'usage recommandés:**
- **Utiliser RDD quand:** [À COMPLÉTER]
- **Utiliser DataFrame quand:** [À COMPLÉTER]

### Impact de la Scalabilité

**Observations principales:**
1. [À COMPLÉTER]
2. [À COMPLÉTER]
3. [À COMPLÉTER]

**Configuration optimale pour ce workload:**
- Nombre de workers recommandé: [X]
- Justification: [À COMPLÉTER]

### Optimisations Appliquées et Impact

| Optimisation | Impact Mesuré | Validation |
|--------------|---------------|------------|
| Co-partitionnement | [X]% | ✅/❌ |
| Cache des liens | [X]% | ✅/❌ |
| Adaptive Query Execution (DF) | [X]% | ✅/❌ |
| Machines préemptibles | 80% économie coût | ✅ |

### Recommandations pour Production

1. **Configuration matérielle:**
   - [À COMPLÉTER]

2. **Optimisations code:**
   - [À COMPLÉTER]

3. **Gestion des coûts:**
   - [À COMPLÉTER]

---

## 💰 Analyse des Coûts

### Coûts Réels Observés

| Configuration | Durée réelle | Coût estimé (préemptible) | Coût si non-préemptible |
|---------------|--------------|--------------------------|-------------------------|
| 2 workers     | [X] min      | ~$[X]                    | ~$[X]                   |
| 4 workers     | [X] min      | ~$[X]                    | ~$[X]                   |
| 6 workers     | [X] min      | ~$[X]                    | ~$[X]                   |
| **TOTAL**     | [X] h        | **~$[X]**                | **~$[X]**               |

**Économies réalisées grâce aux optimisations:**
- Machines préemptibles: ~$[X] économisés (80%)
- Arrêt automatique: ~$[X] économisés
- Test progressif (10% avant 100%): ~$[X] économisés

**Budget consommé:** [X]€ / 150€ (par groupe)  
**Budget restant:** [X]€ pour ajustements

---

## 📚 Références et Contexte

### Données Utilisées

- **Source:** DBpedia Wikilinks 2022.12.01
- **URL:** https://databus.dbpedia.org/dbpedia/generic/wikilinks/2022.12.01/
- **Taille compressée:** 1.8 GB
- **Taille décompressée:** ~[X] GB
- **Format:** Turtle (TTL)
- **Nombre de triplets:** ~[X] millions

### Algorithme PageRank

**Formule:**
```
PageRank(p) = (1 - d) + d × Σ(PageRank(in) / outlinks(in))
```

Où:
- `d` = facteur de damping (0.85)
- `in` = pages pointant vers p
- `outlinks(in)` = nombre de liens sortants de la page "in"

**Convergence:**
- L'algorithme converge généralement en 10-20 itérations
- Chaque itération affine les scores

### Articles de Référence

1. **PageRank original:** Brin & Page (1998)
2. **Article NSDI:** Optimisation du shuffle dans les systèmes distribués
3. **Spark Documentation:** RDD vs DataFrame performance

---

## 📝 Notes et Observations Supplémentaires

[ESPACE LIBRE POUR VOS OBSERVATIONS]

---

**Dernière mise à jour:** [DATE]
