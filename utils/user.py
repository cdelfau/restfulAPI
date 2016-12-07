import sqlite3
import hashlib

DATABASE = "database.db"

def get_user(**kwargs):
    if not kwargs:
        return None

    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    criterion = []
    params = []
    for k,v in kwargs.items():
        criterion.append("%s = ?" % k)
        params.append(str(v))

    query = "SELECT * FROM users WHERE %s" % " AND ".join(criterion)
    c.execute(query, params)

    result = c.fetchone()
    db.close()
    return result

def add_user(username, password, zip_code):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    password = hashlib.sha256(password).hexdigest()

    query = "INSERT INTO users VALUES (NULL, ?, ?, ?)"
    c.execute(query, (username, password, zip_code,))
    db.commit()
    db.close()
