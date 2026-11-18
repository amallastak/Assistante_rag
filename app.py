import streamlit as st
import sys
import os

# Connexion au backend
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from api.generate import generer_reponse

# ==========================================
# 1. CONFIGURATION & DESIGN (Cyber Blue 2026)
# ==========================================
st.set_page_config(
    page_title="Assistant Juridique - SGG",
    page_icon="⚖️",
    layout="centered"
)

# Injection de CSS Avancé
st.markdown("""
<style>
    /* 1. Fond principal : Dégradé de bleu profond */
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e3a8a 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* 2. Titre principal : Effet Néon Cyan */
    h1 {
        text-align: center;
        font-weight: 900;
        font-size: 2.8rem !important;
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(79, 172, 254, 0.4);
        margin-bottom: 5px;
    }

    /* 3. Sous-titre */
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* 4. Bulles de chat (Glassmorphism Bleu) */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 15px;
        padding: 15px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 15px;
        color: #e2e8f0;
    }

    /* 5. Barre de saisie (Fond bleu foncé, bordure cyan) */
    [data-testid="stChatInput"] {
        background-color: #0f172a !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 25px !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
    }
    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
    }

    /* 6. Boutons de suggestions (Style Bouton Bleu) */
    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
        border: 1px solid #60a5fa;
    }

    /* 7. Le texte "Recherche dans les textes officiels..." */
    .stSpinner > div {
        border-color: #38bdf8 transparent transparent transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. EN-TÊTE AVEC L'IMAGE OFFICIELLE
# ==========================================
if os.path.exists("logo_sgg.png"):
    # On centre l'image et on lui donne une taille max
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo_sgg.png", use_container_width=True)
else:
    st.warning("Image 'logo_sgg.png' introuvable.")

st.markdown("<h1>Assistant Juridique IA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Propulsé par les données officielles du SGG. Posez une question, l'IA vous répond avec les articles de loi exacts.</p>", unsafe_allow_html=True)

# ==========================================
# 3. LOGIQUE DU CHAT
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Suggestions de questions ---
if len(st.session_state.messages) == 0:
    st.markdown("<p style='text-align: center; color: #38bdf8; font-weight: bold; margin-top: 20px;'>💡 Commencez par une suggestion :</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌾 Droit d'importation du blé"):
            st.session_state.messages.append({"role": "user", "content": "Quel est le droit d'importation applicable au blé tendre et ses dérivés ?"})
            st.rerun()
        if st.button("💊 Prix des médicaments"):
            st.session_state.messages.append({"role": "user", "content": "Quels sont les prix publics de vente des médicaments commercialisés au Maroc ?"})
            st.rerun()
    with col2:
        if st.button("🏢 Création d'une société"):
            st.session_state.messages.append({"role": "user", "content": "Quelles sont les conditions pour créer une société ?"})
            st.rerun()
        if st.button("📺 Licence TV Satellite"):
            st.session_state.messages.append({"role": "user", "content": "Quelles sont les conditions d'octroi de licence pour l'exploitation d'un service de télévision par satellite ?"})
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

# --- Affichage de l'historique ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Zone de saisie ---
if prompt := st.chat_input("Posez votre question juridique..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyse des textes officiels en cours..."):
            try:
                reponse = generer_reponse(prompt)
                st.markdown(reponse)
                st.session_state.messages.append({"role": "assistant", "content": reponse})
            except Exception as e:
                st.error(f"Erreur : {e}")