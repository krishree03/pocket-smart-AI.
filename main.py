import os
from typing import Optional
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:
    genai = None

load_dotenv()
app = FastAPI(title="PocketSmart AI")
templates = Jinja2Templates(directory="frontend")

def demo_recommendation():
    return """PocketSmart Demo Recommendation

1. Essential items - 60%
2. Style / decoration - 25%
3. Reserve - 15%

Add GEMINI_API_KEY to .env for live AI recommendations."""

def ask_gemini(prompt: str, image_bytes: Optional[bytes] = None, mime: str = "image/jpeg"):
    key = os.getenv("GEMINI_API_KEY")
    if not key or not genai:
        return demo_recommendation()
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        content = [prompt]
        if image_bytes:
            content.append({"mime_type": mime, "data": image_bytes})
        return model.generate_content(content).text
    except Exception:
        return demo_recommendation()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-home", response_class=HTMLResponse)
async def generate_home(request: Request, budget: float = Form(...), room: str = Form(...), style: str = Form(...), items: str = Form("")):
    prompt = f"""Create a practical home interior recommendation.
Budget: ₹{budget}; Room: {room}; Style: {style}; Required items: {items}.
Stay within budget. Give item, quantity, estimated price and total."""
    result = ask_gemini(prompt)
    return templates.TemplateResponse("result.html", {"request": request, "title": "Home Interior Recommendations", "result": result})

@app.post("/generate-party", response_class=HTMLResponse)
async def generate_party(request: Request, budget: float = Form(...), guests: int = Form(...), event: str = Form(...), venue: str = Form("")):
    prompt = f"""Plan a party within ₹{budget}.
Guests: {guests}; Event: {event}; Venue: {venue}.
Allocate budget across food, decoration, venue and entertainment."""
    result = ask_gemini(prompt)
    return templates.TemplateResponse("result.html", {"request": request, "title": "Party Budget Recommendations", "result": result})

@app.post("/generate-jewelry", response_class=HTMLResponse)
async def generate_jewelry(request: Request, budget: float = Form(...), occasion: str = Form(...), style: str = Form(...), image: Optional[UploadFile] = File(None)):
    image_bytes = None
    mime = "image/jpeg"
    if image:
        image_bytes = await image.read()
        mime = image.content_type or mime
    prompt = f"""Recommend jewelry within ₹{budget}.
Occasion: {occasion}; Preferred style: {style}.
If an outfit image is supplied, consider its colors and coordination.
Give 5 suggestions with estimated price ranges and reasons."""
    result = ask_gemini(prompt, image_bytes, mime)
    return templates.TemplateResponse("result.html", {"request": request, "title": "Jewelry Recommendations", "result": result})
