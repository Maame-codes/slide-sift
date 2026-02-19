import os
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

# Configure API Key internally (so app.py doesn't have to)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

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
        # SWITCHING TO TURBO MODE (Gemini 1.5 Flash)
        # This is the line that makes it 30s faster!
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = (
            "Summarize these lecture notes into a structured study guide "
            "with clear bullet points. Keep it concise:\n\n"
            f"{lecture_text}"
        )
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"AI Error: {str(e)}"