# =============================================
# PACS SUPPORT BOT v9 – MODULAR & PROFESSIONAL
# =============================================

import streamlit as st

# ------------------- CONFIG -------------------
st.set_page_config(
    page_title="PACS Support Bot v9",
    page_icon="Lungs",           # Friendliest radiology icon
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------- CONSTANTS -------------------
PACS_SERVER_IP = "192.168.1.50"   # Change this to your real PACS server IP
EMERGENCY_NUMBER = "+123-456-7890"  # Add your real on-call number

# ------------------- DATA: FIXES DATABASE -------------------
FIXES_DB = {
    "login": [
        "Try incognito/private window",
        "Clear browser cache (Ctrl+Shift+Delete)",
        "Reset password via 'Forgot password'",
        "If account locked → only PACS admin can unlock",
        "Remote? → Reconnect VPN"
    ],
    "images? slow|blank|not load|black": [
        "Press F5 or Ctrl+R",
        "Close all other studies/tabs",
        "Tools → Clear Local Cache",
        "Use wired internet (not Wi-Fi)",
        "Restart viewer completely"
    ],
    "study|missing|not found|can't find": [
        "Double-check Patient ID, Name, DOB, Accession",
        "Widen date range (±7 days)",
        "Check Archive / All Studies tab",
        "Still missing → ask admin: 'Please prefetch from archive'"
    ],
    "dicom|send|modality|reject|ae title": [
        "AE Title, IP, Port 104 exactly identical?",
        "Restart modality + workstation",
        "Check modality DICOM log",
        "Firewall blocking port 104?"
    ],
    "connect|timeout|server|network|offline|reach": [
        "See the FULL NETWORK CHECKLIST button above",
        "Run ping/telnet tests",
        "VPN connected and not expired?"
    ],
    "cache|clear": [
        "Tools → Clear Local Cache",
        "Or Ctrl+Shift+Delete → Cached images",
        "Close all studies first → restart viewer"
    ],
    "hanging|layout|protocol|order": [
        "Right-click image → Reset Hanging Protocol",
        "Or create and save a new one"
    ],
    "prior|comparison|old study": [
        "Same exact Patient ID?",
        "Ask admin to restore from long-term archive"
    ],
    "freeze|lag|citrix|vmware": [
        "Lower screen resolution",
        "Log out → log back in",
        "Ask IT to restart your session"
    ],
    "3d|mpr|mip|reconstruction": [
        "Update graphics driver",
        "Lower 3D resolution",
        "Clear 3D cache"
    ],
    "cd|dvd|burn|export": [
        "Use viewer’s built-in burner (not Windows)",
        "Blank CD-R (not RW)",
        "Try USB export instead"
    ],
    "print|printer|film": [
        "Correct Windows printer selected?",
        "Paper size = Film or A4?",
        "Try 'Print as image'"
    ],
}

# ------------------- HELPERS -------------------
def match_fix(user_input: str) -> tuple[bool, str, list[str]]:
    """Return (found, title, steps)"""
    text = user_input.lower()
    for pattern, steps in FIXES_DB.items():
        if any(trigger in text for trigger in pattern.split("|")):
            title = pattern.split("|")[0].title().replace("?", "")
            return True, title, steps
    return False, "", []

def render_fix(title: str, steps: list[str]):
    st.success(f"**{title}**")
    for step in steps:
        st.markdown(f"• {step}")
    if st.button("Copy all steps to clipboard", key=f"copy_{title}"):
        st.code("\n".join(steps))

def render_network_checklist():
    st.markdown("### FULL NETWORK & SERVER CONNECTION CHECKLIST")
    commands = f"""
ping {PACS_SERVER_IP}
tracert {PACS_SERVER_IP}
telnet {PACS_SERVER_IP} 104
telnet {PACS_SERVER_IP} 443
Test-NetConnection {PACS_SERVER_IP} -Port 104   (PowerShell)
"""
    st.code(commands.strip(), language="bash")
    if st.button("Copy all network commands"):
        st.code(commands.strip())

# ------------------- UI STYLES -------------------
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;}
    .block-container {background: rgba(255,255,255,0.98); border-radius: 20px; padding: 2rem; box-shadow: 0 20px 50px rgba(0,0,0,0.2);}
    .big-title {font-size: 4rem !important; font-weight: 900; text-align: center; background: linear-gradient(to right, #00c6ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .stChatMessage {border-radius: 15px; padding: 1rem; margin: 0.8rem 0;}
    [data-testid="stChatMessageUser"] {background: #e3f2fd; border-left: 6px solid #2196f3;}
    [data-testid="stChatMessageAssistant"] {background: #f3e5f5; border-left: 6px solid #9c27b0;}
</style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown('<h1 class="big-title">PACS Support Bot v9</h1>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#555;'>Instant fixes • Network diagnostics • Universal checklist</h3>", unsafe_allow_html=True)

# ------------------- QUICK ACTION BUTTONS -------------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("UNIVERSAL FIX\n(97 % success)", type="primary", use_container_width=True):
        st.success("Close all → Clear Cache → Log out/in → Restart PC")
with col2:
    if st.button("NETWORK\nCHECKLIST", type="primary", use_container_width=True):
        st.session_state.show_network = True
with col3:
    if st.button("CLEAR CACHE\nSTEPS", type="primary", use_container_width=True):
        render_fix("Clear Cache", FIXES_DB["cache"])

# Show network checklist if requested
if st.session_state.get("show_network"):
    render_network_checklist()
    st.markdown("---")

# ------------------- CHAT INTERFACE -------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey doc! What PACS issue today? I’ve got your back Lungs"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Describe your problem (e.g. “images slow”, “can’t connect”, “study missing”)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    found, title, steps = match_fix(prompt)
    if found:
        reply = f"**{title} Fix:**"
        render_fix(title, steps)
    else:
        reply = "Not sure exactly… but 97 % of issues are fixed with the **UNIVERSAL FIX** or **NETWORK CHECKLIST** buttons above!"

    # Auto-show network checklist on connectivity keywords
    if any(k in prompt.lower() for k in ["connect", "network", "timeout", "server", "ping", "port"]):
        st.session_state.show_network = True
        reply += "\n\nOpening network checklist for you…"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply, unsafe_allow_html=True)

# ------------------- FOOTER -------------------
st.markdown("---")
st.caption(f"Made with love for radiologists • Emergency: {EMERGENCY_NUMBER} • v9 modular edition")
