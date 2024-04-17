import streamlit as st
import os

current_directory = os.getcwd()
image_path = os.path.join(current_directory, 'profile_pics', 'ph_1001_pfp.png')
image_path2 = os.path.join(current_directory, 'profile_pics', 'ph_player_icon.png')

st.image('ph_player_icon.png')
st.image(image=image_path)
st.image(image=image_path2)
if st.button('reload'):
    st.rerun()
