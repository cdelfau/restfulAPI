import os

# Generate and store secret key if it doesn't already exist
with open(".secret_key", "a+b") as f:
    key = f.read()
    if not key:
        key = os.urandom(64)
        f.write(key)
        f.flush()

SECRET_KEY = key

options = {
    "DATABASE": "database.db"
}

if os.path.exists(".env"):
    data = open(".env", "r")
    for line in data:
        if "=" in line:
            key = line.split("=")[0]
            value = line.split(key + "=")[1].strip("\n").strip("\r")
            options[key] = value
