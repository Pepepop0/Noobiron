import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from players_info;', ttl=600)

# Print results.
for row in df.itertuples():
    st.dataframe(df)