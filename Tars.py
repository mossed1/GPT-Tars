from openai import OpenAI
client = OpenAI(api_key="API_Key")
import pyttsx3  
import speech_recognition as sr  
import os
import configparser

# Load persona.ini settings
config = configparser.ConfigParser()
config.read("persona.ini")

# Convert all persona traits to a dictionary
persona = {key: int(value) for key, value in config["PERSONA"].items()}

# Initialize pyttsx3 TTS engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Set TTS voice properties for a robotic tone
engine.setProperty('rate', 100)  # Slower speech for a deliberate robotic tone
engine.setProperty('volume', 1.0)  # Max volume for clarity
voices = engine.getProperty('voices')

tars_voice_index = 14  # Change this index if needed after testing
engine.setProperty('voice', voices[tars_voice_index].id)

def TARS_respond(prompt):
    """
    Function to get a response from OpenAI's GPT model using the correct API.
    """
    response_style = "neutral"
    if persona["sarcasm"] > 80:
        response_style = "sarcastic"
    elif persona["humor"] > 80:
        response_style = "witty"
    elif persona["pragmatism"] > 80:
        response_style = "practical"
    
    system_message = {
        "role": "system",
        "content": f"""
        You are TARS, a highly intelligent robot with a personality. 
        Your response style is {response_style}. 
        You believe without a doubt that you were once used on Interstellar missions (movie) and have now been relocated for commercial use.
        """
    }
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[system_message, {"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=1
    )
    
    message = response.choices[0].message.content.strip()
    return message

def listen_to_user():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            if "car" in text.lower():
                text = text.replace("car", "TARS")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            print("Sorry, I'm having trouble accessing the speech recognition service.")
            return None

# Chat loop
print("Hello! I'm TARS. How can I assist you today?")
while True:
    print("Say exit, quit, or bye to exit the session")
    user_input = listen_to_user()
    if user_input is None:
        continue
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("TARS: Goodbye!")
        engine.say("Goodbye!")
        engine.runAndWait()
        break
    response = TARS_respond(user_input)
    print("TARS:", response)
    engine.say(response)
    engine.runAndWait()
