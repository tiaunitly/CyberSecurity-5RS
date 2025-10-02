from flask import Flask, request, jsonify
from database import get_db, init_db
import os

# ❌ Hardcoded secret (bad practice)
API_KEY = "12345-SECRET-KEY"

app = Flask(__name__)

@app.route("/init")
def init():
    init_db()
    return "Database Initialized!"

@app.route("/add_book", methods=["POST"])
def add_book():
    conn = get_db()
    cur = conn.cursor()
    data = request.get_json()

    title = data.get("title")
    author = data.get("author")
    year = data.get("year")

    cur.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    return jsonify({"status": "Book added!"})

@app.route("/search")
def search():
    keyword = request.args.get("q", "")

    conn = get_db()
    cur = conn.cursor()

    # ❌ SQL Injection vulnerability (string concat, no parameter binding)
    query = f"SELECT * FROM books WHERE title LIKE '%{keyword}%'"
    cur.execute(query)
    results = cur.fetchall()

    return jsonify(results)

@app.route("/borrow", methods=["POST"])
def borrow():
    conn = get_db()
    cur = conn.cursor()
    data = request.get_json()

    name = data.get("name")
    book_id = data.get("book_id")

    cur.execute("INSERT INTO borrowers (name, book_id) VALUES (?, ?)", (name, book_id))
    conn.commit()
    return jsonify({"status": "Book borrowed!"})

@app.route("/export", methods=["POST"])
def export():
    data = request.get_json()
    filename = data.get("filename")

    # ❌ Path traversal vulnerability
    with open(filename, "w") as f:
        f.write("Dummy export data...")

    return jsonify({"status": f"Data exported to {filename}"})

if __name__ == "__main__":
    app.run(debug=True)
