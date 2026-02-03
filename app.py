import streamlit as st
import pandas as pd
import random

# Configurazione Pagina
st.set_page_config(
    page_title="Kings League Manager", 
    layout="wide", 
    page_icon="🏆"
)

# Funzione per lo Sfondo e lo Stile Professionale
def aggiungi_stile():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1920&q=80");
            background-attachment: fixed;
            background-size: cover;
        }}
        /* Effetto Glassmorphism per i blocchi */
        [data-testid="stVerticalBlock"] > div {{
            background-color: rgba(0, 0, 0, 0.7) !important;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 10px;
        }}
        h1, h2, h3, p, span {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

aggiungi_stile()

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
    if row.name == 0: return ['background-color: rgba(255, 215, 0, 0.4)'] * len(row)
    if row.name == 1: return ['background-color: rgba(192, 192, 192, 0.3)'] * len(row)
    if row.name == 2: return ['background-color: rgba(205, 127, 50, 0.3)'] * len(row)
    return [''] * len(row)

st.title("👑 Kings League Manager")

# Sidebar - Logo corretto (usiamo l'emoji se il link ibb dà problemi)
st.sidebar.title("🏆 KL Tournament")
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
        col_num = ['Punti', 'Vinte', 'GF', 'GS', 'DR']
        for c in col_num: 
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        
        df_ord = df.sort_values(by=["Punti", "DR", "GF"], ascending=[False, False, False]).reset_index(drop=True)
        
        st.dataframe(
            df_ord.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("🛡️"),
                "Punti": st.column_config.NumberColumn("Pts"),
                "DR": st.column_config.NumberColumn("±DR")
            },
            use_container_width=True, hide_index=True
        )

# --- 2. MARCATORI ---
elif menu == "⚽ Marcatori":
    st.header("Pichichi - Capocannonieri")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
        st.dataframe(df_m.sort_values(by="Gol", ascending=False), use_container_width=True, hide_index=True)

# --- 3. CALENDARIO ---
elif menu == "📅 Calendario":
    st.header("Prossime Sfide")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

# --- DADO E CARTE ---
elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado")
    if st.button("Lancia 🎲"):
        st.balloons()
        st.success(f"### Esito: {random.choice(['1vs1', '2vs2', '3vs3', '4vs4', '5vs5', '🚀 SCONTRO TOTALE'])}")

elif menu == "🃏 Carte Segrete":
    st.header("Carte Speciali")
    if st.button("Pesca 🃏"):
        st.warning(f"### Carta: {random.choice(['🎯 RIGORE', '🧤 PORTIERE FUORI', '💰 GOL DOPPIO', '🚫 SANZIONE', '🃏 RUBACARTA'])}")
