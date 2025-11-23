# 📊 Guide de Rédaction du Rapport Final

Ce document vous guide pour rédiger votre rapport final à partir des résultats obtenus.

---

## 📋 Structure Recommandée du Rapport

### 1. Introduction (1 page)

#### 1.1 Contexte
- PageRank : algorithme de classement des pages web développé par Google
- Importance dans le traitement de graphes à grande échelle
- Cas d'usage : moteurs de recherche, réseaux sociaux, analyse de citations

#### 1.2 Objectifs du Projet
- Comparer les performances de **PySpark RDD** vs **PySpark DataFrame**
- Analyser la scalabilité avec différentes configurations (2, 4, 6 workers)
- Identifier le "centre de Wikipedia" (entité avec le plus grand PageRank)
- Optimiser les coûts sur Google Cloud Platform

#### 1.3 Jeu de Données
- **Source :** Wikipedia DBpedia wikilinks
- **Taille :** 1.8 GB compressé (~8 GB décompressé)
- **Format :** Turtle (TTL) - triplets RDF
- **Contenu :** Liens entre articles Wikipedia

---

### 2. Méthodologie (2-3 pages)

#### 2.1 Architecture Technique

**Infrastructure :**
```
┌─────────────────────────────────────────────────┐
│          Google Cloud Platform (GCP)            │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐        ┌─────────────────┐   │
│  │   Dataproc   │◄──────►│ Cloud Storage   │   │
│  │   Clusters   │        │   (Buckets)     │   │
│  └──────────────┘        └─────────────────┘   │
│                                                 │
│  Configurations testées:                        │
│  • 2 workers (1 master + 2 workers)             │
│  • 4 workers (1 master + 4 workers)             │
│  • 6 workers (1 master + 6 workers)             │
│                                                 │
│  Machine type: n1-standard-4                    │
│  • 4 vCPU par nœud                              │
│  • 15 GB RAM par nœud                           │
│  • VMs préemptibles (80% économie)              │
└─────────────────────────────────────────────────┘
```

**Spark Configuration :**
- Version : Apache Spark 3.5.0
- Partitions : 200 (optimisé pour éviter shuffle)
- Adaptive Query Execution : Activé (DataFrame)
- Cache : Activé sur graphe de liens

#### 2.2 Algorithme PageRank

**Formule mathématique :**

$$
PR(p) = \frac{1-d}{N} + d \sum_{i \in M(p)} \frac{PR(i)}{L(i)}
$$

Où :
- $PR(p)$ = PageRank de la page $p$
- $d$ = facteur d'amortissement (damping factor) = 0.85
- $N$ = nombre total de pages
- $M(p)$ = ensemble des pages pointant vers $p$
- $L(i)$ = nombre de liens sortants de la page $i$

**Paramètres utilisés :**
- Damping factor : 0.85 (standard académique)
- Nombre d'itérations : 10 (convergence généralement atteinte)
- Initialisation : $PR(p) = 1.0$ pour chaque page

**Pseudo-code :**
```python
# Initialisation
for each page p:
    PageRank[p] = 1.0

# Itérations
for iteration in range(10):
    # Calculer les contributions
    for each page p with outlinks L:
        contribution = PageRank[p] / len(L)
        for each destination d in L:
            contributions[d] += contribution
    
    # Mise à jour PageRank
    for each page p:
        PageRank[p] = 0.15 + 0.85 * contributions[p]
```

#### 2.3 Implémentations

**A. RDD (Resilient Distributed Dataset)**

Caractéristiques :
- API bas niveau (map, reduce, join)
- Contrôle fin du partitionnement
- Optimisation manuelle requise

Optimisations appliquées :
```python
# Co-partitionnement pour éviter shuffle
liens = liens_bruts.partitionBy(200, "source").cache()
rangs = rangs.partitionBy(200, "source")

# Lors du join, les données sont déjà co-localisées
# → PAS de shuffle réseau (très coûteux)
```

**B. DataFrame (API SQL)**

Caractéristiques :
- API haut niveau (SQL-like)
- Catalyst optimizer (optimisations automatiques)
- Tungsten engine (gestion mémoire optimisée)

Optimisations automatiques :
- Predicate pushdown
- Column pruning
- Adaptive query execution

```python
# Repartitionnement et cache
df_liens = df_liens.repartition(200, "source").cache()

# Catalyst optimizer analyse le plan et optimise automatiquement
```

#### 2.4 Optimisations de Coûts

**Stratégies appliquées :**

| Optimisation | Description | Économie |
|--------------|-------------|----------|
| VMs préemptibles | Instances interruptibles à bas coût | 80% |
| Arrêt auto (60s) | Suppression immédiate après job | ~90% |
| Région europe-west1 | Région optimisée pour coûts | 10-15% |
| Test progressif | 10% → 100% (validation avant full) | Évite gaspillage |
| Cache intelligent | Évite recalcul des données statiques | 30-40% temps |

**Coût final estimé :** 10-15€ (au lieu de 150€ budget)

---

### 3. Résultats (3-4 pages)

#### 3.1 Résultats Bruts

**Insérez ici les tableaux générés automatiquement :**

```bash
# Copiez depuis results/graphs/summary_table.png
```

**Tableau de synthèse (exemple à remplir) :**

| Configuration | Dataset | RDD (s) | DataFrame (s) | Gagnant | Amélioration |
|---------------|---------|---------|---------------|---------|--------------|
| 2 workers     | 10%     | XXX     | XXX           | ?       | +X.X%        |
| 2 workers     | 100%    | XXX     | XXX           | ?       | +X.X%        |
| 4 workers     | 10%     | XXX     | XXX           | ?       | +X.X%        |
| 4 workers     | 100%    | XXX     | XXX           | ?       | +X.X%        |
| 6 workers     | 10%     | XXX     | XXX           | ?       | +X.X%        |
| 6 workers     | 100%    | XXX     | XXX           | ?       | +X.X%        |

#### 3.2 Graphiques de Comparaison

**Insérez les graphiques PNG depuis `results/graphs/` :**

1. **`comparison_all_configs.png`**
   - Comparaison RDD vs DataFrame par configuration
   - Speedup avec augmentation des workers
   - Amélioration DataFrame vs RDD

2. **`execution_time_evolution.png`**
   - Évolution temps d'exécution selon configuration
   - Lignes 10% vs 100% données
   - Tendances RDD vs DataFrame

#### 3.3 Centre de Wikipedia

**Entité avec le plus grand PageRank :**

```
Entité : [COPIER DEPUIS LES LOGS]
URI : [COPIER L'URI COMPLÈTE]
PageRank final : [VALEUR]

Explication : 
Cette entité est au "centre" de Wikipedia car elle reçoit
le plus grand nombre de liens entrants pondérés.
```

**Top 10 entités :**

| Rang | Entité | PageRank | Interprétation |
|------|--------|----------|----------------|
| 1    | XXX    | X.XXXX   | Centre principal |
| 2    | XXX    | X.XXXX   | Hub important |
| 3    | XXX    | X.XXXX   | ... |
| ...  | ...    | ...      | ... |

#### 3.4 Analyse de Scalabilité

**Speedup observé :**

Calculez le speedup : $S(n) = \frac{T_2}{T_n}$ où $T_2$ = temps avec 2 workers

**Exemple :**
- Speedup 4 workers : $S(4) = T_2 / T_4 = XXX / XXX = X.XX$
- Speedup 6 workers : $S(6) = T_2 / T_6 = XXX / XXX = X.XX$
- Speedup idéal : 2.0 pour 4 workers, 3.0 pour 6 workers

**Efficacité parallèle :**

$$E(n) = \frac{S(n)}{n/2} \times 100\%$$

---

### 4. Discussion (2-3 pages)

#### 4.1 RDD vs DataFrame

**Questions à aborder :**

1. **Quelle approche est plus rapide ? Pourquoi ?**
   - Analysez les résultats obtenus
   - Expliquez les différences (Catalyst optimizer, Tungsten, etc.)
   - Cas où RDD pourrait être meilleur (contrôle fin)

2. **Impact du Catalyst Optimizer**
   - Optimisations automatiques vs manuelles
   - Plan d'exécution physique

3. **Facilité de développement**
   - Complexité du code RDD vs DataFrame
   - Maintenabilité

**Hypothèses (à valider avec vos résultats) :**

- DataFrame généralement plus rapide (Catalyst + Tungsten)
- RDD peut être compétitif si bien optimisé manuellement
- DataFrame plus facile à développer et maintenir

#### 4.2 Scalabilité

**Questions à aborder :**

1. **Le speedup est-il linéaire ?**
   - Comparez speedup observé vs idéal
   - Identifiez les goulots d'étranglement

2. **Limites de la scalabilité**
   - Overhead de communication réseau
   - Shuffle entre partitions
   - Loi d'Amdahl

3. **Configuration optimale**
   - Meilleur rapport performance/coût
   - Point de rendement décroissant

**Facteurs limitants :**
- Shuffle réseau (même avec co-partitionnement)
- Overhead de coordination entre workers
- Bande passante réseau
- Partie séquentielle de l'algorithme (agrégation finale)

#### 4.3 Optimisations Techniques

**Impact des optimisations appliquées :**

| Optimisation | Impact Performance | Impact Coût |
|--------------|-------------------|-------------|
| Co-partitionnement (200 partitions) | +30-40% | N/A |
| Cache sur liens statiques | +35-45% | N/A |
| VMs préemptibles | N/A | -80% |
| Adaptive Query Execution | +10-20% (DF) | N/A |
| Arrêt automatique 60s | N/A | -90% |

**Lessons learned :**
- Partitionnement critique pour éviter shuffle
- Cache essentiel pour données réutilisées
- Coûts maîtrisables avec bonnes pratiques

#### 4.4 Limitations et Améliorations Futures

**Limitations identifiées :**
1. Critère de convergence fixe (10 itérations)
   - Amélioration : vérifier convergence réelle (seuil epsilon)
2. Dataset unique (Wikipedia)
   - Amélioration : tester sur autres graphes (réseaux sociaux, citations)
3. Configurations limitées
   - Amélioration : tester 8, 10, 12 workers

**Améliorations possibles :**
- Implémenter PageRank personnalisé (topic-sensitive)
- Tester GraphX (API Spark pour graphes)
- Comparer avec GraphFrames
- Implémenter checkpointing pour convergence

---

### 5. Conclusion (1 page)

**Points clés à résumer :**

1. **Résultat principal**
   - Quelle approche gagne ? Dans quelles conditions ?
   - Centre de Wikipedia identifié

2. **Scalabilité**
   - Comment le système scale avec plus de workers ?
   - Configuration optimale identifiée

3. **Optimisations**
   - Impact des optimisations sur performance et coût
   - Budget respecté (150€ → ~10-15€)

4. **Apprentissages**
   - Différences RDD vs DataFrame
   - Importance du partitionnement
   - Trade-offs performance/coût

5. **Perspectives**
   - Applications futures de PageRank
   - Extensions possibles du projet

**Phrase de conclusion (exemple) :**

> "Ce projet a démontré que l'API DataFrame de PySpark offre généralement 
> de meilleures performances que l'API RDD grâce aux optimisations automatiques 
> du Catalyst optimizer, tout en restant plus facile à développer et maintenir. 
> Cependant, l'optimisation manuelle du partitionnement reste cruciale dans 
> les deux cas pour éviter les coûteux shuffle réseau. Nous avons également 
> montré qu'une gestion rigoureuse des ressources cloud permet de réaliser 
> des analyses à grande échelle tout en respectant un budget limité."

---

## 📊 Checklist Avant Soumission

### Contenu du Rapport

- [ ] Introduction claire avec contexte et objectifs
- [ ] Méthodologie détaillée (architecture, algorithme, optimisations)
- [ ] Résultats complets (tableaux + graphiques)
- [ ] Discussion approfondie (RDD vs DataFrame, scalabilité)
- [ ] Conclusion synthétique
- [ ] Références bibliographiques

### Éléments Graphiques

- [ ] Tous les graphiques PNG insérés depuis `results/graphs/`
- [ ] Légendes claires pour chaque graphique
- [ ] Tableaux formatés proprement
- [ ] Schémas d'architecture (si nécessaire)

### Analyse Technique

- [ ] Comparaison RDD vs DataFrame argumentée
- [ ] Analyse de scalabilité avec calculs de speedup
- [ ] Impact des optimisations quantifié
- [ ] Centre de Wikipedia identifié et expliqué

### Code et Résultats

- [ ] Code source clair et commenté (déjà fait dans le projet)
- [ ] Logs d'exécution sauvegardés
- [ ] CSV de comparaison vérifiés
- [ ] Budget final documenté

---

## 💡 Conseils de Rédaction

### Style

- **Objectif :** Clair, concis, technique mais accessible
- **Temps :** Passé composé pour méthodologie, présent pour résultats
- **Voix :** Passive pour méthodologie ("Les données ont été traitées..."), 
            active pour analyse ("Nous observons que...")

### Figures et Tableaux

- Toujours **référencer** dans le texte : "Comme le montre la Figure 1..."
- **Légendes auto-suffisantes** : lecteur doit comprendre sans lire le texte
- **Unités** : toujours indiquer (secondes, pourcentage, etc.)

### Erreurs à Éviter

- ❌ Présenter résultats sans analyse
- ❌ Graphiques sans légende
- ❌ Affirmations sans preuves
- ❌ Comparaisons sans contexte
- ❌ Oublier de mentionner les limitations

### Bonnes Pratiques

- ✅ Chaque affirmation appuyée par des données
- ✅ Graphiques clairs et lisibles
- ✅ Discussion approfondie des résultats
- ✅ Limitations honnêtement exposées
- ✅ Code reproductible documenté

---

## 📚 Références Suggérées

### Articles Académiques

1. **Page, L., Brin, S., Motwani, R., & Winograd, T. (1999).** 
   *The PageRank Citation Ranking: Bringing Order to the Web.* 
   Stanford InfoLab Technical Report.

2. **Zaharia, M., Chowdhury, M., Franklin, M. J., Shenker, S., & Stoica, I. (2010).** 
   *Spark: Cluster Computing with Working Sets.* 
   HotCloud 2010.

3. **Armbrust, M., Xin, R. S., Lian, C., et al. (2015).** 
   *Spark SQL: Relational Data Processing in Spark.* 
   SIGMOD 2015.

### Documentation Technique

4. **Apache Spark Documentation** 
   https://spark.apache.org/docs/latest/

5. **Google Cloud Dataproc Documentation** 
   https://cloud.google.com/dataproc/docs

6. **PySpark API Reference** 
   https://spark.apache.org/docs/latest/api/python/

---

## 🎓 Exemple de Section Complétée

### Exemple : Section 3.1 Résultats Bruts (avec données fictives)

**Tableau 1 : Temps d'exécution RDD vs DataFrame**

| Configuration | Dataset | RDD (s) | DataFrame (s) | Gagnant | Amélioration |
|---------------|---------|---------|---------------|---------|--------------|
| 2 workers     | 10%     | 245     | 198           | DF      | +19.2%       |
| 2 workers     | 100%    | 1823    | 1456          | DF      | +20.1%       |
| 4 workers     | 10%     | 142     | 108           | DF      | +23.9%       |
| 4 workers     | 100%    | 1047    | 798           | DF      | +23.8%       |
| 6 workers     | 10%     | 98      | 76            | DF      | +22.4%       |
| 6 workers     | 100%    | 728     | 564           | DF      | +22.5%       |

**Observations principales :**

Les résultats montrent que l'approche **DataFrame est systématiquement plus 
rapide** que l'approche RDD, avec une amélioration moyenne de **22.0%** 
sur l'ensemble des configurations testées.

Cette amélioration est **cohérente** entre les tests sur 10% et 100% des 
données, suggérant que les optimisations du Catalyst optimizer sont 
efficaces indépendamment de la taille du dataset.

L'amélioration semble légèrement plus importante avec 4 workers (23.8-23.9%), 
ce qui pourrait indiquer un meilleur équilibre entre parallélisme et overhead 
pour cette configuration.

---

**Utilisez ce guide pour structurer votre rapport final !** 📝
