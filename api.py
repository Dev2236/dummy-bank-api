from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy in-memory "bank account"
account = {
    "balance": 1000  # starting balance
}

@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({"balance": account["balance"]})

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    amount = data.get("amount", 0)
    if amount <= 0:
        return jsonify({"error": "Deposit amount must be positive"}), 400
    
    account["balance"] += amount
    return jsonify({"message": f"Deposited {amount}", "balance": account["balance"]})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    amount = data.get("amount", 0)
    if amount <= 0:
        return jsonify({"error": "Withdrawal amount must be positive"}), 400
    
    if amount > account["balance"]:
        return jsonify({"error": "Insufficient funds"}), 400
    
    account["balance"] -= amount
    return jsonify({"message": f"Withdrew {amount}", "balance": account["balance"]})

if __name__ == "__main__":
    app.run(debug=True)

