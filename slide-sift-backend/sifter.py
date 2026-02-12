import os
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

# Load environment variables from the local .env configuration file
load_dotenv()

# Global configuration for API authentication
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_text_from_pdf(pdf_path):
    """
    Parses a PDF document and returns the extracted text from all pages.
    
    Args:
        pdf_path (str): The file path to the target PDF.
        
    Returns:
        str: The extracted text or a descriptive error message.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error: Failed to extract text from PDF. Details: {e}"

def simplify_lecture(lecture_text, client):
    """
    Submits lecture text to the Gemini generative model for summarization.
    
    Args:
        lecture_text (str): The raw text extracted from the document.
        client (genai.Client): The authenticated Google GenAI client instance.
        
    Returns:
        str: The AI-generated simplified summary.
    """
    # System instructions to define the AI tutor's behavior
    instruction = (
        "You are SlideSift, an academic assistant. Your objective is to "
        "simplify complex university lecture notes. Use plain English, "
        "structured bullet points, and bold technical terminology."
    )
    
    # Generate content using the stable Gemini 2.5 Flash model
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"{instruction}\n\nLecture Content:\n{lecture_text}"
    )
    
    return response.text

if __name__ == "__main__":
    """
    Application entry point. Validates configuration and executes the 
    processing pipeline for the target file.
    """
    if not GEMINI_API_KEY:
        print("Error: The GEMINI_API_KEY is not defined in the environment.")
    else:
        # Initialize the GenAI client using the stable production API version
        client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options={'api_version': 'v1'}
        )
        
        # Target file must be located in the root project directory
        target_pdf = "lecture.pdf"
        
        if os.path.exists(target_pdf):
            print(f"Status: Processing {target_pdf}...")
            
            # Extract content and request simplified summary
            raw_content = extract_text_from_pdf(target_pdf)
            summary_output = simplify_lecture(raw_content, client)
            
            print("\n--- SIMPLIFIED NOTES ---\n")
            print(summary_output)
        else:
            print(f"Error: The file '{target_pdf}' was not found in the current directory.")