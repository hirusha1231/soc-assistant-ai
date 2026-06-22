# test_env.py
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print("✅ API key loaded successfully!")
    print(f"Key starts with: {api_key[:15]}...")
    print(f"Key length: {len(api_key)} characters")
else:
    print("❌ API key not found")
    print("Make sure your .env file has: GROQ_API_KEY=your_key_here")