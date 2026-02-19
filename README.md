# Slide Sift

> Transform chaotic lecture slides into pristine, exam-ready study guides in under 2 seconds.

![Status](https://img.shields.io/badge/status-Live-success) ![AI Engine](https://img.shields.io/badge/AI-Groq%20%2F%20Llama--3-purple) ![Tech Stack](https://img.shields.io/badge/stack-Next.js%20%7C%20Flask%20%7C%20Python-blue)

## Live Demo

**[Try Slide Sift Here](https://slide-sift-backend.onrender.com)**
*(Note: The backend is hosted on a free instance. Please allow ~30 seconds for the initial "cold start" wake-up. Subsequent requests will be instant.)*

---

## The Problem

University students often struggle with "slide fatigue"—lecture PDFs are lengthy and difficult to revise from effectively. Imagine having an exam due in a week and having to read over 200 lecture slides? (Mission Impossible sorry). Manually summarizing 50+ slides into a study guide is time-consuming and prone to burnout.

## The Solution

Slide Sift is a full-stack AI application that ingests PDF lecture slides, extracts the raw text, and generates a structured, academic study guide. It identifies key concepts, defines technical terms, and highlights potential exam topics automatically.

---

## Technical Decision: Why Groq over Gemini?

During the development phase, I initially integrated Google Gemini Pro. While accurate, the latency was significant (45-60 seconds per document), which resulted in a poor user experience.

To solve this, I migrated the inference engine to Groq (running Llama-3).

* **Result:** Reduced processing time from ~50s to <2s.
* **Impact:** Near-instant feedback loop for students, allowing for real-time study sessions.
* **Trade-off:** This required strict prompt engineering to ensure Llama-3 maintained the same academic rigor as Gemini Pro.

---

## Architecture & Tech Stack

### Frontend (Client)
* **Next.js (React):** For a responsive, server-side rendered interface.
* **Tailwind CSS:** For modern, rapid UI development.
* **Axios:** For handling asynchronous API requests.
* **Deployment:** Vercel.

### Backend (Server)
* **Flask (Python):** A lightweight WSGI web application framework.
* **PyPDF:** Robust library for extracting text streams from PDF binaries.
* **Groq SDK:** High-performance AI inference.
* **Gunicorn:** Production-grade WSGI HTTP server.
* **Deployment:** Render.

---

## Local Setup Guide

### Prerequisites
* Node.js & npm
* Python 3.8+
* Git

### 1. Clone the Repository
```bash
git clone [https://github.com/Maame-codes/slide-sift.git](https://github.com/Maame-codes/slide-sift.git)
cd slide-sift
```
### 2. Backend Setup
```bash
cd slide-sift-backend
```
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
```bash
pip install -r requirements.txt
```

Configure Environment
```bash
Create a .env file and add your Groq API key:
GROQ_API_KEY=your_key_here
```

### 3. Frontend Setup
```bash
cd ../slide-sift-web
npm install
npm run dev
```
Visit http://localhost:3000 to run the app locally.

## Challenges & Learnings

### Cross-Origin Resource Sharing (CORS)
Debugging communication issues between the Vercel frontend and Render backend required configuring specific CORS headers in Flask.

### Dependency Management
Resolving version conflicts between `google-generativeai` and `groq` libraries during the migration phase.

### Stateless Architecture
Ensuring the backend remains stateless by processing files in memory or using temporary storage that is immediately cleaned up.

Built with ❤️ by [Maame](https://dev.to/maame-codes)
