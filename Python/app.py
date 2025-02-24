from flask import Flask, request, render_template_string
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = "checklist_data.xlsx"

# Criar arquivo Excel se não existir
def initialize_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=["Nome do Colaborador", "ID do Checklist", "Data de Início", "Data de Fim", "Duração", "Descrição da Atividade"])
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

initialize_excel()

HTML_FORM = '''
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
            }
            .container {
                background: #d0d0d0;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                width: 350px;
                text-align: center;
                position: relative;
            }
            .logo {
                width: 200px;
                margin-bottom: 10px;
            }
            .logo-container {
                text-align: center;
                margin-bottom: 10px;
            }
            h2 {
                color: #008000;
            }
            input, textarea {
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }
            input[type="submit"] {
                background: #008000;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 4px;
            }
            input[type="submit"]:hover {
                background: #006400;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-container">
                <img src="/static/logo.png" class="logo" alt="Logo">
            </div>
            <h2>Cadastro de Atividade</h2>
            <form method="post">
                <label>Nome do Colaborador:</label>
                <input type="text" name="nome" required>
                <label>ID do Checklist:</label>
                <input type="text" name="id_checklist" required>
                <label>Data de Início:</label>
                <input type="date" name="data_inicio" required>
                <label>Data de Fim:</label>
                <input type="date" name="data_fim" required>
                <label>Duração:</label>
                <input type="text" name="duracao" required>
                <label>Descrição da Atividade:</label>
                <textarea name="descricao" required></textarea>
                <input type="submit" value="Enviar">
            </form>
        </div>
    </body>
    </html>
'''

SUCCESS_PAGE = '''
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
            }
            .container {
                background: #d0d0d0;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                width: 350px;
                text-align: center;
            }
            .logo {
                width: 200px;
                margin-bottom: 20px;
            }
            h2 {
                color: #008000;
                font-size: 24px;
                font-weight: bold;
            }
            a {
                display: inline-block;
                margin-top: 15px;
                padding: 10px 15px;
                background: #008000;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-size: 18px;
            }
            a:hover {
                background: #006400;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="/static/logo.png" class="logo" alt="Logo">
            <h2>Registrado com Sucesso!</h2>
            <a href="/">Voltar ao Formulário</a>
        </div>
    </body>
    </html>
'''

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = {
            "Nome do Colaborador": request.form["nome"].strip(),
            "ID do Checklist": request.form["id_checklist"].strip(),
            "Data de Início": request.form["data_inicio"].strip(),
            "Data de Fim": request.form["data_fim"].strip(),
            "Duração": request.form["duracao"].strip(),
            "Descrição da Atividade": request.form["descricao"].strip()
        }

        # Evitar duplicatas
        df = pd.read_excel(EXCEL_FILE)
        if df.isin([data["ID do Checklist"]]).any().any():
            return "Erro: ID do Checklist já cadastrado!"
        
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        
        return render_template_string(SUCCESS_PAGE)
    
    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(debug=True)
