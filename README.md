# PageRank - PySpark Performance Analysis

Comparison of **PySpark DataFrame** vs **PySpark RDD** performance for PageRank calculation on Wikipedia DBpedia data.

---

## 🚀 Quick Start

### Prerequisites
- Google Cloud Platform account with billing enabled
- `gcloud` CLI installed and authenticated
- Budget alert configured (recommended: 50€)

### Setup (One-time)

```bash
# 1. Configure GCP project
gcloud config set project YOUR-PROJECT-ID

# 2. Run setup script
bash setup_gcp.sh

# 3. Download and upload data (~15 min)
cd data && bash download_simple.sh && cd ..
```

### Run Tests (Parallel Execution)

Each team member tests a different configuration:

```bash
cd scripts

# Member 1 - 2 workers
bash test_config_2workers.sh

# Member 2 - 4 workers  
bash test_config_4workers.sh

# Member 3 - 6 workers
bash test_config_6workers.sh
```

### Compile Results

After all tests complete:

```bash
cd scripts
bash compile_results.sh
```

Results will be in `results/` directory with CSV files and summary.

---

## 📊 Results

### Wikipedia Center (Highest PageRank)

**Entity:** `[TO BE COMPLETED]`  
**PageRank Score:** `[TO BE COMPLETED]`

### Performance Comparison (100% Data)

| Configuration | RDD (sec) | DataFrame (sec) | Winner | Improvement |
|---------------|-----------|-----------------|--------|-------------|
| 2 workers     | -         | -               | -      | -           |
| 4 workers     | -         | -               | -      | -           |
| 6 workers     | -         | -               | -      | -           |

---

## 🛠️ Technical Details

### Hardware Configuration

- **Machine type:** `e2-standard-4` (4 vCPU, 16 GB RAM)
- **Region:** `europe-west1` (Belgium)
- **Preemptible VMs:** No (using regular workers for stability)
- **Auto-shutdown:** 10 minutes idle

| Configuration | Master  | Workers | Total vCPU | Quota Check |
|---------------|---------|---------|------------|-------------|
| 2 workers     | 4 vCPU  | 2×4     | 12 vCPU    | ✅ < 32     |
| 4 workers     | 4 vCPU  | 4×4     | 20 vCPU    | ✅ < 32     |
| 6 workers     | 4 vCPU  | 6×4     | 28 vCPU    | ✅ < 32     |

### Data

- **Source:** DBpedia Wikilinks 2022.12.01
- **Size:** 1.8 GB compressed (.bz2), ~11 GB uncompressed
- **Lines:** ~180 million triples
- **Format:** TTL (Turtle RDF)

### Optimizations

#### RDD Implementation
- Co-partitioning to avoid shuffle
- Strategic caching of immutable data
- Custom partitioner for consistent key distribution
- Kryo serialization

#### DataFrame Implementation
- Repartitioning by key
- Adaptive Query Execution (AQE)
- Catalyst optimizer
- Skew join handling

### Spark Configuration

```python
num_partitions = 200
damping_factor = 0.85
iterations = 10

# Both implementations use:
spark.sql.shuffle.partitions = 200
spark.default.parallelism = 200
spark.sql.adaptive.enabled = true
spark.serializer = KryoSerializer
```

---

## 💰 Cost Optimization

### Per Test Run (~20-30 min)
- Cluster uptime: ~30 min
- Cost: ~3-5€ per configuration
- Total for 3 configs: ~15€

### Cost Saving Features
- ✅ Auto-shutdown after 10 min idle
- ✅ Immediate cluster deletion after tests
- ✅ e2-standard-4 (cheaper than n1/n2)
- ✅ Compressed data in GCS (.bz2 format)
- ✅ Efficient spark configuration (200 partitions)

### Budget Monitoring

```bash
# Check costs
gcloud billing accounts list
gcloud alpha billing budgets list --billing-account=ACCOUNT-ID

# List all clusters
gcloud dataproc clusters list --region=europe-west1

# Delete orphaned clusters
bash scripts/cleanup.sh
```

---

## 📁 Project Structure

```
page-rank/
├── README.md                 # This file
├── setup_gcp.sh             # GCP initial setup
├── requirements.txt         # Python dependencies
├── data/
│   └── download_simple.sh   # Download Wikipedia data
├── src/
│   ├── pagerank_rdd.py      # RDD implementation
│   ├── pagerank_dataframe.py # DataFrame implementation
│   └── utils.py             # Shared utilities
├── scripts/
│   ├── test_config_2workers.sh  # Test with 2 workers
│   ├── test_config_4workers.sh  # Test with 4 workers
│   ├── test_config_6workers.sh  # Test with 6 workers
│   ├── compile_results.sh       # Aggregate results
│   ├── generate_graphs.py       # Generate visualizations
│   └── cleanup.sh               # Clean up resources
└── results/
    └── config_*workers/         # Results per configuration
```

---

## 🔧 Configuration Guide

### Before Running ANY Script

**CRITICAL:** Edit `PROJECT_ID` in these files:

1. `setup_gcp.sh`
2. `data/download_simple.sh`
3. `scripts/test_config_2workers.sh` (and 4/6 workers)
4. `scripts/compile_results.sh`
5. `scripts/cleanup.sh`

Change from:
```bash
PROJECT_ID="votre-project-id"
```

To your actual project ID:
```bash
PROJECT_ID="your-actual-project-id"
```

### Test Script Workflow

Each `test_config_*workers.sh` script:

1. ✅ Creates Dataproc cluster
2. ✅ Uploads Python scripts to GCS
3. ✅ Runs RDD on 100% data
4. ✅ Runs DataFrame on 100% data
5. ✅ Generates comparison CSV
6. ✅ Deletes cluster immediately

**Output files:**
- `results/config_Xworkers/summary.txt` - Execution summary
- `results/config_Xworkers/comparison.csv` - Performance data
- `results/config_Xworkers/rdd_full.log` - RDD detailed log
- `results/config_Xworkers/df_full.log` - DataFrame detailed log

---

## 📈 Analysis

### Key Metrics to Compare

1. **Execution time** - Total runtime for 10 iterations
2. **Scalability** - Speedup with more workers
3. **Stability** - Variance across runs
4. **Resource usage** - CPU, memory, shuffle

### Expected Observations

- DataFrame typically faster due to Catalyst optimization
- Linear or near-linear scaling with workers (2→4→6)
- RDD more predictable, DataFrame more optimized
- Shuffle operations dominate execution time

### Generate Graphs

```bash
cd scripts
python generate_graphs.py
```

Creates:
- `results/graphs/comparison_bar.png` - Side-by-side comparison
- `results/graphs/scalability.png` - Speedup by workers
- `results/graphs/improvement.png` - RDD vs DataFrame %

---

## 🧹 Cleanup

### After Testing

```bash
# Check for running clusters
gcloud dataproc clusters list --region=europe-west1

# Delete specific cluster
gcloud dataproc clusters delete CLUSTER-NAME --region=europe-west1

# Or use cleanup script
bash scripts/cleanup.sh
```

### Complete Cleanup

To remove all GCP resources:

```bash
# Delete bucket (WARNING: irreversible!)
gsutil -m rm -r gs://YOUR-PROJECT-ID-pagerank-data

# Disable APIs (optional)
gcloud services disable dataproc.googleapis.com
gcloud services disable storage.googleapis.com
```

---

## 🐛 Troubleshooting

### Common Issues

**Quota exceeded:**
```
Solution 1: Request quota increase to 32 vCPUs in GCP Console
  - Go to: https://console.cloud.google.com/iam-admin/quotas
  - Filter: "CPUs (all regions)"
  - Request increase to 32 or 40 vCPUs

Solution 2: Use only 2 workers configuration (requires 12 vCPUs)
Solution 3: Use smaller machine type (e2-standard-2 instead of e2-standard-4)
```

**Permission denied:**
```bash
# Fix: Enable required APIs
gcloud services enable dataproc.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable compute.googleapis.com
```

**Cluster creation fails:**
```
Check:
1. Correct PROJECT_ID in scripts
2. Billing enabled
3. APIs activated
4. Quota available (gcloud compute regions describe europe-west1)
```

**Out of memory:**
```
Increase num_partitions in Python files (200 → 400)
Or use larger machines (e2-standard-4 → e2-standard-8)
```

### Logs and Debugging

```bash
# View cluster logs
gcloud dataproc jobs list --region=europe-west1 --cluster=CLUSTER-NAME

# Check specific job
gcloud dataproc jobs describe JOB-ID --region=europe-west1

# View detailed logs
gsutil cat gs://YOUR-BUCKET/google-cloud-dataproc-metainfo/*/jobs/*/driveroutput
```

---

## 📚 Implementation Details

### PageRank Algorithm

```python
# Initialization
rank(p) = 1.0 for all pages p

# Iterations (10 times)
for i in 1 to 10:
    contributions(p) = rank(p) / outlinks(p)
    rank(p) = (1 - damping) + damping * Σ(contributions from incoming links)
    
# Where damping = 0.85
```

### RDD Key Operations

```python
# 1. Parse data
links = sc.textFile(input).map(parse_ttl).filter(lambda x: x is not None)

# 2. Group by source (with partitioning)
links = links.groupByKey().mapValues(list).partitionBy(num_partitions).cache()

# 3. Initialize ranks (same partitioning)
ranks = links.map(lambda x: (x[0], 1.0)).partitionBy(num_partitions)

# 4. Iterate
for iteration in range(10):
    # Join avoids shuffle (same partitioning)
    contributions = links.join(ranks).flatMap(calculate_contributions)
    ranks = contributions.reduceByKey(add).mapValues(apply_damping).partitionBy(num_partitions)
```

### DataFrame Key Operations

```python
# 1. Parse data
df_links = spark.createDataFrame(rdd.map(parse_ttl), ["source", "destination"])

# 2. Group and repartition
df_links = df_links.groupBy("source").agg(collect_list("destination")).repartition(num_partitions, "source").cache()

# 3. Initialize ranks
df_ranks = df_links.select("source").distinct().withColumn("rank", lit(1.0)).repartition(num_partitions, "source")

# 4. Iterate
for iteration in range(10):
    # Catalyst optimizes this join
    df_contributions = df_links.join(df_ranks, "source").select(explode(...))
    df_ranks = df_contributions.groupBy("destination").agg(sum("contribution")).select(apply_damping(...))
```

---

## 📝 License

MIT License - See LICENSE file

## 👥 Contributors

[Your Names Here]

## 📧 Contact

For questions or issues, open a GitHub issue or contact [your-email@example.com]

---

**Last Updated:** December 5, 2025
