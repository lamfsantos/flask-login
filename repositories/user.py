import sqlite3
from sqlite3 import Error

database = r"pythonsqlite.db"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def find_all():
    conn = create_connection(database)

    cur = conn.cursor()
    cur.execute("SELECT username, full_name, email, hashed_password, disabled FROM users")

    rows = cur.fetchall()

    conn.close()

    return rows

def find_by_username(username):
    conn = create_connection(database)

    cur = conn.cursor()
    cur.execute("SELECT username, full_name, email, hashed_password, disabled FROM users where username = ?", (username, ))

    rows = cur.fetchall()

    conn.close()

    return rows

def insert(username: str, password: str, email: str, full_name: str):
    conn = create_connection(database)

    sql = ''' INSERT INTO users(username,full_name,email,hashed_password,disabled)
              VALUES(?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, (username, full_name, email, password, 0, ))
    conn.commit()
    return cur.lastrowid
