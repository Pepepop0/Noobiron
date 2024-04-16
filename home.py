import streamlit as st
from players_CRUD import playersCRUD

# Initialize connection.
conn = st.connection('mysql', type='sql')
database = playersCRUD()

# Perform query.
df = conn.query('SELECT * from players_info;', ttl=600)

# Print results.
st.write('get_all_players():')
st.write(database.get_all_players())

st.write('get_all_data:')
st.write(database.get_all_data())

st.write('get_players_names():')
st.write(database.get_players_names())

st.write('get_players_IDs():')
st.write(database.get_players_IDs())

st.write('get_players_info():')
st.write(database.get_players_info())

st.write('get_players_score(1001):')
st.write(database.get_players_score(1001))
