import subprocess
import mysql.connector
import configparser

class playersCRUD:
    def __init__(self):

        config = configparser.ConfigParser()
        config.read("./db_setup/config.cfg")
        params = config["mysql"]

        self.conn = mysql.connector.connect(
            host=params["host"],
            user=params["user"],
            password=params["password"],
            database='players'
        )
        self.cursor = self.conn.cursor()

    def get_all_players(self):
        query = """
            SELECT *
            FROM players_info
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        ret = [[j for j in i] for i in results]
        return ret

    def get_all_data(self):
        query = """
                select *
                from players_info as pi, players_statics as ps
                where pi.player_id = ps.player_id;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        ret = [[j for j in i] for i in results]
        return ret

    def get_players_names(self):
        query = """
        select player_nick
        from players_info
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        ret = [[j for j in i] for i in results]
        return ret

    def get_players_IDs(self):
        query = """
        select player_id
        from players_info
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        ret = [[j for j in i] for i in results]
        return ret
    
    def get_players_info(self):
        query = """
        select player_id, player_nick
        from players_info
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        player_info_dict = {id: nick for id, nick in results}
        return player_info_dict
    
    def get_players_score(self, id):
        query = f"""
        select score_axis, score_alies
        from players_statics
        where player_id = {id}
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [results[0][0], results[0][1]]
        return results
    
    def get_players_score_DF(self, id):
        query = f"""
        select score_axis, score_alies
        from players_statics
        where player_id = {id}
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def update_player_info(self, id, new_score_axis, new_score_allies, new_name):
        # Atualiza as estatísticas do jogador
        query = """
        UPDATE players_statics
        SET score_axis = %s, score_alies = %s
        WHERE player_id = %s
        """
        values = (new_score_axis, new_score_allies, id)
        self.cursor.execute(query, values)
        self.conn.commit()

        # Atualiza o nome do jogador
        query = """
        UPDATE players_info
        SET player_nick = %s
        WHERE player_id = %s
        """
        new_name_values = (new_name, id)
        self.cursor.execute(query, new_name_values)
        self.conn.commit()
        
        print("Infos atualizadas com sucesso para o jogador com ID:", id)

    
    def delete_player(self, id):
        # Excluir da tabela players_info
        query_info = """
        DELETE FROM players_info
        WHERE player_id = %s
        """
        self.cursor.execute(query_info, (id,))
        # Excluir da tabela players_statics
        query_statics = """
        DELETE FROM players_statics
        WHERE player_id = %s
        """
        self.cursor.execute(query_statics, (id,))
        
        self.conn.commit()
        print("Usuário com ID", id, "foi deletado com sucesso.")

    def insert_new_player(self, new_player_name, score_axis, score_allies):
        # Insere o novo jogador na tabela players_info
        insert_info_query = "INSERT INTO players_info (player_nick) VALUES (%s)"
        player_info_data = (new_player_name,)
        self.cursor.execute(insert_info_query, player_info_data)
        player_id = self.cursor.lastrowid

        # Insere as estatísticas do jogador na tabela players_statics
        insert_statics_query = "INSERT INTO players_statics (player_id, score_axis, score_alies) VALUES (%s, %s, %s)"
        statics_data = (player_id, score_axis, score_allies)
        self.cursor.execute(insert_statics_query, statics_data)

        # Commit para salvar as alterações
        self.conn.commit()

        print("Novo jogador inserido com sucesso!")

        # Retorna o ID do novo jogador
        return player_id


    def __end__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    crud = playersCRUD()
    crud.reset_db_from_script()