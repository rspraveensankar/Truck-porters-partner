import streamlit as st
import sqlite3
import bcrypt
import re
import time

# Initialize session state for tracking user or driver
if 'role' not in st.session_state:
    st.session_state.role = None  # Can be 'user' or 'driver'
if 'login_time' not in st.session_state:
    st.session_state.login_time = None

# Database connection
def connect_db():
    return sqlite3.connect('database.db')

# Password handling and validation
def simple_password_check(password):
    if len(password) < 6 or len(password) > 20:
        return "Invalid Password! Length should be between 6 and 20 characters.", False
    if not any(char.isupper() for char in password):
        return "Invalid Password! Should contain at least one uppercase letter.", False
    if not any(char.islower() for char in password):
        return "Invalid Password! Should contain at least one lowercase letter.", False
    if not any(char.isdigit() for char in password):
        return "Invalid Password! Should contain at least one digit.", False
    return "Password is valid.", True

def validate_phone_number(phno):
    if re.fullmatch(r"[6-9]\d{9}", phno):
        return True
    else:
        st.error("Invalid phone number! Please enter a valid 10-digit phone number starting with 6-9.")
        return False

def validate_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(pattern, email):
        return True
    else:
        st.error("Invalid email address!")
        return False

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Session timeout
def check_timeout():
    if st.session_state.login_time and (time.time() - st.session_state.login_time > 3600):  # 1 hour timeout
        st.session_state.role = None
        st.warning("Session timed out. Please log in again.")
        
def login_successful(role, phno):
    st.session_state.role = role
    st.session_state.phno = phno
    st.session_state.login_time = time.time()
    st.success(f"{role.capitalize()} login successful!")

# User Registration
def register_user():
    st.title("Register User")
    name = st.text_input("Name")
    phno = st.text_input("Phone Number")
    email = st.text_input("Email")
    address = st.text_area("Address")
    password = st.text_input("Password", type='password')

    if st.button("Register"):
        if validate_phone_number(phno) and validate_email(email):
            a, b = simple_password_check(password)
            if not b:
                st.error(a)
            else:
                hashed_password = hash_password(password)
                conn = connect_db()
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO users (name, phno, email, address, password) VALUES (?, ?, ?, ?, ?)", 
                              (name, phno, email, address, hashed_password))
                    conn.commit()
                    st.success("User registered successfully!")
                    login_user()
                except sqlite3.IntegrityError:
                    st.error("User already exists!")
                finally:
                    conn.close()

# Driver Registration
def register_driver():
    st.title("Register Driver")
    name = st.text_input("Name")
    phno = st.text_input("Phone Number")
    age = st.number_input("Age", min_value=18, max_value=99)
    licenseno = st.text_input("License Number")
    yoe = st.number_input("Years of Experience", min_value=0, max_value=50)
    bloodgroup = st.text_input("Blood Group")
    password = st.text_input("Password", type='password')

    if st.button("Register Driver"):
        if validate_phone_number(phno):
            a, b = simple_password_check(password)
            if not b:
                st.error(a)
            else:
                hashed_password = hash_password(password)
                conn = connect_db()
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO drivers (name, phno, age, licenseno, yoe, bloodgroup, password) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                              (name, phno, age, licenseno, yoe, bloodgroup, hashed_password))
                    conn.commit()
                    st.success("Driver registered successfully!")
                    login_driver()
                except sqlite3.IntegrityError:
                    st.error("Phone number already exists!")
                finally:
                    conn.close()

# User login
def login_user():
    st.title("User Login")
    phno = st.text_input("Phone Number", key="user_phno")
    password = st.text_input("Password", type='password', key="user_password")

    if st.button("Login as User"):
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE phno=?", (phno,))
        user = c.fetchone()
        conn.close()

        if user:
            hashed_password = user[0]
            if check_password(hashed_password, password):
                login_successful('user', phno)
            else:
                st.error("Wrong Password!")
        else:
            st.error("User does not exist!")

# Driver login
def login_driver():
    st.title("Driver Login")
    phno = st.text_input("Phone Number", key="driver_phno")
    password = st.text_input("Password", type='password', key="driver_password")

    if st.button("Login as Driver"):
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT password FROM drivers WHERE phno=?", (phno,))
        driver = c.fetchone()
        conn.close()

        if driver:
            hashed_password = driver[0]
            if check_password(hashed_password, password):
                login_successful('driver', phno)
            else:
                st.error("Wrong Password!")
        else:
            st.error("Driver does not exist!")

# Add parcel for users
def add_parcel():
    st.title("Add Parcel")
    weight = st.number_input("Weight (kg)", min_value=0.0)
    height = st.number_input("Height (cm)")
    length = st.number_input("Length (cm)")
    width = st.number_input("Width (cm)")
    pickup_location = st.text_input("Pickup Location")
    dropoff_location = st.text_input("Dropoff Location")
    pickupzipcode = st.text_input("Pickup Zipcode")
    dropzipcode = st.text_input("Dropoff Zipcode")

    if st.button("Submit Parcel"):
        if all([weight, height, length, width, pickup_location, dropoff_location, pickupzipcode, dropzipcode]):
            conn = connect_db()
            c = conn.cursor()
            c.execute("""INSERT INTO parcels (weight, height, length, width, uphno, pickup_location, dropoff_location, pickupzipcode, dropzipcode) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (weight, height, length, width, st.session_state.phno, pickup_location, dropoff_location, pickupzipcode, dropzipcode))
            conn.commit()
            c.execute("SELECT id FROM parcels WHERE uphno=?", (st.session_state.phno,))
            parcel_id = c.fetchone()[0]
            conn.close()
            st.success(f"Parcel created successfully! Parcel ID: {parcel_id}")
            st.info(f"Details: {weight} kg, {length}x{width}x{height} cm, Pickup: {pickup_location} - {pickupzipcode}, Dropoff: {dropoff_location} - {dropzipcode}")
        else:
            st.error("Please fill in all the required fields.")

# Add route for drivers
def add_route():
    st.title("Add Route")
    pickupcode = st.text_input("Pickup Code")
    dropcode = st.text_input("Drop Code")
    pickup_location = st.text_input("Pickup Location")
    dropoff_location = st.text_input("Dropoff Location")
    zipcodes = st.text_input("Zip Codes covered (comma separated)")

    if st.button("Submit Route"):
        if all([pickupcode, dropcode, pickup_location, dropoff_location, zipcodes]):
            conn = connect_db()
            c = conn.cursor()
            c.execute("""INSERT INTO route (pickupcode, dropcode, pickup_location, dropoff_location, zipcodes, phno) 
                         VALUES (?, ?, ?, ?, ?, ?)""",
                      (pickupcode, dropcode, pickup_location, dropoff_location, zipcodes, st.session_state.phno))
            conn.commit()
            conn.close()
            st.success("Route added successfully!")
        else:
            st.error("Please fill in all the required fields.")

# Driver Availability
def toggle_availability():
    st.title("Driver Availability")
    availability = st.radio("Availability", ["Available", "Unavailable"])
    if st.button("Update Availability"):
        conn = connect_db()
        c = conn.cursor()
        c.execute("UPDATE drivers SET availability=? WHERE phno=?", (availability, st.session_state.phno))
        conn.commit()
        conn.close()
        st.success(f"Availability updated to {availability}")

# Search for Routes
def search_routes():
    st.title("Search Routes")
    zipcode = st.text_input("Enter a zip code to find available routes:")
    if st.button("Search"):
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM route WHERE zipcodes LIKE ?", (f"%{zipcode}%",))
        routes = c.fetchall()
        conn.close()
        if routes:
            for route in routes:
                st.write(f"Route ID: {route[0]}, Pickup: {route[1]}, Dropoff: {route[2]}, Covered Zipcodes: {route[4]}")
        else:
            st.error("No routes found for the given zip code.")

# Check parcel status
def check_parcel_status():
    st.title("Check Parcel Status")
    parcel_id = st.text_input("Enter Parcel ID")
    if st.button("Check Status"):
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT status FROM parcels WHERE id=?", (parcel_id,))
        status = c.fetchone()
        conn.close()
        if status:
            st.write(f"Parcel Status: {status[0]}")
        else:
            st.error("Parcel not found!")

# Main app logic
def main():
    st.sidebar.title("TRUCK PORTERS PARTNER")
    
    # Check for session timeout
    check_timeout()

    if st.session_state.role == 'user':
        st.sidebar.success(f"Logged in as User: {st.session_state.phno}")
        add_parcel()
        check_parcel_status()

    elif st.session_state.role == 'driver':
        st.sidebar.success(f"Logged in as Driver: {st.session_state.phno}")
        add_route()
        toggle_availability()
        search_routes()

    else:
        user_option = st.sidebar.radio("Login/Register", ["User Login", "Driver Login", "User Registration", "Driver Registration"])

        if user_option == "User Login":
            login_user()
        elif user_option == "Driver Login":
            login_driver()
        elif user_option == "User Registration":
            register_user()
        elif user_option == "Driver Registration":
            register_driver()

if __name__ == "__main__":
    main()
