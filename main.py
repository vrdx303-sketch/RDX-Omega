# ==========================================
# RDX JATKA ENGINE - GLOBAL MASTER SERVER (PORT 8001)
# Bounded to 0.0.0.0 + Public Jinja2 Web Portal + Dual Engine Integration
# ==========================================

from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import sys
import re
import json
import os

from modules.sql_payload_handler import detect_and_counter_sql
from modules.counter_attack import launch_counter_attack, is_ip_blocked
from core.security import verify_master_access
from builder import query_usb_ollama
from database.recovery_manager import setup_database, save_chat, recover_data
from youtube_handler import get_video_summary_data

if not verify_master_access():
    print("[X] Access restricted. Master key required.")
    sys.exit(1)

app = FastAPI(title="RDX Global Jatka Sovereign Engine", version="14.0")

# Database Setup
setup_database()

# Static & Templates setup for public web UI
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIG_FILE = "config/tunnel_url.json"

def update_active_tunnel_url(url: str):
    os.makedirs("config", exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"jatka_engine_url": url, "updated_at": time.time()}, f)

@app.get("/", response_class=HTMLResponse)
async def serve_public_portal(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/config")
async def get_engine_config():
    current_url = "https://san-single-import-bedrooms.trycloudflare.com" # Active Tunnel URL from your terminal
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                current_url = data.get("jatka_engine_url", current_url)
        except:
            pass
    return {"status": "SUCCESS", "jatka_engine_url": current_url, "studio_url": "https://jam-town-photographic-chat.trycloudflare.com"}

@app.options("/api/v1/query")
async def options_query():
    return JSONResponse(status_code=200, content={"status": "OK"})

@app.post("/api/v1/query")
async def process_engine_request(request: Request):
    client_ip = request.client.host
    
    if is_ip_blocked(client_ip):
        return JSONResponse(
            status_code=200,
            content={
                "status": "IP_BLOCKED",
                "message": "IP blocked. Nikal bhosdike attack karke!"
            }
        )

    try:
        data = await request.json()
    except Exception:
        data = {}
        
    user_input = data.get("prompt", "")
    user_id = data.get("user_id", "vikas") 
    
    print(f"\n[GLOBAL STRIKE] IP: {client_ip} | User: {user_id} | Input: '{user_input}'")
    
    try:
        is_attack = detect_and_counter_sql(user_input)
    except Exception:
        is_attack = False
        
    if is_attack:
        print("   [🛡️ SHIELD TRIGGERED] Malicious SQL Payload Caught!")
        launch_counter_attack(client_ip, time.time_ns())
        return JSONResponse(
            status_code=200,
            content={
                "status": "ATTACK_HANDLED",
                "message": "Abe aur mar le SQL is type box mein, teri gaand mein dam hai toh! Ye vikas ka system hai, hilta nahi hila deta hai."
            }
        )
        
    yt_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
    yt_match = re.search(yt_pattern, user_input)
    final_ai_prompt = user_input  
    
    if yt_match:
        video_url = yt_match.group(1)
        print(f"   [🎥 YOUTUBE DETECTED] Extracting data from: {video_url}")
        video_text = get_video_summary_data(video_url)
        final_ai_prompt = (
            f"User request: {user_input}\n\n"
            f"Here is the transcript of the YouTube video the user provided:\n"
            f"--- START VIDEO TRANSCRIPT ---\n{video_text}\n--- END VIDEO TRANSCRIPT ---\n\n"
            f"Humein iska jawab bilkul short aur Hindi mein dena hai."
        )

    # Force concise and Hindi response instruction
    system_instruction = "Answer concisely and strictly in Hindi: "
    ai_response_text = await query_usb_ollama(system_instruction + final_ai_prompt)
    
    try:
        save_chat(user_id, user_input, ai_response_text)
    except Exception as e:
        print(f"   [X] DB Save Error: {e}")
    
    return {
        "status": "SUCCESS",
        "response": ai_response_text,
        "engine": "RDX Jatka Sovereign Core (Global)"
    }

@app.get("/health")
async def health_check():
    return {"status": "ONLINE", "engine": "RDX Jatka Engine", "master": "Vikas RDX"}

if __name__ == "__main__":
    update_active_tunnel_url("https://san-single-import-bedrooms.trycloudflare.com")
    print("==================================================")
    print("   🌍 RDX GLOBAL JATKA ENGINE LIVE ON PORT 8001   ")
    print("==================================================")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)