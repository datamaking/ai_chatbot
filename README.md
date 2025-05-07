# ai_chatbot/README.md
# AI Chatbot for SQL Queries

This project is an AI-powered chatbot built with Python and Streamlit. It converts natural language queries into SQL, executes them on SQLite or PostgreSQL databases, and displays results in various formats (tables, bar charts, line charts, pie charts).

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys**:
   - For OpenAI GPT, add your API key to a `secrets.toml` file in `.streamlit/`:
     ```toml
     [secrets]
     OPENAI_API_KEY = "your-openai-api-key"
     ```
   - For Ollama, ensure the Llama model is installed and accessible (refer to Ollama documentation).

3. **Prepare the database**:
   - **SQLite**: Run the app and click "Create Sample SQLite DB" to generate `data/sample_sqlite.db`.
   - **PostgreSQL**: Execute `data/sample_postgres.sql` in your PostgreSQL server.

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage

- Select a database system (SQLite or PostgreSQL) and provide connection details.
- Choose an LLM (GPT or Llama) for text-to-SQL conversion.
- Enter a natural language query (e.g., "Show me the average salary per department").
- Select a visualization type and click "Run Query".

## Project Structure

- `app.py`: Main Streamlit application.
- `utils/nlp.py`: Handles text-to-SQL conversion.
- `utils/database.py`: Manages database interactions.
- `utils/visualization.py`: Visualizes query results.
- `data/sample_sqlite.db`: Sample SQLite database.
- `data/sample_postgres.sql`: Sample PostgreSQL database script.

## Sample Queries

- "List all employees in the Engineering department"
- "Show the total salary by department"
- "How many employees are in each department?"

## Requirements

See `requirements.txt` for the list of Python libraries.
