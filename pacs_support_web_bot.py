# PACS SUPPORT BOT - Version Simplifiée et Fonctionnelle
import streamlit as st
import time
import random
from datetime import datetime

# =================== CONFIGURATION ===================
st.set_page_config(
    page_title="PACS Helper Bot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== STYLES CSS ===================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
        padding: 20px;
    }
    
    .medical-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #1e90ff;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .emergency-card {
        background: #fff5f5;
        border-left: 5px solid #ff6b6b;
    }
    
    .solution-card {
        background: #f0fff4;
        border-left: 5px solid #38a169;
    }
    
    .chat-user {
        background: #e3f2fd;
        border-radius: 10px 10px 0 10px;
        padding: 10px;
        margin: 5px;
    }
    
    .chat-assistant {
        background: #f0fff4;
        border-radius: 10px 10px 10px 0;
        padding: 10px;
        margin: 5px;
    }
    
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        margin: 2px;
    }
    
    .critical { background: #fed7d7; color: #742a2a; }
    .high { background: #fef3c7; color: #92400e; }
    .medium { background: #dbeafe; color: #1e40af; }
    .low { background: #d1fae5; color: #065f46; }
</style>
""", unsafe_allow_html=True)

# =================== BASE DE DONNÉES DES PROBLÈMES ===================
PROBLEMS_DATABASE = {
    "images_not_loading": {
        "name": "📸 Images ne se chargent pas",
        "triggers": ["image", "charger", "afficher", "blanc", "vide"],
        "symptoms": ["Écran blanc", "Loader infini", "Message d'erreur"],
        "severity": "medium",
        "solutions": [
            "1. 🔌 Vérifier la connexion au serveur PACS",
            "2. 🖥️ Redémarrer la station de travail",
            "3. 🧹 Nettoyer le cache navigateur (Ctrl+Shift+R)",
            "4. 📞 Contacter le support IT si persiste >15min"
        ],
        "time": "5-15 minutes"
    },
    "slow_performance": {
        "name": "🐌 Performance lente",
        "triggers": ["lent", "ralenti", "performance", "chargement"],
        "symptoms": ["Délais importants", "Interface gelée", "CPU à 100%"],
        "severity": "low",
        "solutions": [
            "1. ❌ Fermer applications inutiles",
            "2. 🗑️ Vider cache temporaire",
            "3. 🌐 Vérifier connexion réseau",
            "4. 🔄 Redémarrer la machine"
        ],
        "time": "10-20 minutes"
    },
    "login_failure": {
        "name": "🔐 Échec de connexion",
        "triggers": ["login", "connexion", "mot de passe", "accès"],
        "symptoms": ["Erreur 401/403", "Identifiants rejetés", "Session expirée"],
        "severity": "high",
        "solutions": [
            "1. 🔒 Vérifier caps lock",
            "2. 🔄 Réinitialiser mot de passe",
            "3. 📞 Contacter helpdesk",
            "4. 👥 Utiliser compte temporaire"
        ],
        "time": "2-10 minutes"
    },
    "printing_issue": {
        "name": "🖨️ Problème d'impression",
        "triggers": ["imprimante", "impression", "papier", "film"],
        "symptoms": ["File d'attente bloquée", "Mauvais format", "Erreur driver"],
        "severity": "medium",
        "solutions": [
            "1. 🔌 Vérifier connexion imprimante",
            "2. 🔄 Redémarrer spooler d'impression",
            "3. 📐 Vérifier format DICOM",
            "4. 🖨️ Tester avec autre imprimante"
        ],
        "time": "5-15 minutes"
    },
    "dicom_error": {
        "name": "⚠️ Erreur DICOM",
        "triggers": ["dicom", "transfert", "pacs", "orthanc"],
        "symptoms": ["Transfert échoué", "Étiquette incorrecte", "Metadata manquante"],
        "severity": "high",
        "solutions": [
            "1. 🏷️ Vérifier AETitle configuration",
            "2. 🔌 Contrôler port DICOM (104)",
            "3. 📝 Regarder logs serveur",
            "4. 👨‍💼 Contacter admin PACS"
        ],
        "time": "15-30 minutes"
    }
}

# =================== FONCTIONS UTILITAIRES ===================
def find_matching_problem(user_input):
    """Trouve le problème correspondant à l'entrée utilisateur"""
    user_input_lower = user_input.lower()
    
    for problem_id, problem in PROBLEMS_DATABASE.items():
        for trigger in problem["triggers"]:
            if trigger in user_input_lower:
                return problem
    
    return None

def get_severity_color(severity):
    """Retourne la couleur correspondant à la sévérité"""
    colors = {
        "critical": "critical",
        "high": "high", 
        "medium": "medium",
        "low": "low"
    }
    return colors.get(severity, "medium")

def simulate_network_test():
    """Simule un test réseau"""
    time.sleep(1)
    return {
        "Ping": f"{random.randint(10, 50)}ms",
        "Download": f"{random.randint(50, 100)} Mbps",
        "Upload": f"{random.randint(20, 50)} Mbps",
        "Packet Loss": f"{random.randint(0, 2)}%",
        "Status": "✅ Connecté" if random.random() > 0.2 else "⚠️ Problème"
    }

def simulate_system_check():
    """Simule une vérification système"""
    return {
        "CPU Usage": f"{random.randint(30, 90)}%",
        "Memory": f"{random.randint(40, 85)}%",
        "Disk": f"{random.randint(20, 80)}%",
        "Network": "✅ OK" if random.random() > 0.3 else "⚠️ Lent"
    }

# =================== INITIALISATION SESSION ===================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'diagnosis_history' not in st.session_state:
    st.session_state.diagnosis_history = []

# =================== INTERFACE PRINCIPALE ===================
st.title("🤖 PACS Helper Bot")
st.markdown("Votre assistant pour résoudre les problèmes PACS en radiologie")

# Sidebar
with st.sidebar:
    st.markdown("### 🏥 Tableau de Bord")
    
    # Sélecteur de langue
    language = st.selectbox("🌍 Langue", ["Français", "English"])
    
    # Métriques rapides
    st.markdown("#### 📊 État du Système")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("PACS", "✅ Online")
    with col2:
        st.metric("Tickets", "3")
    
    # Outils rapides
    st.markdown("#### ⚡ Outils Rapides")
    
    if st.button("🌐 Test Réseau"):
        with st.spinner("Test en cours..."):
            results = simulate_network_test()
            st.success("Test terminé!")
            for key, value in results.items():
                st.metric(key, value)
    
    if st.button("🖥️ Vérifier Système"):
        with st.spinner("Vérification..."):
            results = simulate_system_check()
            st.success("Vérification terminée!")
            for key, value in results.items():
                st.metric(key, value)
    
    # Historique
    if st.session_state.diagnosis_history:
        st.markdown("#### 📜 Historique")
        for item in st.session_state.diagnosis_history[-3:]:
            st.caption(f"• {item}")

# Section Urgence
st.markdown("### 🚨 Problèmes Urgents")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📛 IMAGES PERDUES", use_container_width=True):
        st.error("CONTACTEZ IT IMMÉDIATEMENT!")
        st.markdown("**Procédure:**")
        st.markdown("1. 📞 Appeler IT: Ext. 5555")
        st.markdown("2. 🖥️ Ne pas éteindre")
        st.markdown("3. 📋 Documenter patients")

with col2:
    if st.button("🔥 SERVEUR DOWN", use_container_width=True):
        st.warning("Serveur inaccessible")
        st.markdown("**Vérifications:**")
        st.markdown("1. 🔌 Alimentation serveur")
        st.markdown("2. 🌐 Ping serveur")
        st.markdown("3. 📞 Contacter admin")

with col3:
    if st.button("⚠️ ERREUR CRITIQUE", use_container_width=True):
        st.warning("Erreur système")
        st.markdown("**Actions:**")
        st.markdown("1. 🔍 Vérifier logs")
        st.markdown("2. 🖥️ Mode sans échec")
        st.markdown("3. 📞 Support technique")

# Questions fréquentes
st.markdown("### 💡 Questions Fréquentes")

questions = [
    "Comment transférer des images?",
    "Problème avec les annotations?",
    "L'impression ne fonctionne pas",
    "Je ne vois pas tous les patients",
    "Erreur de sauvegarde",
    "Comment faire une mesure?"
]

cols = st.columns(3)
for idx, question in enumerate(questions):
    with cols[idx % 3]:
        if st.button(f"❓ {question}", use_container_width=True):
            problem = find_matching_problem(question)
            if problem:
                # Ajouter au chat
                st.session_state.messages.append({"role": "user", "content": question})
                
                response = f"### {problem['name']}\n\n"
                response += f"**Sévérité:** <span class='status-badge {get_severity_color(problem['severity'])}'>{problem['severity'].upper()}</span>\n\n"
                response += f"**Temps estimé:** {problem['time']}\n\n"
                response += "**Solution:**\n"
                for solution in problem["solutions"]:
                    response += f"{solution}\n"
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.diagnosis_history.append(f"{datetime.now().strftime('%H:%M')} - {problem['name']}")
                st.rerun()

# Interface Chat
st.markdown("### 💬 Assistant de Diagnostic")

# Afficher l'historique du chat
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-user'><strong>Vous:</strong> {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-assistant'><strong>Assistant:</strong> {message['content']}</div>", unsafe_allow_html=True)

# Entrée utilisateur
user_input = st.text_input("Décrivez votre problème:", placeholder="Ex: Les images ne s'affichent pas...")

if user_input:
    # Ajouter message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Chercher solution
    with st.spinner("🔍 Recherche de solution..."):
        time.sleep(1)
        
        problem = find_matching_problem(user_input)
        
        if problem:
            # Construire réponse
            response = f"### 🩺 Diagnostic Trouvé\n\n"
            response += f"**{problem['name']}**\n\n"
            response += f"**Sévérité:** <span class='status-badge {get_severity_color(problem['severity'])}'>{problem['severity'].upper()}</span>\n\n"
            response += f"**Temps de résolution:** {problem['time']}\n\n"
            response += "**Procédure de résolution:**\n"
            
            for solution in problem["solutions"]:
                response += f"\n{solution}"
            
            response += "\n\n**💡 Conseil:** Si le problème persiste après ces étapes, contactez le support IT."
            
            # Ajouter à l'historique
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.diagnosis_history.append(f"{timestamp} - {problem['name']}")
        else:
            # Réponse générique
            response = "### 🤔 Je n'ai pas trouvé de solution exacte\n\n"
            response += "**Essayez de préciser:**\n"
            response += "• Quelle application/station?\n"
            response += "• Quel message d'erreur exact?\n"
            response += "• Depuis quand le problème?\n\n"
            response += "**Ou essayez ces solutions générales:**\n"
            response += "🔄 Redémarrer la station\n"
            response += "🌐 Vérifier la connexion réseau\n"
            response += "🧹 Nettoyer le cache\n"
            response += "📞 Contacter le support IT"
        
        # Ajouter réponse assistant
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Recharger pour afficher
        st.rerun()

# Outils de Diagnostic
st.markdown("### 🛠️ Outils de Diagnostic")

tab1, tab2, tab3 = st.tabs(["🔧 Tests", "📊 Monitoring", "📚 Base"])

with tab1:
    st.markdown("#### Tests de Connexion")
    
    if st.button("Lancer test complet", key="full_test"):
        with st.spinner("Test en cours..."):
            results = simulate_network_test()
            st.success("✅ Test terminé")
            
            for key, value in results.items():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(f"**{key}:**")
                with col2:
                    st.write(value)

with tab2:
    st.markdown("#### Monitoring Système")
    
    if st.button("Vérifier ressources", key="check_res"):
        with st.spinner("Analyse..."):
            results = simulate_system_check()
            
            for key, value in results.items():
                if "%" in value:
                    value_num = int(value.replace("%", ""))
                    st.progress(value_num/100)
                    st.write(f"**{key}:** {value}")
                else:
                    st.write(f"**{key}:** {value}")

with tab3:
    st.markdown("#### Base de Connaissances")
    
    for problem_id, problem in PROBLEMS_DATABASE.items():
        with st.expander(f"{problem['name']} ({problem['severity'].upper()})"):
            st.write("**Symptômes:**")
            for symptom in problem["symptoms"]:
                st.write(f"• {symptom}")
            
            st.write("\n**Solution:**")
            for solution in problem["solutions"]:
                st.write(solution)
            
            st.write(f"\n**Temps estimé:** {problem['time']}")

# Footer
st.markdown("---")
st.markdown("**Support IT:** 📞 Ext. 5555 | ✉️ support@pacs-hospital.fr")
st.caption("PACS Helper Bot v1.0 • Assistant pour radiologie")
