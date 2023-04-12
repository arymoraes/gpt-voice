import openai
import sys

from audio import text_to_speech


class Gpt:
    def __init__(self):
        with open("api_key.txt", "r") as file:
            self.api_key = file.read().strip()
        openai.api_key = self.api_key

    def call_chat_gpt(self, input, instructions):
        text_to_speech("Please wait.")

        messages = [{"role": "system", "content": instructions}]
        messages.append({"role": "user", "content": input})

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
