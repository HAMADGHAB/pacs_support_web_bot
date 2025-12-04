import streamlit as st
from openai import OpenAI
import time
import json
import os
from datetime import datetime

# =================== CONFIGURATION ===================
st.set_page_config(
    page_title="PACS Helper Bot Pro",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/pacs-helper',
        'Report a bug': 'https://github.com/pacs-helper/issues',
        'About': "### PACS Helper Bot Pro v2.0\nAssistant intelligent pour radiologie\n🚀 Powered by Grok xAI"
    }
)

# =================== STYLES MÉDICAUX PROFESSIONNELS ===================
st.markdown("""
<style>
    /* Thème médical professionnel */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    }
    
    .medical-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #1e90ff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.3s;
    }
    
    .medical-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    .emergency-card {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
        border-left: 6px solid #ff6b6b;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
    }
    
    .success-card {
        background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
        border-left: 6px solid #38a169;
    }
    
    .tech-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
        border-left: 6px solid #3182ce;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #1e90ff, #4169e1);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.3);
    }
    
    .urgent-button {
        background: linear-gradient(45deg, #ff6b6b, #ff4757) !important;
    }
    
    .quick-fix-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-ok { background: #c6f6d5; color: #22543d; }
    .status-warning { background: #fed7d7; color: #742a2a; }
    .status-info { background: #bee3f8; color: #2a4365; }
    
    .chat-user {
        background: #e3f2fd !important;
        border-radius: 15px 15px 5px 15px;
        margin: 0.5rem;
    }
    
    .chat-assistant {
        background: #f0fff4 !important;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #1e90ff, #4169e1);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .metric-box {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# =================== INITIALISATION DE SESSION ===================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'diagnosis_history' not in st.session_state:
    st.session_state.diagnosis_history = []
if 'quick_access' not in st.session_state:
    st.session_state.quick_access = []
if 'language' not in st.session_state:
    st.session_state.language = "Français"

# =================== BASE DE CONNAISSANCE ÉTENDUE ===================
PACS_KNOWLEDGE_BASE = {
    "fr": {
        "common_issues": {
            "images_not_loading": {
                "name": "📸 Images ne se chargent pas",
                "triggers": ["image", "charger", "afficher", "blanc", "vide", "patient"],
                "symptoms": ["Écran blanc", "Loader infini", "Message d'erreur", "Images partielles"],
                "severity": "Medium",
                "solutions": [
                    "1. Vérifier la connexion au serveur PACS",
                    "2. Redémarrer la station de travail",
                    "3. Vérifier les permissions utilisateur",
                    "4. Nettoyer le cache navigateur",
                    "5. Contacter le support IT si persiste >15min"
                ],
                "time_estimate": "5-15 minutes"
            },
            "slow_performance": {
                "name": "🐌 Performance lente",
                "triggers": ["lent", "ralenti", "performance", "chargement", "buffer"],
                "symptoms": ["Délais importants", "Interface gelée", "CPU à 100%"],
                "severity": "Low",
                "solutions": [
                    "1. Fermer applications inutiles",
                    "2. Vider cache temporaire",
                    "3. Vérifier connexion réseau",
                    "4. Redémarrer la machine",
                    "5. Contacter IT pour optimisation"
                ],
                "time_estimate": "10-20 minutes"
            },
            "login_failure": {
                "name": "🔐 Échec de connexion",
                "triggers": ["login", "connexion", "mot de passe", "accès", "authentification"],
                "symptoms": ["Erreur 401/403", "Identifiants rejetés", "Session expirée"],
                "severity": "High",
                "solutions": [
                    "1. Vérifier caps lock",
                    "2. Réinitialiser mot de passe",
                    "3. Vérifier AD/LDAP",
                    "4. Contacter helpdesk",
                    "5. Utiliser compte temporaire"
                ],
                "time_estimate": "2-10 minutes"
            },
            "printing_issue": {
                "name": "🖨️ Problème d'impression",
                "triggers": ["imprimante", "impression", "papier", "film", "dimension"],
                "symptoms": ["File d'attente bloquée", "Mauvais format", "Erreur driver"],
                "severity": "Medium",
                "solutions": [
                    "1. Vérifier connexion imprimante",
                    "2. Redémarrer spooler d'impression",
                    "3. Vérifier format DICOM",
                    "4. Reconfigurer préférences",
                    "5. Tester avec autre imprimante"
                ],
                "time_estimate": "5-15 minutes"
            },
            "dicom_error": {
                "name": "⚠️ Erreur DICOM",
                "triggers": ["dicom", "transfert", "pacs", "orthanc", "store"],
                "symptoms": ["Transfert échoué", "Étiquette incorrecte", "Metadata manquante"],
                "severity": "High",
                "solutions": [
                    "1. Vérifier AETitle",
                    "2. Contrôler port DICOM (104)",
                    "3. Vérifier storage commitment",
                    "4. Regarder logs serveur",
                    "5. Contacter admin PACS"
                ],
                "time_estimate": "15-30 minutes"
            }
        },
        "quick_fixes": [
            {"icon": "🔄", "text": "Redémarrer station", "action": "restart"},
            {"icon": "🌐", "text": "Tester connexion", "action": "network_test"},
            {"icon": "🧹", "text": "Nettoyer cache", "action": "clear_cache"},
            {"icon": "📋", "text": "Vérifier logs", "action": "check_logs"},
            {"icon": "🔧", "text": "Mode diagnostic", "action": "diagnostic_mode"}
        ],
        "predefined_questions": [
            "Comment transférer des images ?",
            "Problème avec les annotations ?",
            "L'impression ne fonctionne pas",
            "Je ne vois pas tous les patients",
            "Erreur de sauvegarde automatique",
            "Comment faire une mesure ?",
            "Problème de contraste/fenêtrage",
            "L'application se ferme toute seule"
        ]
    },
    "en": {
        "common_issues": {
            "images_not_loading": {
                "name": "📸 Images not loading",
                "triggers": ["image", "load", "display", "white", "blank", "patient"],
                "symptoms": ["White screen", "Infinite loader", "Error message", "Partial images"],
                "severity": "Medium",
                "solutions": [
                    "1. Check PACS server connection",
                    "2. Restart workstation",
                    "3. Verify user permissions",
                    "4. Clear browser cache",
                    "5. Contact IT if persists >15min"
                ],
                "time_estimate": "5-15 minutes"
            },
            "slow_performance": {
                "name": "🐌 Slow performance",
                "triggers": ["slow", "lag", "performance", "loading", "buffer"],
                "symptoms": ["Significant delays", "Frozen interface", "CPU at 100%"],
                "severity": "Low",
                "solutions": [
                    "1. Close unnecessary applications",
                    "2. Clear temporary cache",
                    "3. Check network connection",
                    "4. Restart machine",
                    "5. Contact IT for optimization"
                ],
                "time_estimate": "10-20 minutes"
            }
        },
        "quick_fixes": [
            {"icon": "🔄", "text": "Restart workstation", "action": "restart"},
            {"icon": "🌐", "text": "Test connection", "action": "network_test"},
            {"icon": "🧹", "text": "Clear cache", "action": "clear_cache"},
            {"icon": "📋", "text": "Check logs", "action": "check_logs"},
            {"icon": "🔧", "text": "Diagnostic mode", "action": "diagnostic_mode"}
        ],
        "predefined_questions": [
            "How to transfer images?",
            "Problem with annotations?",
            "Printing not working",
            "Can't see all patients",
            "Auto-save error",
            "How to make a measurement?",
            "Contrast/windowing issue",
            "Application crashes randomly"
        ]
    }
}

# =================== FONCTIONS UTILITAIRES ===================
def perform_network_test():
    """Simule un test réseau"""
    with st.spinner("🔍 Test réseau en cours..."):
        time.sleep(2)
        return {
            "status": "✅ OK",
            "ping": "15ms",
            "download": "85 Mbps",
            "upload": "45 Mbps",
            "server_connection": "✅ Connecté"
        }

def clear_cache():
    """Simule le nettoyage du cache"""
    with st.spinner("🧹 Nettoyage du cache..."):
        time.sleep(1)
        return "Cache nettoyé avec succès !"

def check_logs():
    """Affiche les logs simulés"""
    logs = [
        f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Connexion utilisateur établie",
        f"[{datetime.now().strftime('%H:%M:%S')}] WARN: Cache presque plein (85%)",
        f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Transfert DICOM réussi",
        f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: Échec authentification LDAP"
    ]
    return logs

def get_diagnosis_suggestions(user_input, language="fr"):
    """Analyse l'entrée utilisateur et suggère des solutions"""
    suggestions = []
    knowledge = PACS_KNOWLEDGE_BASE[language]["common_issues"]
    
    for issue_id, issue in knowledge.items():
        for trigger in issue["triggers"]:
            if trigger.lower() in user_input.lower():
                suggestions.append({
                    "issue": issue["name"],
                    "solutions": issue["solutions"],
                    "severity": issue["severity"],
                    "time": issue["time_estimate"]
                })
                break
    
    return suggestions

# =================== SIDEBAR ===================
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    st.markdown("### 🏥 PACS Dashboard")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Sélecteur de langue
    language = st.selectbox(
        "🌍 Langue / Language",
        ["Français", "English"],
        index=0 if st.session_state.language == "Français" else 1
    )
    st.session_state.language = language
    lang_key = "fr" if language == "Français" else "en"
    
    # Métriques système
    st.markdown("### 📊 État du système")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("PACS Status", "✅ Online", "+2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Tickets Actifs", "3", "-1")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Accès rapide
    st.markdown("### ⚡ Accès Rapide")
    knowledge = PACS_KNOWLEDGE_BASE[lang_key]
    
    for fix in knowledge["quick_fixes"]:
        if st.button(f"{fix['icon']} {fix['text']}", use_container_width=True):
            if fix['action'] == 'network_test':
                result = perform_network_test()
                st.success("Test réseau complété !")
                st.json(result)
            elif fix['action'] == 'clear_cache':
                result = clear_cache()
                st.success(result)
    
    # Historique des diagnostics
    if st.session_state.diagnosis_history:
        st.markdown("### 📜 Historique")
        for hist in st.session_state.diagnosis_history[-3:]:
            st.caption(f"• {hist}")

# =================== MAIN INTERFACE ===================
st.title("🤖 PACS Helper Bot Pro")
st.markdown("### Votre assistant intelligent pour la radiologie - Diagnostique et résout les problèmes PACS en temps réel")

# =================== SECTION D'URGENCE ===================
with st.expander("🚨 URGENCE - Problèmes Critiques", expanded=False):
    emergency_col1, emergency_col2, emergency_col3 = st.columns(3)
    
    with emergency_col1:
        if st.button("📛 IMAGES PERDUES", use_container_width=True, type="primary"):
            st.error("CONTACTEZ IMMÉDIATEMENT LE SUPPORT IT !")
            st.markdown("**Procédure d'urgence:**")
            st.markdown("1. Ne pas éteindre la station")
            st.markdown("2. Appeler IT: Ext. 5555")
            st.markdown("3. Documenter les patients concernés")
    
    with emergency_col2:
        if st.button("🔥 SERVEUR DOWN", use_container_width=True, type="primary"):
            st.warning("Serveur PACS inaccessible")
            st.markdown("**Actions immédiates:**")
            st.markdown("1. Vérifier alimentation serveur")
            st.markdown("2. Contacter administrateur")
            st.markdown("3. Activer mode dégradé")
    
    with emergency_col3:
        if st.button("⚠️ ERREUR DICOM", use_container_width=True, type="primary"):
            st.warning("Problème de transfert DICOM")
            st.markdown("**Vérifications:**")
            st.markdown("1. Port 104 accessible")
            st.markdown("2. AETitle correct")
            st.markdown("3. Stockage disponible")

# =================== QUESTIONS PRÉDÉFINIES ===================
st.markdown("### 💡 Questions Fréquentes")
knowledge = PACS_KNOWLEDGE_BASE[lang_key]
questions = knowledge["predefined_questions"]

cols = st.columns(4)
for idx, question in enumerate(questions):
    with cols[idx % 4]:
        if st.button(f"❓ {question}", use_container_width=True):
            suggestions = get_diagnosis_suggestions(question, lang_key)
            if suggestions:
                st.session_state.messages.append({"role": "user", "content": question})
                response = f"**Solution suggérée pour :** {question}\n\n"
                for suggestion in suggestions:
                    response += f"### {suggestion['issue']} ({suggestion['severity']})\n"
                    response += f"*Temps estimé: {suggestion['time']}*\n\n"
                    for solution in suggestion['solutions']:
                        response += f"{solution}\n"
                    response += "\n"
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

# =================== CHAT INTERFACE ===================
st.markdown("### 💬 Chat avec l'Assistant PACS")

# Affichage de l'historique du chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Décrivez votre problème PACS ici..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Analyser et répondre
    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyse en cours..."):
            time.sleep(1)
            
            # Obtenir les suggestions
            suggestions = get_diagnosis_suggestions(prompt, lang_key)
            
            if suggestions:
                response = f"### 🩺 Diagnostic Automatique\n\n"
                
                for suggestion in suggestions[:2]:  # Limiter à 2 suggestions max
                    severity_color = {
                        "High": "🔴",
                        "Medium": "🟡", 
                        "Low": "🟢"
                    }.get(suggestion["severity"], "⚪")
                    
                    response += f"**{severity_color} {suggestion['issue']}**\n"
                    response += f"*Sévérité: {suggestion['severity']} | Temps estimé: {suggestion['time']}*\n\n"
                    
                    for i, solution in enumerate(suggestion["solutions"], 1):
                        response += f"{solution}\n"
                    
                    response += "\n---\n"
                
                response += "\n### 🛠️ Actions Recommandées\n"
                response += "1. Essayer les solutions ci-dessus\n"
                response += "2. Si problème persiste, contactez IT\n"
                response += "3. Documenter l'incident\n\n"
                response += "Besoin d'aide supplémentaire ? Continuez à décrire votre problème !"
                
                # Enregistrer dans l'historique
                issue_name = suggestions[0]["issue"] if suggestions else "Problème général"
                st.session_state.diagnosis_history.append(
                    f"{datetime.now().strftime('%H:%M')} - {issue_name}"
                )
            else:
                response = "### 🤔 Je n'ai pas reconnu exactement votre problème\n\n"
                response += "**Veuillez préciser :**\n"
                response += "- Quelle station/application ?\n"
                response += "- Quand le problème est apparu ?\n"
                response += "- Message d'erreur exact ?\n"
                response += "- Combien d'utilisateurs affectés ?\n\n"
                response += "**Ou essayez une solution générale :**\n"
                response += "🔁 Redémarrer la station de travail\n"
                response += "🌐 Vérifier la connexion réseau\n"
                response += "🧹 Nettoyer le cache navigateur\n"
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# =================== OUTILS DE DIAGNOSTIC ===================
st.markdown("### 🛠️ Outils de Diagnostic")

tab1, tab2, tab3, tab4 = st.tabs(["🔧 Tests Réseau", "📊 Logs Système", "💾 Ressources", "🎯 Diagnostic Avancé"])

with tab1:
    st.markdown("#### Test de Connexion PACS")
    if st.button("Lancer le test complet", type="primary"):
        result = perform_network_test()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Résultats")
            for key, value in result.items():
                st.metric(key, value)
        
        with col2:
            st.markdown("##### Recommandations")
            if result["ping"] > "50ms":
                st.warning("Latence élevée détectée")
                st.markdown("1. Vérifier câbles réseau")
                st.markdown("2. Contacter service réseau")
            else:
                st.success("Connexion optimale")

with tab2:
    st.markdown("#### Logs Système Récent")
    if st.button("Afficher les logs"):
        logs = check_logs()
        for log in logs:
            if "ERROR" in log:
                st.error(log)
            elif "WARN" in log:
                st.warning(log)
            else:
                st.info(log)

with tab3:
    st.markdown("#### Utilisation des Ressources")
    # Graphiques simulés
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**CPU**")
        st.progress(65)
        st.caption("65% - Normal")
    with col2:
        st.markdown("**Mémoire**")
        st.progress(78)
        st.caption("78% - Élevé")
    with col3:
        st.markdown("**Stockage**")
        st.progress(42)
        st.caption("42% - Bon")
    
    st.markdown("##### Recommandations")
    st.info("""
    - 💾 Nettoyer fichiers temporaires
    - 🗃️ Archiver anciennes études
    - 🔄 Redémarrer hebdomadairement
    """)

with tab4:
    st.markdown("#### Diagnostic Avancé")
    symptoms = st.multiselect(
        "Sélectionnez les symptômes",
        ["Écran blanc", "Lenteur", "Erreur DICOM", "Connexion perdue", "Crash", "Autre"]
    )
    
    if symptoms:
        st.markdown("##### Analyse des symptômes")
        for symptom in symptoms:
            if symptom == "Écran blanc":
                st.markdown("🔍 **Écran blanc:** Problème probable de cache ou GPU")
                st.markdown("Solution: Ctrl+Shift+R (hard refresh)")
            elif symptom == "Lenteur":
                st.markdown("🔍 **Lenteur:** Possible surcharge mémoire")
                st.markdown("Solution: Fermer onglets inutiles")

# =================== FOOTER ===================
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.markdown("**Support IT** 📞 Ext. 5555")
with footer_col2:
    st.markdown("**Email** ✉️ support@pacs-hospital.fr")
with footer_col3:
    st.markdown("**Version** 2.0.1 🚀")

st.caption("© 2024 PACS Helper Bot Pro - Assistant intelligent pour la radiologie - Tous droits réservés")
