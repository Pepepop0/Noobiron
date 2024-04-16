import streamlit as st
import pandas as pd
from db_setup.players_crud import playersCRUD

atributes_player = [
    'player_id',
    'player_nick',
    'score_id_score',
    'score_axis',
    'score_allies',
]


def show_results(args , results, selected = atributes_player):

    if len(args) == 0 or len(results) == 0:
        st.table(pd.DataFrame())  # Exibe uma tabela vazia
        print("Nenhum resultado encontrado.")
    else:
        df = pd.DataFrame(results, columns=args)
        st.table(df[selected])



st.write("Todo o DB:")
db = playersCRUD()
show_results(atributes_player, db.get_all_data())
