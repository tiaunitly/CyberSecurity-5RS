import sqlite3

def get_db():
    conn = sqlite3.connect("library.db")
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Tabel buku
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year INTEGER
        )
    """)

    # Tabel peminjam
    cur.execute("""
        CREATE TABLE IF NOT EXISTS borrowers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            book_id INTEGER,
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)

    conn.commit()
    conn.close()
