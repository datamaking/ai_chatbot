import sqlite3
import psycopg2
import pandas as pd
from typing import Dict, Any

def execute_query(db_choice: str, query: str, db_params: Dict[str, Any]) -> pd.DataFrame:
    """Execute the SQL query on the chosen database."""
    if db_choice == "sqlite":
        return _execute_sqlite_query(query, db_params["db_path"])
    elif db_choice == "postgresql":
        return _execute_postgresql_query(query, db_params)
    else:
        raise ValueError(f"Unsupported database choice: {db_choice}")

def _execute_sqlite_query(query: str, db_path: str) -> pd.DataFrame:
    """Execute query on SQLite database."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def _execute_postgresql_query(query: str, db_params: Dict[str, Any]) -> pd.DataFrame:
    """Execute query on PostgreSQL database."""
    conn = psycopg2.connect(**db_params)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_db_schema(db_choice: str, db_params: Dict[str, Any]) -> str:
    """Retrieve the database schema for the chosen database."""
    if db_choice == "sqlite":
        return _get_sqlite_schema(db_params["db_path"])
    elif db_choice == "postgresql":
        return _get_postgresql_schema(db_params)
    else:
        raise ValueError(f"Unsupported database choice: {db_choice}")

def _get_sqlite_schema(db_path: str) -> str:
    """Get schema from SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = ""
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema += f"Table: {table_name}\n"
        for column in columns:
            schema += f"  {column[1]} ({column[2]})\n"
    conn.close()
    return schema

def _get_postgresql_schema(db_params: Dict[str, Any]) -> str:
    """Get schema from PostgreSQL database."""
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    rows = cursor.fetchall()
    schema = ""
    current_table = ""
    for row in rows:
        table_name, column_name, data_type = row
        if table_name != current_table:
            schema += f"\nTable: {table_name}\n"
            current_table = table_name
        schema += f"  {column_name} ({data_type})\n"
    conn.close()
    return schema
