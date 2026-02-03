import streamlit as st
import pandas as pd
import random

# 1. Configurazione Iniziale
st.set_page_config(page_title="Kings League Manager", layout="wide", page_icon="👑")

# 2. Funzione per caricare i dati (Con gestione errori migliorata)
def carica_dati(nome_foglio):
    try:
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        return pd.read_csv(url)
    except Exception as e:
        return None

# 3. Funzione per i colori del Podio
def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

st.title("👑 Kings League Manager")

# --- BARRA LATERALE ---
st.sidebar.header("Gestione Torneo")
if st.sidebar.button("🔄 Aggiorna Pagina"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "🎲 Il Dado", "🃏 Carte Segrete", "🎥 Highlights"])

# --- SEZIONE CRONACA (Sempre visibile) ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo_evento = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo_evento['Ora']}:** {ultimo_evento['Evento']}")
else:
    st.write("In attesa di eventi live...")

# --- LOGICA DELLE PAGINE ---

if menu == "📊 Classifica":
    st.header("Classifica Live")
    df = carica_dati("Classifica")
    
    if df is not None:
        df_ordinata = df.sort_values(by="Punti", ascending=False).reset_index(drop=True)
        
        # Configurazione colonne (Logo deve essere il nome esatto della colonna su Google Sheets)
        st.data_editor(
            df_ordinata.style.apply(colora_podio, axis=1),
            column_config={
                "Logo": st.column_config.ImageColumn("Stemma"),
                "Punti": st.column_config.NumberColumn(format="%d 🏆")
            },
            use_container_width=True,
            hide_index=True,
            disabled=True
        )
    else:
        st.error("Errore: Assicurati che il foglio Google sia pubblico e si chiami 'Classifica'")

elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado (Minuto 18)")
    if st.button("Lancia il Dado 🎲"):
        opzioni = ["1 vs 1", "2 vs 2", "3 vs 3", "4 vs 4", "5 vs 5", "🚀 SCONTRO TOTALE"]
        risultato = random.choice(opzioni)
        st.balloons()
        st.success(f"### Risultato: **{risultato}**")

elif menu == "🃏 Carte Segrete":
    st.header("Pesca la tua Carta")
    if st.button("Estrai Carta 🃏"):
        carte = ["🎯 RIGORE", "🧤 PORTIERE FUORI", "💰 GOL DOPPIO", "🚫 SANZIONE", "🃏 CARTA RUBATA"]
        st.warning(f"### Hai pescato: **{random.choice(carte)}**")

elif menu == "🎥 Highlights":
    st.header("Galleria Video")
    link_video = st.text_input("Incolla link (YouTube, TikTok o Instagram):", "")
    
    if link_video:
        if "youtube.com" in link_video or "youtu.be" in link_video:
            st.video(link_video)
        else:
            st.write("Questo social non permette la visione diretta. Clicca il tasto sotto:")
            st.link_button("Guarda il Video 📺", link_video)
