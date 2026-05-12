"""
Streamlit UI Builder - ACTUAL working code.
"""

import streamlit as st
from typing import Callable, Any, Dict


def page_config(title: str = "AI Agent", layout: str = "wide"):
    """Set page config."""
    st.set_page_config(page_title=title, layout=layout)


def chat_ui(agent_fn: Callable):
    """Build chat interface."""
    st.title("AI Chat Agent")
    
    if "history" not in st.session_state:
        st.session_state.history = []
    
    for msg, resp in st.session_state.history:
        st.chat_message("user").write(msg)
        st.chat_message("assistant").write(resp)
    
    prompt = st.chat_input("Type your message...")
    if prompt:
        response = agent_fn(prompt)
        st.session_state.history.append((prompt, response))
        st.rerun()


def agent_card(agent_fn: Callable):
    """Build agent config card."""
    st.title("AI Agent")
    
    with st.sidebar:
        st.header("Configuration")
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
        max_tokens = st.slider("Max Tokens", 100, 4000, 1000)
    
    st.header("Input")
    input_text = st.text_area("Message", height=200)
    
    if st.button("Run"):
        if input_text:
            result = agent_fn(input_text)
            st.success(result)


def config_form(agent_fn: Callable):
    """Build config form."""
    st.title("Agent Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini", "claude-3.5-sonnet"])
    with col2:
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
    
    mode = st.radio("Mode", ["chat", "completion"])
    stream = st.checkbox("Stream responses", value=True)
    
    if st.button("Initialize Agent"):
        st.success(f"Agent initialized with {model}")


def metrics_dashboard():
    """Build metrics dashboard."""
    st.title("Agent Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Requests", "1,234")
    col2.metric("Tokens", "45.2K")
    col3.metric("Latency", "120ms")
    col4.metric("Errors", "2")
    
    st.header("Usage Over Time")
    st.line_chart({"requests": [10, 20, 15, 25, 30]})


def file_uploader(agent_fn: Callable):
    """Build file upload interface."""
    st.title("Upload & Process")
    
    file = st.file_uploader("Choose a file", type=["txt", "pdf", "csv"])
    if file:
        st.success(f"Uploaded: {file.name}")
        if st.button("Process"):
            result = agent_fn(file)
            st.write(result)
