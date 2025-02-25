from flask import Flask, request, render_template_string, send_file, redirect, url_for
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = "checklist_data.xlsx"

# Criar arquivo Excel se não existir
def initialize_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=["ID", "Nome do Colaborador", "ID do Checklist", "Data de Início", "Data de Fim", "Duração", "Descrição da Atividade"])
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

initialize_excel()

@app.route("/", methods=["GET", "POST"])
def form():
    FORMULARIO_PAGE = '''
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                }
                .container {
                    background: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                    width: 350px;
                    text-align: center;
                }
                input {
                    width: 100%;
                    padding: 10px;
                    margin: 5px 0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-size: 16px;
                }
                input[type="submit"], .button {
                    background: #28a745;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 4px;
                    width: 100%;
                    text-decoration: none;
                    display: block;
                    margin-top: 10px;
                }
                .button:hover { background: #218838; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Preenchimento de Checklist</h2>
                <form method="post">
                    <label>Nome do Colaborador:</label>
                    <input type="text" name="nome" required>
                    <label>ID do Checklist:</label>
                    <input type="text" name="id_checklist" required>
                    <label>Data de Início:</label>
                    <input type="datetime-local" name="data_inicio" required>
                    <label>Data de Fim:</label>
                    <input type="datetime-local" name="data_fim" required>
                    <label>Descrição da Atividade:</label>
                    <input type="text" name="descricao" required>
                    <input type="submit" value="Salvar">
                </form>
                <a href="/download" class="button">Baixar Checklist</a>
                <a href="/listar" class="button">Ver Registros</a>
            </div>
        </body>
        </html>
    '''
    
    if request.method == "POST":
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        novo_id = len(df) + 1
        nome = request.form["nome"].strip()
        id_checklist = request.form["id_checklist"].strip()
        data_inicio = request.form["data_inicio"].strip()
        data_fim = request.form["data_fim"].strip()
        descricao = request.form["descricao"].strip()

        try:
            dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
            dt_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")
            duracao = str(dt_fim - dt_inicio)
        except ValueError:
            duracao = "Erro no cálculo"

        novo_registro = pd.DataFrame([{ 
            "ID": novo_id,
            "Nome do Colaborador": nome, 
            "ID do Checklist": id_checklist, 
            "Data de Início": data_inicio, 
            "Data de Fim": data_fim, 
            "Duração": duracao, 
            "Descrição da Atividade": descricao 
        }])

        df = pd.concat([df, novo_registro], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        return redirect(url_for('form'))
    
    return render_template_string(FORMULARIO_PAGE)

@app.route("/listar")
def listar():
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    html_table = df.to_html(index=False, escape=False)
    html_page = f'''
        <html>
        <head>
            <style>
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
                th {{ background-color: #f4f4f4; }}
                .button {{ padding: 8px 12px; color: white; background: red; text-decoration: none; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <h2>Registros</h2>
            {html_table}
            <form action="/deletar" method="post">
                <label>ID para deletar:</label>
                <input type="number" name="id" required>
                <input type="submit" value="Deletar">
            </form>
            <a href="/" class="button">Voltar</a>
        </body>
        </html>
    '''
    return html_page

@app.route("/deletar", methods=["POST"])
def deletar():
    id_para_deletar = int(request.form["id"])
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    df = df[df["ID"] != id_para_deletar]
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    return redirect(url_for('listar'))

@app.route("/download")
def download():
    return send_file(EXCEL_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
