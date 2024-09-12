from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Serve the index.html frontend
@app.route('/')
def index():
    return render_template('index.html')


# Connect to the database
def connect_db():
    return sqlite3.connect('database.db')


@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = connect_db()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists!"}), 400
    finally:
        conn.close()


@app.route('/register_driver', methods=['POST'])
def register_driver():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')

    conn = connect_db()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO drivers (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        return jsonify({"message": "Driver registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Phone number already exists!"}), 400
    finally:
        conn.close()


@app.route('/create_parcel', methods=['POST'])
def create_parcel():
    data = request.json
    user_id = data.get('user_id')
    driver_id = data.get('driver_id')
    pickup_location = data.get('pickup_location')
    dropoff_location = data.get('dropoff_location')

    conn = connect_db()
    c = conn.cursor()

    c.execute("""INSERT INTO parcels (user_id, driver_id, pickup_location, dropoff_location) 
                 VALUES (?, ?, ?, ?)""",
              (user_id, driver_id, pickup_location, dropoff_location))
    conn.commit()
    conn.close()

    return jsonify({"message": "Parcel created successfully!"}), 201


@app.route('/track_parcel/<int:parcel_id>', methods=['GET'])
def track_parcel(parcel_id):
    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT * FROM parcels WHERE id=?", (parcel_id,))
    parcel = c.fetchone()
    conn.close()

    if parcel:
        return jsonify({
            "parcel_id": parcel[0],
            "user_id": parcel[1],
            "driver_id": parcel[2],
            "pickup_location": parcel[3],
            "dropoff_location": parcel[4],
            "status": parcel[5]
        }), 200
    else:
        return jsonify({"message": "Parcel not found!"}), 404


if __name__ == '__main__':
    app.run(debug=True)