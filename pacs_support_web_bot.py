# =============================================
# PACS SUPPORT BOT v11 – ULTRA FRIENDLY EDITION
# =============================================
import streamlit as st
st.set_page_config(
    page_title="PACS Helper Bot",
    page_icon="🩺",  # Friendlier medical icon
    layout="wide",
    initial_sidebar_state="collapsed"
)
# =================== EVEN WARMER & FRIENDLIER DESIGN ===================
st.markdown("""
<style>
    .main {background: linear-gradient(to bottom, #f0f7ff, #d9efff); min-height: 100vh; padding: 2rem;}
    .block-container {background: white; border-radius: 30px; padding: 3rem; box-shadow: 0 12px 35px rgba(0,0,0,0.08);}
    .big-title {font-size: 4.2rem !important; font-weight: 900; text-align: center;
                background: linear-gradient(to right, #4facfe, #00f2fe, #ff69b4);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .subheader {font-size: 1.8rem !important; text-align: center; color: #333; margin-bottom: 1rem;}
    .friend-btn button {height: 85px !important; font-size: 1.4rem !important;
                        background: linear-gradient(45deg, #667eea, #764ba2, #ff69b4) !important;
                        border-radius: 25px !important; box-shadow: 0 10px 25px rgba(0,0,0,0.15) !important;
                        transition: transform 0.3s; }
    .friend-btn button:hover {transform: scale(1.05);}
    .step-box {background: #f8f9ff; padding: 1.8rem; border-radius: 20px; border-left: 8px solid #4facfe; margin: 1.2rem 0;
               box-shadow: 0 4px 10px rgba(0,0,0,0.05);}
    .stChatMessage {border-radius: 22px; padding: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);}
    [data-testid="stChatMessageUser"] {background: #e3f2fd;}
    [data-testid="stChatMessageAssistant"] {background: #fce4ec;}
    .emoji-title {font-size: 2rem; margin-top: 2rem;}
    .resource-expander {background: #fff; border-radius: 15px; padding: 1rem; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)
# =================== HEADER ===================
st.markdown('<h1 class="big-title">PACS Helper Bot 🩺</h1>', unsafe_allow_html=True)
st.markdown("<h3 class='subheader'>Your super friendly 24/7 PACS assistant – Always here to help!<br>English • عربي • Français</h3>", unsafe_allow_html=True)
st.markdown("###### 😊 Just tell me what’s wrong – I’ll guide you step by step with a smile!")
# =================== EXPANDED QUICK FIXES DATABASE ===================
QUICK_FIXES = {
    "login|password|locked|تسجيل|mot de passe": {
        "name": "Login problem",
        "solution": "→ Try logging in via incognito mode\n→ Clear your browser cache (Ctrl+Shift+Delete)\n→ Reset password through admin\n→ If locked, contact PACS admin immediately 🛡️"
    },
    "image|slow|blank|not load|صور|lent": {
        "name": "Images not loading or slow",
        "solution": "→ Press F5 to refresh\n→ Close other open studies\n→ Go to Tools → Clear Local Cache\n→ Switch to wired internet if on WiFi\n→ Check network speed – images can be huge! 📸"
    },
    "study|missing|not found|دراسة|examen": {
        "name": "Study not showing",
        "solution": "→ Double-check Patient ID & Accession Number\n→ Widen the search date range\n→ Ask admin to prefetch the study\n→ Verify if it's in MiniPACS instead 🌟"
    },
    "dicom|send|modality|إرسال": {
        "name": "Modality not sending images",
        "solution": "→ Check AE Title in RIS menu: Parameters → Exam Rooms\n→ Ensure Work List IP & Port are set correctly (e.g., 192.168.0.1:2575)\n→ Verify Java VM is installed on client\n→ Contact machine supplier for MPPS setup ⚙️"
    },
    "connect|timeout|network|server|offline|mpls": {
        "name": "Connection or network problem",
        "solution": "→ Run ping and tracert to PACS IP\n→ Check latency (<50ms ideal)\n→ Use iperf3 for bandwidth test\n→ Verify MPLS routing\n→ Test DICOM Echo via web interface 🔌"
    },
    "cache|clear": {
        "name": "Clear cache",
        "solution": "→ In browser: Ctrl+Shift+Delete → Clear cached images & files\n→ In PACS viewer: Tools → Clear Local Cache\n→ Restart browser – 97% of issues fixed! ✨"
    },
    "block|blocage|server down|pacs down|mini pacs|worklist|crash": {
        "name": "Server blockage or down",
        "solution": "→ Verify network ping to server\n→ Test DICOM Echo: http://IP:8080/dcm4chee-web3/\n→ SSH with admsite / [your password]\n→ Check services: sudo systemctl status dcm4chee.service & xampp.service\n→ If down >30min, restart: stop then start xampp & dcm4chee\n→ Check disk space: sudo df -h 💻"
    },
    "config|parametrage|setup|ris|work list|pacs config": {
        "name": "Configuration or setup issue",
        "solution": "→ For RIS to Work List: Set IP:Port in Admin System → Install Parameters, enable auto send\n→ Work List to Modalities: Set AE Titles in RIS Parameters → Exam Rooms\n→ Modalities to PACS/MiniPACS: Get IPs, Ports, AETs from product responsible\n→ Supplier handles auto storage setup 🛠️"
    },
    "performance|qos|jitter|loss|bandwidth": {
        "name": "Performance or QoS issue",
        "solution": "→ Measure bandwidth & latency with iperf3\n→ Check jitter & packet loss with mtr\n→ Goal: Jitter <20ms, loss <1%, bandwidth sufficient for DICOM files\n→ Test app: Connect to PACS, C-FIND, C-MOVE, WADO viewer 📊"
    },
}
# =================== STEP-BY-STEP GUIDED CHECKLIST (EXPANDED) ===================
def guided_checklist():
    st.markdown("<p class='emoji-title'>🛠️ Let's fix this together – step by step!</p>", unsafe_allow_html=True)
    
    progress = st.progress(0)
    step = st.session_state.get("check_step", 0)
    
    steps = [
        ("What's the main problem?", [
            "Can't login",
            "Images are slow or blank",
            "Study is missing",
            "Modality not sending images",
            "Can't connect to PACS / timeout",
            "Server is blocked or down",
            "Configuration or setup issue",
            "Performance is bad (slow network)",
            "Everything is freezing",
            "Other problem"
        ]),
        ("Can other doctors open PACS right now?", ["Yes", "No, everyone has the same problem", "Not sure"]),
        ("Have you tried clearing cache yet?", ["Yes", "No – show me how", "I did but no change"]),
        ("Have you checked network connection (ping/tracert)?", ["Yes, it's fine", "No – show me how", "It's bad"]),
        ("Is this a server-side issue (e.g., blockage after power cut)?", ["Yes", "No", "Not sure"]),
    ]
    
    if step < len(steps):
        progress.progress((step + 1) / len(steps))
        q, options = steps[step]
        st.markdown(f"<div class='step-box'><strong>Step {step+1}/{len(steps)}: {q}</strong></div>", unsafe_allow_html=True)
        choice = st.radio("", options, key=f"step{step}")
        
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state[f"ans{step}"] = choice
            st.session_state.check_step = step + 1
            st.rerun()
    else:
        progress.progress(1.0)
        st.success("Diagnosis complete! Here's what I recommend based on your answers 😊")
        
        # Expanded logic based on answers
        a1 = st.session_state.get("ans0", "").lower()
        a2 = st.session_state.get("ans1", "").lower()
        a3 = st.session_state.get("ans2", "").lower()
        a4 = st.session_state.get("ans3", "").lower()
        a5 = st.session_state.get("ans4", "").lower()
        
        if "everyone" in a2:
            st.error("PACS is down for everyone → Switch to backup viewer → Call emergency IT line now! 📞")
        elif "login" in a1:
            st.info(QUICK_FIXES["login|password|locked|تسجيل|mot de passe"]["solution"])
        elif "image" in a1:
            st.info(QUICK_FIXES["image|slow|blank|not load|صور|lent"]["solution"])
        elif "study" in a1:
            st.info(QUICK_FIXES["study|missing|not found|دراسة|examen"]["solution"])
        elif "modality" in a1:
            st.info(QUICK_FIXES["dicom|send|modality|إرسال"]["solution"])
        elif "connect" in a1 or "performance" in a1:
            st.info(QUICK_FIXES["connect|timeout|network|server|offline|mpls"]["solution"])
        elif "server" in a1 or "yes" in a5:
            st.info(QUICK_FIXES["block|blocage|server down|pacs down|mini pacs|worklist|crash"]["solution"])
        elif "config" in a1:
            st.info(QUICK_FIXES["config|parametrage|setup|ris|work list|pacs config"]["solution"])
        else:
            st.info("Try the UNIVERSAL FIX first → Clear cache & restart – it works 97% of the time! ✨")
        
        if st.button("Start over"):
            st.session_state.check_step = 0
            st.rerun()
# =================== NETWORK CHECK (WITH PLACEHOLDER IP) ===================
def network_check():
    st.markdown("<p class='emoji-title'>🔌 Network & Server Connection Test</p>", unsafe_allow_html=True)
    st.info("Replace `YOUR_PACS_IP_HERE` with your actual PACS server IP (ask your IT team if unsure) 🌐")
    
    commands = """
ping YOUR_PACS_IP_HERE
tracert YOUR_PACS_IP_HERE  # Windows
traceroute YOUR_PACS_IP_HERE  # Linux/Mac
telnet YOUR_PACS_IP_HERE 104
telnet YOUR_PACS_IP_HERE 443
Test-NetConnection YOUR_PACS_IP_HERE -Port 104  # PowerShell
iperf3 -c YOUR_PACS_IP_HERE  # Bandwidth test (install iperf3 if needed)
mtr YOUR_PACS_IP_HERE  # Jitter & loss
"""
    st.code(commands.strip(), language="bash")
    
    if st.button("Copy commands (ready to paste)"):
        st.code(commands.strip())
# =================== ADDITIONAL TROUBLESHOOTING RESOURCES ===================
def show_resources():
    st.markdown("<p class='emoji-title'>📚 Extra Troubleshooting Guides</p>", unsafe_allow_html=True)
    
    with st.expander("🛠️ RIS/Work List/PACS Configuration Guide", expanded=False):
        st.markdown("""
        **Steps for Setup:**
        1. **RIS to Work List:** Install Java VM, set IP:Port in Admin → Install Parameters, enable auto send.
        2. **Work List to Modalities:** Set AE Titles in Parameters → Exam Rooms. Configure MPPS if needed.
        3. **Modalities to PACS/MiniPACS:** Get IPs, Ports, AETs from product responsible. Supplier sets auto storage.
        """)
    
    with st.expander("🔍 MPLS Test Checklist for PACS", expanded=False):
        st.markdown("""
        **Network Connectivity:**
        - Ping PACS: Check latency <50ms, no packet loss.
        - Tracert/Traceroute: Ensure traffic via MPLS.
        
        **Performance & QoS:**
        - iperf3: Measure bandwidth/latency for DICOM files.
        - mtr: Jitter <20ms, loss <1%.
        
        **PACS App Tests:**
        - Connect from distant site.
        - C-FIND for exams.
        - C-MOVE/C-GET for images.
        - WADO viewer: Test scanner, IRM, standard radiology.
        """)
    
    with st.expander("🚨 Server Blockage Procedure (PACS/MiniPACS/Worklist)", expanded=False):
        st.markdown("""
        **Initial Verification:**
        1. Ping server.
        2. DICOM Echo: http://IP:8080/dcm4chee-web3/
        3. SSH: admsite / [your password]
        4. Check services: sudo systemctl status dcm4chee.service & xampp.service
        5. Disk space: sudo df -h (check /opt/dcm4chee/...)
        
        **Manual Restart (if >30min down):**
        1. sudo systemctl stop dcm4chee.service
        2. sudo systemctl stop xampp.service
        3. sudo systemctl start xampp.service
        4. sudo systemctl start dcm4chee.service
        5. Verify & contact IT if persists.
        """)
# =================== MAIN BUTTONS (MORE FRIENDLY GRID) ===================
st.markdown("---")
cols = st.columns(3)
with cols[0]:
    if st.button("✨ UNIVERSAL FIX\n(Works 97% of time!)", type="primary", use_container_width=True, key="universal"):
        st.success("1. Close all tabs & PACS apps\n2. Clear browser cache (Ctrl+Shift+Delete)\n3. Restart your computer\n4. Try again – magic! 🎉")
with cols[1]:
    if st.button("🧭 STEP-BY-STEP\nGUIDED HELP", type="primary", use_container_width=True, key="guided"):
        st.session_state.check_step = 0
with cols[2]:
    if st.button("🧹 CLEAR CACHE\nQuick How-to", type="primary", use_container_width=True, key="cache"):
        st.info(QUICK_FIXES["cache|clear"]["solution"])
cols2 = st.columns(3)
with cols2[0]:
    if st.button("🔌 NETWORK CHECK\n& Ports Test", type="primary", use_container_width=True, key="network"):
        network_check()
with cols2[1]:
    if st.button("🚨 SERVER BLOCKAGE\nProcedure", type="primary", use_container_width=True, key="blockage"):
        st.info(QUICK_FIXES["block|blocage|server down|pacs down|mini pacs|worklist|crash"]["solution"])
with cols2[2]:
    if st.button("📚 MORE GUIDES\n& Resources", type="primary", use_container_width=True, key="resources"):
        show_resources()
st.markdown("---")
# =================== SHOW GUIDED CHECKLIST IF ACTIVE ===================
if st.session_state.get("check_step", 0) > 0:
    guided_checklist()
    st.markdown("---")
# =================== CHAT (SMARTER FALLBACK WITH MORE MATCHES) ===================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content":"Hey there, doctor! 😊 What’s not working with PACS today? I'm here to help! 🩺"}]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if prompt := st.chat_input("Or just type your issue here… (e.g. “images slow”, “server blocked”, “مرحبا”, “je n’arrive pas à me connecter”)"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    found = False
    for triggers, info in QUICK_FIXES.items():
        if any(t in prompt.lower() for t in triggers.split("|")):
            st.success(f"→ {info['name']} detected! Here's the fix:")
            st.info(info["solution"])
            found = True
    
    if not found:
        st.info("Hmm, I didn’t quite catch that... But no worries! 😊 Try one of the buttons above or describe it more (e.g., 'network slow' or 'configuration RIS').")
# =================== FOOTER ===================
st.markdown("---")
st.caption("Made with ❤️ for radiologists who deserve the best • Free forever • Share with your team! 🩺")
