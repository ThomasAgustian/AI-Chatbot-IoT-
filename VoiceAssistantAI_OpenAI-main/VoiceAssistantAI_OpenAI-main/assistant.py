import sys
import speech_recognition as sr
import pyttsx3 as tts
import requests

from neuralintents import GenericAssistant
from datetime import date
from datetime import datetime

import api_secret
import openai

# Make a Global Functions
response = ""

# Set API for OpenAI
openai.api_key = api_secret.API_KEY

# Set Today Date variable
today = date.today()
time = datetime.now()

# Set for Speech Recognition
recognizer = sr.Recognizer()

# Audio to Text
def audio_to_text(audio):
    result = recognizer.recognize_google(audio, language="en-US", show_all=False)
    return result

# Set for Text to Speech
speaker = tts.init()
speaker.setProperty('rate', 150)

# Set for Voice Preferences for Text to Speech
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id) #it depends on the list of TTS on your devices

# Text to Speech Functions
def text_to_speech(text):
    print("Chatbot: " + text)
    speaker.say(text)
    speaker.runAndWait()
    speaker.stop()

# Function for get today date
def getdate():
    date = today.strftime("%d %B %Y")
    result = "Today's date is", date
    
    if date is not None:
        text_to_speech(result)

# Function for get now time
def gettime():
    nowtime = time.strftime("%I:%M %p")
    result = "The time is", nowtime

    if nowtime is not None:
        text_to_speech(result)

# Control the light
def control_light(action):
    if action == "on":
        # Send request to turn on the light
        requests.get("http://192.168.1.18/light/on")
    elif action == "off":
        # Send request to turn off the light
        requests.get("http://192.168.1.18/light/off")

# Call a Function to Search VIA OpenAI
def openai_search():

    # Search in OpenAI
    result = openai.Completion.create(
            model="text-davinci-003", prompt=response, max_tokens=100
        )
    # Purge the Answer Result from OpenAI
    final_result = result["choices"][0]["text"].replace("\n", "")
    final_result = final_result.split("Chatbot:", 1)[0]

    # Set to TTS
    if final_result is not None:
        text_to_speech(final_result)

# Exit Session
def exit_session():
    text_to_speech("Goodbye, see you later!")
    sys.exit(0)

# Mapping the Functions for this Assistant
mappings = {
    "search": openai_search,
    "exit": exit_session,
    "date": getdate,
    "time": gettime,
    "turn on the light": lambda:control_light("on"),
    "turn off the light": lambda:control_light("off")
}

# Set the Intents and Train the Model
assistant = GenericAssistant('C:/Users/Acer/OneDrive/Documents/kuliah/Semester 6/ISAD/VoiceAssistantAI_OpenAI-main/VoiceAssistantAI_OpenAI-main/intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        # Start Mic Session
        with sr.Microphone() as mic:
            # Start Listening
            print("Listening... (press ctrl+c to stop)")
            recognizer.adjust_for_ambient_noise(mic, duration=3)
            audio = recognizer.listen(mic)
            print("Listening is stopped")

            # Change from the Audio into Text
            response = audio_to_text(audio)
            
            print("Me: " + response)

            if response == "turn on the light":
               control_light("on")

            elif response == "turn off the light":
               control_light("off")

            # Make the result is Lowercase
            response = response.lower()

        # Check the response
        if response is not None:
            # Call to Assistant Result
            response_text = assistant.request(response)
            # Check for the Response text
            if response_text is not None:
                text_to_speech(response_text)
    
    # Start Exception
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        continue
