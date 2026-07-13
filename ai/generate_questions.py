import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv("key.env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_questions(subject):

    prompt = f"""
Generate 5 multiple choice questions for {subject}.

Return ONLY valid JSON.

Format:

[
  {{
    "question":"Question",
    "options":["A","B","C","D"],
    "answer":"Correct Answer"
  }}
]
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json","").replace("```","").strip()

    return json.loads(text)