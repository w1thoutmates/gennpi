import sqlite3
from cryptography.fernet import Fernet
import os
import appdirs

appname = "gennpi-v1.1"
appauthor = "gennpi"
data_dir = appdirs.user_data_dir(appname, appauthor)
os.makedirs(data_dir, exist_ok=True)

DB_FILE = os.path.join(data_dir, 'passwords.db')
KEY_FILE = os.path.join(data_dir, 'encryption_key.key')

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def create_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            encrypted_password TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

create_tables()