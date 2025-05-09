from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
WALLET_SESSION_FILE = "wallet_session.json"
STREAMLIT_URL = "https://aiverseweb-fd9b9idf9ede7rqvzn3dkd.streamlit.app/"

@app.route("/wallet-login", methods=["POST"])
def wallet_login():
    data = request.get_json()
    wallet_address = data.get("wallet")
    
    if wallet_address:
        with open(WALLET_SESSION_FILE, "w") as f:
            json.dump({"wallet": wallet_address}, f)
        return jsonify({"status": "success", "redirect": STREAMLIT_URL})
    else:
        return jsonify({"status": "failed", "error": "No wallet provided"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
