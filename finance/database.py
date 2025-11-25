import sqlite3
import os

# Caminho absoluto do banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            senha TEXT
        )
    """)
    conn.commit()
    conn.close()

def registrar_usuario(usuario, senha):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def validar_login(usuario, senha):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    user = cur.fetchone()
    conn.close()
    return user
