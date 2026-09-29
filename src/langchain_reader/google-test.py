import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

try:
    api_key = os.getenv("GEMINI_API_KEY")
except Exception as e:
    print(f"Error while parsing API key: {e}")
if not api_key: # type: ignore
    raise SystemExit("Google AI Studio API is not set. Check your .env file and try again.")


# model = init_chat_model("", temperature=0)
client = genai.Client(api_key=api_key)

# interaction = client.interactions.create(
#     model="gemini-3.1-flash-lite",
#     input="What is RAG"
# )

# # print("="*50)
# # print(interaction.output_text)
# # print("="*50)
# # print(interaction.usage)

stream = client.interactions.create(
    model="gemini-3.1-flash-lite",
    input="Explain how RAG works",
    stream=True
)

for event in stream:
    if event.event_type == "step.delta":
        if event.delta.type == "text":
            print(event.delta.text, end="")

