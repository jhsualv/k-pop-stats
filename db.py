# db.py
import psycopg
from psycopg.rows import dict_row

from config import DATABASE_URL

def get_connection():
    """Create and return a database connection. 
    The connection uses dict_row so the query results are returned as dictionaries instead of tuples.
    """
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)
   
def fetch_all(query, params=None, conn=None):
    """Execute a SELECT query and return all the rows as dictionaries.
    
    If a connection is provided, it is used directly and its lifetime
    remains the responsibility of the caller. Otherwise, a new connection
    is created for this query.
    """
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

def execute(query, params=None, conn=None):
    """Execute a query that doesn't return any rows.

    If a connection is provided, it is used directly and its lifetime
    remains the responsibility of the caller. Otherwise, a new connection
    is created for this query.
    
    Returns the number of rows affected.
    """
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.rowcount

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.rowcount