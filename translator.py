import requests
import streamlit as st

# Cache translations so we don't ask the AI for the same word 50 times
@st.cache_data
def get_ai_translation(text, target_lang):
    # If offline or target is English, return original
    if target_lang == "en":
        return text
    
    try:
        # We use MyMemory API (Free, No API Key required, uses Neural AI Translation)
        # It supports: en, ar, fr, es, pt, ru, de, sw, zh
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_lang}"
        response = requests.get(url, timeout=2)  # 2 second timeout for offline speed
        data = response.json()
        
        if 'responseData' in data:  # ✅ FIXED: Added 'data' here
            return data['responseData']['translatedText']
        return text
    except Exception:
        # If internet is down (Offline), return original English
        return text