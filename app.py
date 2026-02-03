import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings Valdagri Cup", 
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

# 3. TITOLO E SIDEBAR
st.title("👑 Kings Valdagri Cup")

# METODO 1: Pulsante Social nella Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png", width=30)
st.sidebar.write("📸 **Seguici su Instagram**")
st.sidebar.link_button("kings_valdagri_cup", "https://www.instagram.com/kings_valdagri_cup/")
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "⚽ Marcatori", "📅 Calendario", "🎥 Highlights", "📜 Regolamento"])

# --- LIVE TICKER ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    st.info(f"🔴 **LIVE {df_cronaca.iloc[-1]['Ora']}:** {df_cronaca.iloc[-1]['Evento']}")

# --- SEZIONI ---

if menu == "📊 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        for c in ['Punti', 'Vinte', 'GF', 'GS', 'DR']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        df_ord = df.sort_values(by=["Punti", "DR", "GF"], ascending=[False, False, False]).reset_index(drop=True)
        st.dataframe(df_ord, column_config={"Stemma": st.column_config.ImageColumn("🛡️")}, use_container_width=True, hide_index=True)

elif menu == "⚽ Marcatori":
    st.header("Classifica Marcatori")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
        st.dataframe(df_m.sort_values(by="Gol", ascending=False), use_container_width=True, hide_index=True)

elif menu == "📅 Calendario":
    st.header("Calendario e Risultati")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

# METODO 2 e 3: Sezione Video integrata
elif menu == "🎥 Highlights":
    st.header("🎥 Video e Highlights")
    st.write("Resta aggiornato sui momenti più spettacolari del torneo.")
    
    # Pulsante grande per Instagram
    st.link_button("Vedi tutti i Reel su Instagram 📸", "https://www.instagram.com/kings_valdagri_cup/")
    
    st.divider()
    
    # METODO 3: Archivio Permanente da Google Sheets
    st.subheader("📺 Archivio Video Scelti")
    df_vid = carica_dati("Video")
    if df_vid is not None:
        for index, row in df_vid.iterrows():
            st.write(f"**{row['Titolo']}**")
            # Nota: Alcuni browser bloccano l'embed diretto di Instagram per privacy. 
            # In tal caso apparirà un link cliccabile.
            st.video(row['Link'])
    else:
        st.info("Aggiungi i link ai post di Instagram nel foglio Google 'Video' per vederli qui.")

elif menu == "📜 Regolamento":
    st.header("Regolamento Ufficiale")
    st.markdown("""
    ### 📜 Regole Principali
    * **Punti**: Vittoria 3, Sconfitta 0.
    * **Classifica**: In caso di pari merito conta la Differenza Reti (DR).
    """)
