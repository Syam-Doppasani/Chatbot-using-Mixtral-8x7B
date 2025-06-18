from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv("req.env")
HF_API_KEY = os.getenv("HF_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_prompt = request.json.get("prompt")
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": user_prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 150
        }
    }
    res = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
        headers=headers, json=payload
    )
    if res.status_code == 200:
        data = res.json()
        text = data[0]["generated_text"].replace(user_prompt, "").strip()
        return jsonify({"reply": text})
    else:
        return jsonify({"reply": f"Error: {res.status_code}"}), res.status_code

if __name__ == "__main__":
    app.run(debug=True)
