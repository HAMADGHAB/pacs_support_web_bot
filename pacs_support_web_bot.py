import streamlit as st

# === PAGE CONFIG & BEAUTIFUL THEME ===
st.set_page_config(
    page_title="PACS Support Bot",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# === CUSTOM CSS – makes it look premium ===
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;}
    .block-container {background: rgba(255,255,255,0.98); border-radius: 20px; padding: 2rem; margin-top: 2rem; box-shadow: 0 20px 40px rgba(0,0,0,0.1);}
    .big-title {font-size: 3.5rem !important; font-weight: 900; text-align: center; background: linear-gradient(to right, #1E88E5, #8E24AA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .subtitle {font-size: 1.4rem; text-align: center; color: #444; margin-bottom: 1rem;}
    .stChatMessage {border-radius: 15px; padding: 1rem; margin: 0.8rem 0;}
    .stChatMessage[data-testid="stChatMessageUser"] {background: #E3F2FD; border-left: 5px solid #1E88E5;}
    .stChatMessage[data-testid="stChatMessageAssistant"] {background: #F3E5F5; border-left: 5px solid #8E24AA;}
    .css-1v0mbdj {font-size: 1.1rem !important;}
    .troubleshoot-btn button {background: linear-gradient(to right, #FF6B6B, #FF8E53) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; padding: 12px 30px !important;}
</style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown('<h1 class="big-title">❤️ PACS Support Bot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Instant fixes + guided troubleshooter • English • عربي • Français</p>', unsafe_allow_html=True)
st.caption("🔥 Built by a radiologist who was tired of waiting on IT")

# === QUICK FAQS (kept short – the beauty is in the guided mode) ===
faqs = [
    (["hi","hello","hey","salut","مرحبا"],"Hey doc! What’s broken today? ❤️"),
    (["login","password","locked","تسجيل"],"Try incognito → clear cache → reset password → call admin if locked"),
    (["image","slow","blank","صور","lent"],"F5 → close other studies → clear cache → wired internet"),
    (["study","missing","غير موجود"],"Check exact ID → widen date → ask prefetch"),
    (["dicom","send","modality","إرسال"],"AE Title/IP/Port match? → restart modality → port 104 open?"),
    (["cache","clear"],"Tools → Clear Local Cache → restart viewer"),
]

def quick_answer(text):
    text = text.lower()
    for keywords, answer in faqs:
        if any(k in text for k in keywords):
            return answer
    return None

# === GUIDED TROUBLESHOOTER (now beautiful too) ===
def guided_troubleshooter():
    st.markdown("<h2 style='text-align:center; color:#8E24AA;'>Let me fix this for you step by step 🚀</h2>", unsafe_allow_html=True)
    
    steps = [
        ("What's the main problem?", ["Can't login", "Images slow / blank", "Study missing", "Modality not sending", "Connectivity / timeout", "Freezing / crashing", "Other"]),
        ("Can others in your department open PACS right now?", ["Yes, they can", "No, everyone is down", "Not sure"]),
        ("Have you tried clearing cache yet?", ["Yes", "No, show me how", "Already did, no help"]),
    ]
    
    if "ts_step" not in st.session_state:
        st.session_state.ts_step = 0
        st.session_state.answers = []

    step = st.session_state.ts_step
    if step < len(steps):
        q, options = steps[step]
        st.markdown(f"<h4>{step+1}. {q}</h4>", unsafe_allow_html=True)
        choice = st.radio("", options, key=f"ts{step}")
        col1, col2 = st.columns([1,1])
        with col2:
            if st.button("Next →", type="primary", use_container_width=True):
                st.session_state.answers.append(choice)
                st.session_state.ts_step += 1
                st.rerun()
    else:
        st.success("Diagnosis ready!")
        a1, a2, a3 = st.session_state.answers
        
        if "login" in a1:
            st.error("Most likely account or browser issue → incognito + clear cache + reset password")
        elif "image" in a1:
            st.error("Local cache or network → Clear cache → wired → restart viewer")
        elif "study" in a1:
            st.error("Wrong search or archived → exact ID + wide date + ask prefetch")
        elif "everyone" in a2:
            st.error("PACS is down globally → use backup viewer → call emergency line")
        else:
            st.info("Try the universal fix: Close everything → Clear cache → Restart PC")
        
        if st.button("Start over"):
            st.session_state.ts_step = 0
            st.session_state.answers = []
            st.rerun()

# === MAIN CHAT ===
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Hey! What PACS nightmare are you facing today? ❤️"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Describe your problem…"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)

    reply = quick_answer(prompt)
    if reply:
        final_reply = reply
    elif any(x in prompt.lower() for x in ["guide","step","troubleshoot","help"]):
        final_reply = "Starting guided troubleshooter…"
        st.session_state.mode = "troubleshoot"
    else:
        final_reply = "I don’t know that one instantly.\nClick the button below for step-by-step help 👇"

    st.session_state.messages.append({"role":"assistant","content":final_reply})
    with st.chat_message("assistant"): st.markdown(final_reply)

# === BIG BEAUTIFUL TROUBLESHOOTER BUTTON ===
if st.button("🔧 Run Step-by-Step Troubleshooter", type="primary", use_container_width=True):
    st.session_state.mode = "troubleshoot"

if st.session_state.get("mode") == "troubleshoot":
    guided_troubleshooter()
