import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAZIONE PAGINA (Con il tuo logo personalizzato)
st.set_page_config(
    page_title="Kings League Manager", 
    layout="wide", 
    page_icon="https://i.ibb.co/6R799fG/logo-kings.png"
)

# 2. FUNZIONE CARICAMENTO DATI
def carica_dati(nome_foglio):
    try:
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() # Pulisce spazi vuoti nei nomi colonne
        return df
    except:
        return None

# 3. FUNZIONE ESTETICA PODIO
def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

# TITOLO PRINCIPALE
st.title("👑 Kings League Manager")

# BARRA LATERALE
st.sidebar.image("https://i.ibb.co/6R799fG/logo-kings.png", width=100)
st.sidebar.header("Menu Torneo")
if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "⚽ Marcatori", "🎲 Il Dado", "🃏 Carte Segrete"])

# --- SEZIONE CRONACA (Sempre visibile) ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- 1. PAGINA CLASSIFICA ---
if menu == "📊 Classifica":
    st.header("Classifica Live")
    df = carica_dati("Classifica")
    if df is not None:
        df['Punti'] = pd.to_numeric(df['Punti'], errors='coerce').fillna(0)
        df_ordinata = df.sort_values(by="Punti", ascending=False).reset_index(drop=True)
        
        st.dataframe(
            df_ordinata.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("Stemma", width="small"),
                "Punti": st.column_config.NumberColumn(format="%d 🏆")
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.error("Errore: Controlla che il foglio si chiami 'Classifica'")

# --- 2. PAGINA MARCATORI ---
elif menu == "⚽ Marcatori":
    st.header("Classifica Marcatori (Pichichi)")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0)
        df_m_ordinata = df_m.sort_values(by="Gol", ascending=False).reset_index(drop=True)
        st.table(df_m_ordinata)
    else:
        st.write("Nessun marcatore registrato ancora.")

# --- 3. PAGINA DADO ---
elif menu == "🎲 Il Dado":
    st.header("Lancio del Dado (Minuto 18)")
    st.write("Clicca per decidere il formato della sfida finale!")
    if st.button("Lancia il Dado 🎲"):
        opzioni = ["1 vs 1", "2 vs 2", "3 vs 3", "4 vs 4", "5 vs 5", "🚀 SCONTRO TOTALE"]
        risultato = random.choice(opzioni)
        st.balloons()
        st.success(f"### Si gioca: **{risultato}**")

# --- 4. PAGINA CARTE ---
elif menu == "🃏 Carte Segrete":
    st.header("Arma Segreta del Presidente")
    if st.button("Pesca una Carta 🃏"):
        carte = ["🎯 RIGORE", "🧤 PORTIERE FUORI", "💰 GOL DOPPIO", "🚫 SANZIONE", "🃏 RUBACARTA"]
        st.warning(f"### Hai ottenuto: **{random.choice(carte)}**")
