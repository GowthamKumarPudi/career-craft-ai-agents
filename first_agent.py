import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Your first agent
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='You are a career guidance AI agent. Introduce yourself briefly!'
)

print(response.text)
