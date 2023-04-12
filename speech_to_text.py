import speech_recognition as sr
import openai
import sys
import os

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile


def listen_to_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
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


def call_chat_gpt(input):
    with open("api_key.txt", "r") as file:
        openai.api_key = file.read().strip()

    text_to_speech("Please wait.")

    messages = []
    # Ask it it the needful
    messages.append(
        {"role": "user", "content": input})

    try:
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Print the response
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    # Pretty-print the response to stderr
    print("Pretty:\n", file=sys.stderr)

    # Print the response from the choices
    for choice in result.choices:
        response_text = choice.message.content
        print(choice.message.content, file=sys.stderr)
        print("\n-----", file=sys.stderr)

    return response_text


if __name__ == "__main__":
    while True:
        text = listen_to_microphone()
        print(text)
        if "overlord" in text.lower():
            response = call_chat_gpt(text)
            text_to_speech(response)
        elif text:
            print("Phrase 'Overlord' not detected, try again.")
        else:
            print("No speech detected, try again.")
