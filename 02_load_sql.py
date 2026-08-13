"""
02_load_sql.py
Campus Placement Analytics - Step 2: Database Ingestion & Indexing

This script loads the cleaned dataset into a local SQLite database (placement.db)
under the 'students' table and creates a database index on the 'status' column.
"""

import sqlite3
import pandas as pd

def load_sql():
    csv_path = 'placement_clean.csv'
    db_path = 'placement.db'
    table_name = 'students'
    
    print("=" * 60)
    print("STEP 2: SQLITE DATABASE INGESTION")
    print("=" * 60)
    
    # 1. Read Cleaned Data
    print(f"Reading cleaned dataset from '{csv_path}'...")
    df = pd.read_csv(csv_path)
    
    # 2. Connect to SQLite Database
    print(f"Connecting to SQLite database at '{db_path}'...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 3. Write Data to 'students' Table
    df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
    print(f"Loaded {len(df)} records into table '{table_name}'.")
    
    # 4. Create Index on 'status' Column
    print("Creating index on 'status' column for performance...")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_status ON {table_name}(status);")
    conn.commit()
    
    # 5. Verify Table and Index
    cursor.execute(f"SELECT count(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='students';")
    indices = [row[0] for row in cursor.fetchall()]
    
    print(f"Database Verification:")
    print(f"  - Total rows in '{table_name}': {row_count}")
    print(f"  - Active indices on '{table_name}': {', '.join(indices)}")
    
    conn.close()
    print("\nDatabase ingestion step completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    load_sql()
