from flask import Flask, request, render_template_string, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = "checklist_data.xlsx"
LOGO_PATH = "static/logo.png"

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
        
        inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
        fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")
        duracao = round((fim - inicio).total_seconds() / 3600, 2)
        
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        novo_id = len(df) + 1
        df = df.append({
            "ID": novo_id,
            "Nome do Colaborador": nome,
            "ID do Checklist": checklist_id,
            "Data de Início": data_inicio,
            "Data de Fim": data_fim,
            "Duração": duracao,
            "Descrição da Atividade": descricao
        }, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    FORM_PAGE = f'''
        <html>
        <head>
            <style>
                body {{ background-color: #BFBFBF; font-family: Arial, sans-serif; text-align: center; }}
                .container {{ background: #BFBFBF; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); width: 50%; margin: auto; }}
                input, button {{ margin: 5px; padding: 10px; width: 80%; }}
                button {{ background: #28a745; color: white; border: none; cursor: pointer; }}
                button:hover {{ background: #218838; }}
                .logo {{ width: 150px; display: block; margin: auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <img src="{LOGO_PATH}" class="logo" />
                <h2>Registro de Atividades</h2>
                <form method="POST">
                    <input type="text" name="nome" placeholder="Nome do Colaborador" required><br>
                    <input type="text" name="checklist_id" placeholder="ID do Checklist" required><br>
                    <input type="datetime-local" name="data_inicio" required><br>
                    <input type="datetime-local" name="data_fim" required><br>
                    <input type="text" name="descricao" placeholder="Descrição da Atividade" required><br>
                    <button type="submit">Salvar Registro</button>
                </form>
                <br>
                <a href="/listar"><button>Consultar Registros</button></a>
                <a href="/baixar"><button>Baixar Registros</button></a>
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
    
    LISTAR_PAGE = f'''
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #BFBFBF; text-align: center; }}
                .container {{ background: #BFBFBF; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); width: 80%; margin: auto; }}
                .table-container {{ max-height: 500px; overflow-y: auto; border: 1px solid #ddd; border-radius: 4px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
                th {{ background: #28a745; color: white; }}
                button {{ background: #dc3545; color: white; border: none; padding: 10px; cursor: pointer; }}
                button:hover {{ background: #c82333; }}
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
