import streamlit as st

st.image('ph_player_icon.png')
st.image(image=f'pfp_test\ph_player_icon.png')

if st.button('reload'):
    st.rerun()