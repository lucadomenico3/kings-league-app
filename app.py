import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings Valdagri Cup", 
    layout="wide", 
    page_icon="👑"
)

# 2. FUNZIONE CARICAMENTO DATI
def carica_dati(nome_foglio):
    try:
        # ID del tuo foglio Google
        sheet_id = "1AlDJPezf9n86qapVEzrpn7PEdehmOrnQbKJH2fYE3uY"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nome_foglio}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# Funzione estetica per evidenziare i primi 3 in classifica
def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row) # Oro
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row) # Argento
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row) # Bronzo
    return [''] * len(row)

# 3. SIDEBAR
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png", width=50)
st.sidebar.markdown("### 📸 Kings Valdagri Cup")
st.sidebar.write("Segui storie, gol e interviste!")
st.sidebar.link_button("VAI SU INSTAGRAM ↗️", "https://www.instagram.com/kings_valdagri_cup/", type="primary")
st.sidebar.markdown("---")

st.title("👑 Kings Valdagri Cup")
st.markdown("*Official App - Risultati e Classifiche in tempo reale*")

if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

# Menu Navigazione (Aggiunto "Squadre")
menu = st.sidebar.radio("Menu", [
    "🏆 Classifica", 
    "👕 Squadre",      # <--- NUOVO
    "⚽ Marcatori", 
    "📅 Calendario", 
    "📜 Regolamento"
])

# --- LIVE TICKER ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"📢 **ULTIM'ORA {ultimo['Ora']}:** {ultimo['Evento']}")

# --- SEZIONI DELL'APP ---

# 1. CLASSIFICA
if menu == "🏆 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        cols_num = ['Punti', 'Vinte', 'GF', 'GS', 'DR', 'Gialli', 'Rossi']
        for c in cols_num:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        
        sort_by = ["Punti", "DR", "GF", "GS"]
        ascending_order = [False, False, False, True]
        
        if 'Gialli' in df.columns and 'Rossi' in df.columns:
            sort_by.extend(["Gialli", "Rossi"])
            ascending_order.extend([True, True])

        df_ord = df.sort_values(by=sort_by, ascending=ascending_order).reset_index(drop=True)
        
        st.dataframe(
            df_ord.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("🛡️"),
                "Punti": st.column_config.NumberColumn("PTS 🏆", format="%d"),
                "DR": st.column_config.NumberColumn("Diff."),
                "GF": st.column_config.NumberColumn("GF"),
                "GS": st.column_config.NumberColumn("GS"),
                "Gialli": st.column_config.NumberColumn("🟨"),
                "Rossi": st.column_config.NumberColumn("🟥")
            },
            use_container_width=True, 
            hide_index=True
        )

# 2. SQUADRE (NUOVO)
elif menu == "👕 Squadre":
    st.header("Le Rose del Torneo")
    st.markdown("Clicca sulla squadra per vedere i giocatori.")
    
    # Usiamo il foglio Marcatori che contiene già Nomi e Squadre
    df_players = carica_dati("Marcatori")
    
    if df_players is not None and 'Squadra' in df_players.columns:
        # Prende la lista unica delle squadre
        squadre_uniche = df_players['Squadra'].unique()
        
        # Per ogni squadra crea un menu a tendina
        for team in squadre_uniche:
            with st.expander(f"🛡️ {team}", expanded=False):
                # Filtra solo i giocatori di quella squadra
                roster = df_players[df_players['Squadra'] == team][['Giocatore', 'Gol']]
                
                # Ordina alfabeticamente
                roster = roster.sort_values(by="Giocatore")
                
                st.dataframe(
                    roster,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Giocatore": st.column_config.TextColumn("Nome"),
                        "Gol": st.column_config.NumberColumn("Gol Segnati")
                    }
                )
    else:
        st.warning("Per vedere le squadre, assicurati di aver compilato il foglio 'Marcatori'.")

# 3. MARCATORI
elif menu == "⚽ Marcatori":
    st.header("👑 Bomber della Lega")
    df_m = carica_dati("Marcatori")
    
    if df_m is not None:
        df_m.columns = [c.capitalize() for c in df_m.columns]
        
        if 'Gol' in df_m.columns and 'Giocatore' in df_m.columns:
            df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
            max_gol = int(df_m['Gol'].max())
            if max_gol == 0: max_gol = 1
            
            st.dataframe(
                df_m.sort_values(by="Gol", ascending=False), 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Giocatore": st.column_config.TextColumn("Giocatore", width="medium"),
                    "Squadra": st.column_config.TextColumn("Squadra", width="small"),
                    "Gol": st.column_config.ProgressColumn(
                        "Reti", 
                        format="%d ⚽", 
                        min_value=0, 
                        max_value=max_gol
                    )
                }
            )

# 4. CALENDARIO
elif menu == "📅 Calendario":
    st.header("📅 Programma Partite")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        if 'Risultato' in df_cal.columns:
            df_cal['Risultato'] = df_cal['Risultato'].fillna("-")
        
        st.dataframe(
            df_cal, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Stato": st.column_config.SelectboxColumn(
                    "Stato Match",
                    options=["In programma", "🔥 LIVE", "Terminata"],
                    disabled=True 
                )
            }
        )

# 5. REGOLAMENTO
elif menu == "📜 Regolamento":
    st.header("📜 Regolamento Ufficiale")
    
    with st.expander("🏆 1. Punteggi e Classifica", expanded=True):
        st.markdown("""
        * **3 Punti:** Vittoria.
        * **2 Punti:** Vittoria Shoot-out.
        * **1 Punto:** Sconfitta Shoot-out.
        * **0 Punti:** Sconfitta.
        * **Spareggio:** 1. DR - 2. GF - 3. GS - 4. Disciplina.
        """)

    with st.expander("⏱️ 2. Fasi della Partita"):
        st.markdown("""
        * **Min 0-1:** 1 vs 1.
        * **Min 18:** Dado (Min 20-23).
        * **Min 36:** Match Ball.
        """)

    with st.expander("🃏 3. Carte e Sanzioni"):
        st.markdown("""
        * **Gol Doppio:** 4 min (x2).
        * **Sospensione:** 3 min fuori.
        * **Giallo:** 2 min fuori.
        * **Rosso:** 4 min fuori.
        """)
