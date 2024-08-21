import datetime
import json
import os
import random
import requests

import openai
from config import apiKey
import speech_recognition as sr
import win32com.client as wc
import webbrowser

speaker = wc.Dispatch("SAPI.SpVoice")

chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apiKey

    chatStr += f"User: {query}\nJarvis: "
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    speaker.Speak(response['choices'][0]['text'])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response['choices'][0]['text']

    # with open(f"OpenAI/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
    #     f.write(text)


def ai(prompt):
    openai.api_key = apiKey
    text = f"OpenAI response for prompt: {prompt} \n *********************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this under try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("OpenAI"):
        os.mkdir("OpenAI")

    with open(f"OpenAI/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

    # except Exception as e:
    #     return "Some error occurred, please say it again"


def wishMe():
    hour = int(datetime.datetime.now().hour)
    # if hour >= 5 and hour < 12:
    #     speaker.Speak("Good night!")
    if hour >= 5 and hour < 12:
        speaker.Speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speaker.Speak("Good afternoon!")
    elif hour >= 18 and hour < 23:
        speaker.Speak("Good evening!")
    else:
        speaker.Speak("Good night!")
    speaker.Speak("I am Jarvis, your virtual assistant, tell me how can I help you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occurred, please say that again."
            # print(e)


if __name__ == '__main__':
    wishMe()

    # while 1:
    #     print("Enter what you want me to speak: ")
    #     s = input()
    #     speaker.Speak(s)

    while True:
        print("Listening...")
        query = takeCommand().lower()

        # todo: you can add more sites
        sites = [["youtube", "https://www.youtube.com/"], ["google", "https://www.google.com/"],
                 ["wikipedia", "https://www.wikipedia.org/"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} for you...")
                webbrowser.open(site[1])

        # todo: play music from desktop
        if "play music" in query:
            music_dir = " " #enter your music directory
            random_song = random.choice(os.listdir(music_dir))
            print(random_song)
            os.startfile(os.path.join(music_dir, random_song))

        # todo: weather details from voice command
        elif "weather" in query:
            # Prompts city of user's choice
            city = input("Enter the name of the city:\n")
            url = f"https://api.weatherapi.com/v1/current.json?key=a3c7ea69fcda4e0e89763208232606&q={city}" #enter your weather api here
            r = requests.get(url)
            # speaker = wc.Dispatch("SAPI.SpVoice")
            # print(r.text)

            # Declares the weather dictionary to get the desired weather
            weather_dic = json.loads(r.text)

            temp = weather_dic["current"]["temp_c"]
            print(temp)
            temp2 = weather_dic["current"]["feelslike_c"]
            print(f"feels like {temp2}")
            condition = weather_dic["current"]["condition"]["text"]
            print(condition)

            # Speaks about the weather parameters
            speaker.Speak(f"The current temperature in {city} is {temp} degree celcius")
            speaker.Speak(f"But it feels like {temp2} degree celcius")
            speaker.Speak(f"And the weather condition in {city} is {condition}")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speaker.Speak(f"The time is {strTime}")

        # todo: open more applications from desktop
        elif 'open vs code' in query:
            codePath = " " #enter vs code directory for your system
            os.startfile(codePath)

        elif 'open whatsapp' in query:
            # path = "C:\\Users\\Chinmay\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
            path = " " #enter whatsapp directory for your system
            os.startfile(path)

        elif "using artificial intelligence" in query:
            ai(prompt=query)


        elif "reset chat" in query:
            chatStr = ""

        elif "jarvis quit" in query:
            speaker.Speak("It was a pleasure helping you. If you have any more query, don't hesitate to reach me out.")
            exit()


        else:
            print("Chatting...")
            chat(query)
        # speaker.Speak(query)
