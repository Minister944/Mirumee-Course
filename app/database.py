import sqlite3
from contextlib import contextmanager

import os

path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'file.db')

@contextmanager
def connection():
    conn =sqlite3.connect(db)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()

@contextmanager
def cursor():
    with connection() as conn:
        cur = conn.cursor()
        try:
            yield cur
        finally:
            cur.close()