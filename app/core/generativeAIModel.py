import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

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