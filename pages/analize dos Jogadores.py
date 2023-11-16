import streamlit as st
from modules.data_loader import load_data

df = load_data("dataset\iron_players.csv")

st.markdown(''' ## Análise dos jogadores ''')
if st.checkbox("Mostrar Estatísticas Descritivas"):
    st.write(df.describe())
