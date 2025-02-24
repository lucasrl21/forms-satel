from flask import Flask, request, render_template_string, send_file
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

@app.route("/", methods=["GET", "POST"])
def form():
    FORMULARIO_PAGE = '''
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
                    background: #808080;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                    width: 350px;
                    text-align: center;
                }
                img {
                    width: 100px;
                    margin-bottom: 10px;
                }
                input {
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
                    width: 100%;
                }
                input[type="submit"]:hover {
                    background: #006400;
                }
                .button {
                    background: #008000;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 4px;
                    text-decoration: none;
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    margin-top: 10px;
                }
                .button:hover {
                    background: #006400;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <img src="/static/logo.png" alt="Logo">
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
                <a href="/download" class="button">&#x1F4E5; Baixar Checklist</a>
            </div>
        </body>
        </html>
    '''
    
    if request.method == "POST":
        nome = request.form["nome"].strip()
        id_checklist = request.form["id_checklist"].strip()
        data_inicio = request.form["data_inicio"].strip()
        data_fim = request.form["data_fim"].strip()
        descricao = request.form["descricao"].strip()

        df = pd.read_excel(EXCEL_FILE)
        novo_registro = pd.DataFrame([{
            "Nome do Colaborador": nome,
            "ID do Checklist": id_checklist,
            "Data de Início": data_inicio,
            "Data de Fim": data_fim,
            "Duração": "",
            "Descrição da Atividade": descricao
        }])

        df = pd.concat([df, novo_registro], ignore_index=True)

        df.to_excel(EXCEL_FILE, index=False)

        return '''
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
                    background: #808080;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                    width: 350px;
                    text-align: center;
                }
                .button {
                    background: #008000;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 4px;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 10px;
                }
                .button:hover {
                    background: #006400;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Registro salvo com sucesso!</h2>
                <a href="/" class="button">Voltar ao formulário</a>
            </div>
        </body>
        </html>
        '''
    
    return render_template_string(FORMULARIO_PAGE)

@app.route("/download")
def download():
    return send_file(EXCEL_FILE, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    