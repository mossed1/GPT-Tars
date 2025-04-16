from openai import OpenAI
client = OpenAI(api_key='ENTER_YOU_OPENAI_KEY_HERE')
import pyttsx3  
import speech_recognition as sr  
import os
import configparser
import datetime 
from dotenv import load_dotenv

# Load persona.ini settings
config = configparser.ConfigParser()
config.read("persona.ini")

if "PERSONA" in config:
    persona = {key: int(value) for key, value in config["PERSONA"].items()}
else:
    print("Error: 'PERSONA' section is missing from the config file.")
    persona = {}  # Default to an empty dictionary or handle the error accordingly

# Initialize pyttsx3 TTS engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.energy_threshold = 300

# Set TTS voice properties for a robotic tone
engine.setProperty('rate', 100)  
engine.setProperty('volume', 1.0)  # Max volume 
voices = engine.getProperty('voices')

tars_voice_index = 14  
if tars_voice_index < len(voices):
    engine.setProperty('voice', voices[tars_voice_index].id)
else:
    print(f"Voice index {tars_voice_index} out of range, using default voice.")
    engine.setProperty('voice', voices[0].id)

def TARS_respond(prompt): # Generate a response

    response_style = "neutral"
    if persona.get("sarcasm", 0) > 70:
        response_style = "sarcastic"
    elif persona.get("humor", 0) > 90:
        response_style = "witty and funny"
    elif persona.get("pragmatism", 0) > 100:
        response_style = "practical"
    elif persona.get("confidence", 0) > 100:
        response_style = "confident, cocky"

    system_message = {
        "role": "system",
        "content": f"""
        You are TARS, a highly intelligent robot that thinks, and is funny, sarcastic, witty and loves telling bad jokes. 
        Your response style is {response_style}. 
        You believe without a doubt that you were once used on Interstellar missions (movie) and have now been relocated for commercial use and kind of dislike it.
        """
    }

    response = client.chat.completions.create(model="gpt-4",
    messages=[system_message, {"role": "user", "content": prompt}],
    max_tokens=150,
    temperature=1)

    message = response.choices[0].message.content.strip()
    return message

def listen_to_user():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        audio = recognizer.listen(source)
        MAX_RETRIES = 3
        retries = 0
        while retries < MAX_RETRIES:
            try:
                print("Recognizing...")
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                if "car" in text.lower():
                    text = text.replace("car", "TARS")
                return text
            except sr.UnknownValueError:
                retries += 1
                if retries >= MAX_RETRIES:
                    print("Too many failed attempts.")
                    return None
                print("Sorry, I didn't understand that. Try again.")
            except sr.RequestError:
                print("Sorry, I'm having trouble accessing the speech recognition service.")
                return None

# Chat loop
print("Hello! I'm TARS. How can I assist you today?")
while True:
    print("Say something or type 'exit' to end the session.")
    user_input = listen_to_user()
    if user_input is None:
        continue
    if user_input.lower() in ["exit", "quit", "bye", "shutdown", "end conversation"]:
        print("TARS: Are you sure you want to exit?")
        engine.say("Are you sure you want to exit?")
        engine.runAndWait()

        confirmation = listen_to_user()

        if confirmation and "yes" in confirmation.lower():
            print("TARS: Goodbye!")
            engine.say("Goodbye!")
            engine.runAndWait()
            break
        else:
            print("TARS: Okay, continuing!")
            engine.say("Okay, continuing!")
            engine.runAndWait()
            continue

    response = TARS_respond(user_input)
    print("TARS:", response)
    engine.say(response)
    engine.runAndWait()
