import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
# Import the logic functions from our sifter module
from sifter import extract_text_from_pdf, simplify_lecture

# Initialize Flask and load environment variables
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the frontend
load_dotenv()

@app.route('/sift', methods=['POST'])
def sift_slides():
    """
    API endpoint that receives a PDF file, extracts text, 
    and returns AI-generated simplified notes.
    """
    temp_path = "temp_lecture.pdf"

    try:
        # 1. Validate that a file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # 2. Save the file temporarily
        file.save(temp_path)
        
        # 3. Process the file
        # Step A: Extract text from the PDF
        text = extract_text_from_pdf(temp_path)
        
        if not text:
            return jsonify({"error": "Could not extract text from PDF"}), 400

        # Step B: Send text to Gemini for summarization
        # Note: We only pass the text now; authentication is handled in sifter.py
        summary = simplify_lecture(text)
        
        return jsonify({"summary": summary})
    
    except Exception as e:
        # Log the error for debugging and return a server error
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    # Run the server
    # Note: debug=True is for development only
    app.run(debug=True, port=5000)