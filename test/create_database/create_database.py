import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"pythonsqlite.db"

    sql_create_planos_table = """ CREATE TABLE IF NOT EXISTS planos (
                                        id integer PRIMARY KEY,
                                        descricao text NOT NULL,
                                        minutos integer NOT NULL
                                    ); """

    sql_create_tarifas_table = """CREATE TABLE IF NOT EXISTS tarifas (
                                    id integer PRIMARY KEY,
                                    origem text NOT NULL,
                                    destino text NOT NULL,
                                    valor float NOT NULL
                                );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_planos_table)

        create_table(conn, sql_create_tarifas_table)
    else:
        print("Erro! não foi possivel criar a conexão com o bd.")


if __name__ == '__main__':
    main()
