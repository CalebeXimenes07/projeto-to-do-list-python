from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys

uri = "mongodb+srv://CalebeXimenes:admin@cluster0.w29zt4w.mongodb.net/?appName=Cluster0"

# Variáveis globais para controle de conexão
db = None
colecao = None
conexao_ok = False

def conectar_bd():
    global db, colecao, conexao_ok
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("Conectado com sucesso!")
        db = client['ListaToDoDB']
        colecao = db['tarefas']
        conexao_ok = True
        return True
    except Exception as erro:
        print(f"Erro de conexão: {erro}")
        conexao_ok = False
        return False

# Tentar conectar ao iniciar
conectar_bd()

def adicionar_tarefas(descricao, prioridade):
    global conexao_ok
    if not conexao_ok and not conectar_bd():
        raise Exception("Não foi possível conectar ao banco de dados")
    
    try:
        colecao.insert_one({"descricao": descricao, "prioridade": prioridade})
        print("Tarefa Adicionada!")
        return True
    except Exception as error:
        print(f'Erro {error} ao adicionar tarefa!')
        conexao_ok = False
        raise

def listar_tarefas():
    global conexao_ok
    if not conexao_ok and not conectar_bd():
        raise Exception("Não foi possível conectar ao banco de dados")
    
    try:
        tarefas = list(colecao.find())
        for tarefa in tarefas:
            print(f"Descrição: {tarefa['descricao']}\nPrioridade: {tarefa['prioridade']}")
        return tarefas
    except Exception as error:
        print(f'Erro {error} ao listar tarefas!')
        conexao_ok = False
        raise

def excluir_tarefa(id_tarefa):
    global conexao_ok
    if not conexao_ok and not conectar_bd():
        raise Exception("Não foi possível conectar ao banco de dados")
    
    try:
        resultado = colecao.delete_one({"_id": id_tarefa})
        if resultado.deleted_count > 0:
            print("Tarefa excluída com sucesso!")
            return True
        else:
            print("Tarefa não encontrada.")
            return False
    except Exception as error:
        print(f'Erro {error} ao excluir tarefa!')
        conexao_ok = False
        return False

