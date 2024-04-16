import streamlit as st
import pandas as pd


class playersCRUD:
    def __init__(self):

        self.conn = st.connection('mysql', type='sql')

    def get_all_players(self):
        query = """
            SELECT player_id, player_nick
            FROM players_info
        """
        results = self.conn.query(query, ttl=600)
        print("get_all_players:\n", results)
        player_list = results.values.tolist()
        print(player_list)
        return player_list


    def get_all_data(self):
        query = """
                select *
                from players_info as pi, players_statics as ps
                where pi.player_id = ps.player_id;
        """
        results = self.conn.query(query, ttl=600)
        print("get_all_data:\n", results.values.tolist())
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


    def __end__(self):
        self.conn.close()

if __name__ == '__main__':
    crud = playersCRUD()
    print(crud.get_selected_players_data([1001, 1002]))