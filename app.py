import streamlit as st
import pandas as pd
import random

# Configurazione Pagina
st.set_page_config(
    page_title="Kings League Manager", 
    layout="wide", 
    page_icon="🏆"
)

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
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

st.title("👑 Kings League Manager")

# Sidebar
st.sidebar.header("Menu Torneo")
if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "⚽ Marcatori", "📅 Calendario", "🎲 Il Dado", "🃏 Carte Segrete"])

# --- CRONACA ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- 1. CLASSIFICA (Spareggio: Punti -> DR -> GF) ---
if menu == "📊 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        # Trasformiamo in numeri per i calcoli
        colonne_num = ['Punti', 'Vinte', 'GF', 'GS', 'DR']
        for col in colonne_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # ORDINE: 1. Punti, 2. Differenza Reti, 3. Gol Fatti (tutti decrescenti)
        df_ordinata = df.sort_values(by=["Punti", "DR", "GF"], ascending=[False, False, False]).reset_index(drop=True)
        
        st.dataframe(
            df_ordinata.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("Logo", width="small"),
                "Punti": st.column_config.NumberColumn(format="%d 🏆"),
                "DR": st.column_config.NumberColumn(format="%d ⚽")
            },
            use_container_width=True, hide_index=True
        )

# --- 2. MARCATORI (Spareggio: Gol -> Nome) ---
elif menu == "⚽ Marcatori":
    st.header("Classifica Marcatori")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0)
        df_m_ordinata = df_m.sort_values(by=["Gol", "Giocatore"], ascending=[False, True]).reset_index(drop=True)
        st.table(df_m_ordinata)

# --- 3. CALENDARIO ---
elif menu == "📅 Calendario":
    st.header("Programma Partite")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        st.table(df_cal)

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
