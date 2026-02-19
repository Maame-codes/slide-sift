import os
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Error: GEMINI_API_KEY not found.")

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"PDF Error: {e}")
        return ""

def simplify_lecture(lecture_text):
    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt = (
            "You are an academic assistant. Summarize these lecture notes "
            "into a clean study guide with bullet points:\n\n"
            f"{lecture_text}"
        )
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"AI Error: {str(e)}"