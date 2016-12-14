import sqlite3

def initialize_tables():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER primary key, username TEXT, password TEXT, zip_code INTEGER, subway INTEGER, bus INTEGER, busnum TEXT, lirr INTEGER)")

    db.commit()
    db.close()
