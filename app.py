import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings League Manager", 
    layout="wide", 
    page_icon="🏆"
)

# 2. FUNZIONE CARICAMENTO DATI
def carica_dati(nome_foglio):
    try:
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# Funzione estetica per evidenziare il podio
def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

# 3. TITOLO E SIDEBAR
st.title("👑 Kings League Manager")

st.sidebar.title("🏆 Menu Torneo")
if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "⚽ Marcatori", "📅 Calendario", "🎲 Il Dado", "🃏 Carte Segrete"])

# --- LIVE TICKER (Cronaca) ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- SEZIONE 1: CLASSIFICA ---
if menu == "📊 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        # Pulizia numeri per ordinamento
        for c in ['Punti', 'Vinte', 'GF', 'GS', 'DR']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        
        # Ordinamento: Punti > Differenza Reti > Gol Fatti
        df_ord = df.sort_values(by=["Punti", "DR", "GF"], ascending=[False, False, False]).reset_index(drop=True)
        
        st.dataframe(
            df_ord.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("🛡️"),
                "Punti": st.column_config.NumberColumn("Pts"),
                "DR": st.column_config.NumberColumn("±DR")
            },
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
    st.header("Lancio del Dado (Minuto 18)")
    if st.button("Lancia il Dado 🎲"):
        st.balloons()
        esito = random.choice(['1vs1', '2vs2', '3vs3', '4vs4', '5vs5', '🚀 SCONTRO TOTALE'])
        st.success(f"### Risultato: **{esito}**")

# --- SEZIONE 5: CARTE ---
elif menu == "🃏 Carte Segrete":
    st.header("Pesca la tua Arma")
    if st.button("Pesca una Carta 🃏"):
        carta = random.choice(['🎯 RIGORE', '🧤 PORTIERE FUORI', '💰 GOL DOPPIO', '🚫 SANZIONE', '🃏 RUBACARTA'])
        st.warning(f"### Hai pescato: **{carta}**")
