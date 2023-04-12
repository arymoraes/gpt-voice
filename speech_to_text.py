from tkinter import ttk
import tkinter as tk
import threading
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


def call_chat_gpt(input, instructions):
    with open("api_key.txt", "r") as file:
        openai.api_key = file.read().strip()

    text_to_speech("Please wait.")

    messages = [{"role": "system", "content": instructions}]
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


class App:
    def __init__(self, master):
        self.master = master
        self.trigger_phrase = "overlord"
        self.running = False
        self.min_words = 1
        self.tts_speed = 1.1

        self.master.title("Voice Assistant")
        self.master.geometry("400x300")

        self.trigger_label = ttk.Label(
            self.master, text="Trigger Phrase:", font=("Arial", 12))
        self.trigger_label.grid(column=0, row=0, padx=10, pady=10)

        self.trigger_entry = ttk.Entry(self.master)
        self.trigger_entry.grid(column=1, row=0, padx=10, pady=10)
        self.trigger_entry.insert(tk.END, self.trigger_phrase)

        self.start_button = ttk.Button(
            self.master, text="Start", command=self.start_listening)
        self.start_button.grid(column=0, row=1, padx=10, pady=10)

        self.stop_button = ttk.Button(
            self.master, text="Stop", command=self.stop_listening)
        self.stop_button.grid(column=1, row=1, padx=10, pady=10)

        self.status_label = ttk.Label(
            self.master, text="Status: Stopped", font=("Arial", 12))
        self.status_label.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

        self.tts_speed_label = ttk.Label(
            self.master, text="TTS Speed:", font=("Arial", 12))
        self.tts_speed_label.grid(column=0, row=3, padx=10, pady=10)

        self.tts_speed_entry = ttk.Entry(self.master)
        self.tts_speed_entry.grid(column=1, row=3, padx=10, pady=10)
        self.tts_speed_entry.insert(tk.END, str(self.tts_speed))

        self.min_words_label = ttk.Label(
            self.master, text="Min Words:", font=("Arial", 12))
        self.min_words_label.grid(column=0, row=4, padx=10, pady=10)

        self.min_words_entry = ttk.Entry(self.master)
        self.min_words_entry.grid(column=1, row=4, padx=10, pady=10)
        self.min_words_entry.insert(tk.END, str(self.min_words))

        self.instructions_label = ttk.Label(
            self.master, text="Instructions:", font=("Arial", 12))
        self.instructions_label.grid(column=0, row=5, padx=10, pady=10)

        self.instructions_text = tk.Text(self.master, height=3, width=20)
        self.instructions_text.grid(column=1, row=5, padx=10, pady=10)

    def start_listening(self):
        if not self.running:
            self.running = True
            self.trigger_phrase = self.trigger_entry.get()
            self.tts_speed = float(self.tts_speed_entry.get())
            self.min_words = int(self.min_words_entry.get())
            self.instructions = self.instructions_text.get(1.0, tk.END).strip()
            self.status_label.config(text="Status: Running")
            self.listen_thread = threading.Thread(target=self.run_app)
            self.listen_thread.start()

    def stop_listening(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Stopped")

    def run_app(self):
        while self.running:
            text = listen_to_microphone()
            print(text)
            if self.trigger_phrase.lower() in text.lower() and len(text.split()) >= self.min_words:
                response = call_chat_gpt(text, self.instructions)
                text_to_speech(response, speed=self.tts_speed)
            elif text:
                print(
                    f"Phrase '{self.trigger_phrase}' not detected or minimum words not met, try again.")
            else:
                print("No speech detected, try again.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
