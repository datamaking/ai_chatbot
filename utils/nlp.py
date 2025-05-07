# ai_chatbot/utils/nlp.py
import openai
import ollama
import streamlit as st

def text_to_sql(input_text: str, llm_choice: str, db_schema: str) -> str:
    """Convert natural language input to SQL using the chosen LLM."""
    if llm_choice == "gpt":
        return _gpt_text_to_sql(input_text, db_schema)
    elif llm_choice == "llama":
        return _llama_text_to_sql(input_text, db_schema)
    else:
        raise ValueError(f"Unsupported LLM choice: {llm_choice}")

def _gpt_text_to_sql(input_text: str, db_schema: str) -> str:
    """Use OpenAI GPT to convert text to SQL."""
    openai.api_key = st.secrets.get("OPENAI_API_KEY", "your-openai-api-key")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Given the following database schema:\n{db_schema}\nConvert this natural language query to SQL: {input_text}\nProvide only SQL query alone so that it can be used to executed using established SQL connection, no explanation needed.",
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].text.strip()

def _llama_text_to_sql(input_text: str, db_schema: str) -> str:
    """Use Llama via Ollama to convert text to SQL."""
    response = ollama.generate(
        model="llama3.2",
        prompt=f"Given the following database schema:\n{db_schema}\nConvert this natural language query to SQL: {input_text}\nProvide only SQL query alone so that it can be used to executed using established SQL connection, no explanation needed."
    )
    print(type(db_schema))
    print(db_schema)
    print("\n")
    print(type(response))
    print(response)
    #return response["text"].strip()
    return response["response"].strip()
