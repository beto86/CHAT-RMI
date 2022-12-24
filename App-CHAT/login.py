
import tkinter as tk
from tkinter import ttk
from cryptography.fernet import Fernet
import rsa
from setings import incluir_valores_no_usuario, consulta_valores, consultaGrupos, consultaBanidos
import pdb
#breakpoint()

#####VARIAVEIS##########
global username
lista = []
listaGrupo = consultaGrupos()
for l in listaGrupo:
    lista.append(l[1])
listaBanidos = []
nomesBanidos = consultaBanidos()
for b in nomesBanidos:
    listaBanidos.append(b[1])


# tela principal 
tela_login = tk.Tk()
tela_login.title("Login")
tela_login.geometry("400x300")
tela_login.config(bg='#333333')

# linha nome
topFrame = tk.Frame(tela_login, bg='#333333')
lbNome = tk.Label(topFrame, text="Nome: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
lbNome.pack(side=tk.LEFT)
entNome = tk.Entry(topFrame)
entNome.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(60,15))


# linha senha
sFrame = tk.Frame(tela_login, bg='#333333')
lbSenha = tk.Label(sFrame, text="Senha: ",bg='#333333',fg='#FFFFFF' ,font=('Arial', 15))
lbSenha.pack(side=tk.LEFT)
entSenha = tk.Entry(sFrame, show="*")
entSenha.pack(side=tk.LEFT)
sFrame.pack(side=tk.TOP, pady=(20,20))

# linha logar
tFrame = tk.Frame(tela_login, bg='#333333')
btEntrar = tk.Button(tFrame, text="ENTRAR", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15),command=lambda : autentica())
btEntrar.pack(side=tk.LEFT)
btCadastrar = tk.Button(tFrame, text="Cadastrar", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15), command=lambda : cadastrar())
btCadastrar.pack(side=tk.LEFT, padx=(20,0))
tFrame.pack(side=tk.TOP, pady=(25,15))


def autentica():
    global username
    #breakpoint()
    nome = consulta_valores(entNome.get(), entSenha.get())
    nomeBan = entNome.get()
    if nomeBan not in listaBanidos:
        if nome:
            username = entNome.get()
            tela_login.destroy()
        else:
            tk.messagebox.showerror(title="ERRO!!", message="Login invalido.")
    else:
        tk.messagebox.showerror(title="ERRO!!", message="NOME BANIDO.")
       
    

def cadastrar():
    # tela de cadastros 
    tela_cadastro = tk.Tk()
    tela_cadastro.title("Cadastro")
    tela_cadastro.geometry("400x300")
    tela_cadastro.config(bg='#333333')

    # linha nome
    nFrame = tk.Frame(tela_cadastro, bg='#333333')
    lbNome = tk.Label(nFrame, text="Nome: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
    lbNome.pack(side=tk.LEFT)
    entNome = tk.Entry(nFrame)
    entNome.pack(side=tk.LEFT)
    nFrame.pack(side=tk.TOP, pady=(40,10))


    # linha sobrenome
    snFrame = tk.Frame(tela_cadastro, bg='#333333')
    lbSN = tk.Label(snFrame, text="Sobrenome: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
    lbSN.pack(side=tk.LEFT)
    entSN = tk.Entry(snFrame)
    entSN.pack(side=tk.LEFT)
    snFrame.pack(side=tk.TOP, pady=(25,10))

    # linha senha
    sFrame = tk.Frame(tela_cadastro, bg='#333333')
    lbSenha = tk.Label(sFrame, text="Senha: ", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
    lbSenha.pack(side=tk.LEFT)
    entSenha = tk.Entry(sFrame)
    entSenha.pack(side=tk.LEFT)
    sFrame.pack(side=tk.TOP, pady=(25,10))

    # linha logar
    tFrame = tk.Frame(tela_cadastro, bg='#333333')
    btEntrar = tk.Button(tFrame, text="ENTRAR", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15), command=lambda : envia_dados())
    btEntrar.pack(side=tk.LEFT)
    tFrame.pack(side=tk.TOP, pady=(15,15))

    
    def envia_dados():
        #identifica a chave do grupo para cadastrr no usuario 
        id_grupo = 99
        #listaGrupo = consultaGrupos()
        #for l in listaGrupo:
        #    print(cbGrupo.get())
        #    if cbGrupo.get() == l[1]:                
        #        id_grupo = l[0]
        #        break
        #publicKey, privateKey = rsa.newkeys(512)
        #senha = str(entSenha.get())
        #encSenha = rsa.encrypt(senha.encode(),publicKey)
        #print(senha)
        #print(encSenha)
        #print(str(encSenha))
        #aux = str(encSenha)
        #print(type(aux))
        incluir_valores_no_usuario(entNome.get(), entSN.get(), entSenha.get(), id_grupo)
        usr = entNome.get()
        menssagem = f"Usuario {usr} cadastrado com sucesso."
        tk.messagebox.showinfo(title="CADASTRADO", message=menssagem)
        tela_cadastro.destroy()
    

    tela_cadastro.mainloop()


def getNome():
    return username

#banco.close()

tela_login.mainloop()