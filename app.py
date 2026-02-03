import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings League Manager", 
    layout="wide", 
    page_icon="🏆"
)

# 2. FUNZIONE SFONDO (Metodo Iniezione CSS Forzata)
def set_bg_hack():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                         url("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920");
             background-size: cover;
             background-position: center;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }}
         /* Rende leggibili i blocchi di testo */
         [data-testid="stVerticalBlock"] > div {{
             background-color: rgba(0, 0, 0, 0.7) !important;
             padding: 20px !important;
             border-radius: 15px !important;
             border: 1px solid rgba(255, 255, 255, 0.1);
         }}
         /* Forza il colore del testo */
         h1, h2, h3, p, span {{
             color: white !important;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack()

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

st.sidebar.title("🏆 Menu Torneo")
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
        st.dataframe(df_ord, column_config={"Stemma": st.column_config.ImageColumn("🛡️")}, use_container_width=True, hide_index=True)

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
    if st.button("Lancia il Dado 🎲"):
        st.balloons()
        st.success(f"### Risultato: **{random.choice(['1vs1', '2vs2', '3vs3', '4vs4', '5vs5', '🚀 SCONTRO TOTALE'])}**")

# --- SEZIONE 5: CARTE ---
elif menu == "🃏 Carte Segrete":
    if st.button("Pesca una Carta 🃏"):
        st.warning(f"### Hai pescato: **{random.choice(['🎯 RIGORE', '🧤 PORTIERE FUORI', '💰 GOL DOPPIO', '🚫 SANZIONE', '🃏 RUBACARTA'])}**")s
