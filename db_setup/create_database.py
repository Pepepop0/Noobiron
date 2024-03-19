import mysql.connector
from mysql.connector import Error
import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read("db_setup\config.cfg")
    return config["mysql"]

def connect():
    config = read_config()
    try:
        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"]
        )
        if connection.is_connected():
            print("Conexão ao MySQL bem-sucedida.")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def schema_exists(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    for database in databases:
        if 'players' in database:
            print("Database encontrado.")
            return True
    return False

def create_schema(connection):
    try:
        with open("./db_setup/create_schema.sql", "r") as file:
            sql_script = file.read()
            cursor = connection.cursor()
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            # Triger de insterção de ID removido  
            connection.commit()
            cursor.close()
        print("Schema do banco de dados criado com sucesso.")
    except Error as e:
        print(f"Erro ao criar schema do banco de dados: {e}")

def main(force_create=False):
    connection = connect()
    if connection:
        if not schema_exists(connection) or force_create:
            create_schema(connection)
        else:
            print("O esquema 'housing' já existe.")
        connection.close()
        print("Conexão ao MySQL fechada.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--force_create', action='store_true', help='Forçar a criação do esquema')
    args = parser.parse_args()
    main(args.force_create)