# ai_chatbot/utils/visualization.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def display_results(df: pd.DataFrame, viz_type: str) -> None:
    """Display query results in the chosen visualization format."""
    if df.empty:
        st.warning("No data returned from the query.")
        return

    if viz_type == "table":
        st.dataframe(df)
    elif viz_type == "bar":
        if len(df.columns) >= 2:
            x_col = st.selectbox("Select X-axis column", df.columns)
            y_col = st.selectbox("Select Y-axis column", df.columns)
            plt.figure(figsize=(10, 6))
            sns.barplot(x=df[x_col], y=df[y_col])
            st.pyplot(plt)
        else:
            st.error("DataFrame must have at least two columns for a bar chart.")
    elif viz_type == "line":
        if len(df.columns) >= 2:
            x_col = st.selectbox("Select X-axis column", df.columns)
            y_col = st.selectbox("Select Y-axis column", df.columns)
            plt.figure(figsize=(10, 6))
            sns.lineplot(x=df[x_col], y=df[y_col])
            st.pyplot(plt)
        else:
            st.error("DataFrame must have at least two columns for a line chart.")
    elif viz_type == "pie":
        if len(df.columns) >= 1:
            col = st.selectbox("Select column for pie chart", df.columns)
            plt.figure(figsize=(8, 8))
            df[col].value_counts().plot.pie(autopct="%1.1f%%")
            st.pyplot(plt)
        else:
            st.error("DataFrame must have at least one column for a pie chart.")
    else:
        st.error(f"Unsupported visualization type: {viz_type}")
