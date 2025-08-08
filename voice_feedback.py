import pyttsx3, datetime, os

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def log_command(command):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open("logs/commands.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {command}\n")
