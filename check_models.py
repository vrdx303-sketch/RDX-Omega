import httpx
import json
import os

API_STORE_FILE = os.path.abspath("./api_store.json")

def check_available_models():
    if not os.path.exists(API_STORE_FILE):
        print("[❌ ERROR] api_store.json file nahi mili!")
        return

    with open(API_STORE_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
        api_key = config.get("gemini_api_key", "").strip()

    if not api_key or api_key == "YAHAN_APNI_GEMINI_API_KEY_DAL_DE":
        print("[❌ ERROR] Pehle api_store.json mein apni valid Gemini API Key daal!")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    print("[🔍 SCANNING] Google server se pooch rahe hain ki kaun-kaun se models available hain...")
    try:
        response = httpx.get(url, timeout=10.0)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"\n[✅ SUCCESS] Total Models Found: {len(models)}\n")
            for m in models:
                print(f" -> Model Name: {m.get('name')}")
                print(f"    Supported Methods: {m.get('supportedGenerationMethods')}")
                print("-" * 50)
        else:
            print(f"\n[❌ API ERROR {response.status_code}]: {response.text}")
    except Exception as e:
        print(f"[❌ EXCEPTION]: {e}")

if __name__ == "__main__":
    check_available_models()