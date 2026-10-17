
from flask import Flask, request, render_template_string

app = Flask(__name__)

login_attempts = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AuthShield Dashboard</title>
    <style>
        body {
            background: #101827;
            color: white;
            font-family: Arial, sans-serif;
            padding: 35px;
        }
        .card {
            background: #1e293b;
            padding: 25px;
            border-radius: 12px;
            max-width: 650px;
            margin: auto;
        }
        input, button {
            padding: 12px;
            margin: 6px 0;
            width: 95%;
            border-radius: 6px;
            border: none;
        }
        button {
            background: #38bdf8;
            cursor: pointer;
            font-weight: bold;
        }
        .result { margin-top: 20px; padding: 15px; background: #334155; }
    </style>
</head>
<body>
<div class="card">
    <h1>AuthShield</h1>
    <p>AI-assisted Suspicious Login Monitoring</p>
    <form method="POST" action="/login-check">
        <label>Username</label>
        <input name="username" required placeholder="Enter test username">
        <label>Failed login attempts</label>
        <input name="attempts" type="number" min="0" required placeholder="e.g. 5">
        <label>Unfamiliar device?</label>
        <select name="device">
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select>
        <button type="submit">Analyze Login</button>
    </form>
    {% if result %}
    <div class="result">
        <h2>{{ result.level }}</h2>
        <p>{{ result.message }}</p>
        <p>Risk score: {{ result.score }}/100</p>
    </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, result=None)

@app.route("/login-check", methods=["POST"])
def login_check():
    username = request.form["username"].strip()
    attempts = int(request.form["attempts"])
    unfamiliar = request.form["device"] == "yes"

    score = min(attempts * 10, 70)
    if unfamiliar:
        score += 30

    if score >= 60:
        level = "HIGH RISK"
        message = f"Alert: Suspicious login activity detected for {username}."
    elif score >= 30:
        level = "MEDIUM RISK"
        message = f"Warning: Review the login activity for {username}."
    else:
        level = "LOW RISK"
        message = f"No major warning signs in this test for {username}."

    result = {"level": level, "message": message, "score": score}
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
