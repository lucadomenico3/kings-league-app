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

# 3. SIDEBAR (Cuore Social)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png", width=50)
st.sidebar.markdown("### 📸 Kings Valdagri Cup")
st.sidebar.write("Segui storie, gol e interviste!")
st.sidebar.link_button("VAI SU INSTAGRAM ↗️", "https://www.instagram.com/kings_valdagri_cup/", type="primary")
st.sidebar.markdown("---")

st.title("👑 Kings Valdagri Cup")
st.markdown("*Official App - Risultati e Classifiche in tempo reale*")

if st.sidebar.button("🔄 Aggiorna Risultati"):
    st.rerun()

# Menu Navigazione
menu = st.sidebar.radio("Menu", [
    "🏆 Classifica", 
    "⚽ Marcatori", 
    "📅 Calendario", 
    "📜 Regolamento"
])

# --- LIVE TICKER (News scorrevoli) ---
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
        # Conversione numeri per evitare errori
        cols_num = ['Punti', 'Vinte', 'GF', 'GS', 'DR', 'Gialli', 'Rossi']
        for c in cols_num:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        
        # Ordinamento Ufficiale (Regolamento Art. 3)
        # 1. Punti
        # 2. Differenza Reti
        # 3. Gol Fatti
        # 4. Gol Subiti (crescente)
        # 5. Ammonizioni (crescente)
        # 6. Espulsioni (crescente)
        
        sort_by = ["Punti", "DR", "GF", "GS"]
        ascending_order = [False, False, False, True]
        
        # Se nel foglio ci sono le colonne disciplinari, le usiamo
        if 'Gialli' in df.columns and 'Rossi' in df.columns:
            sort_by.extend(["Gialli", "Rossi"])
            ascending_order.extend([True, True])

        df_ord = df.sort_values(by=sort_by, ascending=ascending_order).reset_index(drop=True)
        
        st.dataframe(
            df_ord.style.apply(colora_podio, axis=1),
            column_config={
                "Stemma": st.column_config.ImageColumn("🛡️"),
                "Punti": st.column_config.NumberColumn("PTS 🏆", format="%d"),
                "DR": st.column_config.NumberColumn("Diff.", help="Differenza Reti"),
                "GF": st.column_config.NumberColumn("GF", help="Gol Fatti"),
                "GS": st.column_config.NumberColumn("GS", help="Gol Subiti"),
                "Gialli": st.column_config.NumberColumn("🟨", help="Ammonizioni"),
                "Rossi": st.column_config.NumberColumn("🟥", help="Espulsioni")
            },
            use_container_width=True, 
            hide_index=True
        )

# 2. MARCATORI
elif menu == "⚽ Marcatori":
    st.header("👑 Bomber della Lega")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
        st.dataframe(
            df_m.sort_values(by="Gol", ascending=False), 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Gol": st.column_config.ProgressColumn(
                    "Reti", 
                    format="%d ⚽", 
                    min_value=0, 
                    max_value=df_m['Gol'].max()
                )
            }
        )

# 3. CALENDARIO
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
                    disabled=True # Solo lettura per gli utenti
                )
            }
        )

# 4. REGOLAMENTO DETTAGLIATO
elif menu == "📜 Regolamento":
    st.header("📜 Regolamento Ufficiale")
    st.markdown("Tutte le regole per seguire al meglio la Kings Valdagri Cup.")
    
    # SEZIONE 1: PUNTEGGI
    with st.expander("🏆 1. Punteggi e Classifica", expanded=True):
        st.markdown("""
        La partita non può finire in pareggio.
        * **3 Punti:** Vittoria nei tempi regolamentari.
        * **2 Punti:** Vittoria agli Shoot-out.
        * **1 Punto:** Sconfitta agli Shoot-out.
        * **0 Punti:** Sconfitta nei tempi regolamentari.
        
        **In caso di arrivo a pari punti, l'ordine è deciso da:**
        1.  Miglior Differenza Reti (DR).
        2.  Maggior numero di Gol Fatti (GF).
        3.  Minor numero di Gol Subiti (GS).
        4.  Minor numero di Ammonizioni (Coppa Disciplina).
        5.  Minor numero di Espulsioni.
        6.  Lancio della monetina.
        """)

    # SEZIONE 2: SVOLGIMENTO
    with st.expander("⏱️ 2. Fasi della Partita (40 Minuti)"):
        st.markdown("""
        **PRIMO TEMPO (20')**
        * **Min 0-1:** 1 vs 1 (Portieri bloccati in area).
        * **Min 1-2:** 2 vs 2 (Solo portiere usa mani).
        * **Min 2-3:** 3 vs 3.
        * **Min 3-4:** 4 vs 4.
        * **Min 4-17:** 5 vs 5 (Si possono usare le Carte).
        * **Min 17-20:** ⚽ **GOL DOPPIO** (Nessuna carta attivabile).
        
        **SECONDO TEMPO (20')**
        * **Min 20-23:** 🎲 **DADO** (Lancio decide: 1vs1, 2vs2 o 3vs3).
        * **Min 23-36:** 5 vs 5 (Si possono usare le Carte).
        * **Min 36-38:** ⚽ **GOL DOPPIO** (Finale di gara).
        """)

    # SEZIONE 3: CARTE
    with st.expander("🃏 3. Carte Segrete & Bonus"):
        st.markdown("""
        *Le carte possono essere giocate dal 5' al 17' e dal 23' al 36'.*
        
        * ⚽ **Gol Doppio:** Per 4 minuti i gol valgono x2.
        * 🛑 **Sospensione:** Un avversario esce per 3 minuti (anche se prende gol).
        * 🥅 **Rigore Extra:** Un rigore classico aggiuntivo.
        * 🤾 **Shoot-out:** Un rigore in movimento (5 secondi tempo max).
        * 🌟 **Star Player:** Il gol del giocatore designato vale doppio.
        * 🃏 **Joker:** Ruba la carta avversaria o ne copia una a scelta.
        * 👔 **Rigore Presidenziale:** Chiamabile solo se presente il Presidente.
        """)

    # SEZIONE 4: SANZIONI
    with st.expander("⚖️ 4. Cartellini e Sanzioni"):
        st.markdown("""
        * 🟨 **Cartellino Giallo:** Fuori per **2 minuti**. Se la squadra subisce gol, il giocatore rientra.
        * 🟥 **Cartellino Rosso:** Espulsione definitiva. Squadra in inferiorità per **4 minuti** fissi (anche se subisce gol).
        """)

    # SEZIONE 5: SHOOT-OUT
    with st.expander("🥅 5. Regole Shoot-out"):
        st.markdown("""
        * Partenza da centrocampo palla al piede.
        * Tempo massimo: **5 secondi** dal primo tocco.
        * Il portiere non può uscire dall'area durante l'azione.
        * Se il portiere tocca la
