import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Estabelece a conexão com o banco de dados usando uma engine do SQLAlchemy
engine = create_engine('mysql://sql10699541:uD5suGjlyY@sql10.freesqldatabase.com/sql10699541')
Session = sessionmaker(bind=engine)

# Query SQL para atualizar o nome do jogador com ID 1001 para 'b'
query = text("""
UPDATE `players_info` 
SET player_nick = 'b'
WHERE player_id = :id
""")

# Função para atualizar o nome do jogador
def update_player_name():
    with Session() as session:
        session.execute(query, {"id": 1001})  # Define o ID do jogador
        session.commit()  # Commit da transação
        st.write("Done")  # Mensagem de confirmação

# Botão para executar a atualização
if st.button('Go'):
    update_player_name()
