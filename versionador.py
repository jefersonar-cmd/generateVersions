import tkinter as tk
from tkinter import ttk
import random
import sqlite3
from datetime import datetime

# Função para gerar uma nova versão
def gerar_versao():
    sistema = nome_sistema.get()
    if sistema:
        cursor.execute("SELECT nome, versao, data FROM sistemas WHERE nome = ? ORDER BY data DESC limit 1", (sistema,))
        sistema_existente = cursor.fetchone()
        if sistema_existente:
            # Recuperar a versão atual
            versao_atual = sistema_existente[1:4][0]
            versao_atual = versao_atual.split('.')
            versao_atual[0] = int(versao_atual[0])
            versao_atual[1] = int(versao_atual[1])
            versao_atual[2] = int(versao_atual[2])
            print(versao_atual)
            novo_numero = random.randint(1, 9)
            versao_atual[2] += novo_numero
            if versao_atual[2] > 20:
                versao_atual[2] = novo_numero
                versao_atual[1] += 1
            if versao_atual[1] > 20:
                versao_atual[1] = novo_numero
                versao_atual[0] += 1
            nova_versao = '.'.join(map(str, versao_atual))
            cursor.execute("INSERT INTO sistemas (nome, versao, data) VALUES (?, ?, ?)", (sistema, nova_versao, datetime.now()))
        else:
            cursor.execute("INSERT INTO sistemas (nome, versao, data) VALUES (?, '1.0.0', ?)", (sistema, datetime.now()))
        conn.commit()
        atualizar_tabela()

# Função para atualizar a tabela
def atualizar_tabela():
    cursor.execute("SELECT nome, versao, data FROM sistemas ORDER BY data DESC")
    sistemas = cursor.fetchall()
    for i in tabela.get_children():
        tabela.delete(i)
    for sistema in sistemas:
        tabela.insert("", "end", values=sistema)

# Configuração da interface gráfica
app = tk.Tk()
app.title("Sistem"
          "a de Versionamento")
app.geometry("800x600")

nome_sistema_label = tk.Label(app, text="Nome do Sistema:")
nome_sistema_label.pack(pady=10)

nome_sistema = tk.Entry(app)
nome_sistema.pack()

gerar_versao_button = tk.Button(app, text="Gerar Versão", command=gerar_versao)
gerar_versao_button.pack(pady=10)

tabela = ttk.Treeview(app, columns=("Nome", "Versão", "Data"))
tabela.heading("Nome", text="Nome do Sistema")
tabela.heading("Versão", text="Versão")
tabela.heading("Data", text="Data da Versão")
tabela.pack(pady=10)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("versionamento.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS sistemas
                  (id INTEGER PRIMARY KEY, nome text, versao text, data text)''')
conn.commit()

atualizar_tabela()

app.mainloop()
