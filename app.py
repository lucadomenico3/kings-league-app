import streamlit as st
import pandas as pd
import random

# 1. Configurazione Pagina
st.set_page_config(
    page_title="Kings League Manager", 
    layout="wide", 
    page_icon="🏆"
)

# 2. Funzione per lo Sfondo Personalizzato (Campo da calcio notturno)
def aggiungi_sfondo():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        /* Overlay per migliorare la leggibilità */
        [data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0);
        }}
        .stDataFrame, .stTable, .stInfo, .stSuccess, [data-testid="stVerticalBlock"] > div {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            padding: 15px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        h1, h2, h3, p, span {{
            color: white !important;
            text-shadow: 2px 2px 4px #000000;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

aggiungi_sfondo()

# 3. Funzione Caricamento Dati
def carica_dati(nome_foglio):
    try:
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

def colora_podio(row):
    if row.name == 0: return ['background-color: rgba(255, 215, 0, 0.7); color: white; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: rgba(192, 192, 192, 0.5); color: white'] * len(row)
    if row.name == 2: return ['background-color: rgba(205, 127, 50, 0.5); color: white'] * len(row)
    return [''] * len(row)

st.title("👑 Kings League Manager")

# Sidebar
st.sidebar.image("https://i.ibb.co/6R799fG/logo-kings.png", width=100)
st.sidebar.header("Menu Torneo")
if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "⚽ Marcatori", "📅 Calendario", "🎲 Il Dado", "🃏 Carte Segrete"])

# --- CRONACA ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- 1. CLASSIFICA ---
if menu == "📊 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        colonne_num = ['Punti', 'Vinte', 'GF', 'GS', 'DR']
        for col in colonne_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        df_ordinata = df.sort_values(by=["Punti", "DR", "GF"], ascending=[False, False, False]).reset_index(drop=True)
        
        st.dataframe(
            df_ordinata.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("🛡️", width="small"),
                "Punti": st.column_config.NumberColumn("Pts 🏆"),
                "GF": st.column_config.NumberColumn("⚽ F"),
                "GS": st.column_config.NumberColumn("⚽ S"),
                "DR": st.column_config.NumberColumn("± DR")
            },
            use_container_width=True, hide_index=True
        )

# --- 2. MARCATORI ---
elif menu == "⚽ Marcatori":
    st.header("Classifica Marcatori")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
        df_m_ordinata = df_m.sort_values(by=["Gol", "Giocatore"], ascending=[False, True]).reset_index(drop=True)
        st.table(df_m_ordinata)

# --- 3. CALENDARIO ---
elif menu == "📅 Calendario":
    st.header("Programma Partite")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

# --- 4. DADO E CARTE ---
elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado")
    if st.button("Lancia il Dado 🎲"):
        st.balloons()
        st.success(f"### Risultato: {random.choice(['1vs1', '2vs2', '3vs3', '4vs4', '5vs5', '🚀 SCONTRO TOTALE'])}")

elif menu == "🃏 Carte Segrete":
    st.header("Arma Segreta")
    if st.button("Pesca una Carta 🃏"):
        st.warning(f"### Carta: {random.choice(['🎯 RIGORE', '🧤 PORTIERE FUORI', '💰 GOL DOPPIO', '🚫 SANZIONE', '🃏 RUBACARTA'])}")
