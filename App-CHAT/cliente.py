from email import message
from pydoc import cli
from re import X
import tkinter as tk
from tkinter import DISABLED, LEFT, Entry, mainloop, messagebox, ttk
import socket
import threading
from threading import Thread
from login import getNome
from login import autentica #chama a tela login
import time
import pickle
from setings import consultaGrupos, incluir_valores_no_grupo, consultaBanidos, incluirBanidos
#from colorama import Fore

#import sqlite3
#banco = sqlite3.connect("/home/roberto/Projetos/CHAT-RMI/banco.db")

import pdb
#breakpoint()
tela_client = tk.Tk()
tela_client.title("Cliente")
tela_client.geometry("500x630")
tela_client.config(bg='#333333')

#####VARIAVEIS######
username = " "
lista = []
listaBanidos = []
nomesBanidos = consultaBanidos()
for b in nomesBanidos:
    listaBanidos.append(b[1])

listaGrupo = consultaGrupos()
for l in listaGrupo:
    lista.append(l[1])



#frame do nome
topFrame = tk.Frame(tela_client, bg='#333333')
lbNome = tk.Label(topFrame, text="Nome: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15)).pack(side=tk.LEFT)
entNome = tk.Entry(topFrame)
userNome = getNome()
entNome.insert(0, userNome)
entNome.config(state='disabled')
entNome.pack(side=tk.LEFT)
btnConectar = tk.Button(topFrame, text="Conectar", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15), command=lambda : conectar())
btnConectar.pack(side=tk.LEFT, padx=(20,0))
btnSair = tk.Button(topFrame, text="SAIR", bg='#FF0000', fg='#FFFFFF', font=('Arial', 15), command=lambda : sair())
btnSair.pack(side=tk.LEFT, padx=(20,0))
topFrame.pack(side=tk.TOP, pady=(30,10))

#frame do grupo
grFrame = tk.Frame(tela_client, bg='#333333')
grLabel = tk.Label(grFrame, text="Grupo: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15)).pack(side=tk.LEFT, padx=(10,0))
cbGrupo = ttk.Combobox(grFrame, values=lista)
cbGrupo.set("Todos")
cbGrupo.pack(side=tk.LEFT)
btCriarGrupo = tk.Button(grFrame,text="Criar Novo Grupo", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15),  command=lambda: cadastroGrupo())
btCriarGrupo.pack(side=tk.LEFT, padx=(20,10))
grFrame.pack(side=tk.TOP, padx=(10,0))

'''#frame do chat privado
aFrame = tk.Frame(tela_client, bg='#333333')
lbPv = tk.Label(aFrame, text="CHAT pv: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
lbPv.pack(side=tk.LEFT)
entPv = tk.Entry(aFrame)
entPv.pack(side=tk.LEFT)
btPv = tk.Button(aFrame, text="Enviar", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15))
btPv.pack(side=tk.RIGHT, pady=(5,0), padx=(5,0))
aFrame.pack(side=tk.TOP, padx=(10,0))'''

#frame do banir
bFrame = tk.Frame(tela_client, bg='#333333')
lbBanir = tk.Label(bFrame, text="Banir User: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
lbBanir.pack(side=tk.LEFT)
entBanir = tk.Entry(bFrame)
entBanir.pack(side=tk.LEFT)
btBanir = tk.Button(bFrame, text="Banir", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15), command=lambda: banirUsuario())
btBanir.pack(side=tk.RIGHT, pady=(5,0), padx=(5,0))
bFrame.pack(side=tk.TOP, padx=(10,0))

#frame do chat 
displayFrame = tk.Frame(tela_client, bg='#333333')
lbLinha = tk.Label(displayFrame, bg = "#ABB2B9", height=1).pack(fill=tk.X, pady=(10,10))
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
display = tk.Text(displayFrame, height=20, width=55)
display.pack(side=tk.LEFT, fill=tk.Y, padx=(5,0))
display.tag_config("Envie sua menssagem", foreground="blue")
scrollBar.config(command=display.yview)
display.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)

#frame do send menssagem
btnFrame = tk.Frame(tela_client, bg='#333333')
menssagem = tk.Text(btnFrame, height=3, width=58)
menssagem.pack(side=tk.LEFT, pady=(5,10))
menssagem.config(highlightbackground="grey", state="disabled")
menssagem.bind("<Return>", (lambda event: getMensagemChat(menssagem.get("1.0", tk.END))))
btnFrame.pack(side=tk.BOTTOM)

def conectar():
    global username, cliente
    if len(entNome.get()) < 1:
        tk.messagebox.showerror(title="ERRO!!", message="Entre somente com o primeiro nome")
    else:
        username = entNome.get()
        grupo = cbGrupo.get()
        conecta_server(username, grupo)
    

cliente = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 5000
HOST_PORT_2 = 5050
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conecta_server(nome, grupo):
    global cliente, HOST_PORT, HOST_ADDR
    d = []
    d.append(nome)
    d.append(grupo)
    dados = pickle.dumps(d)
    try:
        cliente = cliente
        #cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST_ADDR, HOST_PORT))
        cliente.send(bytes(dados))
        entNome.config(state=tk.DISABLED)
        btnConectar.config(state=tk.DISABLED)
        cbGrupo.config(state=tk.DISABLED)
        menssagem.config(state=tk.NORMAL)
        btCriarGrupo.config(state=DISABLED)

        # comessa uma thread para continuar recebendo menssagem
        threading._start_new_thread(recebe_mesg_do_server, (cliente, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERRO!!", message="Não pode ser conectado ao host: " + HOST_ADDR + " na porta: " + str(HOST_PORT) + " Tente Denovo.")

    
def recebe_mesg_do_server(sck, m):
    while True:
        do_server = sck.recv(4096).decode()
        if not do_server:
            break
        textos = display.get("1.0", tk.END).strip()
        display.config(state=tk.NORMAL)
        if len(textos) < 1:
            display.insert(tk.END, do_server)
        else:
            display.insert(tk.END, "\n\n" + do_server)
        display.config(state=tk.DISABLED)
        display.see(tk.END)
    sck.close()
    tela_client.destroy()

def getMensagemChat(msg):
    msg = msg.replace('\n', '')
    textos = display.get("1.0", tk.END).strip()
    display.config(state=tk.NORMAL)
    if len(textos)< 1:
        display.insert(tk.END, "Voce->" + msg, "informe sua menssagem")
    else:
        display.insert(tk.END, "\n\n" + "Voce->" + msg, "informe sua menssagem")
    display.config(state=tk.DISABLED)
    envia_menssagem_server(msg)
    display.see(tk.END)
    menssagem.delete('1.0', tk.END)

def envia_menssagem_server(msg):
    cliente_msg = str(msg)
    cliente.send(cliente_msg.encode())
    print("Enviando menssagem")


def sair():
    cliente.close()
    tela_client.destroy()


def cadastroGrupo():
    # tela de cadastros de grupo 
    tela_cadastro_grupo = tk.Tk()
    tela_cadastro_grupo.title("Cadastro de Grupo")
    tela_cadastro_grupo.geometry("400x150")
    tela_cadastro_grupo.config(bg='#333333')

    # linha nome
    nFrameGrupo = tk.Frame(tela_cadastro_grupo, bg='#333333')
    lbNomeGrupo = tk.Label(nFrameGrupo, text="Nome do Grupo: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
    lbNomeGrupo.pack(side=tk.LEFT)
    entNomeGrupo = tk.Entry(nFrameGrupo)
    entNomeGrupo.pack(side=tk.LEFT)
    nFrameGrupo.pack(side=tk.TOP, pady=(40,10))

    # linha logar
    tFrameGrupo = tk.Frame(tela_cadastro_grupo, bg='#333333')
    btEntrarGrupo = tk.Button(tFrameGrupo, text="Cadastrar", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15), command=lambda : envia_dados_grupo())
    btEntrarGrupo.pack(side=tk.LEFT)
    tFrameGrupo.pack(side=tk.TOP, pady=(15,15))

    def envia_dados_grupo():
        incluir_valores_no_grupo(entNomeGrupo.get())
        usr = entNomeGrupo.get()
        menssagemGrupo = f"Grupo {usr} cadastrado com sucesso."
        tk.messagebox.showinfo(title="CADASTRADO DE NOVO GRUPO", message=menssagemGrupo)
        cbGrupo.set(usr)
        tela_cadastro_grupo.destroy()

    tela_cadastro_grupo.mainloop()
    
def banirUsuario():
    nome = entBanir.get()
    if nome in listaBanidos:
        menssagem = f"{nome} já esta banido!"
        tk.messagebox.showerror(title="ERRO!!", message=menssagem)    
    elif nome == '':
        pass
    else:
        incluirBanidos(nome)
        listaBanidos.append(nome)
        menssagem = f"{nome} BANIDO!"
        tk.messagebox.showinfo(title="CADASTRADO!", message=menssagem)



tela_client.mainloop()