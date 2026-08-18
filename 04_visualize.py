"""
04_visualize.py
Multi-Degree Campus Placement Analytics - Step 4: Publication-Quality Visualizations

This script reads placement_clean.csv and generates 6 high-resolution PNG charts
covering B.Tech, M.Tech, MCA, BCA, Pharmacy, MBA, BBA, B.Sc candidate analytics.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set global style aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

def create_visualizations():
    csv_path = 'placement_clean.csv'
    charts_dir = 'charts'
    os.makedirs(charts_dir, exist_ok=True)
    
    print("=" * 60)
    print("STEP 4: GENERATING MULTI-DEGREE DATA VISUALIZATIONS")
    print("=" * 60)
    print(f"Reading cleaned data from '{csv_path}'...")
    df = pd.read_csv(csv_path)
    
    status_palette = {"Placed": "#2ca02c", "Not Placed": "#d62728"}
    
    # -------------------------------------------------------------------------
    # Chart 1: Placement Rate by Degree Field
    # -------------------------------------------------------------------------
    print("Generating Chart 1: Placement Rate by Degree Field...")
    plt.figure(figsize=(9, 5))
    degree_summary = df.groupby('degree_t')['Placed_Flag'].mean().reset_index()
    degree_summary['Placement_Rate'] = degree_summary['Placed_Flag'] * 100
    degree_summary = degree_summary.sort_values(by='Placement_Rate', ascending=False)
    
    ax = sns.barplot(
        data=degree_summary, 
        x='degree_t', 
        y='Placement_Rate', 
        palette="viridis"
    )
    plt.title('Placement Rate by Degree Field (B.Tech, M.Tech, MCA, BCA, Pharmacy, MBA)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Degree Program', fontsize=11, fontweight='bold')
    plt.ylabel('Placement Rate (%)', fontsize=11, fontweight='bold')
    plt.ylim(0, 100)
    
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.1f}%',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold',
                    xytext=(0, 5), textcoords='offset points')
                    
    plt.tight_layout()
    chart1_degree_path = os.path.join(charts_dir, 'placement_rate_by_degree.png')
    plt.savefig(chart1_degree_path, dpi=300)
    plt.close()
    print(f" Saved: {chart1_degree_path}")

    # Also update placement_rate_by_specialisation.png for compatibility
    print("Generating Chart 1b: Placement Rate by Specialisation...")
    plt.figure(figsize=(12, 6))
    spec_summary = df.groupby('specialisation')['Placed_Flag'].mean().reset_index()
    spec_summary['Placement_Rate'] = spec_summary['Placed_Flag'] * 100
    spec_summary = spec_summary.sort_values(by='Placement_Rate', ascending=False)
    
    ax = sns.barplot(
        data=spec_summary, 
        x='specialisation', 
        y='Placement_Rate', 
        palette="crest"
    )
    plt.title('Placement Rate by Branch & Specialisation', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Branch / Specialisation', fontsize=11, fontweight='bold')
    plt.ylabel('Placement Rate (%)', fontsize=11, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 100)
    
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.0f}%',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom',
                        fontsize=9, fontweight='bold',
                        xytext=(0, 4), textcoords='offset points')
                        
    plt.tight_layout()
    chart1_spec_path = os.path.join(charts_dir, 'placement_rate_by_specialisation.png')
    plt.savefig(chart1_spec_path, dpi=300)
    plt.close()
    print(f" Saved: {chart1_spec_path}")

    # -------------------------------------------------------------------------
    # Chart 2: Placement Rate by Prior Work Experience
    # -------------------------------------------------------------------------
    print("Generating Chart 2: Placement Rate by Work Experience...")
    plt.figure(figsize=(7, 5))
    workex_summary = df.groupby('workex')['Placed_Flag'].mean().reset_index()
    workex_summary['Placement_Rate'] = workex_summary['Placed_Flag'] * 100
    
    ax = sns.barplot(
        data=workex_summary, 
        x='workex', 
        y='Placement_Rate', 
        palette=["#e06666", "#3d85c6"]
    )
    plt.title('Placement Rate by Prior Work Experience / Internship', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Prior Work Experience (Yes / No)', fontsize=11, fontweight='bold')
    plt.ylabel('Placement Rate (%)', fontsize=11, fontweight='bold')
    plt.ylim(0, 100)
    
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.1f}%',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom',
                    fontsize=11, fontweight='bold',
                    xytext=(0, 5), textcoords='offset points')
                    
    plt.tight_layout()
    chart2_path = os.path.join(charts_dir, 'placement_rate_by_workex.png')
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f" Saved: {chart2_path}")

    # -------------------------------------------------------------------------
    # Chart 3: Salary Distribution for Placed Students
    # -------------------------------------------------------------------------
    print("Generating Chart 3: Salary Distribution for Placed Candidates...")
    placed_df = df[df['status'] == 'Placed']
    plt.figure(figsize=(9, 5.5))
    
    ax = sns.histplot(placed_df['salary'], kde=True, color='#2b5c8f', bins=20)
    mean_sal = placed_df['salary'].mean()
    median_sal = placed_df['salary'].median()
    
    plt.axvline(mean_sal, color='#d9534f', linestyle='--', linewidth=2, label=f'Mean Salary: ₹{mean_sal:,.0f}')
    plt.axvline(median_sal, color='#5cb85c', linestyle='-', linewidth=2, label=f'Median Salary: ₹{median_sal:,.0f}')
    
    plt.title('Salary Offer Package Distribution across All Placed Candidates', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Salary Offer (INR)', fontsize=11, fontweight='bold')
    plt.ylabel('Candidate Count', fontsize=11, fontweight='bold')
    plt.legend(fontsize=11, frameon=True, facecolor='white', edgecolor='#cccccc')
    
    plt.tight_layout()
    chart3_path = os.path.join(charts_dir, 'salary_distribution_placed.png')
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f" Saved: {chart3_path}")

    # -------------------------------------------------------------------------
    # Chart 4: Average Salary by Degree Program and Gender
    # -------------------------------------------------------------------------
    print("Generating Chart 4: Average Salary by Degree Field & Gender...")
    plt.figure(figsize=(10, 5.5))
    sal_degree_gender = placed_df.groupby(['degree_t', 'gender'])['salary'].mean().reset_index()
    
    ax = sns.barplot(
        data=sal_degree_gender, 
        x='degree_t', 
        y='salary', 
        hue='gender', 
        palette=['#3498db', '#e74c3c']
    )
    plt.title('Average Salary Package by Degree Field & Gender', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Degree Program', fontsize=11, fontweight='bold')
    plt.ylabel('Average Salary (INR)', fontsize=11, fontweight='bold')
    plt.legend(title='Gender', frameon=True, facecolor='white')
    
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'₹{height/100000:.1f}L',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom',
                        fontsize=9, fontweight='bold',
                        xytext=(0, 4), textcoords='offset points')
                        
    plt.tight_layout()
    chart4_path = os.path.join(charts_dir, 'avg_salary_by_spec_gender.png')
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f" Saved: {chart4_path}")

    # -------------------------------------------------------------------------
    # Chart 5: Academic Score Comparison (Placed vs Unplaced)
    # -------------------------------------------------------------------------
    print("Generating Chart 5: Academic Score Comparison (Placed vs Not Placed)...")
    plt.figure(figsize=(10, 6))
    
    academic_cols = {'ssc_p': '10th (SSC)', 'hsc_p': '12th (HSC)', 'degree_p': 'Degree %', 'mba_p': 'Final %'}
    score_df = df.groupby('status')[list(academic_cols.keys())].mean().reset_index()
    
    melted = pd.melt(score_df, id_vars=['status'], value_vars=list(academic_cols.keys()),
                     var_name='Stage', value_name='Average_Percentage')
    melted['Stage_Label'] = melted['Stage'].map(academic_cols)
    
    ax = sns.barplot(
        data=melted, 
        x='Stage_Label', 
        y='Average_Percentage', 
        hue='status', 
        palette=status_palette
    )
    
    plt.title('Academic Score Comparison across Education Stages (Placed vs Not Placed)', 
              fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Academic Stage', fontsize=12, fontweight='bold')
    plt.ylabel('Average Percentage Score (%)', fontsize=12, fontweight='bold')
    plt.ylim(0, 100)
    plt.legend(title='Placement Status', frameon=True, facecolor='white', loc='upper right')
    
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.1f}%',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom',
                        fontsize=10, fontweight='bold',
                        xytext=(0, 4), textcoords='offset points')
                        
    plt.tight_layout()
    chart5_path = os.path.join(charts_dir, 'academic_scores_placed_vs_unplaced.png')
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f" Saved: {chart5_path}")

    # -------------------------------------------------------------------------
    # Chart 6: Correlation Heatmap
    # -------------------------------------------------------------------------
    print("Generating Chart 6: Academic Correlation Heatmap...")
    plt.figure(figsize=(8, 6.5))
    
    corr_cols = ['ssc_p', 'hsc_p', 'degree_p', 'etest_p', 'mba_p', 'Placed_Flag']
    corr_matrix = df[corr_cols].corr()
    
    labels = ['10th (SSC)', '12th (HSC)', 'Degree %', 'E-Test %', 'Final %', 'Placed Flag']
    
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt='.2f', 
        cmap='Blues', 
        linewidths=0.8, 
        xticklabels=labels, 
        yticklabels=labels,
        cbar_kws={'label': 'Pearson Correlation'}
    )
    plt.title('Correlation Matrix: Academic Performance & Placement Status', fontsize=14, fontweight='bold', pad=15)
    plt.xticks(rotation=30, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    
    plt.tight_layout()
    chart6_path = os.path.join(charts_dir, 'academic_correlation_heatmap.png')
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print(f" Saved: {chart6_path}")
    
    print("\nMulti-Degree Visualization generation step completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    create_visualizations()
