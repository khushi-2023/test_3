import os
os.environ["VOSK_LOG_LEVEL"] = "0"  # Suppress Vosk logs

import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import json
import pyaudio
import wave
import sounddevice as sd
import whisper

# Path to Vosk model
MODEL_PATH = os.path.join(os.getcwd(), "models", "vosk-model-en-us-0.22")

# ✅ Record fallback audio for Whisper
def record_audio_to_wav(filename="fallback.wav", duration=5, fs=16000):
    print("🎙️ Recording fallback audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())
    return filename

# ✅ Use Whisper as fallback ASR
def whisper_asr(audio_path="fallback.wav"):
    try:
        model = whisper.load_model("base")  # can be 'tiny', 'small', 'base', 'medium', or 'large'
        result = model.transcribe(audio_path)
        return result['text'].strip()
    except Exception as e:
        print(f"❌ Whisper failed: {e}")
        return ""

# ✅ Offline ASR using Vosk, fallback to Whisper if needed
def offline_asr():
    # Step 1: Check if model exists
    if not os.path.exists(MODEL_PATH):
        print("❌ Vosk model not found. Using Whisper fallback.")
        audio_path = record_audio_to_wav()
        return whisper_asr(audio_path)

    # Step 2: Try loading Vosk
    try:
        model = Model(MODEL_PATH)
    except Exception as e:
        print(f"❌ Failed to load Vosk model: {e}")
        audio_path = record_audio_to_wav()
        return whisper_asr(audio_path)

    # Step 3: Record using Vosk
    recognizer = KaldiRecognizer(model, 16000)
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("🎤 [Offline Mode - Vosk] Speak now...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if not text.strip():
                print("⚠ Empty result from Vosk. Using Whisper fallback.")
                audio_path = record_audio_to_wav()
                return whisper_asr(audio_path)
            return text.strip()

# ✅ Online ASR using Google Web Speech API
def cloud_asr():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 [Online Mode - Google] Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("❌ Google could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Google API error: {e}")
        return None

# ✅ Hybrid ASR logic
def hybrid_asr(mode="offline"):
    print(f"🧠 Using mode: {mode}")
    text = offline_asr() if mode == "offline" else cloud_asr()

    if not text or not text.strip():
        print("⚠ No speech detected. Please speak again.")
        return None

    return text.strip()
