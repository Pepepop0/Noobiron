import streamlit as st

st.image('ph_player_icon.png')

player_ID = st.text_input("ID:", value=1001)
st.image(f'assets\profle_pics\ph_player_icon.png')

if st.button('reload'):
    st.rerun()