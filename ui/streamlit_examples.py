"""
Streamlit Examples.

Run with: streamlit run ui/streamlit_examples.py
"""

import streamlit as st
from ui import chat_ui, agent_card, metrics_dashboard, file_uploader

# Example agent function
def echo_agent(msg):
    return f"Echo: {msg}"

# ==== PAGE 1: Chat ====
def chat_page():
    st.title("Chat Agent")
    chat_ui(echo_agent)

# ==== PAGE 2: Agent Config ====
def config_page():
    st.title("Agent Configuration")
    agent_card(echo_agent)

# ==== PAGE 3: Metrics ====
def metrics_page():
    metrics_dashboard()

# ==== PAGE 4: File Upload ====
def upload_page():
    def process_file(f):
        return f"Processed: {f.name}"
    file_uploader(process_file)

# ==== RUN ALL ====
if __name__ == "__main__":
    import sys
    pages = {
        "chat": ("Chat", chat_page),
        "config": ("Config", config_page),
        "metrics": ("Metrics", metrics_page),
        "upload": ("Upload", upload_page),
    }
    
    st.set_page_config(page_title="AI Agent Demo", layout="wide")
    
    page = st.sidebar.selectbox("Select", list(pages.keys()), format_func=lambda x: pages[x][0])
    pages[page][1]()
