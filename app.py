from flask import Flask, request, render_template_string, send_file
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
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        checklist_id = request.form["checklist_id"]
        data_inicio = request.form["data_inicio"]
        data_fim = request.form["data_fim"]
        descricao = request.form["descricao"]
        
        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
            fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")
            duracao = round((fim - inicio).total_seconds() / 3600, 2)  # Duração em horas
        except ValueError:
            duracao = "Erro na data"

        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        new_id = len(df) + 1
        new_row = pd.DataFrame([[new_id, nome, checklist_id, data_inicio, data_fim, duracao, descricao]],
                               columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    FORM_PAGE = '''
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
                    background: #c4c4c4;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                    width: 400px;
                    text-align: center;
                }
                img {
                    width: 150px;
                    margin-bottom: 10px;
                }
                input, textarea {
                    width: 100%;
                    padding: 10px;
                    margin: 5px 0;
                    border-radius: 4px;
                    border: 1px solid #ddd;
                }
                button {
                    background: #28a745;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover { background: #218838; }
            </style>
        </head>
        <body>
            <div class="container">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ab/Logo_Teste.png" alt="Logo">
                <h2>Registro de Atividade</h2>
                <form method="POST">
                    <input type="text" name="nome" placeholder="Nome do Colaborador" required>
                    <input type="text" name="checklist_id" placeholder="ID do Checklist" required>
                    <label>Data de Início</label>
                    <input type="datetime-local" name="data_inicio" required>
                    <label>Data de Fim</label>
                    <input type="datetime-local" name="data_fim" required>
                    <textarea name="descricao" placeholder="Descrição da Atividade" required></textarea>
                    <br>
                    <button type="submit">Salvar Registro</button>
                </form>
                <br>
                <a href="/listar"><button>Consulta</button></a>
                <a href="/baixar"><button>Baixar Registros</button></a>
            </div>
        </body>
        </html>
    '''
    
    return render_template_string(FORM_PAGE)

@app.route("/listar", methods=["GET", "POST"])
def listar():
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')

    if df.empty:
        return "<h3>Nenhum registro encontrado. <a href='/'>Voltar</a></h3>"

    if request.method == "POST":
        ids_para_excluir = request.form.getlist("selecionados")
        df = df[~df["ID"].astype(str).isin(ids_para_excluir)]
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

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
                    background: #c4c4c4;
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
                button {
                    background: #dc3545;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover { background: #b02a37; }
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
                                    <th>Duração (horas)</th>
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
                <a href="/"><button>Voltar</button></a>
                <a href="/baixar"><button>Baixar Planilha</button></a>
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
