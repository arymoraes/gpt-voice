import os
import tempfile
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr


def get_microphone_list():
    mic_list = sr.Microphone.list_microphone_names()
    return mic_list


def listen_to_microphone(mic_index, languages):
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=mic_index) as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            return ""

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(
            audio, language=languages[0])  # Use the passed language
        print(f"Text: {text}")
        return text
    except Exception as e:
        print("Error:", e)
        return ""


def text_to_speech(text, speed=1.1, lang="en"):
    tts = gTTS(text=text, lang=lang)
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


def write_to_file(text, file_name="output.txt"):
    with open(file_name, "a") as file:
        file.write(text + "\n")
