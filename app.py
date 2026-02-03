import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Kings League Manager", layout="wide", page_icon="👑")

def carica_dati(nome_foglio):
    sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
    return pd.read_csv(url)

def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

st.title("👑 Kings League Manager")

# Refresh Manuale
if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

# --- SEZIONE CRONACA ---
try:
    df_cronaca = carica_dati("Cronaca")
    if not df_cronaca.empty:
        ultimo_evento = df_cronaca.iloc[-1]
        st.info(f"🔴 **LIVE {ultimo_evento['Ora']}:** {ultimo_evento['Evento']}")
except:
    st.write("In attesa di eventi...")

# Menu
menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "🎲 Il Dado", "🃏 Carte Segrete", "🎥 Highlights Video"])

if menu == "📊 Classifica":
    st.header("Classifica Live")
    try:
        df = carica_dati("Classifica")
        df_ordinata = df.sort_values(by="Punti", ascending=False).reset_index(drop=True)
        
        # Mostriamo la tabella con i loghi se presenti
        st.data_editor(
            df_ordinata.style.apply(colora_podio, axis=1),
            column_config={
                "Logo": st.column_config.ImageColumn("Stemma", help="Logo della squadra")
            },
            use_container_width=True,
            hide_index=True,
            disabled=True # Impedisce la modifica dall'app, solo dal foglio Google
        )
    except Exception as e:
        st.error("Errore: Assicurati che la colonna 'Logo' esista nel foglio Classifica!")

elif menu == "🎥 Highlights Video":
    st.header("Le migliori giocate")
    st.write("Guarda i momenti più epici del torneo!")
    
    # Esempio di video (puoi sostituire con link YouTube o simili)
    video_url = st.text_input("Presidente, incolla qui il link YouTube del video della giornata:", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if video_url:
        st.video(video_url)

elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado")
    if st.button("Lancia il Dado 🎲"):
        risultati = ["1 vs 1", "2 vs 2", "3 vs 3", "4 vs 4", "5 vs 5", "🚀 SCONTRO TOTALE"]
        st.balloons()
        st.success(f"Risultato: {random.choice(risultati)}")

elif menu == "🃏 Carte Segrete":
    st.header("Estrai la tua Arma Segreta")
    mazzo = ["🎯 RIGORE", "🧤 PORTIERE FUORI", "💰 GOL DOPPIO", "🚫 SANZIONE", "🃏 CARTA RUBATA"]
    if st.button("Pesca una Carta 🃏"):
        st.warning(f"La tua carta è: {random.choice(mazzo)}")
