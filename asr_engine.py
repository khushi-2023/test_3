import os
os.environ["VOSK_LOG_LEVEL"] = "0"  # Suppress Vosk logs

import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import json, pyaudio

MODEL_PATH = os.path.join(os.getcwd(), "models", "vosk-model-small-en-us-0.15")

# Offline ASR using Vosk
def offline_asr():
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("🎤 [Offline Mode] Speak now...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            return json.loads(recognizer.Result())['text']

# Online ASR using Google
def cloud_asr():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 [Online Mode] Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("❌ Could not understand audio. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Google API error: {e}")
        return None

# Hybrid ASR with fallback
def hybrid_asr(mode="offline"):
    text = offline_asr() if mode == "offline" else cloud_asr()
    if not text or not text.strip():
        print("⚠ No speech detected. Please speak again.")
        return None
    return text
