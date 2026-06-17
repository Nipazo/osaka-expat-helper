# 🏯 Osaka Expat Helper

AI-powered service for translating Japanese official documents for expats in Osaka.

## 🚀 Features
- Upload images of official Japanese documents
- AI-powered text recognition (GPT-4o)
- English translation
- Key action points and deadlines extraction

## 🛠️ Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- AI: OpenAI GPT-4o

## 📦 Local Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python app.py
