import streamlit as st
import pandas as pd

# Configurazione della pagina
st.set_page_config(page_title="Kings League Local", layout="wide")

# Titolo e Sidebar
st.title("👑 Kings League - Torneo del Paese")
menu = ["🏠 Home", "📊 Classifica", "⚽ Risultati", "🃏 Carte Speciali"]
scelta = st.sidebar.selectbox("Naviga nell'app", menu)

# --- SEZIONE HOME ---
if scelta == "🏠 Home":
    st.subheader("🔴 Live Match & News")
    st.info("Prossima Partita: **Team A vs Team B** - Ore 21:00")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://via.placeholder.com/400x200", caption="Highlights ultima giornata")
    with col2:
        st.metric(label="MVP Corrente", value="Il Bomber", delta="5 Gol")

# --- SEZIONE CLASSIFICA ---
elif scelta == "📊 Classifica":
    st.subheader("Classifica Generale")
    # Esempio di dati (in futuro verranno da un database)
    dati_classifica = {
        "Squadra": ["Porcinos", "Aniquiladores", "Saiyans"],
        "Punti": [12, 9, 7],
        "Gol Fatti": [20, 15, 12]
    }
    df = pd.DataFrame(dati_classifica)
    st.table(df.sort_values(by="Punti", ascending=False))

# --- SEZIONE CARTE SPECIALI ---
elif scelta == "🃏 Carte Speciali":
    st.subheader("Gestione Carte Segrete")
    carta = st.button("Estrai Carta Random")
    if carta:
        st.warning("Hai estratto: RIGORE PRESIDENZIALE! 🎯")
