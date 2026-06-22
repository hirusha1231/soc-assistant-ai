# chatbot.py
import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from playbooks import PLAYBOOKS, get_playbook_by_alert
from vectordb import db

class SOCBot:
    def __init__(self):
        # Try to get API key from Streamlit secrets (for cloud)
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            print("✅ Using API key from Streamlit Secrets")
        except:
            # If not in cloud, try .env file (for local)
            load_dotenv()
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                print("✅ Using API key from .env file")
        
        # If still no key, show error
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found! Please set it in Streamlit Secrets or .env file")
            
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        
    def get_system_prompt(self):
        return """You are a SOC Analyst Assistant specializing in incident response.

        Your role is to:
        1. Explain security alerts in plain English
        2. Provide actionable response steps based on playbooks
        3. Reference MITRE ATT&CK techniques when applicable
        4. Always be specific and actionable
        5. If you don't know, say "I don't have specific guidance"

        Format your response as:
        🔍 ALERT ANALYSIS:
        [Explanation of what's happening]

        📋 RECOMMENDED RESPONSE:
        1. [Step 1]
        2. [Step 2]
        ...

        🎯 MITRE ATT&CK: [Technique ID]
        ⚠️ SEVERITY: [Low/Medium/High/Critical]
        """
    
    def ask(self, user_question):
        """Process user question and return response"""
        
        # Step 1: Check for exact playbook match
        playbook = get_playbook_by_alert(user_question)
        
        # Step 2: If no direct match, search vector DB
        if not playbook:
            try:
                search_results = db.search(user_question)
                if search_results['ids'] and len(search_results['ids'][0]) > 0:
                    key = search_results['ids'][0][0]
                    playbook = PLAYBOOKS.get(key)
            except:
                pass
        
        # Step 3: Prepare context
        context = ""
        if playbook:
            context = f"""
            Based on our playbook:
            Alert Type: {', '.join(playbook['alert_types'])}
            Description: {playbook['description']}
            MITRE Technique: {playbook['mitre_technique']}
            Response Steps: {'; '.join(playbook['response_steps'])}
            Severity: {playbook['severity']}
            """
        
        # Step 4: Build the prompt
        prompt = f"""
        USER QUESTION: {user_question}
        
        PLAYBOOK CONTEXT:
        {context if context else "No specific playbook found for this alert."}
        
        Provide a comprehensive response. If no context exists, explain you don't have specific guidance.
        """
        
        # Step 5: Get response from LLM
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    bot = SOCBot()
    test = "What does a brute force attack mean?"
    print(bot.ask(test))