import streamlit as st
import pandas as pd
import random
import datetime

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

# Funzione estetica per il podio
def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

# 3. SIDEBAR E MENU
# Immagine e Pulsante Instagram (Sempre visibili)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png", width=40)
st.sidebar.write("📸 **Seguici su Instagram**")
st.sidebar.link_button("VAI ALLA PAGINA INSTAGRAM ↗️", "https://www.instagram.com/kings_valdagri_cup/")
st.sidebar.markdown("---")

st.title("👑 Kings Valdagri Cup Manager")

if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

# Menu semplificato (Rimossa voce Highlights)
menu = st.sidebar.radio("Navigazione", [
    "📊 Classifica", 
    "⚽ Marcatori", 
    "📅 Calendario", 
    "🎲 Il Dado", 
    "🃏 Carte Segrete", 
    "👮 Tool Arbitro", 
    "📜 Regolamento"
])

# --- LIVE TICKER ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- SEZIONI ---

# 1. CLASSIFICA
if menu == "📊 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        cols_num = ['Punti', 'Vinte', 'GF', 'GS', 'DR', 'Gialli', 'Rossi']
        for c in cols_num:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        
        # Ordinamento Ufficiale
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
                "Punti": st.column_config.NumberColumn("Pts 🏆"),
                "DR": st.column_config.NumberColumn("± DR"),
                "GS": st.column_config.NumberColumn("Gol Subiti"),
                "Gialli": st.column_config.NumberColumn("🟨"),
                "Rossi": st.column_config.NumberColumn("🟥")
            },
            use_container_width=True, 
            hide_index=True
        )

# 2. MARCATORI
elif menu == "⚽ Marcatori":
    st.header("Classifica Marcatori")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
        st.dataframe(df_m.sort_values(by="Gol", ascending=False), use_container_width=True, hide_index=True)

# 3. CALENDARIO
elif menu == "📅 Calendario":
    st.header("Calendario e Risultati")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        if 'Risultato' in df_cal.columns:
            df_cal['Risultato'] = df_cal['Risultato'].fillna("-")
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

# 4. DADO
elif menu == "🎲 Il Dado":
    st.header("🎲 Dado della Lega")
    st.markdown("**Da lanciare all'inizio del secondo tempo (Min 20-23)**")
    if st.button("LANCIA IL DADO 🔥"):
        st.balloons()
        esito = random.choice(['1 vs 1 (Portieri Bloccati in area)', '2 vs 2', '3 vs 3'])
        st.success(f"### Modalità di Gioco: **{esito}**")

# 5. CARTE SEGRETE
elif menu == "🃏 Carte Segrete":
    st.header("🃏 Pesca Carta Segreta")
    st.info("Utilizzabili dal min 5:00 al 16:59 e dal 23:00 al 35:59")
    if st.button("PESCA LA TUA ARMA ⚔️"):
        carte = [
            '⚽ GOL DOPPIO (4 Minuti)', 
            '🛑 SOSPENSIONE (3 Minuti)', 
            '🥅 RIGORE EXTRA', 
            '🤾 SHOOT-OUT', 
            '🌟 STAR PLAYER (Gol vale doppio)', 
            '🃏 JOKER (Ruba o Copia)'
        ]
        pescata = random.choice(carte)
        st.warning(f"### Hai pescato: **{pescata}**")

# 6. TOOL ARBITRO
elif menu == "👮 Tool Arbitro":
    st.header("Strumenti di Gara")
    st.markdown("Calcola l'orario di rientro dei giocatori in base alle sanzioni.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👔 Azioni Speciali")
        if st.button("CHIAMA RIGORE PRESIDENZIALE 📢"):
            st.error("### ⚠️ RIGORE PRESIDENZIALE ATTIVATO!")
            st.toast("Gioco fermo! Rigore per il Presidente!")
        
        st.divider()
        st.info("Nota: L'orario calcolato si basa sull'ora del server. Usa sempre il tuo orologio per conferma.")

    with col2:
        st.subheader("⏱️ Calcolatori Penalità")
        
        if st.button("🟨 Ammonizione (2 min)"):
            adesso = datetime.datetime.now()
            rientro = adesso + datetime.timedelta(minutes=2)
            st.success(f"Rientro previsto: **{rientro.strftime('%H:%M:%S')}** (tra 2 min)")
            
        if st.button("🛑 Carta Sospensione (3 min)"):
            adesso = datetime.datetime.now()
            rientro = adesso + datetime.timedelta(minutes=3)
            st.warning(f"Fine sospensione: **{rientro.strftime('%H:%M:%S')}** (tra 3 min)")

        if st.button("🟥 Espulsione / ⚽ Gol Doppio (4 min)"):
            adesso = datetime.datetime.now()
            fine = adesso + datetime.timedelta(minutes=4)
            st.error(f"Termine penalità/bonus: **{fine.strftime('%H:%M:%S')}** (tra 4 min)")

# 7. REGOLAMENTO
elif menu == "📜 Regolamento":
    st.header("📜 Regolamento Sintetico")
    st.markdown("""
    ### 🏆 Punteggi
    * **Vittoria:** 3 Punti
    * **Vittoria agli Shoot-out:** 2 Punti
    * **Sconfitta agli Shoot-out:** 1 Punto
    * **Sconfitta:** 0 Punti
    
    ### ⚖️ Criteri Spareggio
    1. Differenza Reti (DR)
    2. Gol Fatti (GF)
    3. Gol Subiti (GS)
    4. Minor numero di Ammonizioni (Gialli)
    5. Minor numero di Espulsioni (Rossi)
    
    ### ⏱️ Fasi Speciali
    * **Min 0-1:** 1vs1
    * **Min 18-20:** Gol Doppio Finale Primo Tempo
    * **Min 20-23:** Dado (1vs1, 2vs2 o 3vs3)
    * **Min 36:** Inizio Match Ball (se necessario)
    """)
