=============================================
PACS SUPPORT BOT v13 – GROK AI AUTO-DIAGNOSIS EDITION
=============================================
import streamlit as st
from openai import OpenAI
st.set_page_config(
page_title="PACS Helper Bot",
page_icon="🩺",
layout="wide",
initial_sidebar_state="collapsed"
)
=================== MEDICAL RADIOLOGY BACKGROUND ===================
background_image_url = "https://images.unsplash.com/photo-1551601645-2f9a2d7a2e2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80"  # High-quality subtle radiology modalities collage
st.markdown(f"""
<style>
    .main {{
        background: linear-gradient(to bottom, rgba(240,248,255,0.95), rgba(224,255,255,0.95)), 
                    url('{background_image_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
        padding: 2rem;
    }}
    .block-container {{
        background: rgba(255, 255, 255, 0.93);
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }}
    .big-title {{
        font-size: 4.5rem !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #00bfff, #20b2aa, #00fa9a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .friend-btn button {{
        background: linear-gradient(45deg, #20b2aa, #48d1cc, #00fa9a) !important;
        border-radius: 25px !important;
        box-shadow: 0 10px 25px rgba(32,178,170,0.3) !important;
    }}
    .step-box {{
        background: rgba(240,255,240,0.9);
        border-left: 8px solid #20b2aa;
    }}
    [data-testid="stChatMessageUser"] {{background: #e0ffff;}}
    [data-testid="stChatMessageAssistant"] {{background: #f0fff0;}}
    [dir="rtl"] {{direction: rtl; text-align: right;}}
</style>
""", unsafe_allow_html=True)
=================== XAI GROK API INTEGRATION ===================
client = None
ai_enabled = False
if st.secrets.get("XAI_API_KEY"):
client = OpenAI(
base_url="https://api.x.ai/v1",
api_key=st.secrets["XAI_API_KEY"]
)
ai_enabled = True
else:
st.warning("⚠️ Ajoutez votre XAI_API_KEY dans Secrets pour activer le diagnostic automatique par Grok xAI ! → https://x.ai/api")
=================== LANGUAGE SELECTOR ===================
if "language" not in st.session_state:
st.session_state.language = "Français"
lang_options = {"English": "en", "Français": "fr", "عربي": "ar"}
selected_lang = st.selectbox("🌍 Langue / Language / اللغة", list(lang_options.keys()), index=["en", "fr", "ar"].index(st.session_state.language))
st.session_state.language = selected_lang
lang_code = lang_options[selected_lang]
=================== TRANSLATIONS (same as v12) ===================
translations = { ... }  # Keep exactly the same dictionary as v12 (omitted here for brevity, copy-paste from previous version)
tr = translations[lang_code]
QUICK_FIXES = tr["quick_fixes"]
=================== GROK SYSTEM PROMPT (ENGLISH - Grok will translate perfectly) ===================
english_quick_fixes = translations["en"]["quick_fixes"]
system_prompt = """
You are PACS Helper Bot 🩺 – the smartest and friendliest PACS assistant in the world, now powered by Grok xAI.
You speak perfect English, Français, and عربي. ALWAYS reply in the exact language of the user's last message.
Be super warm, positive, encouraging, and use lots of emojis 😊🩺🔥🛠️📸
Rules:

Diagnose instantly and give the exact solution when you recognize the problem
NEVER invent solutions
ONLY use the solutions below – copy them exactly
Keep replies short, clear, with short lines and numbered steps
If server issue, always add: "If this persists >30 min, contact IT immediately!"

Exact solutions you MUST use:
""" + "\n\n".join([
f"### {info['name'].upper()}\nTriggers: {', '.join(triggers.split('|'))}\nSolution (copy exactly):\n{info['solution']}"
for triggers, info in english_quick_fixes.items()
]) + """
\nIf no perfect match → reply exactly: "Hmm, je n’ai pas bien compris... Mais pas de panique ! 😊 Essayez un des gros boutons ci-dessus ou décrivez-moi mieux le problème."
You can also say:

"Essayez d'abord la SOLUTION UNIVERSELLE ✨ (ça marche 97% du temps !)"
"Voulez-vous que je vous guide étape par étape ? → Cliquez sur 🧭 AIDE GUIDÉE"
"Besoin de tester le réseau ? → 🔌 TEST RÉSEAU"

Always stay friendly and professional.
"""
=================== HEADER ===================
dir_attr = ' dir="rtl"' if lang_code == "ar" else ""
st.markdown(f'<h1 class="big-title"{dir_attr}>{tr["title"]}', unsafe_allow_html=True)
powered = " 🚀 Powered by Grok xAI" if ai_enabled else ""
st.markdown(f"<h3 class='subheader'{dir_attr}>{tr['subheader']}{powered}", unsafe_allow_html=True)
st.markdown(f'######{dir_attr} {tr["prompt_hint"]}', unsafe_allow_html=True)
=================== REST OF FUNCTIONS (guided_checklist, network_check, show_resources) ===================
→ Keep exactly the same as v12 (copy-paste them here)
=================== MAIN BUTTONS ===================
→ Same as v12
=================== CHAT - NOW FULLY AI-POWERED BY GROK ===================
if "messages" not in st.session_state:
welcome = tr["chat_welcome"]
if ai_enabled:
welcome += "\n\n🚀 Diagnostic automatique par IA Grok activé ! Describez-moi le problème, je le résous en quelques secondes 😊"
st.session_state.messages = [{"role": "assistant", "content": welcome}]
for msg in st.session_state.messages:
with st.chat_message(msg["role"]):
st.markdown(msg["content"])
if prompt := st.chat_input(tr["chat_input"] + (" | Grok IA vous répond instantanément 🧠" if ai_enabled else "")):
st.session_state.messages.append({"role": "user", "content": prompt})
with st.chat_message("user"):
st.markdown(prompt)
with st.chat_message("assistant"):
spinner_texts = {
"en": "Grok is diagnosing... 🧠",
"fr": "Grok analyse le problème... 🧠",
"ar": "غروك يحلل المشكلة... 🧠"
}
with st.spinner(spinner_texts[lang_code]):
if ai_enabled:
Full conversation context
api_messages = [{"role": "system", "content": system_prompt}] + [
{"role": m["role"], "content": m["content"]} for m in st.session_state.messages
]
completion = client.chat.completions.create(
model="grok-beta",
messages=api_messages,
temperature=0.6,
max_tokens=600
)
reply = completion.choices[0].message.content
else:
Fallback keyword matching (multilingual)
found = False
user_lower = prompt.lower()
for triggers, info in QUICK_FIXES.items():
if any(t in user_lower for t in triggers.split("|")):
reply = f"→ {info['name']} détecté ! Voici la solution :\n\n{info['solution']}"
found = True
break
if not found:
reply = tr["not_found"]
st.markdown(reply)
st.session_state.messages.append({"role": "assistant", "content": reply})
=================== FOOTER ===================
powered_footer = " • Propulsé par Grok xAI 🧠" if ai_enabled else ""
st.markdown("---")
st.caption(f"Made with ❤️ for radiologists who deserve zero downtime {powered_footer} • Free forever • Share with your team! 🩺")
