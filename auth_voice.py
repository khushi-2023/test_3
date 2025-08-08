import librosa, numpy as np

REGISTERED_VOICE = "auth/voice_ref.wav"

def extract_features(file):
    y, sr = librosa.load(file, sr=16000)
    return np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)

def authenticate(user_voice):
    ref = extract_features(REGISTERED_VOICE)
    usr = extract_features(user_voice)
    return np.linalg.norm(ref-usr) < 50  # threshold
