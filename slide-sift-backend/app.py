import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from sifter import extract_text_from_pdf, simplify_lecture
from dotenv import load_dotenv

# Initialize Flask and load environment variables
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing
load_dotenv()

# Setup GenAI Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={'api_version': 'v1'}
)

@app.route('/sift', methods=['POST'])
def sift_slides():
    """
    API endpoint that receives a PDF file and returns simplified notes.
    """
    # Check if a file was sent in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    # Save file temporarily to process it
    temp_path = "temp_lecture.pdf"
    file.save(temp_path)
    
    try:
        # Step 1: Extract Text
        text = extract_text_from_pdf(temp_path)
        
        # Step 2: Simplify with Gemini
        summary = simplify_lecture(text)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return jsonify({"summary": summary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(debug=True, port=5000)