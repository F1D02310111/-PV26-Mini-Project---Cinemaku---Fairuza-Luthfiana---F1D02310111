import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bioskop.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS film (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            genre TEXT NOT NULL,
            sutradara TEXT NOT NULL,
            tahun INTEGER NOT NULL,
            rating TEXT NOT NULL,
            catatan TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_all_films():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM film ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_film(judul, genre, sutradara, tahun, rating, catatan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO film (judul, genre, sutradara, tahun, rating, catatan) VALUES (?, ?, ?, ?, ?, ?)",
        (judul, genre, sutradara, tahun, rating, catatan)
    )
    conn.commit()
    conn.close()

def update_film(id, judul, genre, sutradara, tahun, rating, catatan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE film SET judul=?, genre=?, sutradara=?, tahun=?, rating=?, catatan=? WHERE id=?",
        (judul, genre, sutradara, tahun, rating, catatan, id)
    )
    conn.commit()
    conn.close()

def delete_film(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM film WHERE id=?", (id,))
    conn.commit()
    conn.close()
