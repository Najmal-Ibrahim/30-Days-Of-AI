import os
import time
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
from groq import Groq

#1.Setup Environment
load_dotenv()
client=Groq(api_key=os.environ.get("GROQ_API_KEY"))

#2.The "Ear"
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 LISTENING... (Speak now")
        #Adjust for background noise automatically
        recognizer.adjust_for_ambient_noise(source,duration=1)
        try:
            #Listen for 5 seconds max
            audio=recognizer.listen(source,timeout=5,phrase_time_limit=10)
            print("Processing Audio.....")
            #Send audio to Google to transcribe
            text=recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError:
            print("Internet erorr on Speech APi")
            return None
        except Exception as e:
            print(f"Erorr: {e}")
            return None
        
#3. The "Mouth"(Text to Speech)
def speak_text(text):
    print(f"AI: {text}")
    try:
        #Convert Text to Audio(mp3)
        tts = gTTS(text=text,lang='en',tld='co.in')#co.in gives an indian accent!
        filename="response.mp3"
        tts.save(filename)

        #Play audio(Windows command)
        #We use 'start' to open the default media player
        os.system(f"start {filename}")

        #Wait a bit so we dont record the AI speaking
        time.sleep(len(text)/ 10)
    except Exception as e:
        print(f"Audio Erorr: {e}")

#4 The Loop
print("----VOICE AI ACTIVATED----")
speak_text("System online.I am listening.")


while True:
    #A.Listen
    user_input = listen_to_user()

    if user_input is None:
        continue#Try Listening again

    if "exit" in user_input.lower() or "stop" in user_input.lower():
        speak_text("Shutting down systems.")
        break

       # B. Think (Groq Llama-3)
    completion = client.chat.completions.create(
        messages=[
            # System Prompt: Be concise because speaking long text takes too long
            {"role": "system", "content": "You are a helpful voice assistant. Keep answers SHORT (max 2 sentences). Do not use emojis."},
            {"role": "user", "content": user_input}
        ],
        model="llama-3.3-70b-versatile"
    )
    ai_response = completion.choices[0].message.content
    
    # C. Speak
    speak_text(ai_response)