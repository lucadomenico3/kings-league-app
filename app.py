import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings League Manager", 
    layout="wide", 
    page_icon="🏆"
)

# 2. FUNZIONE SFONDO (Versione "Ultra" per forzare il caricamento)
def set_bg():
    st.markdown(
         f"""
         <style>
         /* Forza lo sfondo su tutti i livelli */
         .stApp, .main, .stAppHeader {{
             background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                         url("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920") !important;
             background-size: cover !important;
             background-position: center !important;
             background-repeat: no-repeat !important;
             background-attachment: fixed !important;
         }}
         /* Rende i blocchi trasparenti (Effetto Glassmorphism) */
         [data-testid="stVerticalBlock"] > div {{
             background-color: rgba(0, 0, 0, 0.7) !important;
             padding: 20px !important;
             border-radius: 15px !important;
             border: 1px solid rgba(255, 255, 255, 0.1) !important;
         }}
         /* Forza il colore del testo in bianco */
         h1, h2, h3, p, span, li, label, .stMarkdown {{
             color: white !important;
             text-shadow: 1px 1px 2px black !important;
         }}
         /* Sidebar scura */
         [data-testid="stSidebar"] {{
             background-color: rgba(20, 20, 20, 0.95) !important;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg()

# 3. FUNZIONE CARICAMENTO DATI
def carica_dati(nome_foglio):
    try:
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# 4. TITOLO E SIDEBAR
st.title("👑 Kings League Manager")

st.sidebar.title("🏆 KL Tournament")
if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "⚽ Marcatori", "📅 Calendario", "🎲 Il Dado", "🃏 Carte Segrete"])

# --- LIVE TICKER ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    st.info(f"🔴 **LIVE {df_cronaca.iloc[-1]['Ora']}:** {df_cronaca.iloc[-1]['Evento']}")

# --- SEZIONE 1: CLASSIFICA ---
if menu == "📊 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        for c in ['Punti', 'Vinte', 'GF', 'GS', 'DR']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        df_ord = df.sort_values(by=["Punti", "DR", "GF"], ascending=[False, False, False]).reset_index(drop=True)
        st.dataframe(
            df_ord, 
            column_config={"Stemma": st.column_config.ImageColumn("🛡️")}, 
            use_container_width=True, 
            hide_index=True
        )

# --- SEZIONE 2: MARCATORI ---
elif menu == "⚽ Marcatori":
    st.header("Classifica Marcatori")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
        st.dataframe(df_m.sort_values(by="Gol", ascending=False), use_container_width=True, hide_index=True)

# --- SEZIONE 3: CALENDARIO ---
elif menu == "📅 Calendario":
    st.header("Programma Partite")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

# --- SEZIONE 4: DADO ---
elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado")
    if st.button("Lancia il Dado 🎲"):
        st.balloons()
        esito = random.choice(['1vs1', '2vs2', '3vs3', '4vs4', '5vs5', '🚀 SCONTRO TOTALE'])
        st.success(f"### Risultato: **{esito}**")

# --- SEZIONE 5: CARTE (Corretta!) ---
elif menu == "🃏 Carte Segrete":
    st.header("Pesca la tua Arma")
    if st.button("Pesca una Carta 🃏"):
        carta = random.choice(['🎯 RIGORE', '🧤 PORTIERE FUORI', '💰 GOL DOPPIO', '🚫 SANZIONE', '🃏 RUBACARTA'])
        st.warning(f"### Hai pescato: **{carta}**")
