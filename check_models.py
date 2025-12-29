import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load Secrets
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("--- CONNECTING TO GROQ... ---")

try:
    # Get the full list
    models = client.models.list()
    
    print(f"Successfully connected. Found {len(models.data)} models.\n")
    print("--- RAW MODEL LIST ---")
    
    # Print every single ID found
    for m in models.data:
        print(f"• {m.id}")
        
except Exception as e:
    print(f"❌ Error: {e}")