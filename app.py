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

@app.route("/listar", methods=["GET", "POST"])
def listar():
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    
    if request.method == "POST":
        ids_para_excluir = request.form.getlist("selecionados")
        df = df[~df["ID"].astype(str).isin(ids_para_excluir)]
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    
    registros_html = df.to_html(index=False, classes='table table-striped', escape=False)
    
    LISTAR_PAGE = '''
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
                    background: #d3d3d3;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                    width: 90%;
                    max-width: 1200px;
                    text-align: center;
                }
                .table-container {
                    max-height: 500px;
                    overflow-y: auto;
                    overflow-x: auto;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: left;
                }
                th {
                    background: #28a745;
                    color: white;
                }
                a.button, button {
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 10px;
                    cursor: pointer;
                }
                a.button:hover, button:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Registros do Checklist</h2>
                <form method="POST">
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Selecionar</th>
                                    <th>ID</th>
                                    <th>Nome do Colaborador</th>
                                    <th>ID do Checklist</th>
                                    <th>Data de Início</th>
                                    <th>Data de Fim</th>
                                    <th>Duração</th>
                                    <th>Descrição da Atividade</th>
                                </tr>
                            </thead>
                            <tbody>
                                ''' + "".join(f"""
                                <tr>
                                    <td><input type='checkbox' name='selecionados' value='{row["ID"]}'></td>
                                    <td>{row["ID"]}</td>
                                    <td>{row["Nome do Colaborador"]}</td>
                                    <td>{row["ID do Checklist"]}</td>
                                    <td>{row["Data de Início"]}</td>
                                    <td>{row["Data de Fim"]}</td>
                                    <td>{row["Duração"]}</td>
                                    <td>{row["Descrição da Atividade"]}</td>
                                </tr>
                                """ for _, row in df.iterrows()) + '''
                            </tbody>
                        </table>
                    </div>
                    <br>
                    <button type="submit">Excluir Selecionados</button>
                </form>
                <br>
                <a href="/" class="button">Voltar</a>
                <a href="/baixar" class="button">Baixar Planilha</a>
            </div>
        </body>
        </html>
    '''
    
    return render_template_string(LISTAR_PAGE)

@app.route("/baixar")
def baixar():
    return send_file(EXCEL_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
