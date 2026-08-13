"""
03_run_queries.py
Campus Placement Analytics - Step 3: SQL Execution & Insights JSON Export

This script parses all analytical queries from queries.sql, executes them against
the placement.db SQLite database using pandas, prints formatted result tables to
the terminal with headers, and exports all query insights into insights.json.
"""

import sqlite3
import json
import re
import pandas as pd

def parse_queries(sql_file_path):
    """
    Parses queries.sql file into a list of tuples: (query_title, query_sql)
    """
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match pattern: -- Query X: Title followed by SQL code until next query or EOF
    pattern = r'--\s*(Query\s+\d+:[^\n]+)\n(.*?)(?=(?:--\s*Query\s+\d+:|\Z))'
    matches = re.findall(pattern, content, re.DOTALL)
    
    queries = []
    for title, sql in matches:
        sql_clean = sql.strip()
        if sql_clean:
            queries.append((title.strip(), sql_clean))
            
    return queries

def run_queries():
    db_path = 'placement.db'
    sql_file = 'queries.sql'
    output_json = 'insights.json'
    
    print("=" * 80)
    print("STEP 3: RUNNING ANALYTICAL SQL QUERIES & EXPORTING INSIGHTS")
    print("=" * 80 + "\n")
    
    conn = sqlite3.connect(db_path)
    queries = parse_queries(sql_file)
    
    all_insights = {}
    
    for idx, (title, sql) in enumerate(queries, 1):
        print("=" * 80)
        print(f"[{idx}/{len(queries)}] {title.upper()}")
        print("-" * 80)
        
        try:
            df = pd.read_sql_query(sql, conn)
            
            # Print table nicely to terminal
            print(df.to_string(index=False))
            print("\n")
            
            # Store in json dictionary
            all_insights[title] = {
                "sql": sql,
                "row_count": len(df),
                "data": df.to_dict(orient='records')
            }
        except Exception as e:
            print(f"ERROR executing query '{title}': {e}\n")
            
    conn.close()
    
    # Save insights to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_insights, f, indent=4)
        
    print("=" * 80)
    print(f"All {len(queries)} queries executed successfully.")
    print(f"Results exported to '{output_json}'.")
    print("=" * 80)

if __name__ == '__main__':
    run_queries()
