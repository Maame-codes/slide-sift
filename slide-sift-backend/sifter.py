import os
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq Client
# It automatically looks for "GROQ_API_KEY" in your environment
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

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
        # We use Llama-3.3-70b-versatile (Smart & Fast)
        # or llama3-8b-8192 (Insanely Fast)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful academic assistant."
                },
                {
                    "role": "user",
                    "content": (
                        "Summarize these lecture notes into a structured study guide "
                        "with clear bullet points. Keep it concise:\n\n"
                        f"{lecture_text}"
                    ),
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )

        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"AI Error: {str(e)}"