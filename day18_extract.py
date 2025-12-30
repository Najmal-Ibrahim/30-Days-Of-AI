import os
import base64
import json
from dotenv import load_dotenv
from groq import Groq

# 1. Load Secrets
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 2. Helper: Encode Image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 3. Main Extraction Function
def extract_receipt_data(image_path):
    print(f"--- PROCESSING INVOICE: {image_path} ---")
    
    try:
        base64_image = encode_image(image_path)
    except FileNotFoundError:
        print("❌ Error: 'receipt.jpg' not found. Please download a sample receipt.")
        return

    print("🔍 Scanning document...")

    # The System Prompt is CRITICAL here. 
    # We define the EXACT Schema we want.
    system_prompt = """
    You are an AI Data Entry Clerk. 
    Your job is to extract data from receipt images into strict JSON format.
    
    Output JSON with these exact keys:
    {
        "store_name": "string",
        "date": "string (YYYY-MM-DD)",
        "total_amount": "float",
        "items": ["list of strings"]
    }
    
    Do NOT add markdown formatting (like ```json). Just return the raw JSON string.
    If you cannot find a value, use null.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract data from this image."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            # Use the Llama 4 Model that worked yesterday
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            temperature=0, # 0 means "Be precise, don't be creative"
        )

        # 4. Parse the Result
        raw_content = chat_completion.choices[0].message.content
        print("\n--- RAW AI OUTPUT ---")
        print(raw_content)
        
        print("\n--- PARSED DATA (Database Ready) ---")
        # Convert String -> Python Dictionary
        data = json.loads(raw_content) 
        
        print(f"🏪 Store: {data['store_name']}")
        print(f"📅 Date:  {data['date']}")
        print(f"💰 Total: ${data['total_amount']}")
        print(f"🛒 Items: {len(data['items'])} items found.")

    except json.JSONDecodeError:
        print("❌ Error: The AI did not output valid JSON. It might have added text.")
    except Exception as e:
        print(f"❌ Error: {e}")

# 5. Execution
if __name__ == "__main__":
    extract_receipt_data("receipt.jpg")