# audio_utils.py

import os
import tempfile
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr


def listen_to_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            return ""

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"Text: {text}")
        return text
    except Exception as e:
        print("Error:", e)
        return ""


def write_to_file(text, file_name="output.txt"):
    with open(file_name, "a") as file:
        file.write(text + "\n")


def text_to_speech(text, speed=1.1):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        temp_path = fp.name
    tts.save(temp_path)

    audio = AudioSegment.from_file(temp_path, format="mp3")
    audio_fast = audio.speedup(playback_speed=speed)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        temp_fast_path = fp.name
    audio_fast.export(temp_fast_path, format="mp3")
    play(audio_fast)

    os.remove(temp_path)
    os.remove(temp_fast_path)
