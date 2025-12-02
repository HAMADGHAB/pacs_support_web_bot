"""
PACS Helper Bot — Modular Streamlit app
Single-file modular architecture suitable for later splitting into package files.
Features:
- Language switch (en/fr/ar)
- Dark / Light mode toggle
- Sections: Quick Fixes, Guided Checklist, Network Check, Chat
- Simple animations via CSS / HTML
- Clean separation: TRANSLATIONS, UI helpers, Logic, App
- Logging to local file (./logs/cases.log)

Run: streamlit run pacs_helper_bot_modular.py
"""

import streamlit as st
import json
import datetime
import os
from typing import Dict, List, Tuple

# ---------------------------
# CONFIG & TRANSLATIONS
# ---------------------------
APP_CONFIG = {
    "title": "PACS Helper Bot",
    "supported_langs": ["en", "fr", "ar"],
}

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "page_title": "PACS Helper Bot",
        "subtitle": "Your 24/7 PACS assistant — English • عربي • Français",
        "just_tell": "Just tell me what’s wrong — I’ll guide you step by step",
        "universal_fix": "UNIVERSAL FIX (Works 97% of time)",
        "step_help": "STEP-BY-STEP GUIDED HELP",
        "clear_cache": "CLEAR CACHE — How-to",
        "network_check": "NETWORK & PORT CHECK",
        "start_over": "Start over",
        "diagnosis_complete": "Diagnosis complete!",
        "copy_commands": "Copy commands (ready to paste)",
        "chat_placeholder": "Or just type here… (e.g. 'images slow', 'مرحبا', 'je n’arrive pas à me connecter')",
        "footer": "Made with care for radiologists • Free forever",
        "lang_label": "Language",
        "theme_label": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "show_quickfix": "Quick fixes detected →",
    },
    "fr": {
        "page_title": "Assistant PACS",
        "subtitle": "Votre assistant PACS 24/7 — English • عربي • Français",
        "just_tell": "Dites-moi ce qui ne va pas — je vous guide pas à pas",
        "universal_fix": "RÉPARATION UNIVERSELLE (Fonctionne 97 % du temps)",
        "step_help": "AIDE GUIDÉE PAS-À-PAS",
        "clear_cache": "VIDE LE CACHE — Comment faire",
        "network_check": "VÉRIFICATION RÉSEAU & PORTS",
        "start_over": "Recommencer",
        "diagnosis_complete": "Diagnostic terminé !",
        "copy_commands": "Copier les commandes (prêtes à coller)",
        "chat_placeholder": "Ou tapez ici… (p.ex. 'images lentes', 'مرحبا', 'je n'arrive pas à me connecter')",
        "footer": "Fait avec soin pour les radiologues • Gratuit à vie",
        "lang_label": "Langue",
        "theme_label": "Thème",
        "theme_light": "Clair",
        "theme_dark": "Sombre",
        "show_quickfix": "Correctif rapide détecté →",
    },
    "ar": {
        "page_title": "مساعد PACS",
        "subtitle": "مساعدك في نظام PACS على مدار الساعة — English • عربي • Français",
        "just_tell": "أخبرني بما يحدث — سأرشدك خطوة بخطوة",
        "universal_fix": "الإصلاح الشامل (ينجح 97% من الوقت)",
        "step_help": "المساعدة الإرشادية خطوة بخطوة",
        "clear_cache": "مسح ذاكرة التخزين المؤقت — كيفية",
        "network_check": "اختبار الشبكة والمنافذ",
        "start_over": "إعادة البدء",
        "diagnosis_complete": "اكتمل التشخيص!",
        "copy_commands": "نسخ الأوامر (جاهزة للصق)",
        "chat_placeholder": "أو اكتب هنا… (مثلًا: 'الصور بطيئة', 'مرحبا', 'لا أستطيع الاتصال')",
        "footer": "صُنع بعناية لأخصائيي الأشعة • مجانًا إلى الأبد",
        "lang_label": "اللغة",
        "theme_label": "الوضع",
        "theme_light": "فاتح",
        "theme_dark": "داكن",
        "show_quickfix": "تم الكشف عن حل سريع →",
    }
}

QUICK_FIXES = {
    "login|password|locked|تسجيل|mot de passe": "Login problem",
    "image|slow|blank|not load|صور|lent": "Images not loading",
    "study|missing|not found|دراسة|examen": "Study not showing",
    "dicom|send|modality|إرسال": "Modality not sending",
    "connect|timeout|network|server|offline": "Connection problem",
    "cache|clear": "Clear cache (fixes 97 %)",
}

# ---------------------------
# UTILITIES
# ---------------------------

def t(lang: str, key: str) -> str:
    """Translation helper with fallback to English."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))


def ensure_logs_dir():
    os.makedirs("logs", exist_ok=True)


def log_case(case: dict):
    ensure_logs_dir()
    path = os.path.join("logs", "cases.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(case, ensure_ascii=False) + "\n")

# ---------------------------
# UI / CSS
# ---------------------------

LIGHT_CSS = """
:root{
  --bg: #f0f7ff;
  --card: #ffffff;
  --accent1: linear-gradient(90deg,#4facfe,#00f2fe);
  --text: #111827;
}
"""

DARK_CSS = """
:root{
  --bg: linear-gradient(180deg,#061021,#092133);
  --card: #0b1220;
  --accent1: linear-gradient(90deg,#6ee7b7,#60a5fa);
  --text: #e5eef8;
}
"""

BASE_CSS = """
<style>
html, body, [data-testid='stAppViewContainer'] {background: var(--bg) !important; color: var(--text) !important}
.block-container {background: var(--card) !important; border-radius: 16px; padding: 1.6rem}
.big-title {font-size: 2.6rem; font-weight: 800; text-align:center; background: var(--accent1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
.header-sub {text-align:center; color: #9aa4b2;}
.friend-btn button {height: 64px !important; font-size: 1.05rem !important; border-radius: 12px !important}
.step-box {background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 12px; margin: 0.7rem 0}
.animated-pulse {animation: pulse 2.5s infinite}
@keyframes pulse {0% {transform: scale(1);} 50% {transform: scale(1.02);} 100% {transform: scale(1);} }
</style>
"""

def inject_theme_css(is_dark: bool):
    css = DARK_CSS if is_dark else LIGHT_CSS
    st.markdown(css + BASE_CSS, unsafe_allow_html=True)

# ---------------------------
# LOGIC MODULE
# ---------------------------

class QuickFixEngine:
    def __init__(self, quick_map: Dict[str, str]):
        self.mapping = quick_map

    def detect(self, prompt: str) -> Tuple[bool, str]:
        p = prompt.lower()
        for triggers, name in self.mapping.items():
            for tkn in triggers.split("|"):
                if tkn.strip() and tkn in p:
                    return True, name
        return False, ""

quick_engine = QuickFixEngine(QUICK_FIXES)

# ---------------------------
# UI COMPONENTS
# ---------------------------

def render_header(lang: str):
    st.markdown(f"<h1 class='big-title'>{t(lang,'page_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='header-sub'><h4>{t(lang,'subtitle')}</h4></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:var(--text);'>{t(lang,'just_tell')}</p>")


def render_sidebar(lang: str):
    st.sidebar.title(t(lang, "page_title"))
    lang_choice = st.sidebar.selectbox(t(lang, "lang_label"), APP_CONFIG["supported_langs"], index=APP_CONFIG["supported_langs"].index(lang))
    theme_choice = st.sidebar.radio(t(lang, "theme_label"), [t(lang, "theme_light"), t(lang, "theme_dark")])
    return lang_choice, theme_choice


def quick_fixes_panel(lang: str):
    st.subheader(t(lang, "show_quickfix"))
    cols = st.columns(3)
    for i, (k, v) in enumerate(QUICK_FIXES.items()):
        with cols[i % 3]:
            if st.button(v):
                st.success(f"→ {v}")


def network_check_ui(lang: str):
    st.markdown(f"### {t(lang,'network_check')}")
    st.info("Replace YOUR_PACS_IP_HERE with your PACS server IP — or use the automatic test below")
    commands = """
ping YOUR_PACS_IP_HERE
tracert YOUR_PACS_IP_HERE
telnet YOUR_PACS_IP_HERE 104
telnet YOUR_PACS_IP_HERE 443
Test-NetConnection YOUR_PACS_IP_HERE -Port 104
"""
    st.code(commands.strip(), language="bash")
    if st.button(t(lang, "copy_commands")):
        st.write(commands)


def guided_checklist_ui(lang: str):
    st.markdown(f"### {t(lang,'step_help')}")
    # maintain steps in session
    step = st.session_state.get("check_step", 0)
    progress = st.progress(0)

    steps = [
        (t(lang, "just_tell"), [
            "Can't login", "Images are slow or blank", "Study is missing", "Modality not sending images", "Can't connect to PACS / timeout", "Everything is freezing", "Other problem"
        ]),
        ("Can other doctors open PACS right now?", ["Yes", "No, everyone has the same problem", "Not sure"]),
        ("Have you tried clearing cache yet?", ["Yes", "No – show me how", "I did but no change"]),
    ]

    if step < len(steps):
        progress.progress((step + 1) / len(steps))
        q, opts = steps[step]
        st.markdown(f"**Step {step+1}/{len(steps)}: {q}**")
        choice = st.radio("", opts, key=f"step{step}")
        if st.button("Next →"):
            st.session_state[f"ans{step}"] = choice
            st.session_state.check_step = step + 1
            st.experimental_rerun()
    else:
        progress.progress(1.0)
        st.success(t(lang, "diagnosis_complete"))
        a1 = st.session_state.get("ans0", "")
        a2 = st.session_state.get("ans1", "")
        a3 = st.session_state.get("ans2", "")

        # Simple decision tree
        if "everyone" in a2.lower():
            st.error("PACS is down for everyone → Use backup viewer → Call emergency line")
        elif "login" in a1.lower():
            st.info("→ Try incognito → Clear cache → Reset password → Call PACS admin if locked")
        elif "image" in a1.lower():
            st.info("→ Press F5 → Close other studies → Tools → Clear Cache → Use wired internet")
        elif "study" in a1.lower():
            st.info("→ Double-check Patient ID & Accession → Widen date range → Ask admin to prefetch")
        elif "connect" in a1.lower():
            st.info("→ Run network & port checks using the button above")
        else:
            st.info("Try the UNIVERSAL FIX first → 97 % of problems disappear!")

        if st.button(t(lang, "start_over")):
            st.session_state.check_step = 0
            st.experimental_rerun()


def chat_ui(lang: str):
    st.markdown("---")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Hey — {t(lang,'just_tell')}"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(t(lang, "chat_placeholder"))
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        # quick fix detection
        found, name = quick_engine.detect(prompt)
        if found:
            st.session_state.messages.append({"role": "assistant", "content": f"{t(lang,'show_quickfix')} {name}"})
            st.success(f"→ {name}")
        else:
            st.session_state.messages.append({"role": "assistant", "content": "I didn't catch that exactly — please try keywords or use guided help."})

        # optionally log the interaction
        case = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "prompt": prompt,
            "detected": name if found else None,
        }
        log_case(case)

# ---------------------------
# APP
# ---------------------------

def main():
    # initial settings
    st.set_page_config(page_title=APP_CONFIG["title"], layout="centered")

    # persistent defaults
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # sidebar controls
    lang_choice, theme_choice = render_sidebar(st.session_state.lang)
    # map theme radio label back to boolean
    is_dark = theme_choice == TRANSLATIONS.get(lang_choice, TRANSLATIONS["en"]).get("theme_dark")

    # update session state only if changed
    st.session_state.lang = lang_choice
    st.session_state.theme = "dark" if is_dark else "light"

    # inject CSS
    inject_theme_css(is_dark)

    # header and layout
    render_header(st.session_state.lang)

    # top buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t(st.session_state.lang, "universal_fix")):
            st.success("Close everything → Clear Cache → Restart computer — That often fixes it.")
    with col2:
        if st.button(t(st.session_state.lang, "step_help")):
            st.session_state.check_step = 0
            st.experimental_rerun()

    col3, col4 = st.columns(2)
    with col3:
        if st.button(t(st.session_state.lang, "clear_cache")):
            st.info("Tools → Clear Local Cache (or Ctrl+Shift+Delete) → Clear cached images")
    with col4:
        if st.button(t(st.session_state.lang, "network_check")):
            network_check_ui(st.session_state.lang)

    st.markdown("---")

    # two-column content: left = panels, right = logs / animations
    left, right = st.columns([2, 1])
    with left:
        # Quick fixes & guided checklist
        with st.expander(t(st.session_state.lang, "universal_fix")):
            quick_fixes_panel(st.session_state.lang)

        if st.session_state.get("check_step", 0) > 0:
            guided_checklist_ui(st.session_state.lang)
        else:
            st.info(t(st.session_state.lang, "just_tell"))

        # chat fallback
        chat_ui(st.session_state.lang)

    with right:
        # small animation / status card
        st.markdown("<div class='step-box animated-pulse'><h4>System Status</h4><p>All good — no critical incidents reported.</p></div>", unsafe_allow_html=True)
        # recent logs preview
        st.markdown("### Recent cases")
        try:
            path = os.path.join("logs", "cases.log")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()[-5:]
                for ln in reversed(lines):
                    try:
                        obj = json.loads(ln)
                        st.write(f"{obj.get('timestamp')} — {obj.get('prompt')} — Detected: {obj.get('detected')}")
                    except Exception:
                        continue
            else:
                st.write("No cases yet — interactions will be logged here.")
        except Exception as e:
            st.write("Error reading logs")

    st.markdown("---")
    st.caption(t(st.session_state.lang, "footer"))


if __name__ == '__main__':
    main()
