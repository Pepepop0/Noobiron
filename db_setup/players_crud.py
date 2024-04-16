import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pymysql


class playersCRUD:
    def __init__(self):
        pymysql.install_as_MySQLdb()
        self.conn = st.connection('mysql', type='sql')
        self.engine = create_engine('mysql://sql10699541:uD5suGjlyY@sql10.freesqldatabase.com/sql10699541')
        self.session = sessionmaker(bind=self.engine)

    def get_all_players(self):
        query = """
            SELECT player_id, player_nick
            FROM players_info
        """
        results = self.conn.query(query, ttl=600)
        #print("get_all_players:\n", results)
        player_list = results.values.tolist()
        #print(player_list)
        return player_list


    def get_all_data(self):
        query = """
                select *
                from players_info as pi, players_statics as ps
                where pi.player_id = ps.player_id;
        """
        results = self.conn.query(query, ttl=600)
        #print("get_all_data:\n", results.values.tolist())
        return results.values.tolist()

    def get_players_names(self):
        query = """
        select player_nick
        from players_info
        """
        results = self.conn.query(query, ttl=600)
        return results.values.tolist()

    def get_players_IDs(self):
        query = """
        select player_id
        from players_info
        """
        results = self.conn.query(query, ttl=600)
        return results.values.tolist()
    
    def get_players_info(self):
        query = """
        select player_id, player_nick
        from players_info
        """
        results = self.conn.query(query, ttl=600)
        player_info_dict = {id: nick for id, nick in results.values.tolist()}
        return player_info_dict
    
    def get_players_score(self, id):
        query = f"""
        select score_axis, score_alies
        from players_statics
        where player_id = {id}
        """
        results = self.conn.query(query, ttl=600)
        results = results.values.tolist()
        results = [results[0][0], results[0][1]]
        return results
    
    def get_players_score_DF(self, id):
        query = f"""
        select score_axis, score_alies
        from players_statics
        where player_id = {id}
        """
        results = self.conn.query(query, ttl=600)
        results = list(results.to_records(index=False))
        return [results]

    def update_player_info(self, id, new_score_axis, new_score_allies, new_name):
        # Atualiza as estatísticas do jogador
        query = text(f"""
        UPDATE players_statics
        SET score_axis = {new_score_axis}, score_alies = {new_score_allies}
        WHERE player_id = {id}
        """)
        #print(query)
        with self.session() as session:
            session.execute(query)
            session.commit()

        # Atualiza o nome do jogador
        query = text(f"""
        UPDATE players_info
        SET player_nick = '{new_name}'
        WHERE player_id = {id}
        """)
        #print(query)

        with self.session() as session:
            session.execute(query)
            session.commit()
        #print("Infos atualizadas com sucesso para o jogador com ID:", id)



    def delete_player(self, id):
        # Excluir da tabela players_info
        query_info = text(f"""
        DELETE FROM players_info
        WHERE player_id = {id}
        """)
        with self.session() as session:
            session.execute(query_info)
            session.commit()
        # Excluir da tabela players_statics
        query_statics = text(f"""
        DELETE FROM players_statics
        WHERE player_id = {id}
        """)
        with self.session() as session:
            session.execute(query_info)
            session.commit()

        #print("Usuário com ID", id, "foi deletado com sucesso.")


    def insert_new_player(self, new_player_name, score_axis, score_allies):
        # Insere o novo jogador na tabela players_info
        query_info = text("""
        INSERT INTO players_info (player_nick) VALUES (:new_player_name)
        """)
        with self.session() as session:
            result = session.execute(query_info, {"new_player_name": new_player_name})
            player_id = result.lastrowid
            #print(f"NOVO ID DE JOGADOR: {player_id}")
            session.commit()

        # Insere as estatísticas do jogador na tabela players_statics
        query_statics = text("""
        INSERT INTO players_statics (player_id, score_axis, score_alies) VALUES (:player_id, :score_axis, :score_allies)
        """)
        with self.session() as session:
            session.execute(query_statics, {"player_id": player_id, "score_axis": score_axis, "score_allies": score_allies})
            session.commit()

        #print("Novo jogador inserido com sucesso!")

        # Retorna o ID do novo jogador
        return player_id


    def get_selected_players_data(self, selected_players_ids):
        # Lista para armazenar os dados dos jogadores selecionados
        selected_players_data = []

        # Consulta para obter os dados dos jogadores selecionados
        query = "SELECT players_info.player_nick, players_statics.score_axis, players_statics.score_alies FROM players_info INNER JOIN players_statics ON players_info.player_id = players_statics.player_id WHERE players_info.player_id IN (%s)" % ','.join(map(str, selected_players_ids))

        # Executar a consulta
        results = self.conn.query(query, ttl=600)
        results = results.values.tolist()

        # Processar os resultados e armazenar em uma lista de dicionários
        for row in results:
            player_data = {
                'name': row[0],
                'score_axis': row[1],
                'score_allies': row[2]
            }
            selected_players_data.append(player_data)

        return selected_players_data

    def reset(self):
        self.conn.reset()
        self.engine = create_engine('mysql://sql10699541:uD5suGjlyY@sql10.freesqldatabase.com/sql10699541')


    def __end__(self):
        self.conn.close()

if __name__ == '__main__':
    crud = playersCRUD()
    #print(crud.get_selected_players_data([1001, 1002]))