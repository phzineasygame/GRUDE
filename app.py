from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "chave-secreta"

DATABASE = "alunos.db"


def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            curso TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# READ - Listar alunos
@app.route("/")
def index():
    conexao = conectar_banco()

    alunos = conexao.execute(
        "SELECT * FROM alunos ORDER BY id DESC"
    ).fetchall()

    conexao.close()

    return render_template("index.html", alunos=alunos)


# CREATE - Formulário de cadastro
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        curso = request.form["curso"]

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO alunos (nome, cpf, email, telefone, curso)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, cpf, email, telefone, curso))

        conexao.commit()
        conexao.close()

        flash("Aluno cadastrado com sucesso!")

        return redirect(url_for("index"))

    return render_template("cadastrar.html")


# UPDATE - Editar aluno
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexao = conectar_banco()

    aluno = conexao.execute(
        "SELECT * FROM alunos WHERE id = ?",
        (id,)
    ).fetchone()

    if aluno is None:
        conexao.close()
        flash("Aluno não encontrado.")
        return redirect(url_for("index"))

    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        curso = request.form["curso"]

        conexao.execute("""
            UPDATE alunos
            SET nome = ?,
                cpf = ?,
                email = ?,
                telefone = ?,
                curso = ?
            WHERE id = ?
        """, (nome, cpf, email, telefone, curso, id))

        conexao.commit()
        conexao.close()

        flash("Aluno atualizado com sucesso!")

        return redirect(url_for("index"))

    conexao.close()

    return render_template("editar.html", aluno=aluno)


# DELETE - Excluir aluno
@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM alunos WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    flash("Aluno excluído com sucesso!")

    return redirect(url_for("index"))


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
