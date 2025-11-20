import streamlit as st
import pandas as pd
import gspread as gs

from ucitaj import ucitaj_podatke


SHEET_URL = st.secrets["sheet_url"]
SHEET_NAME = "filmovi"
df, worksheet = ucitaj_podatke(SHEET_URL, SHEET_NAME)

df["Godine"] = pd.to_numeric(df["Godine"])
df["Ocjena"] = pd.to_numeric(df["Ocjena"])

st.title("moji felimioviiii")

st.subheader("trenutni popis: ")
st.dataframe(df)

st.subheader("Dodaj novi film:")
naslov = st.text_input("naslov")
godina = st.number_input("godina", step=1, format="%d")
zanr = st.text_input("žanr")
ocjena = st.slider("Ocjena", 1, 100)

if st.button("Dodaj film") == True:
    novi_red = [naslov, int(godina), zanr, ocjena]
    worksheet.append_row(novi_red)
    st.success("film je uspješno dodan")
    st.rerun()
    
st.subheader("pretraži filmove")
filtrirani = df.copy()

žanr_filt = st.text_input("pretraži po žanru:")
godina_filt = st.number_input("pretraži po godini:", format="%d")

if žanr_filt:
    filtrirani = filtrirani[["Žanr"].str.contains(žanr_filt, case=False)]
    
if godina_filt:
    filtrirani = filtrirani[filtrirani["Godina"] == int(godina_filt)]
    
st.dataframe(filtrirani)

st.subheader("brisanje filmova")

filmovi_opcije = df.apply(lambda row: f"{row["Naslov"]} ({row["Godina"]})", axis=1).tolist()
film_za_brisanje = st.selectbox("odaberi film za brisanje", options=filmovi_opcije)

if st.button("izbriši film"):
    for idx, row in df.iterrows():
        if f"{row["Naslov"]} ({row["Godina"]})" == film_za_brisanje:
            worksheet.delete_rows(idx + 2)
            st.success("uspješno itzbrisan!!!!!!")
            st.rerun()
            
st.subheader("top 67 cumllection")

top3 = df.sort_values(by = "Ocjena", ascending=False).head(3)
st.table(top3)

