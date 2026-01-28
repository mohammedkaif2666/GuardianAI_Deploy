# import os
# import json
# import asyncio
# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# from PIL import Image

# load_dotenv()
# # Pro members can utilize higher rate limits; ensure your API key is correctly linked in AI Studio.
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# # Gemini 2.5 Flash is recommended for its speed and multimodal accuracy in 2026.
# MODEL_NAME = "gemini-2.5-flash"

# SYSTEM_PROMPT = """
# You are Guardian AI. You are analyzing a chat screenshot for potential cyberbullying.
# 1. Identify all unique participants in the conversation.
# 2. Analyze the power dynamics: who is the aggressor and who is the target?
# 3. Look for subtle forms of bullying: sarcasm, isolation, or passive-aggressive threats.
# 4. Respond ONLY with this JSON structure:
# {
#   "is_bullying": boolean,
#   "severity": "None"|"Low"|"Medium"|"High"|"Critical",
#   "category": "Harassment"|"Hate Speech"|"Threats"|"Trolling"|"Exclusion"|"Other",
#   "reasoning": "Provide a human-like explanation. Quote specific speakers and their text to justify your verdict."
# }
# """

# async def analyze_with_gemini(text_input=None, image_path=None, retries=3):
#     contents = [SYSTEM_PROMPT]
#     if text_input: contents.append(f"Analyze: {text_input}")
#     if image_path:
#         img = Image.open(image_path)
#         contents.append(img)
#         contents.append("Analyze this entire chat for cyberbullying.")

#     for attempt in range(retries):
#         try:
#             # Generate content using the new 2026 SDK Client
#             response = client.models.generate_content(
#                 model=MODEL_NAME,
#                 contents=contents,
#                 config=types.GenerateContentConfig(response_mime_type="application/json")
#             )
#             return json.loads(response.text)
#         except Exception as e:
#             # Even with Pro, rare 429 errors may happen during peak server times.
#             if "429" in str(e) and attempt < retries - 1:
#                 wait_time = (attempt + 1) * 3
#                 await asyncio.sleep(wait_time)
#             else:
#                 print(f"❌ Gemini Error: {e}")
#                 return None







import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the 2026 stable model ID to avoid 404 errors
MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = """
You are Guardian AI. Analyze the input for cyberbullying.
Respond ONLY with this JSON structure:
{
  "is_bullying": boolean,
  "harm_score": number (A score from 0-100 representing toxicity/harm),
  "severity": "None"|"Low"|"Medium"|"High"|"Critical",
  "category": "Harassment"|"Hate Speech"|"Threats"|"Trolling"|"Exclusion"|"Other",
  "reasoning": "A professional analysis using 2-3 icon-friendly bullet points."
}
"""

async def analyze_with_gemini(text_input=None, image_path=None):
    contents = [SYSTEM_PROMPT]
    if text_input: contents.append(f"Analyze: {text_input}")
    if image_path: contents.append(Image.open(image_path))

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None