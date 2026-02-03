import streamlit as st
import pandas as pd
import random

# Configurazione Pagina
st.set_page_config(page_title="Kings League Manager", layout="wide")

# Funzione per leggere i dati da Google Sheets
def carica_dati():
    # Trasformiamo il tuo link in un formato leggibile dal codice
    sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    return pd.read_csv(url)

st.title("👑 Kings League Paesana")

# --- SIDEBAR / MENU ---
menu = st.sidebar.radio("Navigazione", ["📊 Classifica Live", "🎲 Il Dado", "📱 Social"])

if menu == "📊 Classifica Live":
    st.header("Classifica in Tempo Reale")
    try:
        df = carica_dati()
        # Ordiniamo per Punti (dal più alto al più basso)
        df = df.sort_values(by="Punti", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.success("Dati aggiornati dal Foglio Google!")
    except:
        st.error("Caricamento dati fallito. Controlla il Foglio Google!")

elif menu == "🎲 Il Dado":
    st.header("Il Momento del Dado!")
    st.write("Clicca il tasto per decidere il formato della partita (minuto 18)")
    
    opzioni_dado = ["1 vs 1 (Portiere fisso)", "2 vs 2", "3 vs 3", "4 vs 4", "5 vs 5", "🚀 Scontro Totale"]
    
    if st.button("Lancia il Dado 🎲"):
        risultato = random.choice(opzioni_dado)
        st.balloons()
        st.markdown(f"## Risultato: **{risultato}**")

elif menu == "📱 Social":
    st.header("Highlights & Community")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Qui metteremo i tuoi video!
    st.write("Commenta le giocate della giornata!")
