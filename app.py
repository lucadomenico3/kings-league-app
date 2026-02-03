import streamlit as st
import pandas as pd
import random
import time

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings Valdagri Cup", 
    layout="wide", 
    page_icon="👑"
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

def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

# 3. SIDEBAR
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png", width=30)
st.sidebar.write("📸 **Kings Valdagri Cup**")
st.sidebar.link_button("Segui su Instagram", "https://www.instagram.com/kings_valdagri_cup/")
st.sidebar.markdown("---")

st.title("👑 Kings Valdagri Cup Manager")

if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

# Aggiunto "Tool Arbitro" al menu
menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "⚽ Marcatori", "📅 Calendario", "🎲 Il Dado", "🃏 Carte Segrete", "👮 Tool Arbitro", "🎥 Highlights", "📜 Regolamento"])

# --- LIVE TICKER ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- SEZIONI ---

if menu == "📊 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        # Aggiunta gestione colonne disciplinari se presenti
        cols_num = ['Punti', 'Vinte', 'GF', 'GS', 'DR', 'Gialli', 'Rossi']
        for c in cols_num:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        
        # Ordinamento: Punti > DR > GF > GS > Gialli (meno è meglio) > Rossi (meno è meglio)
        sort_by = ["Punti", "DR", "GF", "GS"]
        ascending_order = [False, False, False, True]
        
        # Se hai aggiunto le colonne nel foglio, le usa per l'ordinamento
        if 'Gialli' in df.columns and 'Rossi' in df.columns:
            sort_by.extend(["Gialli", "Rossi"])
            ascending_order.extend([True, True])

        df_ord = df.sort_values(by=sort_by, ascending=ascending_order).reset_index(drop=True)
        
        st.dataframe(
            df_ord.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("🛡️"),
                "Punti": st.column_config.NumberColumn("Pts 🏆"),
                "DR": st.column_config.NumberColumn("± DR"),
                "GS": st.column_config.NumberColumn("Gol Subiti"),
                "Gialli": st.column_config.NumberColumn("🟨"),
                "Rossi": st.column_config.NumberColumn("🟥")
            },
            use_container_width=True, 
            hide_index=True
        )

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
        if 'Risultato' in df_cal.columns:
            df_cal['Risultato'] = df_cal['Risultato'].fillna("-")
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

elif menu == "🎲 Il Dado":
    st.header("🎲 Dado della Lega (Minuto 20-23)")
    st.markdown("Da lanciare all'inizio del secondo tempo.")
    if st.button("LANCIA IL DADO 🔥"):
        st.balloons()
        esito = random.choice(['1 vs 1 (Portieri Bloccati)', '2 vs 2', '3 vs 3'])
        st.success(f"### Modalità di Gioco: **{esito}**")

elif menu == "🃏 Carte Segrete":
    st.header("🃏 Pesca Carta Segreta")
    st.info("Utilizzabili dal min 5:00 al 16:59 e dal 23:00 al 35:59")
    if st.button("PESCA LA TUA ARMA ⚔️"):
        carte = ['⚽ GOL DOPPIO (4 Minuti)', '🛑 SOSPENSIONE (2 Minuti)', '🥅 RIGORE EXTRA', '🤾 SHOOT-OUT', '🌟 STAR PLAYER', '🃏 JOKER']
        pescata = random.choice(carte)
        st.warning(f"### Hai pescato: **{pescata}**")

# NUOVA SEZIONE: TOOL ARBITRO
elif menu == "👮 Tool Arbitro":
    st.header("Strumenti di Gara")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👔 Rigore Presidenziale")
        st.write("Utilizzabile una volta per squadra (se presente il Presidente).")
        if st.button("CHIAMA RIGORE PRESIDENZIALE 📢"):
            st.error("### ⚠️ RIGORE PRESIDENZIALE ATTIVATO!")
            st.toast("Il gioco si ferma! Rigore per il Presidente!")

    with col2:
        st.subheader("⏱️ Timer Rapidi")
        if st.button("🟨 Timer Giallo (2 min)"):
            with st.status("Giocatore espulso temporaneamente..."):
                st.write("Partito!")
                time.sleep(1) # Solo simulativo per non bloccare l'app
                st.write("Usa il cronometro del telefono per precisione, ma ricorda: sono 2 minuti!")
        
        if st.button("⚽ Timer Gol Doppio (4 min)"):
             st.info("Ricorda: Il Gol Doppio dura 4 minuti dal momento dell'attivazione.")

elif menu == "🎥 Highlights":
    st.header("🎥 Highlights Instagram")
    st.link_button("Vedi tutti i Reel su Instagram 📸", "https://www.instagram.com/kings_valdagri_cup/")
    st.divider()
    df_vid = carica_dati("Video")
    if df_vid is not None:
        for index, row in df_vid.iterrows():
            st.write(f"**{row['Titolo']}**")
            st.video(row['Link'])

elif menu == "📜 Regolamento":
    st.header("📜 Regolamento Sintetico")
    st.markdown("""
    ### 🏆 Punti
    * **Vittoria:** 3 | **Shoot-out Vinto:** 2 | **Shoot-out Perso:** 1 | **Sconfitta:** 0
    ### ⚖️ Spareggio
    1. Diff. Reti | 2. Gol Fatti | 3. Gol Subiti | 4. Cartellini
    ### ⏱️ Fasi
    * **Min 0-1:** 1vs1 | **Min 18:** Dado | **Min 38:** Match Ball
    """)
