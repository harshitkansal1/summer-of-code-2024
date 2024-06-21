
from flask import current_app, g
import psycopg2

def get_db():
    if 'db_conn' not in g:
        db_config = current_app.config['DB_CONFIG']
        g.db_conn = psycopg2.connect(**db_config)
        g.db_cursor = g.db_conn.cursor()
    return g.db_cursor

def close_db(e=None):
    db_cursor = g.pop('db_cursor', None)
    db_conn = g.pop('db_conn', None)

    if db_cursor is not None:
        db_cursor.close()
    if db_conn is not None:
        db_conn.close()

def query_db(query, args=(), one=False):
    cursor = get_db()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    if one:
        return rv[0] if rv else None
    return rv