from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    # यह जादुई कोड किसी भी तरह के यूट्यूब लिंक से सीधा 11-अक्षरों का Video ID निकाल लेगा
    pattern = r"(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_video_summary_data(video_url):
    """
    यह फंक्शन वीडियो का लिंक लेगा और उसका पूरा टेक्स्ट निकाल कर देगा।
    """
    video_id = get_video_id(video_url)
    
    if not video_id:
        return "⚠️ Error: लाडले, यह यूट्यूब का लिंक सही नहीं लग रहा।"
    
    try:
        # यूट्यूब से हिंदी ('hi') और इंग्लिश ('en') दोनों के सबटाइटल खींचने की कोशिश
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
        
        # सारे टुकड़ों को जोड़कर एक पूरी कहानी (पैराग्राफ) बनाना
        full_text = " ".join([item['text'] for item in transcript_list])
        
        return full_text
        
    except Exception as e:
        return f"⚠️ Shield Warning: इस वीडियो में सबटाइटल बंद हैं या कोई एरर आ गया।\nDetails: {str(e)}"

# सिर्फ टेस्टिंग के लिए (जब तू इस फाइल को रन करेगा)
if __name__ == "__main__":
    test_url = "https://youtu.be/yw02dHyP0K0" # वो पीसी बिल्ड वाली वीडियो
    print("Fetching data from YouTube...")
    data = get_video_summary_data(test_url)
    print("\n--- Video Text ---")
    print(data[:500] + "...\n(बाकी का टेक्स्ट इंजन को जाएगा)")