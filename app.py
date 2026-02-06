import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import base64

# -----------------------------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Kings Valdagri Cup", 
    layout="wide", 
    page_icon="👑",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. FUNZIONE PER CODIFICARE L'IMMAGINE DI SFONDO
# -----------------------------------------------------------------------------
def get_base64_of_bin_file(bin_file):
    """
    Legge un file binario (come un'immagine) e lo restituisce codificato in base64.
    """
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# --- TENTATIVO DI FORZARE L'ICONA (Codice Invariato) ---
icon_url = "https://cdn-icons-png.flaticon.com/512/2545/2545603.png"
st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{icon_url}">
        <link rel="icon" type="image/png" href="{icon_url}">
        <link rel="shortcut icon" href="{icon_url}">
    </head>
    """, unsafe_allow_html=True)

# --- FUNZIONI UTILI ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

def carica_dati(nome_foglio):
    try:
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# -----------------------------------------------------------------------------
# 3. CSS CON SFONDO PERSONALIZZATO
# -----------------------------------------------------------------------------

# >>> CAMBIA QUI IL NOME DEL TUO FILE IMMAGINE <<<
image_filename = "sfondo.jpeg" 
bin_str = get_base64_of_bin_file(image_filename)

# Crea la regola CSS per lo sfondo
if bin_str:
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
else:
    # Fallback nel caso l'immagine non venga trovata
    page_bg_img = """
    <style>
    .stApp {
        background-color: #020b1c; /* Blu notte di default */
    }
    </style>
    """

# Applica il CSS per lo sfondo e tutto il resto dello stile "Blue Edition"
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;700&display=swap');
    
    /* FONT GENERALE */
    .stApp {
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    
    /* PULIZIA INTERFACCIA */
    footer {visibility: hidden; display: none !important;}
    [data-testid="stElementToolbar"] {display: none !important;}
    header {background-color: rgba(0,0,0,0) !important;} /* Header trasparente */

    /* CARD: BLU SCURO SEMI-TRASPARENTE CON BORDO AZZURRO */
    div.css-card {
        background-color: rgba(10, 25, 48, 0.85); /* Semi-trasparente */
        border: 1px solid #1E90FF;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    /* TITOLI: BIANCO PURO */
    h1, h2, h3 { 
        color: #ffffff !important; 
        text-transform: uppercase; 
        text-shadow: 0px 0px 10px rgba(30, 144, 255, 0.8);
    }
    
    /* TABELLE: SEMI-TRASPARENTI */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border: 1px solid #1E90FF;
        border-radius: 10px;
        overflow: hidden;
        background-color: rgba(10, 25, 48, 0.85) !important; /* Semi-trasparente */
    }
    
    /* SIDEBAR: SEMI-TRASPARENTE */
    [data-testid="stSidebar"] { 
        background-color: rgba(0, 4, 10, 0.9) !important; 
        border-right: 1px solid #1E90FF; 
    }
    
    /* PULSANTI */
    div.stButton > button {
        background-color: #1E90FF;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        width: 100%;
        border: none;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover { 
        background-color: #00bfff;
        transform: scale(1.02);
    }
    
    /* SCRITTE SECONDARIE */
    p, label, span { color: #e0e0e0 !important; }

    /* LIVE SCORE */
    .live-score { font-size: 3rem; font-weight: bold; text-align: center; color: #fff; text-shadow: 0 0 10px #1E90FF; }
    .live-team { font-size: 1.2rem; color: #b0c4de; text-align: center; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. CARICAMENTO ASSETS
# -----------------------------------------------------------------------------
lottie_cup = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_touohxv0.json")
lottie_soccer = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_6YCRFI.json")

# -----------------------------------------------------------------------------
# 5. SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    if lottie_cup: st_lottie(lottie_cup, height=150, key="cup")
    st.markdown("<h2 style='text-align: center;'>KINGS VALDAGRI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("NAVIGAZIONE", [
        "🏠 Home & Live", 
        "🏆 Classifica", 
        "👕 Squadre",
        "⚽ Marcatori", 
        "📅 Calendario", 
        "📜 Regolamento"
    ])
    
    st.markdown("---")
    if st.button("🔄 AGGIORNA DATI"):
        st.rerun()
    st.link_button("📸 Instagram", "https://www.instagram.com/kings_valdagri_cup/", type="primary")

# -----------------------------------------------------------------------------
# 6. LOGICA PAGINE
# -----------------------------------------------------------------------------

# === 1. HOME & LIVE ===
if menu == "🏠 Home & Live":
    st.title("🏟️ Match Center")
    
    # News
    df_cronaca = carica_dati("Cronaca")
    if df_cronaca is not None and not df_cronaca.empty:
        df_cronaca = df_cronaca.dropna(subset=['Evento'])
        if not df_cronaca.empty:
            ultimo = df_cronaca.iloc[-1]
            st.info(f"📢 **ULTIM'ORA {ultimo['Ora']}:** {ultimo['Evento']}")
    
    # Match Live
    df_cal = carica_dati("Calendario")
    match_live = None
    if df_cal is not None and 'Stato' in df_cal.columns:
        match_live = df_cal[df_cal['Stato'].str.contains("LIVE", case=False, na=False)]

    if match_live is not None and not match_live.empty:
        row = match_live.iloc[0]
        gc = int(float(row['Gol Casa'])) if pd.notna(row['Gol Casa']) and row['Gol Casa'] != "" else 0
        go = int(float(row['Gol Ospite'])) if pd.notna(row['Gol Ospite']) and row['Gol Ospite'] != "" else 0
        
        st.markdown(f"""
        <div class="css-card">
            <h3 style="text-align:center; color:#1E90FF !important;">🔴 ORA IN CAMPO</h3>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:20px;">
                <div style="width:30%; text-align:center;"><div class="live-team">{row['Casa']}</div></div>
                <div style="width:40%; text-align:center;">
                    <div class="live-score">{gc} - {go}</div>
                    <small>{row['Ora']}</small>
                </div>
                <div style="width:30%; text-align:center;"><div class="live-team">{row['Ospite']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1,2])
        with col1:
            if lottie_soccer: st_lottie(lottie_soccer, height=200)
        with col2:
            st.markdown("### Nessuna partita in corso.")
            st.write("Consulta il calendario per i prossimi match!")

# === 2. CLASSIFICA ===
elif menu == "🏆 Classifica":
    st.title("🏆 Classifica")
    df = carica_dati("Classifica")
    if df is not None:
        df = df.dropna(subset=['Squadre']) 
        cols_num = ['Punti', 'PG', 'Vinte', 'GF', 'GS', 'DR', 'Gialli', 'Rossi']
        for c in cols_num:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        
        sort_by = ["Punti", "DR", "GF", "GS"]
        asc = [False, False, False, True]
        if 'Gialli' in df.columns: sort_by.extend(["Gialli", "Rossi"]); asc.extend([True, True])

        df_ord = df.sort_values(by=sort_by, ascending=asc).reset_index(drop=True)
        
        st.dataframe(
            df_ord,
            column_config={
                "Stemma": st.column_config.ImageColumn("Team", width="small"),
                "Punti": st.column_config.NumberColumn("PTS", format="%d"),
                "PG": st.column_config.NumberColumn("PG"),
                "DR": st.column_config.NumberColumn("Diff"),
                "Vinte": st.column_config.NumberColumn("V"),
                "Gialli": st.column_config.NumberColumn("🟨"),
                "Rossi": st.column_config.NumberColumn("🟥")
            },
            use_container_width=True, hide_index=True
        )

# === 3. SQUADRE ===
elif menu == "👕 Squadre":
    st.title("👕 Le Rose")
    
    df_players = carica_dati("Marcatori")
    df_stemmi = carica_dati("Classifica")
    
    map_loghi = {}
    if df_stemmi is not None and 'Squadre' in df_stemmi.columns and 'Stemma' in df_stemmi.columns:
        df_clean = df_stemmi.dropna(subset=['Squadre', 'Stemma'])
        map_loghi = dict(zip(df_clean['Squadre'], df_clean['Stemma']))
    
    # URL SCUDO DEFAULT (BLU)
    URL_DEFAULT = "https://cdn-icons-png.flaticon.com/512/10613/10613919.png"

    if df_players is not None and 'Squadra' in df_players.columns:
        df_players = df_players.dropna(subset=['Squadra'])
        df_players = df_players[df_players['Squadra'] != '']
        if 'Gol' in df_players.columns:
             df_players['Gol'] = pd.to_numeric(df_players['Gol'], errors='coerce').fillna(0).astype(int)

        teams = df_players['Squadra'].unique()
        cols = st.columns(2)
        
        for i, team in enumerate(teams):
            with cols[i % 2]:
                with st.container(border=True):
                    logo_url = map_loghi.get(team, URL_DEFAULT)
                    
                    c_img, c_txt = st.columns([1, 4])
                    with c_img:
                        st.image(logo_url, use_container_width=True)
                    with c_txt:
                        st.markdown(f"<h3 style='margin:0; padding-top:10px;'>{team}</h3>", unsafe_allow_html=True)
                    
                    st.divider()
                    roster = df_players[df_players['Squadra'] == team][['Giocatore', 'Gol']]
                    roster = roster.sort_values(by="Giocatore")
                    st.table(roster.set_index('Giocatore'))

# === 4. MARCATORI ===
elif menu == "⚽ Marcatori":
    st.title("👟 Golden Boot")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m = df_m.dropna(subset=['Giocatore']) 
        df_m.columns = [c.capitalize() for c in df_m.columns]
        
        if 'Gol' in df_m.columns:
            df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
            
            top3 = df_m.sort_values(by="Gol", ascending=False).head(3)
            c1, c2, c3 = st.columns(3)
            if len(top3) >= 1: c2.metric("🥇 Top Scorer", top3.iloc[0]['Giocatore'], f"{int(top3.iloc[0]['Gol'])} Gol")
            if len(top3) >= 2: c1.metric("🥈 Secondo", top3.iloc[1]['Giocatore'], f"{int(top3.iloc[1]['Gol'])} Gol")
            if len(top3) >= 3: c3.metric("🥉 Terzo", top3.iloc[2]['Giocatore'], f"{int(top3.iloc[2]['Gol'])} Gol")
            
            st.divider()
            
            st.dataframe(
                df_m.sort_values(by="Gol", ascending=False),
                use_container_width=True, hide_index=True,
                column_config={"Gol": st.column_config.ProgressColumn("Reti", format="%d", min_value=0, max_value=int(df_m['Gol'].max()))}
            )

# === 5. CALENDARIO ===
elif menu == "📅 Calendario":
    st.title("📅 Calendario Gare")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        df_cal = df_cal.dropna(subset=['Casa', 'Ospite'])
        
        required = ['Casa', 'Ospite', 'Gol Casa', 'Gol Ospite', 'Ora', 'Stato']
        if all(c in df_cal.columns for c in required):
            for index, row in df_cal.iterrows():
                gc = int(float(row['Gol Casa'])) if pd.notna(row['Gol Casa']) and row['Gol Casa'] != "" else ""
                go = int(float(row['Gol Ospite'])) if pd.notna(row['Gol Ospite']) and row['Gol Ospite'] != "" else ""
                score = f"{gc} - {go}" if gc != "" else "vs"
                
                border = "#1E90FF" if "LIVE" in str(row['Stato']) else "#333"
                
                st.markdown(f"""
                <div style="background-color: rgba(10, 25, 48, 0.85); border: 1px solid {border}; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:bold; color:#b0c4de;">{row['Ora']}</span>
                        <span style="font-size:0.8em; background-color:#333; padding:2px 8px; border-radius:5px; color: white;">{row['Stato']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; font-size:1.1em;">
                        <span style="width:40%; text-align:right; color: white;">{row['Casa']}</span>
                        <span style="width:20%; text-align:center; font-weight:bold; color:#1E90FF;">{score}</span>
                        <span style="width:40%; text-align:left; color: white;">{row['Ospite']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# === 6. REGOLAMENTO ===
elif menu == "📜 Regolamento":
    st.title("📜 Le Regole del Gioco")
    t1, t2, t3 = st.tabs(["🏆 Punti", "⏱️ Fasi", "🃏 Carte"])
    with t1: st.info("Vittoria: 3pt | Rigori Vinti: 2pt | Rigori Persi: 1pt | KO: 0pt")
    with t2: st.success("Min 0-1: 1vs1 | Min 18: Dado | Min 38: Gol Doppio")
    with t3: st.warning("Carte: Gol Doppio, Sospensione, Rigore, Jolly")
