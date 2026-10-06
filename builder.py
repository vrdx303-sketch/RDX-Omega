# ==========================================
# RDX JATKA BUILDER & OLLAMA BRIDGE (builder.py)
# [DESI HINDI ERROR & TIMEOUT HANDLER]
# ==========================================

import aiohttp
import json
import asyncio

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

async def query_usb_ollama(prompt: str) -> str:
    """Queries the local/USB Ollama instance securely with desi Hindi fallback."""
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": f"Strict instruction: Answer strictly in conversational and natural Hindi. Do not reply in English. User input: {prompt}",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 500
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OLLAMA_API_URL, json=payload, timeout=120) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "Bhai, samajh nahi aaya, kripya dobara boliye na!")
                else:
                    return "Arre laadle, server thoda garam ho gaya hai, kripya apna sawal hindi mein dobara bhejo!"
    except aiohttp.ClientConnectorError:
        return "Connection Fail! Pen drive wala Ollama server band pada hai ya port 11434 par connect nahi ho pa raha."
    except asyncio.TimeoutError:
        return "Connection Timeout! Pen drive se model load hone mein thoda time lag raha hai, ek baar dobara try kar le bhai!"
    except Exception as e:
        return f"Connection Fail ho gaya hai! Kripya thodi der baad dobara koshish karein."