import streamlit as st
import time
import json
import os
import random
from datetime import datetime
from typing import Dict, List, Any

# =================== CONFIGURATION ===================
st.set_page_config(
    page_title="PACS Helper Bot Pro",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/pacs-helper',
        'Report a bug': 'https://github.com/pacs-helper/issues',
        'About': "### PACS Helper Bot Pro v2.0\nAssistant intelligent pour radiologie\n🏥 Powered by AI Médical"
    }
)

# =================== STYLES MÉDICAUX PROFESSIONNELS ===================
st.markdown("""
<style>
    /* Thème médical professionnel */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .medical-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #1e90ff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
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
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.3);
    }
    
    .urgent-button {
        background: linear-gradient(45deg, #ff6b6b, #ff4757) !important;
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
        padding: 1rem;
        border: 1px solid #bbdefb;
    }
    
    .chat-assistant {
        background: #f0fff4 !important;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem;
        padding: 1rem;
        border: 1px solid #c6f6d5;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #1e90ff, #4169e1);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .metric-box {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .symptom-tag {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    
    .solution-step {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .tool-tab {
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
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
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'department' not in st.session_state:
    st.session_state.department = "Radiologie"

# =================== BASE DE CONNAISSANCE ÉTENDUE ===================
class PACSKnowledgeBase:
    """Base de connaissances pour les problèmes PACS"""
    
    def __init__(self):
        self.common_issues = {
            "images_not_loading": {
                "name": "📸 Images ne se chargent pas",
                "triggers": ["image", "charger", "afficher", "blanc", "vide", "patient", "étude", "série", "dicom"],
                "symptoms": ["Écran blanc", "Loader infini", "Message d'erreur", "Images partielles", "Pixelisation"],
                "severity": "Moyen",
                "solutions": [
                    "1. 🔌 Vérifier la connexion au serveur PACS",
                    "2. 🖥️ Redémarrer la station de travail",
                    "3. 🔑 Vérifier les permissions utilisateur",
                    "4. 🧹 Nettoyer le cache navigateur (Ctrl+Shift+R)",
                    "5. 📞 Contacter le support IT si persiste >15min"
                ],
                "time_estimate": "5-15 minutes",
                "probability": 85
            },
            "slow_performance": {
                "name": "🐌 Performance lente",
                "triggers": ["lent", "ralenti", "performance", "chargement", "buffer", "gèle", "freeze"],
                "symptoms": ["Délais importants", "Interface gelée", "CPU à 100%", "Mémoire saturée"],
                "severity": "Faible",
                "solutions": [
                    "1. ❌ Fermer applications inutiles",
                    "2. 🗑️ Vider cache temporaire",
                    "3. 🌐 Vérifier connexion réseau (>50 Mbps)",
                    "4. 🔄 Redémarrer la machine",
                    "5. ⚙️ Contacter IT pour optimisation"
                ],
                "time_estimate": "10-20 minutes",
                "probability": 75
            },
            "login_failure": {
                "name": "🔐 Échec de connexion",
                "triggers": ["login", "connexion", "mot de passe", "accès", "authentification", "compte", "session"],
                "symptoms": ["Erreur 401/403", "Identifiants rejetés", "Session expirée", "Compte bloqué"],
                "severity": "Élevé",
                "solutions": [
                    "1. 🔒 Vérifier caps lock",
                    "2. 🔄 Réinitialiser mot de passe",
                    "3. 🔍 Vérifier AD/LDAP",
                    "4. 📞 Contacter helpdesk",
                    "5. 👥 Utiliser compte temporaire"
                ],
                "time_estimate": "2-10 minutes",
                "probability": 90
            },
            "printing_issue": {
                "name": "🖨️ Problème d'impression",
                "triggers": ["imprimante", "impression", "papier", "film", "dimension", "imprimer", "dicom print"],
                "symptoms": ["File d'attente bloquée", "Mauvais format", "Erreur driver", "Noir et blanc seulement"],
                "severity": "Moyen",
                "solutions": [
                    "1. 🔌 Vérifier connexion imprimante",
                    "2. 🔄 Redémarrer spooler d'impression",
                    "3. 📐 Vérifier format DICOM",
                    "4. ⚙️ Reconfigurer préférences",
                    "5. 🖨️ Tester avec autre imprimante"
                ],
                "time_estimate": "5-15 minutes",
                "probability": 80
            },
            "dicom_error": {
                "name": "⚠️ Erreur DICOM",
                "triggers": ["dicom", "transfert", "pacs", "orthanc", "store", "scu", "scp", "aetitle"],
                "symptoms": ["Transfert échoué", "Étiquette incorrecte", "Metadata manquante", "SOP Class non supporté"],
                "severity": "Élevé",
                "solutions": [
                    "1. 🏷️ Vérifier AETitle configuration",
                    "2. 🔌 Contrôler port DICOM (104, 11112)",
                    "3. ✅ Vérifier storage commitment",
                    "4. 📝 Regarder logs serveur",
                    "5. 👨‍💼 Contacter admin PACS"
                ],
                "time_estimate": "15-30 minutes",
                "probability": 70
            },
            "measurement_tool": {
                "name": "📏 Outils de mesure défectueux",
                "triggers": ["mesure", "règle", "angle", "distance", "curseur", "calibration"],
                "symptoms": ["Mesures inexactes", "Curseur invisible", "Unités incorrectes", "Calibration manquante"],
                "severity": "Faible",
                "solutions": [
                    "1. 🔄 Redémarrer le viewer",
                    "2. ⚙️ Vérifier calibration DICOM",
                    "3. 📐 Réinitialiser préférences de mesure",
                    "4. 🖱️ Tester avec autre souris",
                    "5. 🔧 Mettre à jour le logiciel"
                ],
                "time_estimate": "5-10 minutes",
                "probability": 85
            },
            "window_level": {
                "name": "🎚️ Problème de fenêtrage",
                "triggers": ["fenêtre", "contraste", "luminosité", "wl", "ww", "level", "window"],
                "symptoms": ["Contraste faible", "Niveaux de gris incorrects", "Préréglages absents", "Histogramme erroné"],
                "severity": "Faible",
                "solutions": [
                    "1. 🔄 Réinitialiser fenêtrage DICOM",
                    "2. ⚙️ Appliquer préréglages standards",
                    "3. 🖥️ Vérifier calibration écran",
                    "4. 📊 Contrôler valeurs VOI LUT",
                    "5. 🔧 Redémarrer station"
                ],
                "time_estimate": "3-8 minutes",
                "probability": 90
            },
            "pacs_server_down": {
                "name": "🔥 Serveur PACS inaccessible",
                "triggers": ["serveur", "down", "inaccessible", "hors ligne", "offline", "maintenance"],
                "symptoms": ["Connexion refusée", "Timeout", "Tous utilisateurs affectés", "Message maintenance"],
                "severity": "Critique",
                "solutions": [
                    "1. 🚨 CONTACTER IT IMMÉDIATEMENT",
                    "2. 🔌 Vérifier alimentation serveur",
                    "3. 🌐 Tester ping serveur",
                    "4. ⏱️ Activer mode dégradé si disponible",
                    "5. 📋 Suivre procédure d'urgence"
                ],
                "time_estimate": "30+ minutes",
                "probability": 95
            }
        }
        
        self.quick_fixes = [
            {"icon": "🔄", "text": "Redémarrer station", "action": "restart", "time": "2 min"},
            {"icon": "🌐", "text": "Tester connexion", "action": "network_test", "time": "1 min"},
            {"icon": "🧹", "text": "Nettoyer cache", "action": "clear_cache", "time": "3 min"},
            {"icon": "📋", "text": "Vérifier logs", "action": "check_logs", "time": "5 min"},
            {"icon": "🔧", "text": "Mode diagnostic", "action": "diagnostic_mode", "time": "10 min"},
            {"icon": "📊", "text": "Vérifier ressources", "action": "check_resources", "time": "2 min"},
            {"icon": "🔒", "text": "Vérifier permissions", "action": "check_permissions", "time": "3 min"},
            {"icon": "🔄", "text": "Mettre à jour logiciel", "action": "update_software", "time": "15 min"}
        ]
        
        self.predefined_questions = [
            "Comment transférer des images vers un CD/DVD ?",
            "Problème avec les annotations sur les images",
            "L'impression ne fonctionne pas pour un patient spécifique",
            "Je ne vois pas tous les patients dans la liste",
            "Erreur de sauvegarde automatique des rapports",
            "Comment faire une mesure précise sur un scanner ?",
            "Problème de contraste sur les images IRM",
            "L'application se ferme toute seule pendant une lecture",
            "Comment partager des images avec un médecin externe ?",
            "Problème d'importation depuis une clé USB",
            "Les images disparaissent après fermeture",
            "Comment configurer les raccourcis clavier ?",
            "Problème d'affichage sur écran secondaire",
            "Erreur lors de l'envoi vers le RIS"
        ]
        
        self.departments = {
            "Radiologie": {"color": "#3b82f6", "icon": "🩻"},
            "IRM": {"color": "#8b5cf6", "icon": "🧲"},
            "Scanner": {"color": "#10b981", "icon": "🌀"},
            "Échographie": {"color": "#f59e0b", "icon": "📡"},
            "Mammographie": {"color": "#ec4899", "icon": "🌸"},
            "Médecine Nucléaire": {"color": "#ef4444", "icon": "☢️"}
        }

# =================== FONCTIONS UTILITAIRES ===================
class PACSTools:
    """Classe contenant les outils de diagnostic PACS"""
    
    @staticmethod
    def perform_network_test():
        """Simule un test réseau complet"""
        results = {
            "ping_serveur": random.randint(10, 50),
            "download_speed": random.randint(50, 100),
            "upload_speed": random.randint(20, 50),
            "packet_loss": random.randint(0, 2),
            "dns_resolution": random.choice(["✅ OK", "⚠️ Lent", "✅ OK"]),
            "server_status": random.choice(["✅ Connecté", "✅ Connecté", "❌ Échec"])
        }
        
        # Évaluation
        evaluation = ""
        if results["ping_serveur"] > 30:
            evaluation += "⚠️ Latence élevée détectée\n"
        if results["download_speed"] < 60:
            evaluation += "⚠️ Débit téléchargement faible\n"
        if results["packet_loss"] > 0:
            evaluation += "⚠️ Perte de paquets détectée\n"
        
        if not evaluation:
            evaluation = "✅ Connexion réseau optimale"
        
        return results, evaluation
    
    @staticmethod
    def check_system_resources():
        """Vérifie les ressources système"""
        return {
            "cpu_usage": random.randint(30, 90),
            "memory_usage": random.randint(40, 85),
            "disk_usage": random.randint(20, 80),
            "gpu_memory": random.randint(25, 75),
            "network_connections": random.randint(50, 200)
        }
    
    @staticmethod
    def generate_logs():
        """Génère des logs système simulés"""
        log_types = ["INFO", "WARN", "ERROR", "DEBUG"]
        log_messages = [
            "Connexion utilisateur établie",
            "Cache presque plein (85%)",
            "Transfert DICOM réussi vers ORTHANC",
            "Échec authentification LDAP",
            "Session expirée - reconnexion automatique",
            "Image chargée avec succès",
            "Erreur de parsing DICOM header",
            "Sauvegarde automatique effectuée",
            "Connexion serveur perdue",
            "Recovery mode activé"
        ]
        
        logs = []
        for _ in range(8):
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_type = random.choice(log_types)
            message = random.choice(log_messages)
            logs.append(f"[{timestamp}] {log_type}: {message}")
        
        return logs
    
    @staticmethod
    def diagnose_from_symptoms(symptoms: List[str]) -> Dict[str, Any]:
        """Diagnostique à partir des symptômes"""
        knowledge_base = PACSKnowledgeBase()
        matches = []
        
        for issue_id, issue in knowledge_base.common_issues.items():
            matching_symptoms = [s for s in symptoms if any(word in s.lower() for word in issue["triggers"])]
            if matching_symptoms:
                match_score = len(matching_symptoms) * 20
                matches.append({
                    "issue": issue,
                    "score": match_score,
                    "matching_symptoms": matching_symptoms
                })
        
        # Trier par score
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "matches": matches[:3],  # Top 3 matches
            "total_symptoms": len(symptoms),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# =================== SIDEBAR ===================
def render_sidebar():
    """Affiche la sidebar avec toutes les fonctionnalités"""
    with st.sidebar:
        st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
        st.markdown("### 🏥 PACS Dashboard")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Sélecteur de langue
        language = st.selectbox(
            "🌍 Langue",
            ["Français", "English"],
            key="language_selector"
        )
        st.session_state.language = language
        
        # Informations utilisateur
        st.markdown("### 👤 Profil")
        col1, col2 = st.columns(2)
        with col1:
            department = st.selectbox(
                "Département",
                list(PACSKnowledgeBase().departments.keys()),
                key="dept_selector"
            )
            st.session_state.department = department
        
        with col2:
            user_name = st.text_input("Votre nom", value=st.session_state.get('user_name', ''))
            st.session_state.user_name = user_name
        
        # Métriques système
        st.markdown("### 📊 Métriques Système")
        
        resources = PACSTools.check_system_resources()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("CPU", f"{resources['cpu_usage']}%", 
                     delta=f"{random.randint(-5, 5)}%" if random.random() > 0.5 else None)
            st.metric("Mémoire", f"{resources['memory_usage']}%")
        
        with col2:
            st.metric("Stockage", f"{resources['disk_usage']}%")
            st.metric("Connexions", resources['network_connections'])
        
        # Accès rapide
        st.markdown("### ⚡ Accès Rapide")
        knowledge_base = PACSKnowledgeBase()
        
        for fix in knowledge_base.quick_fixes[:4]:  # Afficher 4 premiers
            if st.button(f"{fix['icon']} {fix['text']} ({fix['time']})", 
                        use_container_width=True, key=f"quick_{fix['action']}"):
                handle_quick_action(fix['action'])
        
        # Historique des diagnostics
        if st.session_state.diagnosis_history:
            st.markdown("### 📜 Historique Récent")
            for hist in st.session_state.diagnosis_history[-5:]:  # 5 derniers
                st.caption(f"• {hist}")
            
            if st.button("🗑️ Effacer historique", use_container_width=True):
                st.session_state.diagnosis_history = []
                st.rerun()

def handle_quick_action(action: str):
    """Gère les actions rapides"""
    tools = PACSTools()
    
    if action == "network_test":
        with st.spinner("🔍 Test réseau en cours..."):
            time.sleep(2)
            results, evaluation = tools.perform_network_test()
            st.success("Test réseau complété !")
            
            # Afficher les résultats dans un expander
            with st.expander("📊 Résultats détaillés", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Ping serveur", f"{results['ping_serveur']}ms")
                    st.metric("Download", f"{results['download_speed']} Mbps")
                    st.metric("Upload", f"{results['upload_speed']} Mbps")
                
                with col2:
                    st.metric("Perte paquets", f"{results['packet_loss']}%")
                    st.metric("DNS", results['dns_resolution'])
                    st.metric("Serveur", results['server_status'])
                
                st.info(f"**Évaluation:** {evaluation}")
    
    elif action == "clear_cache":
        with st.spinner("🧹 Nettoyage du cache..."):
            time.sleep(1)
            st.success("✅ Cache nettoyé avec succès !")
            st.info("Redémarrez l'application pour appliquer les changements.")
    
    elif action == "check_logs":
        with st.spinner("📋 Récupération des logs..."):
            time.sleep(1)
            logs = tools.generate_logs()
            st.success(f"📊 {len(logs)} logs récupérés")
            
            with st.expander("📝 Voir les logs", expanded=True):
                for log in logs:
                    if "ERROR" in log:
                        st.error(log)
                    elif "WARN" in log:
                        st.warning(log)
                    elif "INFO" in log:
                        st.info(log)
                    else:
                        st.text(log)

# =================== HEADER ===================
def render_header():
    """Affiche l'en-tête de l'application"""
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        dept_info = PACSKnowledgeBase().departments.get(st.session_state.department, {})
        color = dept_info.get("color", "#3b82f6")
        icon = dept_info.get("icon", "🏥")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {color}22, {color}44); 
                    padding: 1rem; border-radius: 10px; text-align: center;">
            <h4 style="margin: 0; color: {color};">
                {icon} {st.session_state.department}
            </h4>
            <p style="margin: 0; font-size: 0.9rem; color: #666;">
                {st.session_state.user_name if st.session_state.user_name else "Utilisateur"}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.title("🤖 PACS Helper Bot Pro")
        st.markdown("### Votre assistant intelligent pour la radiologie")
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem;">🏥</div>
            <div style="font-size: 0.8rem; color: #666;">v2.1.0</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

# =================== SECTION D'URGENCE ===================
def render_emergency_section():
    """Affiche la section d'urgence"""
    with st.expander("🚨 SECTION URGENCE - Problèmes Critiques", expanded=False):
        st.warning("⚠️ UTILISEZ CETTE SECTION SEULEMENT POUR LES PROBLÈMES CRITIQUES")
        
        emergency_col1, emergency_col2, emergency_col3 = st.columns(3)
        
        with emergency_col1:
            if st.button("📛 IMAGES PERDUES", use_container_width=True, type="primary"):
                st.error("🚨 URGENCE - CONTACTEZ IMMÉDIATEMENT LE SUPPORT IT !")
                st.markdown("""
                **Procédure d'urgence:**
                1. 📞 Appeler IT: **Ext. 5555** ou **07 12 34 56 78**
                2. 🖥️ Ne pas éteindre la station
                3. 📋 Documenter les patients concernés
                4. 🚫 Ne pas modifier les fichiers
                5. ⏳ Attendre instructions IT
                
                **Personnes à contacter:**
                - Support IT: extension 5555
                - Chef de service: extension 5001
                - Radiologue en chef: extension 5002
                """)
        
        with emergency_col2:
            if st.button("🔥 SERVEUR DOWN", use_container_width=True, type="primary"):
                st.error("🚨 SERVEUR PACS INACCESSIBLE")
                st.markdown("""
                **Actions immédiates:**
                1. 🔌 Vérifier alimentation salle serveur
                2. 🌐 Tester ping: `ping pacs.hopital.local`
                3. 📞 Contacter administrateur système
                4. ⚠️ Activer mode dégradé
                5. 📊 Vérifier panneau de contrôle
                
                **Mode dégradé activable via:**
                Menu → Système → Mode Urgence
                """)
        
        with emergency_col3:
            if st.button("⚠️ ERREUR CRITIQUE", use_container_width=True, type="primary"):
                st.error("🚨 ERREUR SYSTÈME CRITIQUE")
                st.markdown("""
                **Diagnostic rapide:**
                1. 🔍 Vérifier logs d'erreur
                2. 🖥️ Redémarrer en mode sans échec
                3. 📞 Contacter support technique
                4. 📸 Prendre photo message d'erreur
                5. 🕒 Noter heure exacte du problème
                
                **Hotline technique: 0 800 123 456**
                """)

# =================== QUESTIONS PRÉDÉFINIES ===================
def render_predefined_questions():
    """Affiche les questions prédéfinies"""
    st.markdown("### 💡 Questions Fréquentes")
    
    knowledge_base = PACSKnowledgeBase()
    questions = knowledge_base.predefined_questions
    
    # Afficher en grille de 2 colonnes
    col1, col2 = st.columns(2)
    
    for idx, question in enumerate(questions):
        with col1 if idx % 2 == 0 else col2:
            if st.button(f"❓ {question}", key=f"q_{idx}", use_container_width=True):
                handle_predefined_question(question)

def handle_predefined_question(question: str):
    """Gère une question prédéfinie"""
    knowledge_base = PACSKnowledgeBase()
    
    # Chercher la meilleure correspondance
    best_match = None
    best_score = 0
    
    for issue_id, issue in knowledge_base.common_issues.items():
        score = sum(1 for trigger in issue["triggers"] if trigger in question.lower())
        if score > best_score:
            best_score = score
            best_match = issue
    
    if best_match:
        response = f"### 🎯 Solution pour: *{question}*\n\n"
        response += f"**{best_match['name']}** "
        response += f"| Sévérité: {best_match['severity']} "
        response += f"| Temps estimé: {best_match['time_estimate']}\n\n"
        
        response += "**Symptômes possibles:**\n"
        for symptom in best_match['symptoms']:
            response += f"• {symptom}\n"
        
        response += "\n**📋 Solution étape par étape:**\n"
        for solution in best_match['solutions']:
            response += f"\n{solution}"
        
        response += f"\n\n**🎯 Probabilité de résolution: {best_match['probability']}%**"
        
        # Ajouter au chat
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Ajouter à l'historique
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.diagnosis_history.append(
            f"{timestamp} - {best_match['name']}"
        )
        
        st.rerun()
    else:
        st.warning("Question non reconnue. Veuillez la reformuler.")

# =================== CHAT INTERFACE ===================
def render_chat_interface():
    """Affiche l'interface de chat"""
    st.markdown("### 💬 Assistant de Diagnostic")
    
    # Afficher l'historique du chat
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Entrée utilisateur
    if prompt := st.chat_input("Décrivez votre problème PACS ici...", key="chat_input"):
        process_user_input(prompt)

def process_user_input(prompt: str):
    """Traite l'entrée utilisateur"""
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Analyser et répondre
    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyse en cours..."):
            time.sleep(1.5)  # Simuler temps d'analyse
            
            response = generate_ai_response(prompt)
            st.markdown(response)
            
            # Ajouter la réponse à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Ajouter à l'historique des diagnostics
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.diagnosis_history.append(
                f"{timestamp} - Diagnostic via chat"
            )

def generate_ai_response(prompt: str) -> str:
    """Génère une réponse AI simulée"""
    knowledge_base = PACSKnowledgeBase()
    
    # Chercher des correspondances
    matches = []
    for issue_id, issue in knowledge_base.common_issues.items():
        matching_triggers = [t for t in issue["triggers"] if t in prompt.lower()]
        if matching_triggers:
            match_score = len(matching_triggers) * 10 + issue["probability"]
            matches.append((issue, match_score))
    
    # Trier par score
    matches.sort(key=lambda x: x[1], reverse=True)
    
    if matches:
        issue, score = matches[0]
        
        response = f"### 🩺 Diagnostic Automatique\n\n"
        response += f"**{issue['name']}** détecté avec {score}% de confiance\n\n"
        
        response += "**📊 Caractéristiques:**\n"
        response += f"• Sévérité: {issue['severity']}\n"
        response += f"• Temps de résolution estimé: {issue['time_estimate']}\n"
        response += f"• Probabilité de succès: {issue['probability']}%\n\n"
        
        response += "**🛠️ Procédure de résolution:**\n"
        for i, solution in enumerate(issue["solutions"], 1):
            response += f"\n**Étape {i}:** {solution}"
        
        response += "\n\n**💡 Conseils supplémentaires:**\n"
        response += "• Documentez chaque étape réalisée\n"
        response += "• Notez les messages d'erreur exacts\n"
        response += "• Contactez IT si problème persiste après 15min\n"
        response += f"• Référence: INC-{random.randint(1000, 9999)}"
        
        if issue["severity"] == "Critique":
            response += "\n\n🚨 **ACTION IMMÉDIATE REQUISE** 🚨"
            response += "\nContactez le support IT immédiatement au 07 12 34 56 78"
        
        return response
    else:
        # Réponse générique pour problèmes non reconnus
        return f"""
        ### 🤔 Analyse de votre problème
        
        Je n'ai pas pu identifier exactement votre problème avec les informations fournies.
        
        **Pour m'aider à mieux comprendre:**
        
        1. **Quelle application/station?**
           - Station de lecture radiologie
           - Station de travail IRM
           - Poste administratif
           - Mobile/Tablette
        
        2. **Quand est-ce arrivé?**
           - À l'ouverture de l'application
           - Pendant une manipulation spécifique
           - Après une mise à jour
           - Depuis toujours
        
        3. **Message d'erreur exact?**
           - Copiez-collez le message
           - Code d'erreur (ex: 0x80070005)
           - Capture d'écran si possible
        
        4. **Combien de personnes concernées?**
           - Vous seul(e)
           - Tout le département
           - Tous les utilisateurs
        
        **En attendant, essayez:**
        🔄 Redémarrage de la station
        🌐 Vérification connexion réseau
        🧹 Nettoyage cache navigateur
        
        **Ou utilisez les outils de diagnostic ci-dessous** ⬇️
        """

# =================== OUTILS DE DIAGNOSTIC ===================
def render_diagnostic_tools():
    """Affiche les outils de diagnostic"""
    st.markdown("### 🛠️ Centre de Diagnostic")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧 Tests Système", 
        "📊 Analyse Logs", 
        "💾 Monitoring", 
        "🎯 Diagnostic Avancé"
    ])
    
    with tab1:
        render_system_tests()
    
    with tab2:
        render_log_analysis()
    
    with tab3:
        render_resource_monitoring()
    
    with tab4:
        render_advanced_diagnostic()

def render_system_tests():
    """Affiche les tests système"""
    st.markdown("#### Tests de Connexion et Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Test Réseau Complet", use_container_width=True):
            with st.spinner("Exécution des tests..."):
                time.sleep(2)
                results, evaluation = PACSTools.perform_network_test()
                
                st.success("✅ Tests complétés")
                
                for key, value in results.items():
                    st.metric(key.replace("_", " ").title(), 
                             f"{value}{'ms' if 'ping' in key else ' Mbps' if 'speed' in key else '%' if 'loss' in key else ''}")
                
                st.info(f"**Évaluation:** {evaluation}")
    
    with col2:
        if st.button("⚡ Test Performance", use_container_width=True):
            with st.spinner("Mesure des performances..."):
                time.sleep(1.5)
                
                st.success("✅ Test de performance terminé")
                
                metrics = {
                    "Temps chargement image": f"{random.randint(1, 5)}s",
                    "FPS affichage": f"{random.randint(24, 60)}",
                    "Latence interface": f"{random.randint(10, 50)}ms",
                    "Score performance": f"{random.randint(70, 95)}/100"
                }
                
                for key, value in metrics.items():
                    st.metric(key, value)

def render_log_analysis():
    """Affiche l'analyse de logs"""
    st.markdown("#### Analyse des Logs Système")
    
    if st.button("📋 Analyser les Logs", type="primary"):
        with st.spinner("Analyse en cours..."):
            time.sleep(2)
            logs = PACSTools.generate_logs()
            
            # Analyse
            error_count = sum(1 for log in logs if "ERROR" in log)
            warning_count = sum(1 for log in logs if "WARN" in log)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Logs", len(logs))
            with col2:
                st.metric("Erreurs", error_count, delta_color="inverse")
            with col3:
                st.metric("Avertissements", warning_count)
            
            # Afficher les logs avec filtrage
            st.markdown("##### Derniers Logs")
            for log in logs[-5:]:
                if "ERROR" in log:
                    st.error(log)
                elif "WARN" in log:
                    st.warning(log)
                else:
                    st.info(log)
            
            # Recommandations
            if error_count > 2:
                st.error("🚨 Plusieurs erreurs détectées - Contactez IT")
            elif warning_count > 3:
                st.warning("⚠️ Plusieurs avertissements - Surveillance recommandée")
            else:
                st.success("✅ Logs système normaux")

def render_resource_monitoring():
    """Affiche le monitoring des ressources"""
    st.markdown("#### Monitoring des Ressources en Temps Réel")
    
    # Simuler des données en temps réel
    resources = PACSTools.check_system_resources()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Utilisation CPU**")
        st.progress(resources["cpu_usage"] / 100)
        st.caption(f"{resources['cpu_usage']}% - {'⚠️ Élevé' if resources['cpu_usage'] > 80 else '✅ Normal'}")
        
        st.markdown("**Utilisation Mémoire**")
        st.progress(resources["memory_usage"] / 100)
        st.caption(f"{resources['memory_usage']}% - {'⚠️ Critique' if resources['memory_usage'] > 85 else '✅ Acceptable'}")
    
    with col2:
        st.markdown("**Utilisation Disque**")
        st.progress(resources["disk_usage"] / 100)
        st.caption(f"{resources['disk_usage']}% - {'⚠️ Nettoyage requis' if resources['disk_usage'] > 75 else '✅ Correct'}")
        
        st.markdown("**Connexions Réseau**")
        st.metric("Actives", resources["network_connections"])
        st.caption(f"{'✅ Stable' if resources['network_connections'] < 150 else '⚠️ Élevé'}")
    
    # Recommandations
    st.markdown("##### 📋 Recommandations")
    
    recommendations = []
    if resources["cpu_usage"] > 80:
        recommendations.append("• Fermer applications inutiles")
    if resources["memory_usage"] > 85:
        recommendations.append("• Redémarrer la station")
    if resources["disk_usage"] > 75:
        recommendations.append("• Nettoyer fichiers temporaires")
    
    if recommendations:
        for rec in recommendations:
            st.warning(rec)
    else:
        st.success("✅ Toutes les ressources sont dans des limites acceptables")

def render_advanced_diagnostic():
    """Affiche le diagnostic avancé"""
    st.markdown("#### Diagnostic par Symptômes")
    
    # Liste des symptômes courants
    common_symptoms = [
        "Écran blanc/black screen",
        "Lenteur extrême",
        "Images pixelisées",
        "Erreur DICOM",
        "Connexion perdue",
        "Application qui crash",
        "Outils non fonctionnels",
        "Problème impression",
        "Données corrompues",
        "Interface gelée"
    ]
    
    selected_symptoms = st.multiselect(
        "Sélectionnez les symptômes observés:",
        common_symptoms,
        help="Sélectionnez tous les symptômes qui s'appliquent"
    )
    
    if st.button("🔍 Lancer le Diagnostic", type="primary") and selected_symptoms:
        with st.spinner("Diagnostic en cours..."):
            time.sleep(2)
            
            result = PACSTools.diagnose_from_symptoms(selected_symptoms)
            
            st.success(f"✅ Diagnostic terminé - {result['total_symptoms']} symptômes analysés")
            
            if result["matches"]:
                st.markdown("##### 🎯 Problèmes Identifiés")
                
                for i, match in enumerate(result["matches"], 1):
                    issue = match["issue"]
                    
                    with st.expander(f"{i}. {issue['name']} (Score: {match['score']}%)", expanded=i==1):
                        st.markdown(f"**Sévérité:** `{issue['severity']}`")
                        st.markdown(f"**Temps estimé:** `{issue['time_estimate']}`")
                        st.markdown(f"**Probabilité:** `{issue['probability']}%`")
                        
                        st.markdown("**Symptômes correspondants:**")
                        for symptom in match["matching_symptoms"]:
                            st.markdown(f"• {symptom}")
                        
                        st.markdown("**Solution:**")
                        for step in issue["solutions"]:
                            st.markdown(f"📌 {step}")
            else:
                st.warning("Aucun problème spécifique identifié. Essayez de décrire plus précisément.")
    
    # Diagnostic manuel
    st.markdown("---")
    st.markdown("#### 🩺 Diagnostic Manuel Assisté")
    
    with st.form("manual_diagnosis"):
        problem_desc = st.text_area("Décrivez le problème en détail:", 
                                  placeholder="Ex: Lorsque j'essaie d'ouvrir une étude CT, l'écran reste blanc après 30 secondes...")
        
        occurred_when = st.selectbox("Quand est-ce arrivé?", 
                                   ["À l'ouverture", "Pendant une manipulation", "Après mise à jour", "Soudainement"])
        
        affected_users = st.radio("Qui est affecté?", 
                                ["Moi seul", "Mon équipe", "Tout le département", "Tous les utilisateurs"])
        
        submitted = st.form_submit_button("📤 Soumettre pour Analyse")
        
        if submitted and problem_desc:
            st.info("✅ Diagnostic soumis. Consultez le chat pour les résultats.")

# =================== FOOTER ===================
def render_footer():
    """Affiche le footer"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🏥 Support IT Immédiat**
        📞 Extension: **5555**  
        📱 Mobile: **07 12 34 56 78**  
        ✉️ Email: **support@pacs-hospital.fr**
        """)
    
    with col2:
        st.markdown("""
        **🕒 Horaires Support**
        Lundi-Vendredi: 7h-20h  
        Samedi: 8h-14h  
        Urgences: 24h/24
        """)
    
    with col3:
        st.markdown("""
        **📋 Références**
        Version: **2.1.0**  
        Dernière mise à jour: **2024-01-15**  
        © 2024 PACS Helper Bot Pro
        """)
    
    st.caption("Assistant intelligent pour la radiologie - Conçu pour les professionnels de santé")

# =================== APPLICATION PRINCIPALE ===================
def main():
    """Fonction principale de l'application"""
    
    # Initialiser les bases de données
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = PACSKnowledgeBase()
    
    if 'tools' not in st.session_state:
        st.session_state.tools = PACSTools()
    
    # Rendu de l'interface
    render_sidebar()
    render_header()
    render_emergency_section()
    
    # Onglets principaux
    tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "🔧 Outils Diagnostic", "📚 Base de Connaissances"])
    
    with tab1:
        render_predefined_questions()
        st.markdown("---")
        render_chat_interface()
    
    with tab2:
        render_diagnostic_tools()
    
    with tab3:
        render_knowledge_base()
    
    render_footer()

def render_knowledge_base():
    """Affiche la base de connaissances"""
    st.markdown("### 📚 Base de Connaissances PACS")
    
    knowledge_base = st.session_state.knowledge_base
    
    # Filtrer par catégorie
    categories = ["Tous", "Critique", "Élevé", "Moyen", "Faible"]
    selected_category = st.selectbox("Filtrer par sévérité:", categories)
    
    # Afficher les problèmes
    for issue_id, issue in knowledge_base.common_issues.items():
        if selected_category == "Tous" or selected_category == issue["severity"]:
            severity_color = {
                "Critique": "#ef4444",
                "Élevé": "#f97316",
                "Moyen": "#eab308",
                "Faible": "#22c55e"
            }.get(issue["severity"], "#6b7280")
            
            st.markdown(f"""
            <div class="medical-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: {severity_color};">{issue['name']}</h4>
                    <span style="background: {severity_color}22; color: {severity_color}; 
                                padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem;">
                        {issue['severity']}
                    </span>
                </div>
                <p style="color: #666; margin: 0.5rem 0;">
                    <strong>Temps estimé:</strong> {issue['time_estimate']} | 
                    <strong>Probabilité:</strong> {issue['probability']}%
                </p>
                <div style="margin: 0.5rem 0;">
                    <strong>Symptômes:</strong><br>
                    {', '.join([f'<span class="symptom-tag">{s}</span>' for s in issue['symptoms']])}
                </div>
                <details>
                    <summary>Voir la solution</summary>
                    <div style="margin-top: 1rem;">
                        {''.join([f'<div class="solution-step">{s}</div>' for s in issue['solutions']])}
                    </div>
                </details>
            </div>
            """, unsafe_allow_html=True)

# =================== LANCEMENT ===================
if __name__ == "__main__":
    main()
