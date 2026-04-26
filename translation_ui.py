import streamlit as st

# Initialize once
def init_translation():
    if 'lang' not in st.session_state:
        st.session_state.lang = 'en'
    if 'translate_mode' not in st.session_state:
        st.session_state.translate_mode = True

# Translator loader
def get_translator():
    if st.session_state.translate_mode:
        try:
            from translator import get_ai_translation
            return get_ai_translation
        except ImportError:
            pass
    return lambda text, lang: text

# Helper function
def t(text):
    translator = get_translator()
    return translator(text, st.session_state.lang)

# Sidebar UI
def render_translation_sidebar():
    st.session_state.translate_mode = st.toggle(
        t("🌐 Enable AI Translation"),
        value=st.session_state.translate_mode
    )

    # 🌍 MASSIVE LANGUAGE SET
    lang_options = {

        # ===== DEFAULT / GLOBAL =====
        "en": "English",
        "ar": "العربية",
        "zh": "中文",

        # ===== 20 EUROPEAN LANGUAGES =====
        "fr": "Français",
        "es": "Español",
        "pt": "Português",
        "de": "Deutsch",
        "it": "Italiano",
        "nl": "Nederlands",
        "pl": "Polski",
        "sv": "Svenska",
        "no": "Norsk",
        "da": "Dansk",
        "fi": "Suomi",
        "cs": "Čeština",
        "sk": "Slovenčina",
        "hu": "Magyar",
        "ro": "Română",
        "bg": "Български",
        "el": "Ελληνικά",
        "uk": "Українська",
        "hr": "Hrvatski",
        "sr": "Srpski",

        # ===== 20 AFRICAN LANGUAGES =====
        "sw": "Kiswahili",
        "am": "አማርኛ",
        "ha": "Hausa",
        "yo": "Yorùbá",
        "ig": "Igbo",
        "zu": "isiZulu",
        "xh": "isiXhosa",
        "af": "Afrikaans",
        "st": "Sesotho",
        "tn": "Setswana",
        "ts": "Xitsonga",
        "ve": "Tshivenda",
        "rw": "Kinyarwanda",
        "rn": "Kirundi",
        "lg": "Luganda",
        "so": "Soomaali",
        "ff": "Fula",
        "wo": "Wolof",
        "bm": "Bambara",
        "ny": "Chichewa",

        # ===== 10 OTHER GLOBAL LANGUAGES =====
        "hi": "हिन्दी",
        "bn": "বাংলা",
        "ja": "日本語",
        "ko": "한국어",
        "tr": "Türkçe",
        "fa": "فارسی",
        "id": "Bahasa Indonesia",
        "ms": "Bahasa Melayu",
        "th": "ไทย",
        "vi": "Tiếng Việt"
    }

    selected_lang = st.selectbox(
        t("Select Language"),
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(st.session_state.lang)
    )

    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    # RTL support (expandable if needed later)
    if st.session_state.lang in ["ar", "fa"]:
        st.markdown("""
        <style>
        .stApp { direction: rtl; text-align: right; }
        </style>
        """, unsafe_allow_html=True)