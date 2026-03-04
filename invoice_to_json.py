
import os
import json
import re
from dotenv import load_dotenv
from google import genai
from prompt_template import build_prompt

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def clean_text(text):
    text = " ".join(text.split())
    return text[:6000]


def detect_document_type(text):
    text_lower = text.lower()

    if "booking confirmation" in text_lower:
        return "booking_confirmation"
    elif "invoice" in text_lower:
        return "invoice"
    else:
        return "unknown"


def convert_document_to_json(document_text: str) -> dict:

    cleaned_text = clean_text(document_text)
    doc_type = detect_document_type(cleaned_text)

    prompt = build_prompt(doc_type, cleaned_text)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0}
    )

    raw_output = response.text.strip()

    # Remove accidental markdown blocks if Gemini adds them
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        print("Invalid JSON returned from Gemini")
        print(raw_output)
        return {}