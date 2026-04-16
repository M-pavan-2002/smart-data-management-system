from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection

app = Flask(__name__)
CORS(app)

# Create table
def create_table():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)
    db.commit()
    db.close()

create_table()

# Home route
@app.route('/')
def home():
    return "Backend Running Successfully ✅"

# Add user
@app.route('/add', methods=['POST'])
def add_user():
    data = request.json
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (data['email'],))
    if cursor.fetchone():
        db.close()
        return jsonify({"message": "Duplicate email found"}), 400

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (data['name'], data['email'])
    )
    db.commit()
    db.close()

    return jsonify({"message": "User added successfully"})

# Get users
@app.route('/get', methods=['GET'])
def get_users():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    result = []
    for user in users:
        result.append({
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        })

    db.close()
    return jsonify(result)

# Delete user
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    db.commit()
    db.close()

    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)