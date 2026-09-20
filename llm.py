import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def llm(instructions, user_prompt, model="gemini-3.8-flash"):

    interaction = client.interactions.create(
        model=model,
        system_instruction=instructions,
        input=user_prompt
    )

    return interaction.output_text