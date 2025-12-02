import streamlit as st

# === ALL YOUR PACS FAQS (same as before, just cleaner) ===
faqs = [
    (["hi", "hello", "hey", "salut", "help", "bonjour"], 
     "Yo! PACS Support Bot here 👋\nWhat’s breaking today?"),

    (["login", "log in", "sign in", "password", "cant log", "locked", "credential", "mot de passe"],
     "🔐 Login issues:\n• Check username/password (Caps Lock!)\n• Try incognito mode\n• Clear browser cache\n• Reset password\n• Account locked? → Contact PACS admin\n• Remote? → VPN must be connected"),

    (["image", "loading", "slow", "not load", "blank", "not display", "hanging", "lent", "charg"],
     "🖼️ Images not loading / slow:\n• Refresh viewer (F5)\n• Close other studies\n• Use wired internet\n• Tools → Clear Cache\n• Server busy → wait or cry to IT\n• Try different browser/workstation"),

    (["connectivity", "network", "cant connect", "timeout", "server not", "offline", "réseau"],
     "🌐 Connectivity issues:\n• Restart PC\n• Check VPN\n• Ping PACS server\n• Firewall blocking port 104/443?\n• Everyone down or just you?"),

    (["study", "not found", "missing", "cant find", "search", "no results", "examen"],
     "🔍 Study not found:\n• Double-check Patient ID, Name, DOB, Accession\n• Widen date range\n• Check Unread/All/Archive\n• Still sending from modality? Wait 5 min\n• >24h old → ask admin to prefetch"),

    (["dicom", "send fail", "modality", "wont send", "reject", "ae title"],
     "📤 DICOM send failing:\n• Check AE Title, IP, Port on modality\n• Restart modality\n• Check DICOM log for error\n• Firewall port 104?\n• Duplicate AE Title = chaos"),

    (["crash", "down", "not working", "system down", "unavailable"],
     "💀 PACS completely down:\n• Planned maintenance?\n• Use backup viewer\n• Call emergency PACS line\n• Pray"),

    (["hanging protocol", "layout", "wrong order", "display protocol"],
     "🖥️ Hanging protocols messed up:\n• Right-click → Reset to Default\n• Create new one\n• Clear user cache"),

    (["access", "permission", "denied", "cant open", "no rights"],
     "🚫 Access denied:\n• Your account lacks permission\n• Contact PACS admin"),

    (["ris", "worklist", "hl7", "order not showing", "integration"],
     "📋 RIS/HIS issues:\n• HL7 order didn’t arrive\n• Patient merge conflict\n• Re-send order from HIS"),

    (["cache", "clear cache", "memory"],
     "🧹 Clear cache (fixes 90% of weird shit):\n• Tools → Clear Local Cache\n• Or Ctrl+Shift+Delete"),
]

def find_answer(user_input):
    user_input = user_input.lower().strip()
    
    if user_input in ["quit", "bye", "exit", "merci"]:
        return "Good luck bro, PACS will break again tomorrow 😂"
    
    for keywords, answer in faqs:
        if any(k in user_input for k in keywords):
            return answer
    
    return "Didn't catch that one yet 🤔\nTry describing better or call your PACS admin directly.\nCommon ones: login, slow images, study missing, etc."

# === STREAMLIT WEB INTERFACE ===
st.set_page_config(page_title="PACS Support Bot", page_icon="🩻")

st.title("🩻 PACS Support Bot v2")
st.caption("Built for the real radiology struggles 🔥 - Ask anything")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What's your PACS issue today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    response = find_answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
