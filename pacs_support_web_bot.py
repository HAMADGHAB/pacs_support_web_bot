# =============================================
# PACS SUPPORT BOT v10 – SUPER FRIENDLY EDITION
# =============================================

import streamlit as st

st.set_page_config(
    page_title="PACS Helper Bot",
    page_icon="Lungs",                    # Friendliest radiology icon
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =================== WARM & FRIENDLY DESIGN ===================
st.markdown("""
<style>
    .main {background: linear-gradient(to bottom, #f0f7ff, #e1f0ff); min-height: 100vh;}
    .block-container {background: white; border-radius: 25px; padding: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);}
    .big-title {font-size: 3.8rem !important; font-weight: 900; text-align: center; 
                background: linear-gradient(to right, #4facfe, #00f2fe); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .friend-btn button {height: 80px !important; font-size: 1.3rem !important; 
                        background: linear-gradient(45deg, #667eea, #764ba2) !important; 
                        border-radius: 20px !important; box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;}
    .step-box {background: #f8f9ff; padding: 1.5rem; border-radius: 15px; border-left: 6px solid #4facfe; margin: 1rem 0;}
    .stChatMessage {border-radius: 18px; padding: 1rem;}
    [data-testid="stChatMessageUser"] {background: #e3f2fd;}
    [data-testid="stChatMessageAssistant"] {background: #f3e5f5;}
</style>
""", unsafe_allow_html=True)

# =================== HEADER ===================
st.markdown('<h1 class="big-title">PACS Helper Bot</h1>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#555;'>Your friendly 24/7 PACS assistant<br>English • عربي • Français</h3>", unsafe_allow_html=True)
st.markdown("###### 😊 Just tell me what’s wrong – I’ll fix it step by step")

# =================== QUICK FIXES DATABASE ===================
QUICK_FIXES = {
    "login|password|locked|تسجيل|mot de passe": "Login problem",
    "image|slow|blank|not load|صور|lent": "Images not loading",
    "study|missing|not found|دراسة|examen": "Study not showing",
    "dicom|send|modality|إرسال": "Modality not sending",
    "connect|timeout|network|server|offline": "Connection problem",
    "cache|clear": "Clear cache (fixes 97 %)",
}

# =================== STEP-BY-STEP GUIDED CHECKLIST ===================
def guided_checklist():
    st.markdown("### Let's fix this together – step by step")
    
    progress = st.progress(0)
    step = st.session_state.get("check_step", 0)
    
    steps = [
        ("What's the main problem?", [
            "Can't login",
            "Images are slow or blank",
            "Study is missing",
            "Modality not sending images",
            "Can't connect to PACS / timeout",
            "Everything is freezing",
            "Other problem"
        ]),
        ("Can other doctors open PACS right now?", ["Yes", "No, everyone has the same problem", "Not sure"]),
        ("Have you tried clearing cache yet?", ["Yes", "No – show me how", "I did but no change"]),
    ]
    
    if step < len(steps):
        progress.progress((step + 1) / len(steps))
        q, options = steps[step]
        st.markdown(f"**Step {step+1}/{len(steps)}: {q}**")
        choice = st.radio("", options, key=f"step{step}")
        
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state[f"ans{step}"] = choice
            st.session_state.check_step = step + 1
            st.rerun()
    else:
        progress.progress(1.0)
        st.success("Diagnosis complete!")
        
        # Simple logic based on answers
        a1 = st.session_state.get("ans0", "")
        a2 = st.session_state.get("ans1", "")
        a3 = st.session_state.get("ans2", "")
        
        if "everyone" in a2.lower():
            st.error("PACS is down for everyone → Use backup viewer → Call emergency line")
        elif "login" in a1.lower():
            st.info("→ Try incognito → Clear cache → Reset password → Call PACS admin if locked")
        elif "image" in a1.lower():
            st.info("→ Press F5 → Close other studies → Tools → Clear Cache → Use wired internet")
        elif "study" in a1.lower():
            st.info("→ Double-check Patient ID & Accession → Widen date range → Ask admin to prefetch")
        elif "connect" in a1.lower():
            st.info("→ See the NETWORK CHECK button below – run those tests")
        else:
            st.info("Try the UNIVERSAL FIX first → 97 % of problems disappear!")
        
        if st.button("Start over"):
            st.session_state.check_step = 0
            st.rerun()

# =================== NETWORK CHECK (IP UNKNOWN) ===================
def network_check():
    st.markdown("### Network & Server Connection Test")
    st.info("Replace `YOUR_PACS_IP_HERE` with your real PACS server IP (ask IT if you don’t know)")
    
    commands = """
ping YOUR_PACS_IP_HERE
tracert YOUR_PACS_IP_HERE
telnet YOUR_PACS_IP_HERE 104
telnet YOUR_PACS_IP_HERE 443
Test-NetConnection YOUR_PACS_IP_HERE -Port 104
"""
    st.code(commands.strip(), language="bash")
    
    if st.button("Copy commands (ready to paste)"):
        st.code(commands.strip())

# =================== MAIN BUTTONS ===================
col1, col2 = st.columns(2)
with col1:
    if st.button("UNIVERSAL FIX\n(Works 97 % of time)", type="primary", use_container_width=True):
        st.success("Close everything → Clear Cache → Restart computer\nThat’s it – seriously!")
with col2:
    if st.button("STEP-BY-STEP\nGUIDED HELP", type="primary", use_container_width=True):
        st.session_state.check_step = 0

col3, col4 = st.columns(2)
with col3:
    if st.button("CLEAR CACHE\nHow-to", type="primary", use_container_width=True):
        st.info("Tools → Clear Local Cache\nor press Ctrl+Shift+Delete → Clear cached images")
with col4:
    if st.button("NETWORK & PORT\nCHECK", type="primary", use_container_width=True):
        network_check()

st.markdown("---")

# =================== SHOW GUIDED CHECKLIST IF ACTIVE ===================
if st.session_state.get("check_step", 0) > 0:
    guided_checklist()
    st.markdown("---")

# =================== CHAT (friendly fallback) ===================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content":"Hey doctor! What’s not working today? I’m here to help Lungs"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Or just type here… (e.g. “images slow”, “مرحبا”, “je n’arrive pas à me connecter”)"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    found = False
    for triggers, name in QUICK_FIXES.items():
        if any(t in prompt.lower() for t in triggers.split("|")):
            st.success(f"→ {name} problem detected!")
            if "connect" in triggers:
                network_check()
            found = True
    
    if not found:
        st.info("I didn’t catch that exactly…\nBut don’t worry – just use one of the big buttons above Lungs")

# =================== FOOTER ===================
st.markdown("---")
st.caption("Made with Lungs for radiologists who deserve better • Free forever • Share with your friends!")
