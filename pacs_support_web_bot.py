# =============================================
# PACS SUPPORT BOT v12 – MULTILINGUAL MEDICAL EDITION
# =============================================
import streamlit as st
st.set_page_config(
    page_title="PACS Helper Bot",
    page_icon="🩺",  # Friendlier medical icon
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =================== MEDICAL-THEMED DESIGN WITH BACKGROUND ===================
background_image_url = "https://openmedscience.com/wp-content/uploads/2025/07/Understanding-Medical-Imaging-1024x574.jpg"
st.markdown(f"""
<style>
    .main {{
        background: linear-gradient(to bottom, #f0f8ff, #e0ffff); 
        background-image: url('{background_image_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh; 
        padding: 2rem;
        opacity: 0.95;  /* Subtle opacity for readability */
    }}
    .block-container {{
        background: rgba(255, 255, 255, 0.9); 
        border-radius: 30px; 
        padding: 3rem; 
        box-shadow: 0 12px 35px rgba(0,0,0,0.08);
    }}
    .big-title {{
        font-size: 4.2rem !important; 
        font-weight: 900; 
        text-align: center;
        background: linear-gradient(to right, #00bfff, #20b2aa, #00fa9a);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
    }}
    .subheader {{
        font-size: 1.8rem !important; 
        text-align: center; 
        color: #333; 
        margin-bottom: 1rem;
    }}
    .friend-btn button {{
        height: 85px !important; 
        font-size: 1.4rem !important;
        background: linear-gradient(45deg, #48d1cc, #20b2aa, #00fa9a) !important;
        border-radius: 25px !important; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.15) !important;
        transition: transform 0.3s; 
    }}
    .friend-btn button:hover {{
        transform: scale(1.05);
    }}
    .step-box {{
        background: #f0fff0; 
        padding: 1.8rem; 
        border-radius: 20px; 
        border-left: 8px solid #20b2aa; 
        margin: 1.2rem 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}
    .stChatMessage {{
        border-radius: 22px; 
        padding: 1.2rem; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    [data-testid="stChatMessageUser"] {{
        background: #e0ffff;
    }}
    [data-testid="stChatMessageAssistant"] {{
        background: #f0fff0;
    }}
    .emoji-title {{
        font-size: 2rem; 
        margin-top: 2rem;
    }}
    .resource-expander {{
        background: #fff; 
        border-radius: 15px; 
        padding: 1rem; 
        margin: 1rem 0;
    }}
    /* RTL support for Arabic */
    [dir="rtl"] {{
        direction: rtl;
        text-align: right;
    }}
</style>
""", unsafe_allow_html=True)

# =================== LANGUAGE SELECTOR ===================
if "language" not in st.session_state:
    st.session_state.language = "English"

lang_options = {"English": "en", "Français": "fr", "عربي": "ar"}
selected_lang = st.selectbox("Choose language / Choisissez la langue / اختر اللغة", list(lang_options.keys()))
st.session_state.language = selected_lang
lang_code = lang_options[selected_lang]

# =================== TRANSLATIONS ===================
translations = {
    "en": {
        "title": "PACS Helper Bot 🩺",
        "subheader": "Your super friendly 24/7 PACS assistant – Always here to help!<br>English • Français • عربي",
        "prompt_hint": "😊 Just tell me what’s wrong – I’ll guide you step by step with a smile!",
        "guided_title": "🛠️ Let's fix this together – step by step!",
        "diagnosis_complete": "Diagnosis complete! Here's what I recommend based on your answers 😊",
        "pacs_down": "PACS is down for everyone → Switch to backup viewer → Call emergency IT line now! 📞",
        "universal_fix": "Try the UNIVERSAL FIX first → Clear cache & restart – it works 97% of the time! ✨",
        "start_over": "Start over",
        "network_title": "🔌 Network & Server Connection Test",
        "network_info": "Replace `YOUR_PACS_IP_HERE` with your actual PACS server IP (ask your IT team if unsure) 🌐",
        "copy_commands": "Copy commands (ready to paste)",
        "resources_title": "📚 Extra Troubleshooting Guides",
        "config_guide": "🛠️ RIS/Work List/PACS Configuration Guide",
        "config_steps": """
**Steps for Setup:**
1. **RIS to Work List:** Install Java VM, set IP:Port in Admin → Install Parameters, enable auto send.
2. **Work List to Modalities:** Set AE Titles in Parameters → Exam Rooms. Configure MPPS if needed.
3. **Modalities to PACS/MiniPACS:** Get IPs, Ports, AETs from product responsible. Supplier sets auto storage.
        """,
        "mpls_guide": "🔍 MPLS Test Checklist for PACS",
        "mpls_steps": """
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
        """,
        "blockage_guide": "🚨 Server Blockage Procedure (PACS/MiniPACS/Worklist)",
        "blockage_steps": """
**Initial Verification:**
1. Ping server.
2. DICOM Echo: http://IP:8080/dcm4chee-web3/
3. SSH: admsite / your site password
4. Check services: sudo systemctl status dcm4chee.service & xampp.service
5. Disk space: sudo df -h (check /opt/dcm4chee/...)

**Manual Restart (if >30min down):**
1. sudo systemctl stop dcm4chee.service
2. sudo systemctl stop xampp.service
3. sudo systemctl start xampp.service
4. sudo systemctl start dcm4chee.service
5. Verify & contact IT if persists.
        """,
        "universal_button": "✨ UNIVERSAL FIX\n(Works 97% of time!)",
        "universal_solution": "1. Close all tabs & PACS apps\n2. Clear browser cache (Ctrl+Shift+Delete)\n3. Restart your computer\n4. Try again – magic! 🎉",
        "guided_button": "🧭 STEP-BY-STEP\nGUIDED HELP",
        "cache_button": "🧹 CLEAR CACHE\nQuick How-to",
        "network_button": "🔌 NETWORK CHECK\n& Ports Test",
        "blockage_button": "🚨 SERVER BLOCKAGE\nProcedure",
        "resources_button": "📚 MORE GUIDES\n& Resources",
        "chat_welcome": "Hey there, doctor! 😊 What’s not working with PACS today? I'm here to help! 🩺",
        "chat_input": "Or just type your issue here… (e.g. “images slow”, “server blocked”, “مرحبا”, “je n’arrive pas à me connecter”)",
        "detected": "→ {name} detected! Here's the fix:",
        "not_found": "Hmm, I didn’t quite catch that... But no worries! 😊 Try one of the buttons above or describe it more (e.g., 'network slow' or 'configuration RIS').",
        "footer": "Made with ❤️ for radiologists who deserve the best • Free forever • Share with your team! 🩺",
        "steps": [
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
        ],
        "quick_fixes": {
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
                "solution": "→ Verify network ping to server\n→ Test DICOM Echo: http://IP:8080/dcm4chee-web3/\n→ SSH with admin credentials\n→ Check services: sudo systemctl status dcm4chee.service & xampp.service\n→ If down >30min, restart: stop then start xampp & dcm4chee\n→ Check disk space: sudo df -h 💻"
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
    },
    "fr": {
        "title": "Bot d'Assistance PACS 🩺",
        "subheader": "Votre assistant PACS super amical 24/7 – Toujours là pour aider !<br>English • Français • عربي",
        "prompt_hint": "😊 Dites-moi simplement ce qui ne va pas – Je vous guiderai étape par étape avec un sourire !",
        "guided_title": "🛠️ Résolvons cela ensemble – étape par étape !",
        "diagnosis_complete": "Diagnostic terminé ! Voici ce que je recommande basé sur vos réponses 😊",
        "pacs_down": "PACS est en panne pour tout le monde → Passez au visualiseur de secours → Appelez la ligne IT d'urgence maintenant ! 📞",
        "universal_fix": "Essayez d'abord la SOLUTION UNIVERSELLE → Effacez le cache & redémarrez – ça marche 97% du temps ! ✨",
        "start_over": "Recommencer",
        "network_title": "🔌 Test de Connexion Réseau & Serveur",
        "network_info": "Remplacez `YOUR_PACS_IP_HERE` par l'IP réelle de votre serveur PACS (demandez à votre équipe IT si incertain) 🌐",
        "copy_commands": "Copier les commandes (prêtes à coller)",
        "resources_title": "📚 Guides de Dépannage Supplémentaires",
        "config_guide": "🛠️ Guide de Configuration RIS/Liste de Travail/PACS",
        "config_steps": """
**Étapes de Configuration :**
1. **RIS vers Liste de Travail :** Installez Java VM, définissez IP:Port dans Admin → Paramètres d'Installation, activez l'envoi automatique.
2. **Liste de Travail vers Modalités :** Définissez les AE Titles dans Paramètres → Salles d'Examen. Configurez MPPS si nécessaire.
3. **Modalités vers PACS/MiniPACS :** Obtenez IPs, Ports, AETs du responsable produit. Le fournisseur gère la configuration de stockage automatique.
        """,
        "mpls_guide": "🔍 Liste de Contrôle de Test MPLS pour PACS",
        "mpls_steps": """
**Connectivité Réseau :**
- Ping PACS : Vérifiez latence <50ms, pas de perte de paquets.
- Tracert/Traceroute : Assurez-vous que le trafic passe par MPLS.

**Performance & QoS :**
- iperf3 : Mesurez bande passante/latence pour fichiers DICOM.
- mtr : Jitter <20ms, perte <1%.

**Tests App PACS :**
- Connectez depuis un site distant.
- C-FIND pour examens.
- C-MOVE/C-GET pour images.
- Visualiseur WADO : Testez scanner, IRM, radiologie standard.
        """,
        "blockage_guide": "🚨 Procédure de Blocage Serveur (PACS/MiniPACS/Liste de Travail)",
        "blockage_steps": """
**Vérification Initiale :**
1. Ping serveur.
2. Écho DICOM : http://IP:8080/dcm4chee-web3/
3. SSH : identifiants admin
4. Vérifiez services : sudo systemctl status dcm4chee.service & xampp.service
5. Espace disque : sudo df -h (vérifiez /opt/dcm4chee/...)

**Redémarrage Manuel (si >30min en panne) :**
1. sudo systemctl stop dcm4chee.service
2. sudo systemctl stop xampp.service
3. sudo systemctl start xampp.service
4. sudo systemctl start dcm4chee.service
5. Vérifiez & contactez IT si persiste.
        """,
        "universal_button": "✨ SOLUTION UNIVERSELLE\n(Fonctionne 97% du temps !)",
        "universal_solution": "1. Fermez tous les onglets & apps PACS\n2. Effacez le cache navigateur (Ctrl+Shift+Delete)\n3. Redémarrez votre ordinateur\n4. Réessayez – magie ! 🎉",
        "guided_button": "🧭 AIDE GUIDÉE\nÉTAPE PAR ÉTAPE",
        "cache_button": "🧹 EFFACER CACHE\nGuide Rapide",
        "network_button": "🔌 TEST RÉSEAU\n& Ports",
        "blockage_button": "🚨 PROCÉDURE BLOCAGE SERVEUR",
        "resources_button": "📚 PLUS DE GUIDES\n& Ressources",
        "chat_welcome": "Salut, docteur ! 😊 Qu'est-ce qui ne va pas avec PACS aujourd'hui ? Je suis là pour aider ! 🩺",
        "chat_input": "Ou tapez simplement votre problème ici… (ex. “images lentes”, “serveur bloqué”, “مرحبا”, “je n’arrive pas à me connecter”)",
        "detected": "→ {name} détecté ! Voici la solution :",
        "not_found": "Hmm, je n'ai pas tout à fait compris... Mais pas de souci ! 😊 Essayez un des boutons ci-dessus ou décrivez plus (ex. 'réseau lent' ou 'configuration RIS').",
        "footer": "Fait avec ❤️ pour les radiologues qui méritent le meilleur • Gratuit pour toujours • Partagez avec votre équipe ! 🩺",
        "steps": [
            ("Quel est le problème principal ?", [
                "Impossible de se connecter",
                "Images lentes ou vides",
                "Étude manquante",
                "Modalité n'envoie pas d'images",
                "Impossible de se connecter à PACS / timeout",
                "Serveur bloqué ou en panne",
                "Problème de configuration ou setup",
                "Performance mauvaise (réseau lent)",
                "Tout gèle",
                "Autre problème"
            ]),
            ("Les autres docteurs peuvent-ils ouvrir PACS maintenant ?", ["Oui", "Non, tout le monde a le même problème", "Pas sûr"]),
            ("Avez-vous essayé d'effacer le cache ?", ["Oui", "Non – montrez-moi comment", "Je l'ai fait mais pas de changement"]),
            ("Avez-vous vérifié la connexion réseau (ping/tracert) ?", ["Oui, c'est bon", "Non – montrez-moi comment", "C'est mauvais"]),
            ("Est-ce un problème côté serveur (ex. blocage après coupure de courant) ?", ["Oui", "Non", "Pas sûr"]),
        ],
        "quick_fixes": {
            "login|password|locked|تسجيل|mot de passe": {
                "name": "Problème de connexion",
                "solution": "→ Essayez de vous connecter en mode incognito\n→ Effacez le cache de votre navigateur (Ctrl+Shift+Delete)\n→ Réinitialisez le mot de passe via l'admin\n→ Si verrouillé, contactez l'admin PACS immédiatement 🛡️"
            },
            "image|slow|blank|not load|صور|lent": {
                "name": "Images ne chargent pas ou lentes",
                "solution": "→ Appuyez sur F5 pour rafraîchir\n→ Fermez les autres études ouvertes\n→ Allez dans Outils → Effacer Cache Local\n→ Passez à internet filaire si en WiFi\n→ Vérifiez la vitesse réseau – les images peuvent être énormes ! 📸"
            },
            "study|missing|not found|دراسة|examen": {
                "name": "Étude ne s'affiche pas",
                "solution": "→ Vérifiez doublement l'ID Patient & Numéro d'Accession\n→ Élargissez la plage de dates de recherche\n→ Demandez à l'admin de précharger l'étude\n→ Vérifiez si c'est dans MiniPACS à la place 🌟"
            },
            "dicom|send|modality|إرسال": {
                "name": "Modalité n'envoie pas d'images",
                "solution": "→ Vérifiez AE Title dans menu RIS : Paramètres → Salles d'Examen\n→ Assurez-vous que IP & Port Liste de Travail sont corrects (ex. 192.168.0.1:2575)\n→ Vérifiez que Java VM est installé sur client\n→ Contactez fournisseur machine pour setup MPPS ⚙️"
            },
            "connect|timeout|network|server|offline|mpls": {
                "name": "Problème de connexion ou réseau",
                "solution": "→ Exécutez ping et tracert vers IP PACS\n→ Vérifiez latence (<50ms idéal)\n→ Utilisez iperf3 pour test bande passante\n→ Vérifiez routage MPLS\n→ Testez Écho DICOM via interface web 🔌"
            },
            "cache|clear": {
                "name": "Effacer cache",
                "solution": "→ Dans navigateur : Ctrl+Shift+Delete → Effacez images & fichiers en cache\n→ Dans visualiseur PACS : Outils → Effacer Cache Local\n→ Redémarrez navigateur – 97% des problèmes résolus ! ✨"
            },
            "block|blocage|server down|pacs down|mini pacs|worklist|crash": {
                "name": "Blocage serveur ou en panne",
                "solution": "→ Vérifiez ping réseau vers serveur\n→ Testez Écho DICOM : http://IP:8080/dcm4chee-web3/\n→ SSH avec identifiants admin\n→ Vérifiez services : sudo systemctl status dcm4chee.service & xampp.service\n→ Si en panne >30min, redémarrez : stop puis start xampp & dcm4chee\n→ Vérifiez espace disque : sudo df -h 💻"
            },
            "config|parametrage|setup|ris|work list|pacs config": {
                "name": "Problème de configuration ou setup",
                "solution": "→ Pour RIS vers Liste de Travail : Définissez IP:Port dans Système Admin → Paramètres Installation, activez envoi auto\n→ Liste de Travail vers Modalités : Définissez AE Titles dans Paramètres RIS → Salles d'Examen\n→ Modalités vers PACS/MiniPACS : Obtenez IPs, Ports, AETs du responsable produit\n→ Fournisseur gère setup stockage auto 🛠️"
            },
            "performance|qos|jitter|loss|bandwidth": {
                "name": "Problème de performance ou QoS",
                "solution": "→ Mesurez bande passante & latence avec iperf3\n→ Vérifiez jitter & perte paquets avec mtr\n→ Objectif : Jitter <20ms, perte <1%, bande passante suffisante pour fichiers DICOM\n→ Test app : Connectez à PACS, C-FIND, C-MOVE, visualiseur WADO 📊"
            },
        }
    },
    "ar": {
        "title": "روبوت مساعد PACS 🩺",
        "subheader": "مساعد PACS الودي الفائق المتاح 24/7 – دائمًا هنا للمساعدة!<br>English • Français • عربي",
        "prompt_hint": "😊 فقط أخبرني بما هو الخطأ – سأرشدك خطوة بخطوة مع ابتسامة!",
        "guided_title": "🛠️ دعونا نصلح هذا معًا – خطوة بخطوة!",
        "diagnosis_complete": "اكتمل التشخيص! إليك ما أوصي به بناءً على إجاباتك 😊",
        "pacs_down": "PACS معطل للجميع → انتقل إلى العارض الاحتياطي → اتصل بخط الطوارئ IT الآن! 📞",
        "universal_fix": "جرب الإصلاح العالمي أولاً → مسح الذاكرة المؤقتة وإعادة التشغيل – يعمل 97% من الوقت! ✨",
        "start_over": "ابدأ من جديد",
        "network_title": "🔌 اختبار الاتصال بالشبكة والخادم",
        "network_info": "استبدل `YOUR_PACS_IP_HERE` بعنوان IP الفعلي لخادم PACS (اسأل فريق IT إذا غير متأكد) 🌐",
        "copy_commands": "نسخ الأوامر (جاهزة للصق)",
        "resources_title": "📚 دليل إرشادات إصلاح الأخطاء الإضافية",
        "config_guide": "🛠️ دليل تكوين RIS/قائمة العمل/PACS",
        "config_steps": """
**خطوات الإعداد:**
1. **RIS إلى قائمة العمل:** قم بتثبيت Java VM، قم بتعيين IP:Port في الإدارة → معلمات التثبيت، قم بتمكين الإرسال التلقائي.
2. **قائمة العمل إلى الطرق:** قم بتعيين AE Titles في المعلمات → غرف الفحص. قم بتكوين MPPS إذا لزم الأمر.
3. **الطرق إلى PACS/MiniPACS:** احصل على IPs، Ports، AETs من المسؤول عن المنتج. يتعامل المورد مع إعداد التخزين التلقائي.
        """,
        "mpls_guide": "🔍 قائمة تحقق اختبار MPLS لـ PACS",
        "mpls_steps": """
**الاتصال بالشبكة:**
- Ping PACS: تحقق من التأخير <50ms، لا فقدان حزم.
- Tracert/Traceroute: تأكد من مرور الحركة عبر MPLS.

**الأداء & QoS:**
- iperf3: قياس عرض النطاق/التأخير لملفات DICOM.
- mtr: الاهتزاز <20ms، الخسارة <1%.

**اختبارات تطبيق PACS:**
- الاتصال من موقع بعيد.
- C-FIND للفحوصات.
- C-MOVE/C-GET للصور.
- عارض WADO: اختبار الماسح الضوئي، IRM، الإشعاع القياسي.
        """,
        "blockage_guide": "🚨 إجراء انسداد الخادم (PACS/MiniPACS/قائمة العمل)",
        "blockage_steps": """
**التحقق الأولي:**
1. Ping الخادم.
2. صدى DICOM: http://IP:8080/dcm4chee-web3/
3. SSH: بيانات اعتماد الإدارة
4. تحقق من الخدمات: sudo systemctl status dcm4chee.service & xampp.service
5. مساحة القرص: sudo df -h (تحقق /opt/dcm4chee/...)

**إعادة التشغيل اليدوي (إذا >30 دقيقة معطل):**
1. sudo systemctl stop dcm4chee.service
2. sudo systemctl stop xampp.service
3. sudo systemctl start xampp.service
4. sudo systemctl start dcm4chee.service
5. تحقق واتصل بـ IT إذا استمر.
        """,
        "universal_button": "✨ الإصلاح العالمي\n(يعمل 97% من الوقت!)",
        "universal_solution": "1. أغلق جميع التبويبات وتطبيقات PACS\n2. مسح ذاكرة المتصفح المؤقتة (Ctrl+Shift+Delete)\n3. أعد تشغيل جهاز الكمبيوتر\n4. جرب مرة أخرى – سحر! 🎉",
        "guided_button": "🧭 مساعدة موجهة\nخطوة بخطوة",
        "cache_button": "🧹 مسح الذاكرة المؤقتة\nدليل سريع",
        "network_button": "🔌 اختبار الشبكة\n& المنافذ",
        "blockage_button": "🚨 إجراء انسداد الخادم",
        "resources_button": "📚 المزيد من الدليل\n& الموارد",
        "chat_welcome": "مرحبا، دكتور! 😊 ما الذي لا يعمل في PACS اليوم؟ أنا هنا للمساعدة! 🩺",
        "chat_input": "أو اكتب مشكلتك هنا… (مثل “الصور بطيئة”، “الخادم محظور”، “مرحبا”، “je n’arrive pas à me connecter”)",
        "detected": "→ تم اكتشاف {name}! إليك الإصلاح:",
        "not_found": "همم، لم أفهم ذلك تمامًا... لكن لا مشكلة! 😊 جرب أحد الأزرار أعلاه أو وصف أكثر (مثل 'شبكة بطيئة' أو 'تكوين RIS').",
        "footer": "صنع بحب ❤️ للأطباء الإشعاعيين الذين يستحقون الأفضل • مجاني إلى الأبد • شارك مع فريقك! 🩺",
        "steps": [
            ("ما هو المشكل الرئيسي؟", [
                "لا يمكن تسجيل الدخول",
                "الصور بطيئة أو فارغة",
                "الدراسة مفقودة",
                "الطريقة لا ترسل الصور",
                "لا يمكن الاتصال بـ PACS / انتهاء المهلة",
                "الخادم محظور أو معطل",
                "مشكلة تكوين أو إعداد",
                "الأداء سيء (شبكة بطيئة)",
                "كل شيء يتجمد",
                "مشكلة أخرى"
            ]),
            ("هل يمكن للأطباء الآخرين فتح PACS الآن؟", ["نعم", "لا، الجميع لديه نفس المشكلة", "غير متأكد"]),
            ("هل جربت مسح الذاكرة المؤقتة بعد؟", ["نعم", "لا – أرني كيف", "فعلت لكن لا تغيير"]),
            ("هل تحققت من اتصال الشبكة (ping/tracert)؟", ["نعم، جيد", "لا – أرني كيف", "سيء"]),
            ("هل هذا مشكلة جانب الخادم (مثل انسداد بعد انقطاع الكهرباء)؟", ["نعم", "لا", "غير متأكد"]),
        ],
        "quick_fixes": {
            "login|password|locked|تسجيل|mot de passe": {
                "name": "مشكلة تسجيل الدخول",
                "solution": "→ جرب تسجيل الدخول عبر وضع التصفح الخفي\n→ مسح ذاكرة المتصفح المؤقتة (Ctrl+Shift+Delete)\n→ إعادة تعيين كلمة المرور عبر الإدارة\n→ إذا محظور، اتصل بإدارة PACS فورًا 🛡️"
            },
            "image|slow|blank|not load|صور|lent": {
                "name": "الصور لا تحمل أو بطيئة",
                "solution": "→ اضغط F5 للتحديث\n→ أغلق الدراسات الأخرى المفتوحة\n→ اذهب إلى أدوات → مسح الذاكرة المؤقتة المحلية\n→ انتقل إلى إنترنت سلكي إذا على WiFi\n→ تحقق من سرعة الشبكة – الصور يمكن أن تكون هائلة! 📸"
            },
            "study|missing|not found|دراسة|examen": {
                "name": "الدراسة لا تظهر",
                "solution": "→ تحقق مرة أخرى من هوية المريض ورقم الوصول\n→ وسع نطاق تاريخ البحث\n→ اطلب من الإدارة تحميل الدراسة مسبقًا\n→ تحقق إذا كانت في MiniPACS بدلاً من ذلك 🌟"
            },
            "dicom|send|modality|إرسال": {
                "name": "الطريقة لا ترسل الصور",
                "solution": "→ تحقق من AE Title في قائمة RIS: المعلمات → غرف الفحص\n→ تأكد من تعيين IP & Port قائمة العمل بشكل صحيح (مثل 192.168.0.1:2575)\n→ تحقق من تثبيت Java VM على العميل\n→ اتصل بمورد الجهاز لإعداد MPPS ⚙️"
            },
            "connect|timeout|network|server|offline|mpls": {
                "name": "مشكلة اتصال أو شبكة",
                "solution": "→ شغل ping وtracert إلى IP PACS\n→ تحقق من التأخير (<50ms مثالي)\n→ استخدم iperf3 لاختبار عرض النطاق\n→ تحقق من توجيه MPLS\n→ اختبر صدى DICOM عبر واجهة الويب 🔌"
            },
            "cache|clear": {
                "name": "مسح الذاكرة المؤقتة",
                "solution": "→ في المتصفح: Ctrl+Shift+Delete → مسح الصور والملفات المخزنة مؤقتًا\n→ في عارض PACS: أدوات → مسح الذاكرة المؤقتة المحلية\n→ أعد تشغيل المتصفح – 97% من المشكلات محلوطة! ✨"
            },
            "block|blocage|server down|pacs down|mini pacs|worklist|crash": {
                "name": "انسداد الخادم أو معطل",
                "solution": "→ تحقق من ping الشبكة إلى الخادم\n→ اختبر صدى DICOM: http://IP:8080/dcm4chee-web3/\n→ SSH ببيانات اعتماد الإدارة\n→ تحقق من الخدمات: sudo systemctl status dcm4chee.service & xampp.service\n→ إذا معطل >30دقيقة، أعد التشغيل: stop ثم start xampp & dcm4chee\n→ تحقق من مساحة القرص: sudo df -h 💻"
            },
            "config|parametrage|setup|ris|work list|pacs config": {
                "name": "مشكلة تكوين أو إعداد",
                "solution": "→ لـ RIS إلى قائمة العمل: تعيين IP:Port في نظام الإدارة → معلمات التثبيت، تمكين الإرسال التلقائي\n→ قائمة العمل إلى الطرق: تعيين AE Titles في معلمات RIS → غرف الفحص\n→ الطرق إلى PACS/MiniPACS: احصل على IPs، Ports، AETs من المسؤول عن المنتج\n→ يتعامل المورد مع إعداد التخزين التلقائي 🛠️"
            },
            "performance|qos|jitter|loss|bandwidth": {
                "name": "مشكلة أداء أو QoS",
                "solution": "→ قياس عرض النطاق والتأخير مع iperf3\n→ تحقق من الاهتزاز وفقدان الحزم مع mtr\n→ الهدف: الاهتزاز <20ms، الخسارة <1%، عرض النطاق كافٍ لملفات DICOM\n→ اختبار التطبيق: اتصل بـ PACS، C-FIND، C-MOVE، عارض WADO 📊"
            },
        }
    }
}

tr = translations[lang_code]

# =================== HEADER ===================
dir_attr = ' dir="rtl"' if lang_code == "ar" else ""
st.markdown(f'<h1 class="big-title"{dir_attr}>{tr["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<h3 class="subheader"{dir_attr}>{tr["subheader"]}</h3>', unsafe_allow_html=True)
st.markdown(f'######{dir_attr} {tr["prompt_hint"]}', unsafe_allow_html=True)

# =================== EXPANDED QUICK FIXES DATABASE ===================
QUICK_FIXES = tr["quick_fixes"]

# =================== STEP-BY-STEP GUIDED CHECKLIST (EXPANDED) ===================
def guided_checklist():
    st.markdown(f'<p class="emoji-title"{dir_attr}>{tr["guided_title"]}</p>', unsafe_allow_html=True)
    
    progress = st.progress(0)
    step = st.session_state.get("check_step", 0)
    
    steps = tr["steps"]
    
    if step < len(steps):
        progress.progress((step + 1) / len(steps))
        q, options = steps[step]
        st.markdown(f'<div class="step-box"{dir_attr}><strong>Step {step+1}/{len(steps)}: {q}</strong></div>', unsafe_allow_html=True)
        choice = st.radio("", options, key=f"step{step}")
        
        if st.button("Next →" if lang_code != "ar" else "التالي ←", type="primary", use_container_width=True):
            st.session_state[f"ans{step}"] = choice
            st.session_state.check_step = step + 1
            st.rerun()
    else:
        progress.progress(1.0)
        st.success(tr["diagnosis_complete"])
        
        # Expanded logic based on answers
        a1 = st.session_state.get("ans0", "").lower()
        a2 = st.session_state.get("ans1", "").lower()
        a3 = st.session_state.get("ans2", "").lower()
        a4 = st.session_state.get("ans3", "").lower()
        a5 = st.session_state.get("ans4", "").lower()
        
        if "everyone" in a2 or "tout le monde" in a2 or "الجميع" in a2:
            st.error(tr["pacs_down"])
        elif "login" in a1 or "connexion" in a1 or "تسجيل" in a1:
            st.info(QUICK_FIXES["login|password|locked|تسجيل|mot de passe"]["solution"])
        elif "image" in a1:
            st.info(QUICK_FIXES["image|slow|blank|not load|صور|lent"]["solution"])
        elif "study" in a1 or "étude" in a1 or "دراسة" in a1:
            st.info(QUICK_FIXES["study|missing|not found|دراسة|examen"]["solution"])
        elif "modality" in a1 or "modalité" in a1 or "طريقة" in a1:
            st.info(QUICK_FIXES["dicom|send|modality|إرسال"]["solution"])
        elif "connect" in a1 or "performance" in a1:
            st.info(QUICK_FIXES["connect|timeout|network|server|offline|mpls"]["solution"])
        elif "server" in a1 or "yes" in a5 or "oui" in a5 or "نعم" in a5:
            st.info(QUICK_FIXES["block|blocage|server down|pacs down|mini pacs|worklist|crash"]["solution"])
        elif "config" in a1:
            st.info(QUICK_FIXES["config|parametrage|setup|ris|work list|pacs config"]["solution"])
        else:
            st.info(tr["universal_fix"])
        
        if st.button(tr["start_over"]):
            st.session_state.check_step = 0
            st.rerun()

# =================== NETWORK CHECK (WITH PLACEHOLDER IP) ===================
def network_check():
    st.markdown(f'<p class="emoji-title"{dir_attr}>{tr["network_title"]}</p>', unsafe_allow_html=True)
    st.info(tr["network_info"])
    
    commands = """
ping YOUR_PACS_IP_HERE
tracert YOUR_PACS_IP_HERE # Windows
traceroute YOUR_PACS_IP_HERE # Linux/Mac
telnet YOUR_PACS_IP_HERE 104
telnet YOUR_PACS_IP_HERE 443
Test-NetConnection YOUR_PACS_IP_HERE -Port 104 # PowerShell
iperf3 -c YOUR_PACS_IP_HERE # Bandwidth test (install iperf3 if needed)
mtr YOUR_PACS_IP_HERE # Jitter & loss
"""
    st.code(commands.strip(), language="bash")
    
    if st.button(tr["copy_commands"]):
        st.code(commands.strip())

# =================== ADDITIONAL TROUBLESHOOTING RESOURCES ===================
def show_resources():
    st.markdown(f'<p class="emoji-title"{dir_attr}>{tr["resources_title"]}</p>', unsafe_allow_html=True)
    
    with st.expander(tr["config_guide"], expanded=False):
        st.markdown(tr["config_steps"])
    
    with st.expander(tr["mpls_guide"], expanded=False):
        st.markdown(tr["mpls_steps"])
    
    with st.expander(tr["blockage_guide"], expanded=False):
        st.markdown(tr["blockage_steps"])

# =================== MAIN BUTTONS (MORE FRIENDLY GRID) ===================
st.markdown("---")
cols = st.columns(3)
with cols[0]:
    if st.button(tr["universal_button"], type="primary", use_container_width=True, key="universal"):
        st.success(tr["universal_solution"])
with cols[1]:
    if st.button(tr["guided_button"], type="primary", use_container_width=True, key="guided"):
        st.session_state.check_step = 0
with cols[2]:
    if st.button(tr["cache_button"], type="primary", use_container_width=True, key="cache"):
        st.info(QUICK_FIXES["cache|clear"]["solution"])
cols2 = st.columns(3)
with cols2[0]:
    if st.button(tr["network_button"], type="primary", use_container_width=True, key="network"):
        network_check()
with cols2[1]:
    if st.button(tr["blockage_button"], type="primary", use_container_width=True, key="blockage"):
        st.info(QUICK_FIXES["block|blocage|server down|pacs down|mini pacs|worklist|crash"]["solution"])
with cols2[2]:
    if st.button(tr["resources_button"], type="primary", use_container_width=True, key="resources"):
        show_resources()
st.markdown("---")

# =================== SHOW GUIDED CHECKLIST IF ACTIVE ===================
if st.session_state.get("check_step", 0) > 0:
    guided_checklist()
    st.markdown("---")

# =================== CHAT (SMARTER FALLBACK WITH MORE MATCHES) ===================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": tr["chat_welcome"]}]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input(tr["chat_input"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): 
        st.markdown(prompt)
    
    found = False
    for triggers, info in QUICK_FIXES.items():
        if any(t in prompt.lower() for t in triggers.split("|")):
            st.success(tr["detected"].format(name=info['name']))
            st.info(info["solution"])
            found = True
    
    if not found:
        st.info(tr["not_found"])

# =================== FOOTER ===================
st.markdown("---")
st.caption(tr["footer"])
