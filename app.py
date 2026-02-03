import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings Valdagri Cup", 
    layout="wide", 
    page_icon="👑",
    initial_sidebar_state="expanded"
)

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

# --- CSS STILE KINGS LEAGUE (CORRETTO PER MOBILE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;700&display=swap');
    
    .stApp {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    
    /* 1. NASCONDIAMO SOLO IL FOOTER E LE ICONE TABELLA */
    footer {visibility: hidden; display: none !important;}
    [data-testid="stElementToolbar"] {display: none !important;}

    /* NOTA: Ho riattivato l'Header e il MainMenu perché su mobile servono per aprire la sidebar */
    /* header {visibility: hidden; display: none !important;}  <-- RIMOSSO PER FIX MOBILE */
    /* #MainMenu {visibility: hidden; display: none !important;} <-- RIMOSSO PER FIX MOBILE */

    /* Card Stile */
    div.css-card {
        background-color: #1e1e1e;
        border: 1px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    /* Testi */
    h1, h2, h3 { color: #FFD700 !important; text-transform: uppercase; }
    
    /* Tabelle */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border: 1px solid #333;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
    
    /* Pulsanti */
    div.stButton > button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border-radius: 20px;
        width: 100%;
        border: none;
    }
    div.stButton > button:hover { background-color: #ffea70; transform: scale(1.02); }

    /* Live Score */
    .live-score { font-size: 3rem; font-weight: bold; text-align: center; color: #fff; }
    .live-team { font-size: 1.2rem; color: #ccc; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- CARICAMENTO ASSETS ---
lottie_cup = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_touohxv0.json")
lottie_soccer = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_6YCRFI.json")

# --- SIDEBAR ---
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

# --- LOGICA PAGINE ---

# 1. HOME
if menu == "🏠 Home & Live":
    st.title("🏟️ Match Center")
    
    df_cronaca = carica_dati("Cronaca")
    if df_cronaca is not None and not df_cronaca.empty:
        df_cronaca = df_cronaca.dropna(subset=['Evento'])
        if not df_cronaca.empty:
            ultimo = df_cronaca.iloc[-1]
            st.warning(f"📢 **ULTIM'ORA {ultimo['Ora']}:** {ultimo['Evento']}")
    
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
            <h3 style="text-align:center; color:red !important;">🔴 ORA IN CAMPO</h3>
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
            st.info("Nessuna partita in corso.")
            st.write("Consulta il calendario per i prossimi match!")

# 2. CLASSIFICA
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
            },
            use_container_width=True, hide_index=True
        )

# 3. SQUADRE
elif menu == "👕 Squadre":
    st.title("👕 Le Rose")
    df_players = carica_dati("Marcatori")
    
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
                    st.subheader(f"🛡️ {team}")
                    roster = df_players[df_players['Squadra'] == team][['Giocatore', 'Gol']]
                    st.table(roster.set_index('Giocatore'))

# 4. MARCATORI
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

# 5. CALENDARIO
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
                border = "#FFD700" if "LIVE" in str(row['Stato']) else "#333"
                
                st.markdown(f"""
                <div style="background-color: #1a1a1a; border: 1px solid {border}; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:bold; color:#aaa;">{row['Ora']}</span>
                        <span style="font-size:0.8em; background-color:#333; padding:2px 8px; border-radius:5px;">{row['Stato']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; font-size:1.1em;">
                        <span style="width:40%; text-align:right;">{row['Casa']}</span>
                        <span style="width:20%; text-align:center; font-weight:bold; color:#FFD700;">{score}</span>
                        <span style="width:40%; text-align:left;">{row['Ospite']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# 6. REGOLAMENTO
elif menu == "📜 Regolamento":
    st.title("📜 Le Regole del Gioco")
    t1, t2, t3 = st.tabs(["🏆 Punti", "⏱️ Fasi", "🃏 Carte"])
    with t1: st.info("Vittoria: 3pt | Rigori Vinti: 2pt | Rigori Persi: 1pt | KO: 0pt")
    with t2: st.success("Min 0-1: 1vs1 | Min 18: Dado | Min 38: Gol Doppio")
    with t3: st.warning("Carte: Gol Doppio, Sospensione, Rigore, Jolly")
