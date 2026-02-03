import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Kings League Manager", layout="wide", page_icon="👑")

def carica_dati(nome_foglio):
    try:
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        return pd.read_csv(url)
    except:
        return None

def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

st.title("👑 Kings League Manager")

# Sidebar
if st.sidebar.button("🔄 Aggiorna Pagina"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "🎲 Il Dado", "🃏 Carte Segrete", "🎥 Highlights"])

# --- CRONACA ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- CLASSIFICA ---
if menu == "📊 Classifica":
    st.header("Classifica Live")
    df = carica_dati("Classifica")
    
    if df is not None:
        # Pulizia: togliamo righe vuote e ordiniamo
        df = df.dropna(subset=['Squadre']) if 'Squadre' in df.columns else df.dropna(subset=['Squadre'])
        df['Punti'] = pd.to_numeric(df['Punti'], errors='coerce').fillna(0)
        df_ordinata = df.sort_values(by="Punti", ascending=False).reset_index(drop=True)
        
        # VISUALIZZAZIONE LOGHI (Usiamo 'Stemma' perché è il nome nel tuo foglio)
        st.dataframe(
            df_ordinata.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("🏆", width="small"),
                "Punti": st.column_config.NumberColumn(format="%d 🏆")
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.error("Assicurati che il foglio si chiami 'Classifica' e la colonna F 'Stemma'")

# --- RESTO DELLE FUNZIONI ---
elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado")
    if st.button("Lancia il Dado 🎲"):
        st.balloons()
        st.success(f"Risultato: {random.choice(['1vs1', '2vs2', '3vs3', '4vs4', '5vs5', 'SCONTRO TOTALE'])}")

elif menu == "🃏 Carte Segrete":
    st.header("Arma Segreta")
    if st.button("Pesca 🃏"):
        st.warning(f"Carta: {random.choice(['🎯 RIGORE', '🧤 PORTIERE FUORI', '💰 GOL DOPPIO', '🚫 SANZIONE'])}")

elif menu == "🎥 Highlights":
    st.header("Highlights Video")
    link = st.text_input("Link Video:", "")
    if link:
        if "youtube" in link or "youtu.be" in link: st.video(link)
        else: st.link_button("Guarda Video 📺", link)
