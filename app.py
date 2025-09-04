
from flask import Flask, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app, origins=["chrome-extension://fonpmnbkodmahnnjejckklifbfkejona"])

# Placeholder CLIENT_ID
CLIENT_ID = "691619432775-88lo1pq7oakt87hi5vc5mhc6p01lgs3n.apps.googleusercontent.com"

@app.route('/get-config', methods=['POST'])
def get_config():
    data = request.get_json()
    if not data or 'idToken' not in data:
        return jsonify({'error': 'Missing idToken'}), 400
    token = data['idToken']
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
        email = idinfo.get('email')
        if not email:
            return jsonify({'error': 'Email not found in token'}), 401
        # Send secret JSON from .env if authenticated
        secret_json = os.getenv('SECRET_JSON')
        if not secret_json:
            return jsonify({'error': 'Secret not configured'}), 500
        return jsonify(json.loads(secret_json)), 200
    except Exception:
        return jsonify({'error': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(port=3000)
