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

        dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
        dt_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")
        duracao = round((dt_fim - dt_inicio).total_seconds() / 3600, 2)

        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        new_id = len(df) + 1
        novo_registro = pd.DataFrame([[new_id, nome, checklist_id, data_inicio, data_fim, duracao, descricao]],
                                     columns=df.columns)
        df = pd.concat([df, novo_registro], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    FORM_PAGE = '''
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; }
                .container { background: #BFBFBF; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); width: 50%; margin: auto; }
                input, textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; }
                button { background: #28a745; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; }
                button:hover { background: #218838; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Registro de Atividade</h2>
                <form method="POST">
                    <input type="text" name="nome" placeholder="Nome do Colaborador" required><br>
                    <input type="text" name="checklist_id" placeholder="ID do Checklist" required><br>
                    <input type="datetime-local" name="data_inicio" required><br>
                    <input type="datetime-local" name="data_fim" required><br>
                    <textarea name="descricao" placeholder="Descrição da Atividade" required></textarea><br>
                    <button type="submit">Salvar Registro</button>
                </form>
                <br>
                <a href="/listar"><button>Consultar Registros</button></a>
                <a href="/baixar"><button>Baixar Planilha</button></a>
            </div>
        </body>
        </html>
    '''
    return render_template_string(FORM_PAGE)

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
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; }
                .container { background: #BFBFBF; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); width: 80%; margin: auto; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
                th { background: #28a745; color: white; }
                button { background: #dc3545; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; }
                button:hover { background: #c82333; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Registros do Checklist</h2>
                <form method="POST">
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
