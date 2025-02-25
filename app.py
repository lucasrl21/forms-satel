from flask import Flask, request, render_template_string, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = "checklist_data.xlsx"

def initialize_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=["ID", "Nome do Colaborador", "ID do Checklist", "Data de Início", "Data de Fim", "Duração", "Descrição da Atividade"])
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

initialize_excel()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        checklist_id = request.form["checklist_id"]
        data_inicio = request.form["data_inicio"]
        data_fim = request.form["data_fim"]
        descricao = request.form["descricao"]

        inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
        fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")
        duracao = round((fim - inicio).total_seconds() / 3600, 2)

        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        new_id = len(df) + 1
        df.loc[len(df)] = [new_id, nome, checklist_id, data_inicio, data_fim, duracao, descricao]
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    FORM_PAGE = '''
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #BFBFBF;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                }
                .container {
                    background: #A0A0A0;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                    width: 90%;
                    max-width: 400px;
                    text-align: center;
                }
                .logo {
                    width: 120px;
                    display: block;
                    margin: 0 auto 10px auto;
                }
                input, button {
                    width: 100%;
                    padding: 10px;
                    margin: 5px 0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    background: white;
                }
                button {
                    background: #28a745;
                    color: white;
                    cursor: pointer;
                }
                button:hover { background: #218838; }
                a {
                    display: block;
                    margin-top: 10px;
                    text-decoration: none;
                    color: white;
                    background: #007bff;
                    padding: 10px;
                    border-radius: 4px;
                }
                a:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <img src="https://via.placeholder.com/120" class="logo" alt="Logo">
                <h2>Registrar Atividade</h2>
                <form method="POST">
                    <input type="text" name="nome" placeholder="Nome do Colaborador" required><br>
                    <input type="text" name="checklist_id" placeholder="ID do Checklist" required><br>
                    <label>Data de Início:</label><input type="datetime-local" name="data_inicio" required><br>
                    <label>Data de Fim:</label><input type="datetime-local" name="data_fim" required><br>
                    <input type="text" name="descricao" placeholder="Descrição da Atividade" required><br>
                    <button type="submit">Salvar Registro</button>
                </form>
                <a href="/listar">Consultar Registros</a>
                <a href="/baixar">Baixar Registros</a>
            </div>
        </body>
        </html>
    '''
    return render_template_string(FORM_PAGE)

@app.route("/listar")
def listar():
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    records_html = df.to_html(index=False)

    LIST_PAGE = f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #BFBFBF;
                    text-align: center;
                    padding: 20px;
                }}
                table {{
                    width: 90%;
                    margin: 20px auto;
                    border-collapse: collapse;
                    background: white;
                }}
                th, td {{
                    padding: 10px;
                    border: 1px solid #ddd;
                }}
                th {{
                    background: #007bff;
                    color: white;
                }}
                a {{
                    display: inline-block;
                    margin-top: 20px;
                    text-decoration: none;
                    color: white;
                    background: #007bff;
                    padding: 10px;
                    border-radius: 4px;
                }}
                a:hover {{
                    background: #0056b3;
                }}
            </style>
        </head>
        <body>
            <h2>Registros Salvos</h2>
            {records_html}
            <br>
            <a href="/">Voltar</a>
        </body>
        </html>
    '''
    return render_template_string(LIST_PAGE)

@app.route("/baixar")
def baixar():
    return send_file(EXCEL_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
