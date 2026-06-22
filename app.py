# app.py
import streamlit as st
from chatbot import SOCBot
from playbooks import PLAYBOOKS

# Page configuration
st.set_page_config(
    page_title="SOC Analyst Assistant",
    page_icon="🔐",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'bot' not in st.session_state:
    st.session_state.bot = SOCBot()

# Sidebar
with st.sidebar:
    st.title("🔐 SOC Assistant")
    st.markdown("---")
    
    st.subheader("Quick Questions")
    quick_questions = [
        "What does a brute force alert mean?",
        "How to handle phishing?",
        "What to do for malware detection?",
        "How to respond to data exfiltration?"
    ]
    for q in quick_questions:
        if st.button(q, use_container_width=True):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": q})
            # Generate and add assistant response
            with st.spinner("Analyzing..."):
                response = st.session_state.bot.ask(q)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.markdown("---")
    st.subheader("Available Playbooks")
    for key, playbook in PLAYBOOKS.items():
        with st.expander(f"📋 {key.replace('_', ' ').title()}"):
            st.write(f"**Alert Types:** {', '.join(playbook['alert_types'])}")
            st.write(f"**MITRE:** {playbook['mitre_technique']}")
            st.write(f"**Severity:** {playbook['severity']}")
            st.write("**Steps:**")
            for i, step in enumerate(playbook['response_steps'], 1):
                st.write(f"{i}. {step}")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("🔐 SOC Analyst Assistant")
st.caption("Ask me about security alerts, incidents, or response procedures")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about a security alert..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = st.session_state.bot.ask(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()