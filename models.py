import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    name TEXT NOT NULL,
                    phno TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
    
    # Drivers table
    c.execute('''CREATE TABLE IF NOT EXISTS drivers (
                    name TEXT NOT NULL,
                    phno TEXT PRIMARY KEY,
                    age INTEGER,
                    licenseno TEXT,
                    yoe INTEGER,
                    bloodgroup VARCHAR(5),
                    password TEXT NOT NULL
                )''')
    
    # Vehicles table
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    vehicleno TEXT UNIQUE,
                    weight INTEGER,
                    height INTEGER,
                    length INTEGER,
                    width INTEGER,
                    driver_phno TEXT,
                    FOREIGN KEY(driver_phno) REFERENCES drivers(phno)
                )''')
    
    # Parcels table
    c.execute('''CREATE TABLE IF NOT EXISTS parcels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    weight INTEGER,
                    height INTEGER,
                    length INTEGER,
                    width INTEGER,
                    dphno TEXT,
                    uphno TEXT,
                    pickup_location TEXT,
                    dropoff_location TEXT,
                    pickupzipcode INTEGER,
                    dropzipcode INTEGER,
                    status TEXT DEFAULT 'Pending',
                    FOREIGN KEY(uphno) REFERENCES users(phno),
                    FOREIGN KEY(dphno) REFERENCES drivers(phno)
                )''')
    
    # Routes table
    c.execute('''CREATE TABLE IF NOT EXISTS route (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pickupcode INTEGER,
                    dropcode INTEGER,
                    pickup_location TEXT,
                    dropoff_location TEXT,
                    zipcodes TEXT,
                    driver_phno TEXT,
                    FOREIGN KEY(driver_phno) REFERENCES drivers(phno)
                )''')
    
    conn.commit()
    conn.close()