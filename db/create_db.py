import sqlite3

def db_create():
    conn = sqlite3.connect("expences.db")
    cur = conn.cursor()



