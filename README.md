#  ChatGPT-Mini (Gemini API Powered Chatbot)

A Django-based chatgpt web app integrated with Google's Gemini API for generating smart and interactive responses.

---

## 🚀 Features
- Chat interface using Gemini 1.5 Flash API
- Django-powered backend
- Environment variable `.env` setup for secure API usage
- Voice message

---

## ⚙️ Setup Instructions

1. **Clone the repo**  
```bash
git clone https://github.com/Mishwacoder/Chatgpt-mini.git
cd Chatgpt-mini

2. Create virtual environment and install requirements
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3.Create a .env file
GEMINI_API_KEY=your_api_key_here

4.Run the project
python manage.py runserver

5.Open it with the url like:http://127.0.0.1:8000/register/
