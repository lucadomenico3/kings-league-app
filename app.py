import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings League Manager", 
    layout="wide", 
    page_icon="🏆"
)

# 2. FUNZIONE SFONDO E STILE (FORZATO)
def aggiungi_stile_definitivo():
    st.markdown(
        """
        <style>
        /* Sfondo forzato su tutta l'app */
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920") !important;
            background-attachment: fixed !important;
            background-size: cover !important;
            background-position: center !important;
        }

        /* Contenitori trasparenti (effetto vetro) */
        [data-testid="stVerticalBlock"] > div {
            background-color: rgba(0, 0, 0, 0.7) !important;
            padding: 20px !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* Testo sempre bianco e leggibile */
        h1, h2, h3, p, span, .stMarkdown, [data-testid="stWidgetLabel"] {
            color: white !important;
            text-shadow: 1px 1px 2px black !important;
        }
        
        /* Sidebar scura */
        [data-testid="stSidebar"] {
            background-color: rgba(20, 20, 20, 0.9) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

aggiungi_stile_definitivo()

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

def colora_podio(row):
    if row.name == 0: return ['background-color: rgba(255, 215, 0, 0.3)'] * len(row)
    if row.name == 1: return ['background-color: rgba(192, 192, 192, 0.2)'] * len(row)
    if row.name == 2: return ['background-color: rgba(205, 127, 50, 0.2)'] * len(row)
    return [''] * len(row)

# 4. TITOLO E SIDEBAR
st.title("👑 Kings League Manager")

st.sidebar.title("🏆 KL Tournament")
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
        # Pulizia numeri
        for c in ['Punti', 'Vinte', 'GF', 'GS', 'DR']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        
        # Ordinamento: Punti > DR > GF
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

# --- SEZIONE 2: MARCATORI ---
elif menu == "⚽ Marcatori":
    st.header("Classifica Marcatori")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
        df_m_ord = df_m.sort_values(by="Gol", ascending=False).reset_index(drop=True)
        st.dataframe(df_m_ord, use_container_width=True, hide_index=True)

# --- SEZIONE 3: CALENDARIO ---
