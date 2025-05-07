# ai_chatbot/app.py
import streamlit as st
import sqlite3
from utils.nlp import text_to_sql
from utils.database import execute_query, get_db_schema
from utils.visualization import display_results


def create_sample_sqlite_db(db_path: str) -> None:
    """Create a sample SQLite database for testing."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department_id INTEGER,
            salary REAL,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    """)

    cursor.execute("DELETE FROM employees")
    cursor.execute("DELETE FROM departments")

    cursor.execute("INSERT INTO departments (name) VALUES ('HR'), ('Engineering'), ('Sales')")
    cursor.execute("""
        INSERT INTO employees (name, department_id, salary) VALUES
        ('Alice', 1, 50000),
        ('Bob', 2, 60000),
        ('Charlie', 2, 65000),
        ('David', 3, 55000),
        ('Eve', 1, 52000)
    """)

    conn.commit()
    conn.close()


st.title("AI Chatbot for SQL Queries")

# Database selection
db_choice = st.selectbox("Choose database system", ["sqlite", "postgresql"])

if db_choice == "sqlite":
    db_path = st.text_input("Enter SQLite database path", "data/sample_sqlite.db")
    if st.button("Create Sample SQLite DB"):
        create_sample_sqlite_db(db_path)
        st.success(f"Sample database created at {db_path}")
    db_params = {"db_path": db_path}
else:
    host = st.text_input("Enter PostgreSQL host", "localhost")
    port = st.text_input("Enter PostgreSQL port", "5432")
    database = st.text_input("Enter database name", "mydatabase")
    user = st.text_input("Enter username", "myuser")
    password = st.text_input("Enter password", type="password")
    db_params = {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password
    }

# LLM selection
llm_choice = st.selectbox("Choose LLM for text-to-SQL", ["gpt", "llama"])

# User input
input_text = st.text_area("Enter your query in natural language", "Show me the average salary per department")

# Visualization selection
viz_type = st.selectbox("Choose visualization type", ["table", "bar", "line", "pie"])

if st.button("Run Query"):
    try:
        # Fetch database schema
        db_schema = get_db_schema(db_choice, db_params)

        # Convert text to SQL
        sql_query = text_to_sql(input_text, llm_choice, db_schema)
        st.write("Generated SQL Query:")
        st.code(sql_query, language="sql")

        # Execute query
        df = execute_query(db_choice, sql_query, db_params)

        # Display results
        display_results(df, viz_type)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
