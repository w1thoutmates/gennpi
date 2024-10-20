from database import create_connection, encrypt_password, decrypt_password

def save_password(user_id, password):
    conn = create_connection()
    cursor = conn.cursor()
    encrypted_password = encrypt_password(password)
    cursor.execute("INSERT INTO passwords (user_id, encrypted_password) VALUES (?, ?)", (user_id, encrypted_password))
    conn.commit()
    conn.close()

def get_passwords(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_password FROM passwords WHERE user_id = ?", (user_id,))
    encrypted_passwords = cursor.fetchall()
    conn.close()
    return [decrypt_password(pw[0]) for pw in encrypted_passwords]