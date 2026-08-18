---
title: Multi-Degree Campus Placement Data Analytics
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.32.0"
app_file: app.py
pinned: false
---

# Multi-Degree Campus Placement Analytics & Driver Analysis

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![SQLite3](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Library-Pandas-150458.svg)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Visualization-Seaborn-informational.svg)](https://seaborn.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow)](https://huggingface.co/spaces/KavyaThakar/campus-placement-analytics)

An end-to-end multi-degree campus placement analytics portfolio project examining candidate records across **B.Tech, M.Tech, MCA, BCA, Pharmacy (B.Pharm, M.Pharm), MBA, BBA, B.Sc, and B.Com**. The project extracts actionable recruitment insights into placement success, salary packages, work experience leverage, and academic score impacts using Python, SQLite, advanced analytical SQL (CTEs, Window Functions), Seaborn visual analytics, and an interactive Streamlit dashboard.

---

## 📌 Executive Summary

Analysing 475 candidate records across Technical, Computer Applications, Pharmacy, Management, and Basic Science disciplines:

### Key Cross-Disciplinary Findings

1. **Technical & Master's Degrees Lead Package Valuations**
   - **M.Tech** and **MCA** graduates achieved top-tier salary packages, averaging **₹8.2L+** and **₹6.6L+** respectively.
   - **B.Tech** candidates demonstrated high placement demand, averaging **~₹6.8L** packages across Computer Science, IT, and Engineering branches.
   - **M.Pharm** and **B.Pharm** candidates secured specialized industry roles with robust placement stability (~75%+ placement rate).

2. **Prior Work Experience & Internships Drive Recruitment Success**
   - Candidates with prior work experience or industry internships achieved a **~65.9% placement rate**, compared to **~16.0%** for candidates without.
   - Industry exposure boosts placement probability by **+49.9 percentage points**.

3. **Foundational Academic Consistency Trumps Final Score Alone**
   - Recruiters evaluate cumulative academic history (10th, 12th, and aptitude test performance) alongside final degree percentages.

---

## 📊 Visual Highlights

- **`charts/placement_rate_by_degree.png`**: Placement Rate comparison across B.Tech, M.Tech, MCA, BCA, Pharmacy, MBA, and BBA.
- **`charts/placement_rate_by_specialisation.png`**: Placement Rate across top branches and specializations.
- **`charts/placement_rate_by_workex.png`**: Impact of work experience and internships on recruitment rates.
- **`charts/salary_distribution_placed.png`**: Package distribution across placed candidates.
- **`charts/avg_salary_by_spec_gender.png`**: Salary breakdown by degree field and gender.
- **`charts/academic_correlation_heatmap.png`**: Pearson correlation matrix across academic performance metrics.

---

## 🗂️ Dataset Schema (`placement_raw.csv`)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `student_id` | Integer | Unique candidate identifier |
| `gender` | Text | Gender (`M` / `F`) |
| `ssc_p` | Float | 10th (Secondary School) percentage |
| `ssc_b` | Text | 10th Board of Education (`Central` / `Others`) |
| `hsc_p` | Float | 12th (Higher Secondary) percentage |
| `hsc_b` | Text | 12th Board of Education (`Central` / `Others`) |
| `hsc_s` | Text | 12th Specialization stream (`Science` / `Commerce` / `Arts`) |
| `degree_p` | Float | Undergraduate / Bachelor Degree percentage |
| `degree_t` | Text | Degree Course (`B.Tech` / `M.Tech` / `MCA` / `BCA` / `B.Pharm` / `M.Pharm` / `MBA` / `BBA` / `B.Sc`) |
| `workex` | Text | Prior work experience / Internship (`Yes` / `No`) |
| `etest_p` | Float | Employability / Aptitude test percentage |
| `specialisation` | Text | Branch / Specialization (`Computer Science`, `IT`, `Pharmaceutics`, `Mkt&Fin`, `Data Science`, etc.) |
| `mba_p` | Float | Final Degree / Post-Graduation percentage score |
| `status` | Text | Placement Status (`Placed` / `Not Placed`) |
| `salary` | Float | Annual salary package in INR (*NULL for unplaced candidates*) |
| `Placed_Flag` | Integer | Binary target flag (`1` = Placed, `0` = Not Placed) |

---

## 🏗️ Project Architecture

```
campus-placement-analytics/
├── placement_raw.csv            # Raw multi-degree dataset (475 rows)
├── 01_clean_data.py             # Preprocessing & binary target creation
├── placement_clean.csv          # Cleaned multi-degree dataset
├── 02_load_sql.py               # SQLite database setup & multi-index creation
├── placement.db                 # SQLite database
├── queries.sql                  # 10 analytical SQL queries
├── 03_run_queries.py            # SQL query executor & insights.json exporter
├── insights.json                # Structured JSON query results
├── 04_visualize.py              # Publication-quality chart generator
├── charts/                      # Generated visualization PNGs
│   ├── placement_rate_by_degree.png
│   ├── placement_rate_by_specialisation.png
│   ├── placement_rate_by_workex.png
│   ├── salary_distribution_placed.png
│   ├── avg_salary_by_spec_gender.png
│   ├── academic_scores_placed_vs_unplaced.png
│   └── academic_correlation_heatmap.png
├── app.py                       # Live Streamlit Interactive Web Dashboard
├── index.html                   # Web Report & Portfolio Showcase
└── README.md                    # Project documentation
```

---

## 🛠️ Advanced SQL & Analytics Techniques

1. **Window Functions (`RANK() OVER`)**:
   - Ranks candidates by score partitioned by degree program (`PARTITION BY degree_t ORDER BY mba_p DESC`).
2. **Common Table Expressions (CTEs)**:
   - Aggregates academic scores in `AcademicAverages` CTE across placed vs unplaced cohorts.
3. **Database Multi-Indexing**:
   - Explicit indexes on `status`, `degree_t`, and `specialisation` columns for high-speed SQLite queries.
4. **Conditional Aggregation (`SUM(Placed_Flag)`)**:
   - Dynamic placement percentage computation across degree streams.

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- Required packages: `pandas`, `matplotlib`, `seaborn`, `plotly`, `streamlit`

```bash
pip install pandas matplotlib seaborn plotly streamlit
```

### Sequential Pipeline Execution

```bash
# 1. Clean data and generate placement_clean.csv
py 01_clean_data.py

# 2. Ingest cleaned data into SQLite database placement.db
py 02_load_sql.py

# 3. Run analytical SQL queries and export insights.json
py 03_run_queries.py

# 4. Generate high-resolution PNG charts in charts/
py 04_visualize.py

# 5. Launch interactive Streamlit Web Dashboard
py -m streamlit run app.py
```
