import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_planos(conn, plano):
    sql = ''' INSERT INTO planos(descricao,minutos)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, plano)
    return cur.lastrowid


def create_tarifas(conn, tarifa):
    sql = ''' INSERT INTO tarifas(origem,destino,valor)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, tarifa)
    return cur.lastrowid


def main():
    database = r"pythonsqlite.db"

    conn = create_connection(database)
    with conn:
        plano1 = ('Fale mais 30', 30);
        plano2 = ('Fale mais 60', 60);
        plano3 = ('Fale mais 120', 120);

        create_planos(conn, plano1)
        create_planos(conn, plano2)
        create_planos(conn, plano3)

        tarifa1 = ('011', '016', 1.90)
        tarifa2 = ('016', '011', 2.90)
        tarifa3 = ('011', '017', 1.70)
        tarifa4 = ('017', '011', 2.70)
        tarifa5 = ('011', '018', 0.90)
        tarifa6 = ('018', '011', 1.90)

        create_tarifas(conn, tarifa1)
        create_tarifas(conn, tarifa2)
        create_tarifas(conn, tarifa3)
        create_tarifas(conn, tarifa4)
        create_tarifas(conn, tarifa5)
        create_tarifas(conn, tarifa6)

if __name__ == '__main__':
    main()
