import requests
import streamlit as st

# Cache translations so we don't ask the AI for the same word 50 times
@st.cache_data
def get_ai_translation(text, target_lang):
    # If target is English, or text is empty/None, return original
    if target_lang == "en" or not text or str(text).strip() == "":
        return text
    
    try:
        # We use MyMemory API (Free, No API Key required, uses Neural AI Translation)
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_lang}"
        response = requests.get(url, timeout=2)
        data = response.json()
        
        # Check if we got a valid response
        if 'responseData' in data and 'translatedText' in data['responseData']:
            translated = data['responseData']['translatedText']
            # Make sure it's not an error message
            if 'NO QUERY SPECIFIED' not in translated and 'ERROR' not in translated.upper():
                return translated
        
        # Return original text if translation fails or returns error
        return text
        
    except Exception:
        # If internet is down or any error occurs, return original English
        return text