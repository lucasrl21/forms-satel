import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Criando banco de dados SQLite
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

# Função para inserir dados
def inserir_dados():
    nome = entry_nome.get()
    valor = entry_valor.get()
    if nome and valor:
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO registros (nome, valor) VALUES (?, ?)", (nome, valor))
        conexao.commit()
        conexao.close()
        messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_valor.delete(0, tk.END)
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")

# Função para buscar dados
def buscar_dados():
    tree.delete(*tree.get_children())
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM registros")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conexao.close()

# Função para excluir registros selecionados
def excluir_dados():
    selecionados = tree.selection()
    if not selecionados:
        messagebox.showwarning("Aviso", "Selecione pelo menos um registro para excluir!")
        return
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    for item in selecionados:
        id_registro = tree.item(item, "values")[0]
        cursor.execute("DELETE FROM registros WHERE id = ?", (id_registro,))
    conexao.commit()
    conexao.close()
    buscar_dados()

# Criando a interface
tela = tk.Tk()
tela.title("Cadastro de Dados")
tela.geometry("500x400")
tela.configure(bg="white")

frame_principal = tk.Frame(tela, bg="#E0E0E0", padx=10, pady=10)
frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

# Logo
try:
    imagem = Image.open("logo.png")
    imagem = imagem.resize((100, 100))
    logo = ImageTk.PhotoImage(imagem)
    label_logo = tk.Label(frame_principal, image=logo, bg="#E0E0E0")
    label_logo.pack()
except Exception as e:
    print("Erro ao carregar a imagem:", e)

# Campos de entrada
tk.Label(frame_principal, text="Nome:", bg="#E0E0E0").pack()
entry_nome = tk.Entry(frame_principal)
entry_nome.pack()

tk.Label(frame_principal, text="Valor:", bg="#E0E0E0").pack()
entry_valor = tk.Entry(frame_principal)
entry_valor.pack()

# Botões
btn_inserir = tk.Button(frame_principal, text="Inserir", bg="green", fg="white", command=inserir_dados)
btn_inserir.pack(pady=5)

btn_buscar = tk.Button(frame_principal, text="Buscar", bg="green", fg="white", command=buscar_dados)
btn_buscar.pack(pady=5)

btn_excluir = tk.Button(frame_principal, text="Excluir Selecionados", bg="green", fg="white", command=excluir_dados)
btn_excluir.pack(pady=5)

# Tabela para exibir os dados
tree = ttk.Treeview(frame_principal, columns=("ID", "Nome", "Valor"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Valor", text="Valor")
tree.pack(fill="both", expand=True)

# Atualizar lista ao iniciar
buscar_dados()

tela.mainloop()
