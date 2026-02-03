import streamlit as st
import pandas as pd
import random

# Configurazione Pagina
st.set_page_config(page_title="Kings League Manager", layout="wide", page_icon="👑")

# Funzione dati
def carica_dati():
    sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    return pd.read_csv(url)

st.title("👑 Kings League Manager")

# Menu
menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "🎲 Il Dado", "🃏 Carte Segrete"])

if menu == "📊 Classifica":
    st.header("Classifica Live")
    df = carica_dati()
    st.dataframe(df.sort_values(by="Punti", ascending=False), use_container_width=True, hide_index=True)

elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado (Minuto 18)")
    if st.button("Lancia il Dado 🎲"):
        risultati = ["1 vs 1", "2 vs 2", "3 vs 3", "4 vs 4", "5 vs 5", "🚀 SCONTRO TOTALE"]
        scelta = random.choice(risultati)
        st.balloons()
        st.success(f"Si gioca in: {scelta}")

elif menu == "🃏 Carte Segrete":
    st.header("Estrai la tua Arma Segreta")
    mazzo = [
        "🎯 RIGORE: Calcia un rigore subito!",
        "🧤 PORTIERE FUORI: Un giocatore avversario fuori per 2 min",
        "💰 GOL DOPPIO: I tuoi gol valgono doppio per 5 minuti",
        "🚫 SANZIONE: Togli un giocatore avversario per 2 minuti",
        "🃏 CARTA RUBATA: Ruba la carta all'avversario!"
    ]
    if st.button("Pesca una Carta 🃏"):
        carta = random.choice(mazzo)
        st.warning(f"La tua carta è: {carta}")
