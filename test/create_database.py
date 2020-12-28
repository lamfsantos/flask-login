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

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        full_name text NOT NULL,
                                        email text NOT NULL,
                                        hashed_password text NOT NULL,
                                        disabled BOOLEAN NOT NULL CHECK (disabled IN (0,1))
                                    ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_users_table)

    else:
        print("Erro! não foi possivel criar a conexão com o bd.")


if __name__ == '__main__':
    main()
