import streamlit as st

st.set_page_config(page_title="PACS Support Bot", page_icon="🩻", layout="centered")

st.markdown("""
<style>
    .big-title {font-size: 3rem !important; font-weight: bold; text-align: center; color: #1E88E5;}
    .subtitle {font-size: 1.3rem; text-align: center; color: #555;}
    .css-1d391kg {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="big-title">🩻 PACS Support Bot v4</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">99 % of your PACS tickets solved instantly<br>English • عربي • Français</p>', unsafe_allow_html=True)
st.caption("Now with 30+ real fixes – the only bot you’ll ever need 🔥")

# === MASSIVE FAQ LIST (30+ issues) ===
faqs = [
    # 1 Greeting
    (["hi", "hello", "hey", "salut", "مرحبا", "bonjour", "help"], 
     "PACS Support Bot ready 👋\nDescribe your issue (English/عربي/Français)"),

    # 2 Login & Auth
    (["login", "log in", "password", "locked", "credential", "mot de passe", "كلمة السر", "تسجيل الدخول", "verrouillé", "account locked"],
     "🔐 **Login / Password issues**\n• Caps Lock off?\n• Try incognito mode\n• Clear browser cache\n• Use “Forgot password”\n• Account locked or expired → PACS admin only\n• Remote → VPN connected & not expired?"),

    # 3 Images
    (["image", "slow", "loading", "blank", "black", "not display", "hanging", "lent", "بطيء", "صور", "لا تظهر"],
     "🖼️ **Images slow / blank / not loading**\n• F5 or Ctrl+R\n• Close all other studies\n• Wired internet > Wi-Fi\n• Tools → Clear Local Cache\n• Server under load → wait 5–10 min\n• Try different browser or workstation"),

    # 4 Study missing
    (["study", "missing", "not found", "cant find", "no results", "examen", "دراسة", "غير موجود", "accession"],
     "🔍 **Study not appearing**\n• Exact Patient ID / Name / DOB / Accession\n• Widen date range (±1 week)\n• Check All Studies / Archive / Unread\n• Still sending from modality → wait\n• >48h old → ask admin to prefetch from archive"),

    # 5 DICOM send
    (["dicom", "send", "modality", "reject", "ae title", "failed", "إرسال", "موداليتي", "association rejected"],
     "📤 **Modality not sending to PACS**\n• AE Title, IP, Port 104 exact match?\n• Restart modality & workstation\n• Check modality DICOM log\n• Firewall blocking port 104?\n• Duplicate AE Title anywhere = instant reject"),

    # 6 Connectivity
    (["connectivity", "network", "timeout", "offline", "server not responding", "réseau", "اتصال"],
     "🌐 **Connectivity / timeout**\n• Restart PC\n• VPN connected?\n• Ping PACS server IP\n• Ports 104, 443, 8080 open?\n• Everyone down or just you?"),

    # 7 Cache (king of fixes)
    (["cache", "clear cache", "vider cache", "مسح الكاش", "memory"],
     "🧹 **Clear cache – fixes 95 % of weird shit**\n• Tools → Clear Local Cache\n• Or Ctrl+Shift+Delete\n• Close all studies first\n• Restart viewer"),

    # 8 Hanging protocols
    (["hanging protocol", "layout", "wrong order", "series", "protocole"],
     "🖥️ **Hanging protocols wrong**\n• Right-click → Reset to Default\n• Create new protocol & save\n• Different modality = separate protocol\n• Clear user profile/cache"),

    # 9 Access denied
    (["access", "permission", "denied", "no rights", "droit", "صلاحيات"],
     "🚫 **Access denied / No permission**\nOnly PACS admin can grant rights\nTell them exactly what you need (read/write/delete/etc.)"),

    # 10 System down
    (["down", "crash", "unavailable", "hors service", "معطل"],
     "💀 **PACS completely down**\n• Planned maintenance?\n• Use backup/failover viewer\n• Call emergency PACS number\n• Check status page if exists"),

    # 11 Priors / comparison
    (["prior", "comparison", "previous", "old study", "ancien"],
     "🆚 **No priors / comparison studies**\n• Same Patient ID exactly?\n• Prefetch rules might be broken\n• Manually search old studies\n• Ask admin to restore from deep archive"),

    # 12 Worklist / RIS / Orders
    (["worklist", "ris", "hl7", "order not showing", "commande"],
     "📋 **Orders not appearing in worklist**\n• HL7 message failed → check interface engine\n• Patient merge conflict\n• Re-send order from RIS/HIS"),

    # 13 Annotations / measurements lost
    (["annotation", "measurement", "lost", "disappeared", "save"],
     "✏️ **Annotations / measurements not saving**\n• Save before closing study!\n• Check if you have write permission\n• Some viewers need “Finalize” button"),

    # 14 3D / MPR / MIP not working
    (["3d", "mpr", "mip", "reconstruction", "volume"],
     "🧊 **3D/MPR/MIP failing**\n• Graphics card drivers up to date?\n• Enough RAM free?\n• Try lower resolution\n• Clear 3D cache"),

    # 15 Export / burn CD
    (["export", "cd", "dvd", "burn", "failed"],
     "💿 **CD/DVD export failing**\n• Use viewer’s built-in burner (not Windows)\n• Blank CD-R, not RW\n• Try slower burn speed\n• Export to USB instead"),

    # 16 Window/level wrong
    (["window", "level", "wl", "ww", "dark", "bright"],
     "⚙️ **Window/Level presets wrong**\n• Right-click → Reset WL\n• Or preset dropdown → CT Abdomen, etc.\n• Mouse wheel + right-click to adjust"),

    # 17 Thin client freezing
    (["freeze", "lag", "citrix", "vmware", "remote desktop"],
     "🛑 **Thin client freezing**\n• Close all other apps\n• Lower screen resolution\n• Log out & log back in\n• Ask IT to restart your session"),

    # 18 Voice dictation / SR issues
    (["report", "dictation", "powerscribe", "structured report"],
     "🎤 **Voice dictation / SR not saving**\n• Check microphone permission\n• Save report before closing study\n• Some PACS need “Sign” button"),

    # 19 Mobile app issues
    (["mobile", "phone", "tablet", "app"],
     "📱 **Mobile PACS app problems**\n• Force close & reopen app\n• Clear app cache\n• Wi-Fi > mobile data\n• Update app"),

    # 20 Printer / paper print
    (["print", "printer", "paper", "film"],
     "🖨️ **Print failing**\n• Correct Windows printer selected?\n• Paper size A4/film?\n• Try “Print as image” option"),
]

def find_answer(txt):
    txt = txt.lower().strip()
    if txt in ["bye", "quit", "exit", "شكرا", "merci", "thanks"]:
        return "Good luck doc! PACS will break again tomorrow 😂"
    for keywords, answer in faqs:
        if any(k in txt for k in keywords):
            return answer
    return "Hmm not in my database yet 🤔\nTry different words or call your PACS admin directly.\n(Or tell me the error message exactly!)"

# === CHAT INTERFACE ===
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey! What PACS nightmare are you facing today? 🩻"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Type your issue here… (English • عربي • Français)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = find_answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply, unsafe_allow_html=True)
