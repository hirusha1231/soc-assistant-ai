# 🔐 SOC Assistant AI

An AI-powered chatbot for SOC (Security Operations Center) analysts that explains security alerts and provides step-by-step incident response guidance.

---

## 📌 Features

- 🔍 **Alert Translation** – Converts raw security alerts into simple English
- 📋 **Incident Response** – Gives actionable steps to handle threats
- 🎯 **MITRE ATT&CK Mapping** – Maps alerts to attack techniques
- 🤖 **AI-Powered** – Uses Groq LLM with RAG (Retrieval-Augmented Generation)
- 💬 **Easy to Use** – Clean web interface built with Streamlit

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Programming language |
| Streamlit | Web interface |
| Groq API | AI / LLM (Llama 3.3-70B) |
| ChromaDB | Vector database for RAG |
| Sentence Transformers | Text embeddings |

---

## 🚀 How to Run This Project

### 1. Clone the Repository

```bash
git clone https://github.com/hirusha1231/soc-assistant-ai.git
cd soc-assistant-ai