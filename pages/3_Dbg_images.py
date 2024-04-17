import streamlit as st
import os

current_directory = os.getcwd()
image_path = os.path.join(current_directory, 'assets', 'profile_pics', '1001_pfp.png')

st.image('ph_player_icon.png')
st.image(image=image_path)

if st.button('reload'):
    st.rerun()