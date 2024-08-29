import sqlite3

def init_db():
    conn = sqlite3.connect('capsule_time.db')  # Создаем/подключаем к базе данных
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS letters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        letter TEXT NOT NULL
    )
    ''')
    conn.commit()
    return conn

def save_letter(name, letter):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO letters (name, letter) VALUES (?, ?)', (name, letter))
    conn.commit()
    conn.close()

def fetch_all_letters():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM letters')
    letters = cursor.fetchall()
    conn.close()
    return letters