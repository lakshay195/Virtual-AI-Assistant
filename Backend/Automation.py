from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables
env_vars = dotenv_values(".env")
classes = [
    "zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", 
    "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", 
    "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", 
    "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

# Define user-agent
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize Groq client
client = Groq(api_key='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')

# Predefined responses
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]
messages = []
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        subprocess.Popen(['notepad.exe', File])
    
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})
        try:
            completion = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=SystemChatBot + messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=True
            )
            Answer = "".join(chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content)
            messages.append({"role": "assistant", "content": Answer})
            return Answer
        except Exception as e:
            print(f"Error generating content: {e}")
            return "An error occurred while generating content."

    Topic = Topic.replace("Content", "")
    ContentByAI = ContentWriterAI(Topic)
    file_name = rf"Data\{Topic.lower().replace(' ','_')}.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
    OpenNotepad(file_name)
    return True

def YouTubeSearch(Topic):
    webbrowser.open(f"https://www.youtube.com/results?search_query={Topic}")
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        print(f"Successfully opened {app}")
        return True
    except Exception as e:
        print(f"Error opening app: {app}. Error: {e}")
        if app.lower() == "youtube":
            webbrowser.open("https://www.youtube.com")
            return True
        def extract_links(html):
            return [link.get('href') for link in BeautifulSoup(html, 'html.parser').find_all('a', {'jsname': 'UWckNb'})] if html else []
        def search_google(query):
            response = sess.get(f"https://www.google.com/search?q={query}", headers={"User-Agent": useragent})
            return response.text if response.status_code == 200 else None
        html = search_google(app)
        if html:
            webopen(extract_links(html)[0])
            print(f"Opened webpage for {app}")
            return True
    return False

def CloseApp(app):
    if "chrome" not in app:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume unmute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down"),
    }
    if command in actions:
        actions[command]()
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open") and "open it" not in command and "open file" not in command:
            funcs.append(asyncio.to_thread(OpenApp, command.removeprefix("open")))
        elif command.startswith("close"):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close")))
        elif command.startswith("play"):
            funcs.append(asyncio.to_thread(PlayYoutube, command.removeprefix("play")))
        elif command.startswith("content"):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content")))
        elif command.startswith("google search"):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search")))
        elif command.startswith("youtube search"):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search")))
        elif command.startswith("system"):
            funcs.append(asyncio.to_thread(System, command.removeprefix("system")))
        else:
            print(f"No Function Found for command: {command}")
    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
