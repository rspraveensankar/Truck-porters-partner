import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS drivers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS parcels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    driver_id INTEGER,
                    pickup_location TEXT,
                    dropoff_location TEXT,
                    status TEXT DEFAULT 'Pending',
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(driver_id) REFERENCES drivers(id)
                )''')

    conn.commit()
    conn.close()

create_db()