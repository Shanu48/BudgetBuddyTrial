import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    # Expenses table
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    conn.commit()
    conn.close()

create_tables()
