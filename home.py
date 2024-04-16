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

st.write('get_players_score_DF(1001):')
st.write(database.get_players_score_DF(1001))

st.write('Update_player_info(1001):')
if st.button('update'):
    database.update_player_info(id = 1001 , new_score_axis = 9, new_score_allies = 8.5, new_name = 'pEEEEEEEEEE')
    st.rerun()

st.write('delete_player(1001)')
if st.button('delete'):
    st.write(database.delete_player(id = 1001))
    st.rerun()

st.write('insert_new_player(new_player_name ="pepe" , score_axis = 9 , score_allies = 8)')
if st.button('insert'):
    st.write(database.insert_new_player(new_player_name ="pepe" , score_axis = 9 , score_allies = 8))
    st.rerun()
