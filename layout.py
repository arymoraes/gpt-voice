import tkinter as tk
from tkinter import ttk

from audio import get_microphone_list


def create_layout(app):
    app.master.title("GPT Voice Assistant")
    app.master.geometry("500x500")
    app.master.protocol("WM_DELETE_WINDOW", app.on_close)

    app.notebook = ttk.Notebook(app.master)
    app.notebook.pack(expand=True, fill="both")

    app.settings_frame = ttk.Frame(app.notebook)
    app.instructions_frame = ttk.Frame(app.notebook)

    app.notebook.add(app.settings_frame, text="Settings")
    app.notebook.add(app.instructions_frame, text="Instructions")

    # Settings tab
    app.trigger_label = ttk.Label(
        app.settings_frame, text="Trigger Phrase:", font=("Arial", 12))
    app.trigger_label.grid(column=0, row=0, padx=10, pady=10)

    app.trigger_entry = ttk.Entry(app.settings_frame)
    app.trigger_entry.grid(column=1, row=0, padx=10, pady=10)
    app.trigger_entry.insert(tk.END, app.trigger_phrase)

    app.tts_speed_label = ttk.Label(
        app.settings_frame, text="TTS Speed:", font=("Arial", 12))
    app.tts_speed_label.grid(column=0, row=1, padx=10, pady=10)

    app.tts_speed_entry = ttk.Entry(app.settings_frame)
    app.tts_speed_entry.grid(column=1, row=1, padx=10, pady=10)
    app.tts_speed_entry.insert(tk.END, str(app.tts_speed))

    app.min_words_label = ttk.Label(
        app.settings_frame, text="Min Words:", font=("Arial", 12))
    app.min_words_label.grid(column=0, row=2, padx=10, pady=10)

    app.min_words_entry = ttk.Entry(app.settings_frame)
    app.min_words_entry.grid(column=1, row=2, padx=10, pady=10)
    app.min_words_entry.insert(tk.END, str(app.min_words))

    app.mic_list = get_microphone_list()

    app.mic_label = ttk.Label(
        app.settings_frame, text="Microphone:", font=("Arial", 12))
    app.mic_label.grid(column=0, row=3, padx=10, pady=10)

    app.selected_mic = tk.StringVar(app.settings_frame)
    app.selected_mic.set(app.mic_list[0])

    app.mic_menu = ttk.OptionMenu(
        app.settings_frame, app.selected_mic, *app.mic_list)
    app.mic_menu.grid(column=1, row=3, padx=10, pady=10)

    # Instructions tab
    app.instructions_label = ttk.Label(
        app.instructions_frame, text="Instructions:", font=("Arial", 12))
    app.instructions_label.pack(side="top", padx=10, pady=10)

    app.instructions_text = tk.Text(
        app.instructions_frame, height=10, width=40)
    app.instructions_text.pack(side="top", padx=10, pady=10)

    app.start_button = ttk.Button(
        app.master, text="Start", command=app.start_listening)
    app.start_button.pack(side="left", padx=10, pady=10)
    app.stop_button = ttk.Button(
        app.master, text="Stop", command=app.stop_listening)
    app.stop_button.pack(side="left", padx=10, pady=10)

    app.status_label = ttk.Label(
        app.master, text="Status: Stopped", font=("Arial", 12))
    app.status_label.pack(side="left", padx=10, pady=10)

    app.language_label = ttk.Label(
        app.settings_frame, text="Language:", font=("Arial", 12))
    app.language_label.grid(column=0, row=4, padx=10, pady=10)

    app.selected_language = tk.StringVar(app.settings_frame)
    app.selected_language.set(app.language)

    app.language_menu = ttk.OptionMenu(
        app.settings_frame, app.selected_language, *["en", "en", "pt-BR"])
    app.language_menu.grid(column=1, row=4, padx=10, pady=10)
