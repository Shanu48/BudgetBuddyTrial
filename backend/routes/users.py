from flask import Blueprint, request, jsonify
import sqlite3

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400
    finally:
        conn.close()

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, email FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful', 'user': {'id': user[0], 'name': user[1], 'email': user[2]}})
    return jsonify({'error': 'Invalid credentials'}), 401
