from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy in-memory database
accounts = {}
balances = {}
account_counter = 1000

@app.route("/open", methods=["POST"])
def open_account():
    global account_counter
    data = request.json
    acc_num = account_counter
    account_counter += 1

    # Save dummy data
    accounts[acc_num] = {
        "owner_name": data.get("name", "Unknown"),
        "birth_date": data.get("birth", ""),
        "address": data.get("address", ""),
        "phone_number": data.get("phone", ""),
        "email": data.get("email", ""),
        "account_type": data.get("type", "s")
    }
    balances[acc_num] = 0

    return jsonify({
        "message": "Account created successfully",
        "account_number": acc_num
    })

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.json
    acc_num = data["account_number"]
    amount = data["amount"]

    if acc_num not in accounts:
        return jsonify({"error": "Account not found"}), 404
    if amount < 0:
        return jsonify({"error": "Invalid amount"}), 400

    balances[acc_num] += amount
    return jsonify({"message": "Deposit successful", "balance": balances[acc_num]})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    acc_num = data["account_number"]
    amount = data["amount"]

    if acc_num not in accounts:
        return jsonify({"error": "Account not found"}), 404
    if amount < 0 or amount > balances[acc_num]:
        return jsonify({"error": "Insufficient balance"}), 400

    balances[acc_num] -= amount
    return jsonify({"message": "Withdrawal successful", "balance": balances[acc_num]})

@app.route("/account/<int:acc_num>", methods=["GET"])
def get_account(acc_num):
    if acc_num not in accounts:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "account_number": acc_num,
        **accounts[acc_num],
        "balance": balances[acc_num]
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
