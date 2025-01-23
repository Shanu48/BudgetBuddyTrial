from flask import Blueprint, request, jsonify
import sqlite3

transactions_routes = Blueprint('transactions_routes', __name__)

@transactions_routes.route('/add_transaction', methods=['POST'])
def add_transaction():
    # Parse request data
    data = request.json
    user_id = data.get('user_id')
    transaction_type = data.get('type')  # 'credit' or 'debit'
    category = data.get('category')
    amount = data.get('amount')
    description = data.get('description', '')

    # Validate the inputs
    if transaction_type not in ('credit', 'debit'):
        return jsonify({"error": "Invalid transaction type. Must be 'credit' or 'debit'"}), 400

    if not user_id or not category or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    # Insert into the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO transactions (user_id, type, category, amount, description) VALUES (?, ?, ?, ?, ?)',
        (user_id, transaction_type, category, amount, description)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"{transaction_type.capitalize()} transaction added successfully!"})

@transactions_routes.route('/get_balance', methods=['GET'])
def get_balance():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT 
            SUM(CASE WHEN type = 'credit' THEN amount ELSE 0 END) -
            SUM(CASE WHEN type = 'debit' THEN amount ELSE 0 END)
        AS balance
        FROM transactions
        WHERE user_id = ?
        ''',
        (user_id,)
    )
    balance = cursor.fetchone()[0] or 0  # Default to 0 if no transactions found
    conn.close()

    return jsonify({"current_balance": f"{balance:.2f}"})

