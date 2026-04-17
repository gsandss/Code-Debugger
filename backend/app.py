from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os
import requests

app = Flask(__name__)
CORS(app)

LM_STUDIO_API = "http://127.0.0.1:1234/v1/chat/completions"
LM_STUDIO_MODEL = "essentialai/rnj-1" 

def query_lm_studio(prompt):
    payload ={
        "model": LM_STUDIO_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful Python debugging assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post(LM_STUDIO_API, json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()

def analyze_error(error_message):
    prompt = f"""
Explain this Python error clearly in simple terms.
Then suggest how to fix it.

Error:
{error_message}
"""
    return query_lm_studio(prompt)

@app.route("/")
def home():
    return "Backend is running."


@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data.get("code", "")

    if not code.strip():
        return jsonify({"success": False, "error": "No code provided."}), 400

    temp_file = "temp_code.py"

    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return jsonify({
                "success": True,
                "output": result.stdout
            })

        error_message = result.stderr

        try:
            ai_explanation = analyze_error(error_message)
        except Exception as e:
            ai_explanation = f"Could not get AI explanation: {e}"

        return jsonify({
            "success": False,
            "error": error_message,
            "ai_explanation": ai_explanation
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": "Code execution timed out."
        }), 408

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected server error: {str(e)}"
        }), 500

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@app.route("/ask", methods=["POST"])
def ask_about_code():
    data = request.get_json()
    code = data.get("code", "")
    question = data.get("question", "")

    if not code.strip() or not question.strip():
        return jsonify({
            "success": False,
            "error": "Code and question are required."
        }), 400

    prompt = f"""
Here is some Python code:

{code}

Answer this question about the code:
{question}
"""

    try:
        answer = query_lm_studio(prompt)
        return jsonify({
            "success": True,
            "answer": answer
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Could not get answer from AI: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)