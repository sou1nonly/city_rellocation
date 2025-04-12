# backend/advisor.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class RelocationAdvisor:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.embed_model = genai.GenerativeModel('embedding-001')
    
    def generate_response(self, prompt):
        return self.model.generate_content(prompt)
    
    def create_embeddings(self, text):
        return self.embed_model.embed_content(text)