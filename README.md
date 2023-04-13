# Voice Assistant

A Voice Assistant using OpenAI GPT-4 and speech recognition.

## Prerequisites

- Python 3
- ffmpeg
- OpenAI API Key (Please note that using the OpenAI API is not free.)
- A microphone

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/voice-assistant.git
cd voice-assistant
```

2. Install the requirements:

```bash
pip install -r requirements.txt
```

3. Obtain an OpenAI API key from the OpenAI website.

4. Add your OpenAI API key to api_key.txt

## Usage

```bash
python main.py
```

The app has two main tabs: "Settings" and "Instructions".

In the "Settings" tab, you can configure the trigger phrase, TTS speed, minimum number of words, microphone, and language.
In the "Instructions" tab, you can add instructions for the GPT model to follow when generating responses.

Press the "Start" button to begin listening. The app will listen for the trigger phrase followed by a command. The GPT model will then generate a response based on your command and the instructions you provided.

Press the "Stop" button to stop listening.
