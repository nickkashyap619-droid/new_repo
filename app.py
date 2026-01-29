from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY, text TEXT, author TEXT)")
    # Add one starter quote if empty
    cursor.execute("SELECT COUNT(*) FROM quotes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO quotes (text, author) VALUES (?, ?)", ("Keep coding!", "Gemini"))
    conn.commit()
    conn.close()

init_db()

# --- HTML TEMPLATE (Embedded for simplicity) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Quote Cloud</title>
    <style>
        body { font-family: sans-serif; text-align: center; background: #f0f2f5; padding: 50px; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }
        input { padding: 10px; margin: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🌟 Community Quotes</h1>
    <form action="/add" method="POST">
        <input type="text" name="quote" placeholder="Enter quote" required>
        <input type="text" name="author" placeholder="Author" required>
        <button type="submit">Share Quote</button>
    </form>
    <hr>
    {% for q in quotes %}
        <div class="card">
            <p>"{{ q[1] }}"</p>
            <strong>- {{ q[2] }}</strong>
        </div><br><br>
    {% endfor %}
</body>
</html>
"""

# --- ROUTES ---
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.fetchall()
    cursor = conn.execute("SELECT * FROM quotes ORDER BY id DESC")
    quotes = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, quotes=quotes)

@app.route("/add", methods=["POST"])
def add_quote():
    text = request.form.get("quote")
    author = request.form.get("author")
    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO quotes (text, author) VALUES (?, ?)", (text, author))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)