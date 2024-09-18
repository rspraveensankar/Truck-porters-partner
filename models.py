import sqlite3

def create_db():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('porters.db')
    c = conn.cursor()

    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    name TEXT NOT NULL,
                    phno TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
    
    # Create Drivers table
    c.execute('''CREATE TABLE IF NOT EXISTS drivers (
                    name TEXT NOT NULL,
                    phno TEXT PRIMARY KEY,
                    age INTEGER,
                    licenseno TEXT,
                    yoe INTEGER,
                    bloodgroup VARCHAR(5),
                    password TEXT NOT NULL,
                    availability TEXT
                )''')
    
    # Create Vehicles table
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
    
    # Create Parcels table
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
    
    # Create Routes table
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

    # Check the tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    print("Tables in the database:", tables)
    #c.execute("ALTER TABLE parcels ADD COLUMN driver_phno TEXT;")
    # Fetch and display all rows from all tables
    for table in tables:
        table_name = table[0]
        print(f"\nData in the '{table_name}' table:")
        c.execute(f"SELECT * FROM {table_name};")
        rows = c.fetchall()
        for row in rows:
            print(row)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Call the function to create the database and tables
create_db()
