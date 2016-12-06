import sqlite3
import hashlib

def get_user(username):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    query = "SELECT * FROM users WHERE username = ?"
    c.execute(query, (username,))
    result = c.fetchone()
    return result


def add_user(username, password):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    password = hashlib.sha256(password).hexdigest()

    query = "INSERT INTO users VALUES (NULL, ?, ?, NULL)"
    c.execute(query, (username, password,))
    db.commit()
    db.close()
