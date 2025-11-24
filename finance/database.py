# database.py
import sqlite3
from sqlite3 import Connection
import hashlib
from typing import List, Tuple, Optional

DB_PATH = "app.db"

def conectar() -> Connection:
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    # Usuários
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    );
    """)

    # Despesas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        categoria TEXT,
        data TEXT NOT NULL
    );
    """)

    # Entradas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS entradas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        categoria TEXT,
        data TEXT NOT NULL
    );
    """)
    conn.commit()

# -------------------------
# Usuários
# -------------------------
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def registrar_usuario(username: str, senha: str) -> bool:
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)",
                    (username, hash_senha(senha)))
        conn.commit()
        return True
    except Exception:
        return False

def autenticar_usuario(username: str, senha: str) -> bool:
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT senha FROM usuarios WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        return False
    return row[0] == hash_senha(senha)

# -------------------------
# Despesas CRUD
# -------------------------
def adicionar_despesa(usuario: str, descricao: str, valor: float, categoria: str, data: str):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO despesas (usuario, descricao, valor, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    """, (usuario, descricao, valor, categoria, data))
    conn.commit()

def listar_despesas(usuario: str) -> List[Tuple]:
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, descricao, valor, categoria, data
        FROM despesas
        WHERE usuario = ?
        ORDER BY date(data) DESC, id DESC
    """, (usuario,))
    return cur.fetchall()

def excluir_despesa(id_: int):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM despesas WHERE id = ?", (id_,))
    conn.commit()

def editar_despesa(id_: int, descricao: str, valor: float, categoria: str, data: str):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE despesas
        SET descricao = ?, valor = ?, categoria = ?, data = ?
        WHERE id = ?
    """, (descricao, valor, categoria, data, id_))
    conn.commit()

def adicionar_entrada(usuario: str, descricao: str, valor: float, categoria: str, data: str):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO entradas (usuario, descricao, valor, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    """, (usuario, descricao, valor, categoria, data))
    conn.commit()

def listar_entradas(usuario: str) -> List[Tuple]:
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, descricao, valor, categoria, data
        FROM entradas
        WHERE usuario = ?
        ORDER BY date(data) DESC, id DESC
    """, (usuario,))
    return cur.fetchall()

def excluir_entrada(id_: int):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM entradas WHERE id = ?", (id_,))
    conn.commit()

def editar_entrada(id_: int, descricao: str, valor: float, categoria: str, data: str):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE entradas
        SET descricao = ?, valor = ?, categoria = ?, data = ?
        WHERE id = ?
    """, (descricao, valor, categoria, data, id_))
    conn.commit()

# alias compatibilidade (alguns arquivos antigos usam validar_login)
def validar_login(username: str, senha: str) -> bool:
    """
    Alias para compatibilidade com código antigo que importava validar_login.
    """
    return autenticar_usuario(username, senha)


# Função opcional para deletar usuário (usada por configuracoes.py se preferir centralizar)
def excluir_usuario(username: str):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM despesas WHERE usuario = ?", (username,))
    cur.execute("DELETE FROM entradas WHERE usuario = ?", (username,))
    cur.execute("DELETE FROM usuarios WHERE username = ?", (username,))
    conn.commit()



def registrar_usuario(username, senha):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, senha))
        conn.commit()
        return True
    except Exception as e:
        print("Erro ao registrar:", e)
        return False
    finally:
        conn.close()

def autenticar_usuario(username, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND senha = ?", (username, senha))
    usuario = cursor.fetchone()

    conn.close()

    return usuario is not None

