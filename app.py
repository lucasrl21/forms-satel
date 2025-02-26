from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Criar banco de dados
def criar_tabela():
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        valor TEXT NOT NULL)''')
    conexao.commit()
    conexao.close()

criar_tabela()

@app.route('/')
def index():
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM registros")
    registros = cursor.fetchall()
    conexao.close()
    return render_template('index.html', registros=registros)

@app.route('/inserir', methods=['POST'])
def inserir():
    nome = request.form['nome']
    valor = request.form['valor']
    if nome and valor:
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO registros (nome, valor) VALUES (?, ?)", (nome, valor))
        conexao.commit()
        conexao.close()
    return redirect(url_for('index'))

@app.route('/excluir', methods=['POST'])
def excluir():
    ids = request.json.get('ids', [])
    if ids:
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()
        cursor.executemany("DELETE FROM registros WHERE id = ?", [(id,) for id in ids])
        conexao.commit()
        conexao.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
