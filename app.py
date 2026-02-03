import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Kings League Manager", layout="wide", page_icon="👑")

def carica_dati(nome_foglio):
    try:
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        # Forziamo la lettura di tutte le colonne come stringhe per i link
        return pd.read_csv(url, dtype=str)
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

# --- SEZIONE CRONACA ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- PAGINA CLASSIFICA ---
if menu == "📊 Classifica":
    st.header("Classifica Live")
    df = carica_dati("Classifica")
    
    if df is not None:
        # Convertiamo i punti in numeri per l'ordinamento
        df['Punti'] = pd.to_numeric(df['Punti'], errors='coerce').fillna(0)
        df_ordinata = df.sort_values(by="Punti", ascending=False).reset_index(drop=True)
        
        # MOSTRA TABELLA CON LOGHI
        st.dataframe(
            df_ordinata.style.apply(colora_podio, axis=1),
            column_config={
                "Logo": st.column_config.ImageColumn("Stemma"), # 'Logo' deve essere uguale a cella F1
                "Punti": st.column_config.NumberColumn(format="%d 🏆")
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.error("Errore: Il foglio 'Classifica' non risponde. Controlla il nome del tab!")

# (Il resto delle funzioni Dado e Carte rimane invariato...)
elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado")
    if st.button("Lancia il Dado 🎲"):
        ris = random.choice(["1 vs 1", "2 vs 2", "3 vs 3", "4 vs 4", "5 vs 5", "🚀 SCONTRO TOTALE"])
        st.balloons()
        st.success(f"### Risultato: {ris}")

elif menu == "🃏 Carte Segrete":
    st.header("Arma Segreta")
    if st.button("Pesca 🃏"):
        st.warning(f"### Carta: {random.choice(['🎯 RIGORE', '🧤 PORTIERE FUORI', '💰 GOL DOPPIO', '🚫 SANZIONE'])}")

elif menu == "🎥 Highlights":
    st.header("Highlights Video")
    link = st.text_input("Link Video:", "")
    if link:
        if "youtube" in link or "youtu.be" in link: st.video(link)
        else: st.link_button("Guarda il Video 📺", link)
