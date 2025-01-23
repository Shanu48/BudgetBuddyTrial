import requests
from flask import Blueprint, request, jsonify
import sqlite3

goals_routes = Blueprint('goals_routes', __name__)

# Replace this with your actual AI proxy token
AIPROXY_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDQ5MDRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.1C8QpqZCx1Ik1aTaMlGHq26IJpupgdDAuOd1vEW7-_o'

@goals_routes.route('/set_goal', methods=['POST'])
def set_goal():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    target_amount = data.get('target_amount')
    deadline = data.get('deadline')
    description = data.get('description', '')

    if not user_id or not name or not target_amount or not deadline:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO goals (user_id, name, target_amount, deadline, description) VALUES (?, ?, ?, ?, ?)',
        (user_id, name, target_amount, deadline, description)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Goal added successfully!'}), 201


@goals_routes.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id parameter'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch user data
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "debit"', (user_id,))
    total_expenses = cursor.fetchone()[0] or 0

    cursor.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "credit"', (user_id,))
    total_income = cursor.fetchone()[0] or 0

    cursor.execute('SELECT * FROM goals WHERE user_id = ?', (user_id,))
    goals = cursor.fetchall()

    conn.close()

    # Generate recommendations
    recommendations = []
    for goal in goals:
        goal_name, target, current, deadline = goal[1], goal[2], goal[3], goal[4]
        remaining = target - current
        months_remaining = (datetime.strptime(deadline, "%Y-%m-%d") - datetime.now()).days // 30

        if months_remaining > 0:
            monthly_saving = remaining / months_remaining
            recommendations.append(
                f"Save ₹{monthly_saving:.2f} per month to achieve your goal '{goal_name}' by {deadline}."
            )
        else:
            recommendations.append(
                f"Goal '{goal_name}' is past its deadline. Consider revising the target or deadline."
            )

    return jsonify({'recommendations': recommendations})

