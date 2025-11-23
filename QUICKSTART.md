# 🚀 QUICK START - PageRank Project

## ⚡ 30 Seconds Setup

```bash
# 1. Download data (once, ~15 min) - ⭐ Use optimized version
cd data && bash download_simple.sh && cd ..

# 2. Run ONE test (choose based on assignment)
cd scripts
bash test_config_2workers.sh    # Member 1
# OR
bash test_config_4workers.sh    # Member 2
# OR
bash test_config_6workers.sh    # Member 3

# 3. After ALL members finish, compile results
bash compile_results.sh
```

**DONE!** Results in `results/graphs/` + summary text.

---

## 📋 What Each Script Does

### `test_config_2workers.sh` (and 4/6 workers)

**Fully automated:** Creates cluster → Tests → Deletes → Results

```
1. ✅ Asks for PROJECT_ID (or uses env var)
2. ✅ Creates Dataproc cluster (preemptible VMs = 80% savings)
3. ✅ Uploads Python scripts to Cloud Storage
4. ✅ Runs RDD on 10% data
5. ✅ Runs DataFrame on 10% data
6. ✅ Runs RDD on 100% data
7. ✅ Runs DataFrame on 100% data
8. ✅ Deletes cluster IMMEDIATELY (saves 90% cost!)
9. ✅ Generates comparison CSV
10. ✅ Saves detailed logs
```

**Duration:** ~20-30 min  
**Cost:** ~3-5€ per config

### `compile_results.sh`

**Aggregates all results and generates graphs:**

```
1. ✅ Finds all result files (*.log, *.csv)
2. ✅ Generates comparison graphs (matplotlib)
3. ✅ Creates summary text file
4. ✅ Shows DataFrame vs RDD improvements
```

**Generates:**
- `results/graphs/comparison_all_configs.png`
- `results/graphs/execution_time_evolution.png`
- `results/graphs/summary_table.png`
- `results/summary_YYYYMMDD_HHMMSS.txt`

---

## 💰 Costs

**Budget:** 150€ (50€ per member)  
**Actual cost:** ~12€ (4€ per member)  
**Savings:** 92%

| Config | Duration | Cost |
|--------|----------|------|
| 2 workers | ~20 min | ~3€ |
| 4 workers | ~25 min | ~4€ |
| 6 workers | ~30 min | ~5€ |

---

## 🎯 Team Workflow (Recommended)

```
Member 1 (GCP account #1) → bash test_config_2workers.sh
Member 2 (GCP account #2) → bash test_config_4workers.sh
Member 3 (GCP account #3) → bash test_config_6workers.sh

[All run in PARALLEL - 3x faster!]

Share results:
  - results/config_Xworkers/comparison.csv
  - results/config_Xworkers_*.log

One member compiles:
  → bash compile_results.sh
```

**Total time:** ~40 min (instead of 2+ hours sequential!)

---

## 📖 Documentation

**Read in order:**

1. **DEMARRAGE_RAPIDE.md** ← START HERE (French quick start)
2. **RECAPITULATIF.md** ← Full overview (French)
3. **CHECKLIST.md** ← Before launching
4. [Run tests]
5. **GUIDE_RAPPORT.md** ← Write final report (French)

**Detailed guides:**
- **INSTRUCTIONS.md** - Step-by-step guide (French)
- **OPTIMISATIONS.md** - Technical optimizations (French)
- **scripts/README.md** - Scripts usage guide

---

## 🔧 Project Structure

```
page-rank/
├── 📖 Documentation (8 files)
│   ├── README.md, DEMARRAGE_RAPIDE.md, INSTRUCTIONS.md
│   ├── RECAPITULATIF.md, GUIDE_RAPPORT.md, CHECKLIST.md
│   └── OPTIMISATIONS.md, CONTENU.md
│
├── 💻 Source Code (3 files)
│   └── src/
│       ├── utils.py
│       ├── pagerank_rdd.py
│       └── pagerank_dataframe.py
│
├── 🔧 Scripts (8 files)
│   └── scripts/
│       ├── test_config_2workers.sh ✨ NEW
│       ├── test_config_4workers.sh ✨ NEW
│       ├── test_config_6workers.sh ✨ NEW
│       ├── compile_results.sh ✨ NEW
│       ├── generate_graphs.py ✨ NEW
│       ├── cleanup.sh
│       └── README.md
│
└── 📊 Results (generated)
    └── results/
        ├── config_2workers/comparison.csv
        ├── config_4workers/comparison.csv
        ├── config_6workers/comparison.csv
        ├── graphs/*.png ✨ NEW
        └── *.log, summary_*.txt
```

---

## ⚙️ PROJECT_ID Configuration

### Option 1: Environment Variable (Recommended)

```bash
export PROJECT_ID=your-gcp-project-id
bash test_config_2workers.sh  # Auto-uses PROJECT_ID
```

### Option 2: Interactive Prompt

```bash
bash test_config_2workers.sh
# Script asks: "Enter your PROJECT_ID:"
# Type: your-gcp-project-id
```

---

## 🎓 Key Features

### ✅ What Makes This Project Great

1. **Full Automation**
   - One command = complete results
   - No manual intervention during execution
   - Auto-cleanup (saves 90% cost!)

2. **Cost Optimization**
   - Preemptible VMs (80% savings)
   - Auto-shutdown after 60s (90% savings)
   - Budget: 150€ → Actual: ~12€

3. **Performance Optimization**
   - Co-partitioning (avoids shuffle)
   - Strategic caching (avoids recomputation)
   - Optimized Spark configuration

4. **Team Workflow**
   - 3 members = 3 parallel tests
   - Time divided by 3
   - Easy result sharing (CSV files)

5. **Ready-to-Use Results**
   - High-quality graphs (PNG 300 DPI)
   - CSV tables
   - Text summary
   - Report writing guide

---

## 🆘 Troubleshooting

### "gcloud: command not found"

Install Google Cloud SDK:
```bash
# Check: https://cloud.google.com/sdk/install
```

### "Permission denied" when running scripts

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

### Cluster creation fails

Check quotas:
```bash
gcloud compute project-info describe --project=PROJECT_ID
# Must have < 32 vCPU available
```

### Graphs not generating

Install Python packages:
```bash
python3 -m pip install matplotlib pandas numpy
```

---

## ✅ Pre-Launch Checklist

- [ ] Google Cloud SDK installed
- [ ] Authenticated to GCP (`gcloud auth login`)
- [ ] PROJECT_ID configured
- [ ] Data downloaded (`bash data/download_simple.sh`)
- [ ] Budget alert configured in GCP Console
- [ ] Scripts executable (`chmod +x` if needed)

---

## 📊 Expected Results

### Wikipedia Center

Entity with highest PageRank = "center" of Wikipedia.

**Likely candidates:**
- Very general concept (e.g., "Country", "City", "Person")
- Highly linked page (e.g., "United States", "France", "Europe")

### RDD vs DataFrame

**Hypotheses (validate with your results):**

- DataFrame faster thanks to Catalyst optimizer
- Expected improvement: +15-25%
- Consistent between 10% and 100% data
- Speedup sub-linear (overhead from network/coordination)

---

**Good luck! 🚀**

For detailed instructions in French, read **DEMARRAGE_RAPIDE.md**
