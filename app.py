import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Kings League Manager", 
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

def colora_podio(row):
    if row.name == 0: return ['background-color: #FFD700; color: black; font-weight: bold'] * len(row)
    if row.name == 1: return ['background-color: #C0C0C0; color: black'] * len(row)
    if row.name == 2: return ['background-color: #CD7F32; color: black'] * len(row)
    return [''] * len(row)

# 3. TITOLO E SIDEBAR
st.title("👑 Kings League Manager")

st.sidebar.title("🏆 Menu Torneo")
if st.sidebar.button("🔄 Aggiorna Dati"):
    st.rerun()

menu = st.sidebar.radio("Navigazione", ["📊 Classifica", "⚽ Marcatori", "📅 Calendario", "📜 Regolamento"])

# --- LIVE TICKER ---
df_cronaca = carica_dati("Cronaca")
if df_cronaca is not None and not df_cronaca.empty:
    ultimo = df_cronaca.iloc[-1]
    st.info(f"🔴 **LIVE {ultimo['Ora']}:** {ultimo['Evento']}")

# --- SEZIONI ---

# CLASSIFICA
if menu == "📊 Classifica":
    st.header("Classifica Generale")
    df = carica_dati("Classifica")
    if df is not None:
        for c in ['Punti', 'Vinte', 'GF', 'GS', 'DR']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        df_ord = df.sort_values(by=["Punti", "DR", "GF"], ascending=[False, False, False]).reset_index(drop=True)
        st.dataframe(df_ord.style.apply(colora_podio, axis=1), column_config={"Stemma": st.column_config.ImageColumn("🛡️")}, use_container_width=True, hide_index=True)

# MARCATORI
elif menu == "⚽ Marcatori":
    st.header("Classifica Marcatori")
    df_m = carica_dati("Marcatori")
    if df_m is not None:
        df_m['Gol'] = pd.to_numeric(df_m['Gol'], errors='coerce').fillna(0).astype(int)
        st.dataframe(df_m.sort_values(by="Gol", ascending=False), use_container_width=True, hide_index=True)

# CALENDARIO & STORICO
elif menu == "📅 Calendario":
    st.header("Calendario e Risultati")
    df_cal = carica_dati("Calendario")
    if df_cal is not None:
        # Gestione colonna Risultato se presente
        if 'Risultato' in df_cal.columns:
            df_cal['Risultato'] = df_cal['Risultato'].fillna("-")
        
        st.dataframe(
            df_cal, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Risultato": st.column_config.TextColumn("Punteggio ⚽"),
                "Stato": st.column_config.SelectboxColumn(
                    "Stato",
                    options=["In programma", "Live", "Terminata"]
                )
            }
        )
    else:
        st.warning("Assicurati di avere un foglio 'Calendario' con le colonne: Ora, Sfida, Risultato, Stato.")

# REGOLAMENTO
elif menu == "📜 Regolamento":
    st.header("Regolamento Ufficiale")
    st.markdown("""
    ### 📜 Norme del Torneo
    * **Durata**: 40 minuti totali.
    * **Punti**: 3 per la vittoria, 0 per la sconfitta.
    * **Spareggio**: In caso di parità punti, conta la Differenza Reti (DR), poi i Gol Fatti (GF).
    
    ### ⚖️ Disciplina
    * Il comportamento antisportivo comporterà sanzioni immediate.
    """)
