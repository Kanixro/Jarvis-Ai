import pyttsx3
import speech_recognition as sr
import os
from datetime import datetime
import webbrowser
import threading
import pygame
from persiantools.jdatetime import JalaliDate
import random
import requests

user_nickname = "Mr. Adams"

engine = pyttsx3.init()
pygame.mixer.init()

music_playing = False
music_paused = False

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            return ""
    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
        return ""
    except sr.RequestError:
        print("Speech service is down.")
        return ""

def play_music():
    global music_playing, music_paused
    music_path = r"C:\Users\GAMING\Music\hans_zimmer_interstellar_day one 128.mp3"
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        music_playing = True
        music_paused = False
    except Exception as e:
        speak("I couldn't play the music.")
        print(e)

def stop_music():
    global music_playing, music_paused
    pygame.mixer.music.stop()
    music_playing = False
    music_paused = False

def pause_music():
    global music_playing, music_paused
    if music_playing:
        pygame.mixer.music.pause()
        music_paused = True
        speak("Music paused.")
    else:
        speak("No music is currently playing.")

def resume_music():
    global music_playing, music_paused
    if music_paused:
        pygame.mixer.music.unpause()
        music_paused = False
        speak("Resuming music.")
    else:
        speak("Music is already playing.")

def get_iranian_date():
    persian_date = JalaliDate.today()
    return persian_date.strftime('%Y-%m-%d')

def get_weather(city):
    api_key = 'YOUR_OPENWEATHER_API_KEY'  # Replace with your actual key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        data = response.json()
        if data.get("cod") == "404":
            speak(f"Sorry, I couldn't find the weather for {city}.")
        else:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {description}.")
    except Exception as e:
        speak("Sorry, I couldn't retrieve the weather information.")
        print(e)

def tell_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why did the math book look sad? Because it had too many problems.",
        "What do you call fake spaghetti? An impasta!"
    ]
    joke = random.choice(jokes)
    speak(joke)

def jarvis():
    global music_playing, music_paused
    greetings = ["hello", "hi", "hey", "hi there", "hello jarvis", "yo", "what's up"]
    sad_phrases = ["i'm feeling down", "i'm sad", "i feel depressed", "i'm not okay", "i feel lonely", "i'm tired of life"]
    open_chrome_phrases = ["open chrome", "open the chrome", "can you open the chrome", "please open chrome", "open up chrome"]
    close_chrome_phrases = ["close chrome", "close the chrome", "can you close the chrome", "please close chrome", "close up chrome"]
    weather_phrases = ["what's the weather", "tell me the weather", "how's the weather", "is it cold outside", "is it hot outside"]
    joke_phrases = ["tell me a joke", "make me laugh", "say something funny", "tell a joke"]

    while True:
        print("Waiting for wake word... (say 'Jarvis')")
        wake_word = listen()

        if "jarvis" in wake_word:
            speak("Yes sir?")
            command = listen()

            if "how are you" in command:
                responses = [
                    f"I'm doing great, {user_nickname}! Thanks for asking!",
                    f"I'm feeling fantastic, {user_nickname}, how about you?",
                    f"I'm in top shape, {user_nickname}, ready to assist you!",
                    f"I'm doing wonderful, {user_nickname}! How can I help today?",
                ]
                speak(random.choice(responses))

            elif "can you play music" in command or "please play music" in command or "play music" in command:
                speak("Sure, I can play some music for you.")
                threading.Thread(target=play_music).start()

            elif any(phrase in command for phrase in open_chrome_phrases):
                speak("Opening Chrome.")
                webbrowser.open("https://www.google.com")

            elif any(phrase in command for phrase in close_chrome_phrases):
                speak("Closing Chrome.")
                os.system("taskkill /f /im chrome.exe")

            elif any(phrase in command for phrase in weather_phrases):
                speak("Which city's weather would you like to know?")
                city = listen()
                if city:
                    get_weather(city)
                else:
                    speak("I didn't catch the city name.")

            elif any(phrase in command for phrase in joke_phrases):
                tell_joke()

            elif any(greet in command for greet in greetings):
                speak(f"Hello {user_nickname}.")

            elif any(sad in command for sad in sad_phrases):
                speak("I'm here for you. You're not alone.")
                speak("Would you like to hear some calming music?")
                follow_up = listen()
                if "yes" in follow_up or "sure" in follow_up or "okay" in follow_up:
                    speak("Playing some relaxing music for you.")
                    threading.Thread(target=play_music).start()
                else:
                    speak("Alright, just remember, you're not alone.")

            elif "pause music" in command:
                pause_music()
            elif "resume music" in command:
                resume_music()
            elif "stop music" in command:
                stop_music()
            elif "what time is it" in command:
                now = datetime.now()
                speak(f"The time is {now.strftime('%H:%M')}")
            elif "what date is it in iran" in command:
                iranian_date = get_iranian_date()
                speak(f"Today's date in Iran is {iranian_date}.")
            elif "stop" in command or "exit" in command:
                speak("Goodbye sir.")
                stop_music()
                break
            else:
                speak("I'm not sure how to respond to that.")

jarvis()
