---
title: Campus Placement Data Analytics
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.32.0"
app_file: app.py
pinned: false
---

# Campus Placement Analytics & Predictive Driver Analysis

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![SQLite3](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Library-Pandas-150458.svg)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Visualization-Seaborn-informational.svg)](https://seaborn.pydata.org/)

An end-to-end data analytics portfolio project examining 215 campus recruitment records. The project extracts actionable insights into what drives student placement success and salary offers using Python, SQLite, advanced analytical SQL (CTEs, Window Functions), and Seaborn visual analytics.

---

## 📌 Executive Summary

Out of **215 MBA candidates**, **148 (68.84%)** secured campus placement offers, while **67 (31.16%)** remained unplaced. Salary offers for placed candidates averaged **₹291,015**, ranging from a minimum of **₹200,000** to a peak of **₹940,000**.

### Key Empirical Findings

1. **Prior Work Experience is the #1 Placement Booster**
   - Candidates with prior work experience achieved an **86.49% placement rate** compared to **59.57%** for those without.
   - Having work experience increases placement probability by **+26.92 percentage points**.

2. **Marketing & Finance Outperforms Marketing & HR**
   - **Mkt&Fin** specialisation recorded a **79.17% placement rate** and an average salary of **₹298,853**.
   - **Mkt&HR** specialisation recorded a **55.79% placement rate** and an average salary of **₹270,377**.
   - Specialising in Finance yielded a **+23.38% higher placement rate** and **+10.53% higher average compensation**.

3. **Early Academic History (10th/12th) Out-predicts MBA Scores**
   - **10th Grade (`ssc_p`)**: Placed average = **71.72%** vs Unplaced = **57.54%** ($\Delta = \mathbf{+14.18\%}$).
   - **12th Grade (`hsc_p`)**: Placed average = **69.93%** vs Unplaced = **58.40%** ($\Delta = \mathbf{+11.53\%}$).
   - **Undergraduate (`degree_p`)**: Placed average = **68.74%** vs Unplaced = **61.13%** ($\Delta = \mathbf{+7.61\%}$).
   - **MBA (`mba_p`)**: Placed average = **62.58%** vs Unplaced = **61.61%** ($\Delta = \mathbf{+0.97\%}$).
   - *Takeaway*: Recruiters rely heavily on foundational academic consistency over post-graduate scores.

---

## 📊 Visual Highlights

- **`charts/academic_scores_placed_vs_unplaced.png`**: Key comparison chart showing academic score trajectories across secondary, higher secondary, undergraduate, and MBA levels.
- **`charts/placement_rate_by_workex.png`**: Impact of work experience on recruitment rates.
- **`charts/placement_rate_by_specialisation.png`**: Placement rates across MBA specialisations.
- **`charts/salary_distribution_placed.png`**: Histogram & KDE distribution of accepted salary offers.
- **`charts/avg_salary_by_spec_gender.png`**: Gender and specialisation compensation breakdown.
- **`charts/academic_correlation_heatmap.png`**: Pearson correlation matrix across academic performance metrics.

---

## 🗂️ Dataset Schema (`placement_raw.csv`)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `student_id` | Integer | Unique student identifier (renamed from `sl_no`) |
| `gender` | Text | Gender (`M` / `F`) |
| `ssc_p` | Float | 10th (Secondary School) percentage |
| `ssc_b` | Text | 10th Board of Education (`Central` / `Others`) |
| `hsc_p` | Float | 12th (Higher Secondary) percentage |
| `hsc_b` | Text | 12th Board of Education (`Central` / `Others`) |
| `hsc_s` | Text | 12th Specialization stream (`Commerce` / `Science` / `Arts`) |
| `degree_p` | Float | Undergraduate Degree percentage |
| `degree_t` | Text | Undergrad field (`Comm&Mgmt` / `Sci&Tech` / `Others`) |
| `workex` | Text | Prior work experience (`Yes` / `No`) |
| `etest_p` | Float | Employability test percentage |
| `specialisation` | Text | MBA Specialisation (`Mkt&Fin` / `Mkt&HR`) |
| `mba_p` | Float | MBA Percentage score |
| `status` | Text | Placement Status (`Placed` / `Not Placed`) |
| `salary` | Float | Annual salary offer in INR (*NULL for unplaced students by design*) |
| `Placed_Flag` | Integer | Binary target flag (`1` = Placed, `0` = Not Placed) |

---

## 🏗️ Project Architecture

```
campus-placement-analytics/
├── placement_raw.csv            # Original raw dataset (215 rows)
├── 01_clean_data.py             # Data cleaning & binary flag creation
├── placement_clean.csv          # Preprocessed dataset
├── 02_load_sql.py               # SQLite DB setup & table indexing
├── placement.db                 # SQLite database storage
├── queries.sql                  # 10 analytical SQL queries
├── 03_run_queries.py            # SQL executor & insights.json exporter
├── insights.json                # Structured JSON query results
├── 04_visualize.py              # Chart generator script
├── charts/                      # Generated visualization PNGs (6 charts)
│   ├── placement_rate_by_specialisation.png
│   ├── placement_rate_by_workex.png
│   ├── salary_distribution_placed.png
│   ├── avg_salary_by_spec_gender.png
│   ├── academic_scores_placed_vs_unplaced.png
│   └── academic_correlation_heatmap.png
├── README.md                    # Project documentation
└── .gitignore                   # Standard Python gitignore
```

---

## 🛠️ Advanced SQL Techniques Demonstrated

1. **Window Functions (`RANK() OVER`)**:
   - Ranks candidates by MBA performance (`mba_p`) partitioned by specialisation (`Mkt&Fin` vs `Mkt&HR`) to evaluate top-tier candidates within peer groups.
2. **Common Table Expressions (CTEs)**:
   - Encapsulates score aggregation logic in `AcademicAverages` CTE to cleanly evaluate mean scores across 5 academic stages for placed vs unplaced cohorts.
3. **Database Indexing**:
   - Explicit `CREATE INDEX idx_status ON students(status)` for optimal filtered query lookup performance.
4. **Conditional Aggregation (`SUM(Placed_Flag)`)**:
   - Computes dynamic placement percentages without unnecessary subqueries.

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- Required packages: `pandas`, `matplotlib`, `seaborn`

```bash
pip install pandas matplotlib seaborn
```

### Sequential Execution

Execute the scripts in order:

```bash
# 1. Clean data and generate placement_clean.csv
python 01_clean_data.py

# 2. Ingest cleaned data into SQLite database placement.db
python 02_load_sql.py

# 3. Run all analytical SQL queries and export insights.json
python 03_run_queries.py

# 4. Generate high-resolution PNG charts in charts/
python 04_visualize.py
```
