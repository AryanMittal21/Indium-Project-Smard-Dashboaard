# db_conn.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="database",
        user="postgres",
        password="root"
    )
