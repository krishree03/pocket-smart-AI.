# PocketSmart AI
Smart Budget & Recommendation Assistant

FastAPI + Gemini AI budget recommendation project with Home, Party and Jewelry planners.

## Run
1. Install Python 3.10+
2. Create environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your Gemini API key.
6. Run: `uvicorn backend.main:app --reload`
7. Open: http://127.0.0.1:8000

Never upload `.env` or your API key to GitHub.
