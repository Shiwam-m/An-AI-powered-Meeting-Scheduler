import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# AzureOpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
DEPLOYMENT_NAME = "gpt-4-km"  


def parse_meeting_details(natural_query):
    prompt = f"""
    Extract the following meeting details from this request:
    "{natural_query}"

    Respond ONLY with valid JSON in the following format (no explanations, no markdown, no extra text):

    {{
        "title": "...",
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "duration": "...",
        "participants": ["name1", "name2"],
        "platform": "..."

        "platform_link": "..."
    }}

    If any field is not mentioned, use a reasonable default or leave it blank (e.g., empty list or "Not specified").
    """

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=512
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").strip()
    if content.endswith("```"):
        content = content.replace("```", "").strip()

    print("🔍 Raw LLM output:", content)

    try:
        return json.loads(content)
    except Exception as e:
        print(" JSON parsing error:", e)
        return {
            "title": "Error parsing LLM response",
            "date": "",
            "time": "",
            "duration": "",
            "participants": [],
            "platform": ""
        }