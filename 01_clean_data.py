"""
01_clean_data.py
Campus Placement Analytics - Step 1: Data Cleaning & Preprocessing

This script loads raw campus placement data, performs data quality checks
(nulls and duplicates), renames key identifiers, creates derived flags,
and outputs a clean CSV ready for SQL loading and analysis.
"""

import pandas as pd

def clean_data():
    raw_path = 'placement_raw.csv'
    clean_path = 'placement_clean.csv'
    
    print("=" * 60)
    print("STEP 1: DATA CLEANING & PREPROCESSING")
    print("=" * 60)
    
    # 1. Load Dataset
    print(f"Loading raw dataset from '{raw_path}'...")
    df = pd.read_csv(raw_path)
    print(f"Initial Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
    
    # 2. Rename Columns
    df = df.rename(columns={'sl_no': 'student_id'})
    print("Renamed column 'sl_no' -> 'student_id'.")
    
    # 3. Check Duplicates
    duplicate_count = df.duplicated().sum()
    print(f"Duplicate Rows Count: {duplicate_count}")
    
    # 4. Check Missing / Null Values
    print("\nMissing Values Summary:")
    null_summary = df.isnull().sum()
    print(null_summary[null_summary > 0] if null_summary.sum() > 0 else "No missing values found.")
    
    # Explicit Note on Salary Nulls by Design
    unplaced_count = (df['status'] == 'Not Placed').sum()
    salary_null_count = df['salary'].isnull().sum()
    print("\n" + "-" * 60)
    print(f"NOTE: 'salary' is missing for exactly {salary_null_count} rows.")
    print(f"Total 'Not Placed' students: {unplaced_count}.")
    print("DESIGN DECISION: Salary is null for unplaced students by design.")
    print("No rows are dropped and salary is not imputed (remains NULL).")
    print("-" * 60 + "\n")
    
    # 5. Add Placed_Flag Column (1 for Placed, 0 for Not Placed)
    df['Placed_Flag'] = (df['status'] == 'Placed').astype(int)
    print("Added binary target feature 'Placed_Flag' (1 = Placed, 0 = Not Placed).")
    
    # 6. Save Clean Dataset
    df.to_csv(clean_path, index=False)
    print(f"Clean dataset successfully saved to '{clean_path}'.\n")
    print("Data cleaning step completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    clean_data()
