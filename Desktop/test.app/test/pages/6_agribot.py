"""AgriBot Assistant - Premium AI Research Support."""
import streamlit as st
import sys
from pathlib import Path

# Fix path to include src/research_suite
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.research_suite.chatbot import chatbot
from src.utils import inject_custom_css

# Page config
st.set_page_config(page_title="AgriBot Assistant", page_icon="🤖", layout="wide")
inject_custom_css()

st.title("🤖 AgriBot Research Assistant")
st.markdown("### AI-Powered Agricultural Guidance & Productivity")
st.divider()

# Sidebar info
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/bot.png", width=80)
    st.info("**Knowledge Base v1.2**\n- Crop Lifecycle Management\n- Material Stabilization Laws\n- Storage Best Practices")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        chatbot.clear_history()
        st.rerun()

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask about seed storage, crop diseases, or cultivation tips..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("AgriBot is analyzing..."):
        response_data = chatbot.chat(prompt)
        response = response_data['response']

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Bottom tips
with st.expander("Example Research Queries"):
    st.markdown("""
    - "How does relative humidity affect wheat storage?"
    - "What are the common diseases for high-yield rice?"
    - "Explain the Harrington Hundred Rule for seed longevity."
    - "What is the optimal NPK for corn in clay soil?"
    """)
