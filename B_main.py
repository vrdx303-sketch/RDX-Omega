# ==========================================
# RDX JATKA ENGINE - GLOBAL MASTER SERVER (PORT 8001)
# Bounded to 0.0.0.0 + Full CORS for HTML Integration
# ==========================================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import sys
import re

from modules.sql_payload_handler import detect_and_counter_sql
from modules.counter_attack import launch_counter_attack, is_ip_blocked
from core.security import verify_master_access
from builder import query_usb_ollama
from database.recovery_manager import setup_database, save_chat, recover_data
from youtube_handler import get_video_summary_data

if not verify_master_access():
    print("[X] Access restricted. Master key required.")
    sys.exit(1)

app = FastAPI(title="RDX Global Jatka Engine", version="15.0")

setup_database()

# CORS Middleware - ताकी HTML फाइल सीधे इस पोर्ट पर रिक्वेस्ट मार सके बिना किसी रुकावट के
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    user_id = data.get("user_id", "rdx_master") 
    
    print(f"\n[GLOBAL STRIKE] IP: {client_ip} | User: {user_id} | Input: '{user_input}'")
    
    # SQL Shield Detection
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
        
    # YouTube Link Detection
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
            f"Based on the transcript above, please fulfill the user's request."
        )

    print("   [⚡ ROUTING TO USB-OLLAMA] Fetching sovereign AI response...")
    try:
        ai_response_text = await query_usb_ollama(final_ai_prompt)
    except Exception as e:
        ai_response_text = f"Ollama Bridge Error: {str(e)}"
    
    try:
        save_chat(user_id, user_input, ai_response_text)
    except Exception:
        pass
    
    return {
        "status": "SUCCESS",
        "response": ai_response_text,
        "engine": "RDX Jatka Sovereign Core (Global)"
    }

@app.get("/health")
async def health_check():
    return {"status": "ONLINE", "engine": "RDX Jatka Engine", "master": "Vikas RDX"}

if __name__ == "__main__":
    print("==================================================")
    print("   🌍 RDX GLOBAL JATKA ENGINE LIVE ON PORT 8001   ")
    print("==================================================")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)