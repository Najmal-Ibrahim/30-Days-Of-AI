import os
import base64
from dotenv import load_dotenv
from groq import Groq

# 1. Load Secrets
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 2. Helper: Convert Image to String (Base64)
# AI models need images translated into text strings to read them over the API.
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 3. Main Vision Function
def analyze_image(image_path):
    print(f"--- ANALYZING IMAGE: {image_path} ---")
    
    # Step A: Encode
    try:
        base64_image = encode_image(image_path)
    except FileNotFoundError:
        print("❌ Error: Image file not found. Make sure 'test_image.jpg' exists.")
        return

    # Step B: Send to Llama-3.2-Vision
    print("👁️  Looking at the image...")
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail. If there is text, read it. If there is code, explain it."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct", # Specialized Vision Model
    )

    print("\n--- AI OBSERVATION ---")
    print(chat_completion.choices[0].message.content)

# 4. Execution
if __name__ == "__main__":
    # Ensure you have a file named 'test_image.jpg' or 'test_image.png'
    # Update the filename below if yours is a .png
    analyze_image("test_image.jpg")