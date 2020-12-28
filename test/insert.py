import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_users(conn, user):
    sql = ''' INSERT INTO users(username,full_name,email,hashed_password,disabled)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def main():
    database = r"pythonsqlite.db"

    conn = create_connection(database)
    with conn:
        user1 = ('johndoe', 'John Doe', 'johndoe@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 0);

        create_users(conn, user1)

if __name__ == '__main__':
    main()
