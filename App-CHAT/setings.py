####CONEXÃO BANCO DE DADOS########
import sqlite3

banco = sqlite3.connect("/home/roberto/Projetos/CHAT-RMI/banco.db")

def abre_banco():
   global banco
   return banco


def  criar_tabela():
    cursor = banco.cursor()
   
    cursor.execute( """CREATE TABLE USUARIOS (
                            ID_USUARIO INTEGER PRIMARY KEY AUTOINCREMENT, 
                            NOME VARCHAR(15), 
                            SOBRENOME VARCHAR(15), 
                            SENHA VARCHAR(10)
                            )
                    """)
    cursor.execute( """CREATE TABLE GRUPO (
                            ID_GRUPO INTEGER PRIMARY KEY AUTOINCREMENT, 
                            NOME VARCHAR(15)
                            )
                    """)

    cursor.execute( """CREATE TABLE BANIDOS (
                            ID_BANIDOS INTEGER PRIMARY KEY AUTOINCREMENT, 
                            NOME VARCHAR(15)
                            )
                    """)

    cursor.close()



def incluir_valores_no_usuario(nome, sobrenome, senha, grupo):
    cursor = banco.cursor()
    cursor.execute('INSERT INTO USUARIOS (NOME, SOBRENOME, SENHA, SK_GRUPO) VALUES(?,?,?,?)', (nome, sobrenome, senha, grupo))
    banco.commit()
    #cursor.close()


def consulta_valores(nome, senha):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM USUARIOS WHERE NOME = ? AND SENHA = ?", (nome, senha))
    res = cursor.fetchone()
    #cursor.close()
    return res


def consultaAll():
    cursor = banco.cursor()
    res = cursor.execute("SELECT * FROM USUARIOS")
    #cursor.close()


def consultaGrupos():
    cursor = banco.cursor()
    res = cursor.execute("SELECT * FROM GRUPO")
    #cursor.close()
    return res


def consultaBanidos():
    cursor = banco.cursor()
    res = cursor.execute("SELECT * FROM BANIDOS")
    #cursor.close()
    return res


def incluirBanidos(nome):
    cursor = banco.cursor()
    cursor.execute("INSERT INTO BANIDOS (NOME) VALUES(?)", (nome,))
    banco.commit()
    #cursor.close()


def incluir_valores_no_grupo(nome):
    cursor = banco.cursor()
    cursor.execute("INSERT INTO GRUPO (NOME) VALUES(?)", (nome,))
    banco.commit()
    #cursor.close()


def fecha_banco():
    banco.close()


def tesbanco():
    cursor = banco.cursor()
    #cursor.execute("INSERT INTO GRUPO (NOME) VALUES('teste7')")
    #banco.commit()
    cursor.close()

#criar_tabela()
#incluir_valores_no_grupo("amigos")
#banco.commit()
#fecha_banco()
#tesbanco()