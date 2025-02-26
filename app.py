from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "database.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            data_inicio TEXT NOT NULL,
                            data_fim TEXT NOT NULL,
                            descricao TEXT NOT NULL
                        )''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    descricao = request.form['descricao']
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registros (nome, data_inicio, data_fim, descricao) VALUES (?, ?, ?, ?)",
                       (nome, data_inicio, data_fim, descricao))
        conn.commit()
    
    return redirect('/')

@app.route('/consultar')
def consultar():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registros")
        registros = cursor.fetchall()
    return render_template('consulta.html', registros=registros)

@app.route('/excluir', methods=['POST'])
def excluir():
    ids_para_excluir = request.form.getlist('selecionados')
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.executemany("DELETE FROM registros WHERE id = ?", [(id,) for id in ids_para_excluir])
        conn.commit()
    return redirect('/consultar')

if __name__ == '__main__':
    app.run(debug=True)
