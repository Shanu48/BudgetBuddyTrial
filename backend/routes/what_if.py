import requests
from flask import Blueprint, request, jsonify
import sqlite3

what_if_routes = Blueprint('what_if_routes', __name__)

# Replace this with your actual AI proxy token
AIPROXY_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDQ5MDRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.1C8QpqZCx1Ik1aTaMlGHq26IJpupgdDAuOd1vEW7-_o'

@what_if_routes.route('/what_if', methods=['POST'])
def what_if():
    # Get the user question from the request
    user_question = request.json.get('question')
    user_id = request.json.get('user_id')  # Assuming you send user_id in the request

    if not user_question or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    # Fetch the user data from the database (transactions)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch transactions for the user
    cursor.execute(
        '''
        SELECT type, category, amount, description
        FROM transactions
        WHERE user_id = ?
        ''',
        (user_id,)
    )
    transactions = cursor.fetchall()
    conn.close()

    # Organize transactions by type (credit and debit)
    credit_transactions = [
        {"category": row[1], "amount": row[2], "description": row[3]}
        for row in transactions if row[0] == 'credit'
    ]
    debit_transactions = [
        {"category": row[1], "amount": row[2], "description": row[3]}
        for row in transactions if row[0] == 'debit'
    ]

    # Prepare the prompt for the AI model
    prompt = (
        f"User has the following financial data:\n\n"
        f"Credits: {credit_transactions}\n"
        f"Debits: {debit_transactions}\n\n"
        f"The user asks: {user_question}"
    )

    # Send the prompt to the AI proxy service
    ai_response = get_ai_response(prompt)

    # Return the response from the AI model
    return jsonify({"response": ai_response})

def get_ai_response(prompt):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"  # AI Proxy endpoint for chat completions
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",  # Model you want to use
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        # Assuming the response contains 'choices' which includes the AI response
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No response from AI')
    else:
        return f"Error: {response.status_code} - {response.text}"
