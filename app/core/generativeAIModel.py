import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

class GeminiService:
    def __init__(self, model_name: str = "gemini-1.5-flash", api_key: Optional[str] = None):
        
        self.api_key = api_key or os.getenv("GOOGLE_GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GOOGLE_GEMINI_API_KEY in .env or pass it explicitly.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_article(self, topic: str, format_instructions: str, word_count: int = 600) -> str:
        prompt = f"""
        Write a {word_count}-word article on the topic '{topic}'. 
        {format_instructions}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error generating article: {e}")
        
    def generate_content(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error generating content: {e}")
        
    def generate_lead_analysis(self, chats: str) -> list[dict]:
        try:
            prompt = f"""
            Analyze the following chat conversations to identify potential leads (users interested in buying a product or service or ready to book a meeting to look forward).
            For each chat, return a JSON object with:
            - from_id: string (the chat's from_id)
            - is_lead: boolean (true if the user is a potential lead, false otherwise)
            - reason: string (brief explanation of why the user is/isn't a lead)
            Return the response as a JSON array.
            Chats: {chats}
            Ensure the output is valid JSON.
            """

            response = self.model.generate_content(prompt)

            cleaned = response.text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip("`")
                if cleaned.lower().startswith("json"):
                    cleaned = cleaned[4:].strip()

            parsed = json.loads(cleaned) 
            return parsed

        except json.JSONDecodeError:
            raise RuntimeError("Invalid JSON response from Gemini model")
        except Exception as e:
            raise RuntimeError(f"Error generating lead analysis: {e}")
