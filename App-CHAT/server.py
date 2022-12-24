import socket
import threading
from threading import Thread
import time
import tkinter as tk
from setings import consultaGrupos, consultaAll, fecha_banco
import pickle
import select
#banco = sqlite3.connect("/home/roberto/Projetos/CHAT-RMI/banco.db")
import pdb
#breakpoint()
#tela principal 
tela_server = tk.Tk()
tela_server.title("Servidor")
tela_server.geometry("400x450")
tela_server.config(bg='#333333')

# topo da tela, HEADER
topFrame = tk.Frame(tela_server, bg='#333333')
btnStart = tk.Button(topFrame, text="Conectar", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15), command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Parar", bg='#0000CD', fg='#FFFFFF', font=('Arial', 15), command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(40,10))

#meio da tela, CORPO
meioFrame = tk.Frame(tela_server, bg='#333333')
lbHost = tk.Label(meioFrame, text="Host: X.X.X.X", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
lbHost.pack(side=tk.LEFT)
lbPorta = tk.Label(meioFrame, text="Porta: XXXX", bg='#333333', fg='#FFFFFF' , font=('Arial', 15))
lbPorta.pack(side=tk.LEFT)
meioFrame.pack(side=tk.TOP, pady=(5,0))

#tela para os grupos
grupoFrame = tk.Frame(tela_server, bg='#333333')
lbLinhaGr = tk.Label(grupoFrame, text="LISTA DE GRUPOS", bg='#333333', fg='#FFFFFF' , font=('Arial', 15, 'bold')).pack()
scrollBarGr = tk.Scrollbar(grupoFrame)
scrollBarGr.pack(side=tk.RIGHT, fill=tk.Y)
displayGr = tk.Text(grupoFrame, height=5, width=40)
displayGr.pack(side=tk.LEFT, fill=tk.Y, padx=(5,0))
scrollBarGr.config(command=displayGr.yview)
displayGr.config(yscrollcommand=scrollBarGr.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
grupoFrame.pack(side=tk.BOTTOM, pady=(5,10))

#tela para os clientes
clienteFrame = tk.Frame(tela_server, bg='#333333')
lbLinha = tk.Label(clienteFrame, text="LISTA DE CLIENTES", bg='#333333', fg='#FFFFFF' , font=('Arial', 15, 'bold')).pack()
scrollBar = tk.Scrollbar(clienteFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
display = tk.Text(clienteFrame, height=10, width=40)
display.pack(side=tk.LEFT, fill=tk.Y, padx=(5,0))
scrollBar.config(command=display.yview)
display.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clienteFrame.pack(side=tk.BOTTOM, pady=(5,10))

#variaveis para o servidor se conectar
servidor = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 5000
HOST_PORT_2 = 5050
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_nome = " "
clientes = []
grupos = []
salas = {}
nomesBanidos = []
gruposBD = consultaGrupos()

clientes_nomes = []
try:
    clientesBD = consultaAll()
except:
    pass

#função para iniciar o servidor
def start_server(): 
    global servidor, HOST_ADDR, HOST_PORT
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)
    atualiza_lista_grupo() #mostra os grupos disponiveis no server
    servidor = servidor
    #servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET é para IPv4, e socket.SOCK_STREAM é para protocolo TCP.
    servidor.bind((HOST_ADDR, HOST_PORT))
    servidor.listen(5) 

    threading._start_new_thread(aceitar_clientes, (servidor, " ")) 

    lbHost["text"] = "Host: " + HOST_ADDR
    lbPorta["text"] = "Porta: " + str(HOST_PORT)


def stop_server():
    global servidor
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
    fecha_banco()


def aceitar_clientes(servidor, y):
    #para um novo cliente, cria uma nova threader
    while True: 
        cliente, addr = servidor.accept()
        sala = cliente.recv(4096)
        d = pickle.loads(sala)
        if d[1] not in salas.keys():
            salas[d[1]] = []
        salas[d[1]].append(cliente)

        threading._start_new_thread(envia_recebe_menssagem_cliente, (cliente, addr, d))


#manda menssagem para outros clientes
def envia_recebe_menssagem_cliente(cliente_conexao, cliente_ip_addr, d):
    global servidor, cliente_nome, clientes, clientes_addr, cliente_grupo
    cliente_msg = " "
    clientes = salas
    cliente_nome = d[0]
    time.sleep(0.5)
    msg_bem_vindo = "Bem vindo " + d[0] + ". No grupo de " + d[1] + " com ID " + str(cliente_ip_addr[1])
    cliente_conexao.send(msg_bem_vindo.encode())

    clientes_nomes.append(d[0]) #para imprimir na lista de clientes

    #atualiza a lista dos clientes no display
    atualisa_lista_clientes(clientes_nomes) 

    #envia menssagem enquanto estiver conectado
    while True:
        data = cliente_conexao.recv(4096).decode() #fica esperando alguma menssagem do cliente
        if not data:
            break
        cliente_msg = data
        manda_nome_cliente = d[0]
        for c in salas[d[1]]: 
            if c != cliente_conexao:
                msg_server = str(manda_nome_cliente + "->" + cliente_msg)
                c.send(msg_server.encode())

    ind = 0
    for i in clientes_nomes:
        if i == d[0]:
            del clientes_nomes[ind]
            break
        ind = ind + 1
    for c in salas[d[1]]:
        if c == cliente_conexao:
            del c
    msg_server = "Até mais!"
    cliente_conexao.send(msg_server.encode())
    cliente_conexao.close()
    atualisa_lista_clientes(clientes_nomes)

    
def atualisa_lista_clientes(nome_lista):
    display.config(state=tk.NORMAL)
    display.delete('1.0', tk.END)

    for c in nome_lista:
        display.insert(tk.END, str(c) + "\n")
    display.config(state=tk.DISABLED)


def atualiza_lista_grupo():
    displayGr.config(state=tk.NORMAL)
    displayGr.delete('1.0', tk.END)
    gruposBD = consultaGrupos()
    for g in gruposBD:
        displayGr.insert(tk.END, str(g[1]) + "\n")
    displayGr.config(state=tk.DISABLED)


def mensagemPrivada():
    pass


def banirUsuario():
    pass

    #poller = select.poll()



'''poller = select.poll()
poller.register(socket_1, select.POLLIN)
poller.register(socket_2, select.POLLIN)'''

tela_server.mainloop()