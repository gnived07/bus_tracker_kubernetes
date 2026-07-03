from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import random

app = Flask(__name__)
CORS(app)

DB_NAME = "buses.db"

# ---------------------------------
# DATABASE SETUP
# ---------------------------------

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route TEXT,
        status TEXT,
        eta TEXT,
        capacity TEXT
    )
    """)

    conn.commit()

    # Insert default buses if empty
    cursor.execute("SELECT COUNT(*) FROM buses")
    count = cursor.fetchone()[0]

    if count == 0:

        default_buses = [

            ("Karunagappally -> Amritapuri Campus",
             "On Time",
             "5 mins",
             "32/40"),

            ("Ochira -> Amritapuri Campus",
             "Delayed",
             "15 mins",
             "21/40"),

            ("Kayamkulam -> Amritapuri Campus",
             "Arriving",
             "1 min",
             "38/40")

        ]

        cursor.executemany("""
        INSERT INTO buses(route,status,eta,capacity)
        VALUES(?,?,?,?)
        """, default_buses)

        conn.commit()

    conn.close()

init_db()

# ---------------------------------
# GET ALL BUSES
# ---------------------------------

@app.route('/api/buses', methods=['GET'])
def get_buses():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM buses")

        rows = cursor.fetchall()

        conn.close()

        buses = []

        for row in rows:

            buses.append({
                "id": row[0],
                "route": row[1],
                "status": row[2],
                "eta": row[3],
                "capacity": row[4]
            })

        return jsonify(buses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------
# ADD BUS
# ---------------------------------

@app.route('/api/addbus', methods=['POST'])
def add_bus():
    try:
        data = request.json

        if not data or not all(k in data for k in ['route', 'status', 'eta', 'capacity']):
            return jsonify({"error": "Missing required fields"}), 400

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO buses(route,status,eta,capacity)
        VALUES(?,?,?,?)
        """, (

            data['route'],
            data['status'],
            data['eta'],
            data['capacity']

        ))

        conn.commit()
        bus_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "Bus added successfully",
            "bus_id": bus_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------
# UPDATE BUS
# ---------------------------------

@app.route('/api/updatebus/<int:bus_id>', methods=['PUT'])
def update_bus(bus_id):
    try:
        data = request.json

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Check if bus exists
        cursor.execute("SELECT * FROM buses WHERE id=?", (bus_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Bus not found"}), 404

        # Update only provided fields
        update_fields = []
        values = []

        if 'route' in data:
            update_fields.append("route=?")
            values.append(data['route'])
        if 'status' in data:
            update_fields.append("status=?")
            values.append(data['status'])
        if 'eta' in data:
            update_fields.append("eta=?")
            values.append(data['eta'])
        if 'capacity' in data:
            update_fields.append("capacity=?")
            values.append(data['capacity'])

        if not update_fields:
            conn.close()
            return jsonify({"error": "No fields to update"}), 400

        values.append(bus_id)
        query = f"UPDATE buses SET {', '.join(update_fields)} WHERE id=?"

        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Bus updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------
# DELETE BUS
# ---------------------------------

@app.route('/api/deletebus/<int:bus_id>', methods=['DELETE'])
def delete_bus(bus_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM buses WHERE id=?", (bus_id,))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Bus deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------
# STATS
# ---------------------------------

@app.route('/api/stats', methods=['GET'])
def stats():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM buses")
        total_buses = cursor.fetchone()[0]

        conn.close()

        return jsonify({

            "active_buses": total_buses,
            "students_tracking": random.randint(150, 400),
            "routes_online": total_buses

        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------
# ALERTS
# ---------------------------------

@app.route('/api/alerts', methods=['GET'])
def alerts():
    try:
        return jsonify([

            {"message": "⚠ Heavy rain near Kayamkulam"},
            {"message": "🚧 Traffic delay near Ochira"},
            {"message": "🚌 Extra buses added for evening rush"}

        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------
# HEALTH CHECK
# ---------------------------------

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"}), 200

# ---------------------------------
# MAIN
# ---------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)