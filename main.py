import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
DB = "usuarios.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                senha TEXT PRIMARY KEY,
                imagem TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

def get_imagem(senha):
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT imagem FROM usuarios WHERE senha = ?", (senha,))
        row = c.fetchone()
        return row[0] if row else None

def add_usuario(senha, imagem):
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO usuarios (senha, imagem) VALUES (?, ?)", (senha, imagem))
        conn.commit()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form.get("senha")
        imagem = get_imagem(senha)
        if imagem:
            return redirect(url_for("mostrar_imagem", senha=senha))
        else:
            return render_template_string(PAGINA_LOGIN, erro="Senha inválida!")
    return render_template_string(PAGINA_LOGIN)

@app.route("/imagem/<senha>")
def mostrar_imagem(senha):
    imagem = get_imagem(senha)
    if imagem:
        return render_template_string(PAGINA_IMAGEM, imagem=imagem)
    return redirect(url_for("login"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        senha = request.form.get("senha")
        imagem = request.form.get("imagem")
        add_usuario(senha, imagem)
        return redirect(url_for("login"))
    return render_template_string(PAGINA_CADASTRO)

PAGINA_LOGIN = """
<h1>Login</h1>
<form method="POST">
  Senha: <input type="password" name="senha" required>
  <button type="submit">Entrar</button>
</form>
{% if erro %}<p style="color:red">{{ erro }}</p>{% endif %}
<a href="/cadastro">Cadastrar novo usuário</a>
"""

PAGINA_IMAGEM = """
<h1>Imagem Liberada ✅</h1>
<img src="{{ url_for('static', filename=imagem) }}" alt="Imagem" width="400">
<br><a href="/">Sair</a>
"""

PAGINA_CADASTRO = """
<h1>Cadastrar Novo Usuário</h1>
<form method="POST">
  Nova Senha: <input type="text" name="senha" required><br>
  Nome da Imagem (ex: gato.jpg): <input type="text" name="imagem" required><br>
  <button type="submit">Cadastrar</button>
</form>
<a href="/">Voltar</a>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
