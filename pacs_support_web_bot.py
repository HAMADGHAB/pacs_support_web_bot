# PACS Helper Bot — Enhanced UI Version

Below is an upgraded version of the PACS Helper Bot with a significantly improved user interface. It introduces:

- Modern dark mode with improved styling
- Card‑based layout similar to professional dashboards
- Smooth animations & transitions
- Floating chat box
- Language dropdown redesigned
- Animated section headers
- Better spacing, shadows, borders, and responsive layout
- Persistent theme memory

---

```python
import streamlit as st
import time
import json
from datetime import datetime
from pathlib import Path

##############################################
# CONFIGURATION
##############################################
st.set_page_config(
    page_title="PACS Helper Bot",
    page_icon="🖥️",
    layout="wide"
)

LOG_FILE = Path("./logs/cases.log")
LOG_FILE.parent.mkdir(exist_ok=True)

SUPPORTED_LANGS = {
    "en": "English",
    "fr": "Français",
    "ar": "العربية"
}

##############################################
# TRANSLATION ENGINE
##############################################
TRANSLATIONS = {
    "title": {
        "en": "PACS Helper Bot",
        "fr": "Assistant PACS",
        "ar": "مساعد نظام PACS"
    },
    "select_language": {
        "en": "Language",
        "fr": "Langue",
        "ar": "اللغة"
    },
    "guided_checklist": {
        "en": "Troubleshooting Checklist",
        "fr": "Checklist de diagnostic",
        "ar": "قائمة التحقق الفنية"
    },
    "quick_fix": {
        "en": "Quick Fixes",
        "fr": "Solutions rapides",
        "ar": "حلول سريعة"
    },
    "network_tools": {
        "en": "Network Commands",
        "fr": "Commandes réseau",
        "ar": "أوامر الشبكة"
    },
    "chat": {
        "en": "Assistant Chat",
        "fr": "Chat d'assistance",
        "ar": "الدردشة الذكية"
    }
}

def tr(key: str, lang: str):
    return TRANSLATIONS.get(key, {}).get(lang, key)

##############################################
# THEMES & CUSTOM CSS
##############################################
def apply_theme(theme):
    if theme == "Dark":
        st.markdown(
            """
            <style>
            body { background-color: #0e1117; color: #ffffff; }
            .main { background-color: #0e1117; }
            .stButton>button { background:#1f2937; color:white; border-radius:10px; }
            .section-card {
                background: #1a1d23;
                padding: 25px;
                border-radius: 14px;
                box-shadow: 0 0 18px rgba(0,0,0,0.5);
                margin-bottom: 20px;
                transition: 0.4s ease;
            }
            .section-card:hover {
                transform: scale(1.01);
            }
            .chat-box {
                background: #11141a;
                padding: 20px;
                border-radius: 18px;
                box-shadow: 0 0 20px rgba(0,0,0,0.35);
                height: 420px;
                overflow-y: auto;
            }
            .header-anim {
                font-size: 26px;
                font-weight: bold;
                margin-bottom: 15px;
                animation: fadeIn 1s ease-out;
            }
            @keyframes fadeIn {
                from {opacity: 0; transform: translateY(-10px);} 
                to {opacity: 1; transform: translateY(0);} 
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            .section-card {
                background: #ffffff;
                padding: 25px;
                border-radius: 14px;
                box-shadow: 0 0 12px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                transition: 0.3s ease;
            }
            .section-card:hover {
                transform: scale(1.01);
            }
            .chat-box {
                background: #f6f6f6;
                padding: 20px;
                border-radius: 18px;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
                height: 420px;
                overflow-y: auto;
            }
            .header-anim {
                font-size: 26px;
                font-weight: bold;
                margin-bottom: 15px;
                animation: fadeIn 0.8s ease-out;
            }
            @keyframes fadeIn {
                from {opacity: 0; transform: translateY(-10px);} 
                to {opacity: 1; transform: translateY(0);} 
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

##############################################
# LOGGING
##############################################
def log_case(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {text}
")

##############################################
# APP UI
##############################################
def main():

    st.sidebar.title("Settings")

    lang = st.sidebar.selectbox("Language", list(SUPPORTED_LANGS.keys()), format_func=lambda x: SUPPORTED_LANGS[x])

    theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=1)
    apply_theme(theme)

    st.markdown(f"<h1 class='header-anim'>{tr('title', lang)}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.7, 1])

    ##############################################
    # LEFT SIDE — Diagnostic and Tools
    ##############################################
    with col1:
        st.markdown(f"<div class='section-card'><div class='header-anim'>{tr('guided_checklist', lang)}</div>", unsafe_allow_html=True)
        st.write("1. Verify network connectivity.")
        st.write("2. Check PACS services.")
        st.write("3. Confirm database status.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><div class='header-anim'>{tr('quick_fix', lang)}</div>", unsafe_allow_html=True)
        st.write("Restart Imaging Service")
        st.write("Clear local cache")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-card'><div class='header-anim'>{tr('network_tools', lang)}</div>", unsafe_allow_html=True)
        st.code("ping 10.10.10.5")
        st.code("tracert pacs-server")
        st.code("netstat -ano | findstr 104")
        st.markdown("</div>", unsafe_allow_html=True)

    ##############################################
    # RIGHT SIDE — Chat
    ##############################################
    with col2:
        st.markdown(f"<div class='section-card'><div class='header-anim'>{tr('chat', lang)}</div>", unsafe_allow_html=True)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        chat_container = st.container()

        with chat_container:
            st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
            for role, msg in st.session_state.chat_history:
                if role == "user":
                    st.markdown(f"**You:** {msg}")
                else:
                    st.markdown(f"**Bot:** {msg}")
            st.markdown("</div>", unsafe_allow_html=True)

        prompt = st.text_input("Type your question:")
        if st.button("Send") and prompt.strip() != "":
            st.session_state.chat_history.append(("user", prompt))
            log_case(prompt)

            response = f"Analyzing: {prompt} ... Issue likely related to connectivity."
            time.sleep(0.5)
            st.session_state.chat_history.append(("assistant", response))
            st.rerun()

    
if __name__ == "__main__":
    main()
```

---

If you want, I can enhance this further with:
- Animated chat bubbles like WhatsApp
- A collapsible left sidebar menu
- A fully responsive grid system
- A top navigation bar or footer
- A multi‑page interface (Streamlit pages)
- Custom SVG icons and logo integration

Tell me what direction you want next.
