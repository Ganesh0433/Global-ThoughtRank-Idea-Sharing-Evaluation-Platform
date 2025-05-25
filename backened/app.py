from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_handler import evaluate_with_gemini
import os
from evaluate_controller import evaluate_idea_pipeline

app = Flask(__name__)
CORS(app, resources={r"/evaluate": {"origins": "http://localhost:3000"}}) # Allow frontend requests

@app.route('/evaluate', methods=['POST'])
def evaluate_idea():
    data = request.json
    user_text = data.get('text', '').strip()
    user_id = data.get('user_id')  # optional

    if not user_text:
        return jsonify({"error": "Text cannot be empty"}), 400

    try:
        result = evaluate_idea_pipeline(user_text, user_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
