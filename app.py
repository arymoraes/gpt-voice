import tkinter as tk
from tkinter import ttk
import threading
from gpt import Gpt
import speech_recognition as sr
import json

from audio import listen_to_microphone, text_to_speech
from layout import create_layout


class App:
    def __init__(self, master):
        self.master = master
        self.trigger_phrase = "overlord"
        self.running = False
        self.language = "en"
        self.min_words = 1
        self.tts_speed = 1.1
        self.gpt = Gpt()

        create_layout(self)

        self.load_settings()

    def load_settings(self, settings_file="settings.json"):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
                self.trigger_entry.delete(0, tk.END)
                self.trigger_entry.insert(tk.END, settings["trigger_phrase"])

                self.min_words_entry.delete(0, tk.END)
                self.min_words_entry.insert(tk.END, str(settings["min_words"]))

                self.tts_speed_entry.delete(0, tk.END)
                self.tts_speed_entry.insert(tk.END, str(settings["tts_speed"]))

                self.selected_mic.set(settings["selected_mic"])

                self.instructions_text.delete(1.0, tk.END)
                self.instructions_text.insert(tk.END, settings["instructions"])

                self.language.set(settings["language"])
        except FileNotFoundError:
            print(
                f"Settings file '{settings_file}' not found. Using default settings.")
        except Exception as e:
            print(f"Error loading settings: {e}. Using default settings.")

    def on_close(self):
        self.save_settings()
        self.master.destroy()

    def run_app(self):
        selected_mic_index = self.mic_list.index(self.selected_mic.get())
        while self.running:
            text = listen_to_microphone(selected_mic_index, [self.language])
            print(text)
            if not self.master.winfo_exists():
                break

            if self.trigger_phrase.lower() in text.lower() and len(text.split()) >= self.min_words:
                # remove the trigger phrase from the text, regardless of casing
                text = text.replace(self.trigger_phrase, "", 1)
                response = self.gpt.call_chat_gpt(text, self.instructions)
                text_to_speech(response, speed=self.tts_speed,
                               lang=self.language)
            elif text:
                print(
                    f"Phrase '{self.trigger_phrase}' not detected or minimum words not met, try again.")
            else:
                print("No speech detected, try again.")

    def save_settings(self, settings_file="settings.json"):
        settings = {
            "trigger_phrase": self.trigger_entry.get(),
            "min_words": int(self.min_words_entry.get()),
            "tts_speed": float(self.tts_speed_entry.get()),
            "selected_mic": self.selected_mic.get(),
            "instructions": self.instructions_text.get(1.0, tk.END).strip(),
            "language": self.language
        }

        with open(settings_file, "w") as f:
            json.dump(settings, f)

    def start_listening(self):
        if not self.running:
            self.running = True
            self.trigger_phrase = self.trigger_entry.get()
            self.tts_speed = float(self.tts_speed_entry.get())
            self.min_words = int(self.min_words_entry.get())
            self.instructions = self.instructions_text.get(1.0, tk.END).strip()
            self.language = self.selected_language.get()
            self.status_label.config(text="Status: Running")
            self.listen_thread = threading.Thread(target=self.run_app)
            self.listen_thread.start()

    def stop_listening(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Stopped")
