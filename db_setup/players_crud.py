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
        return results


    def __end__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    crud = playersCRUD()
    print(crud.get_players_score('1001'))
