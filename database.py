from math import degrees

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys

uri = "mongodb+srv://CalebeXimenes:admin@cluster0.w29zt4w.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Conectado com sucesso!")
    db = client['ListaToDoDB']
    colecao = db['tarefas']

except Exception as erro:
    print(erro)
    sys.exit()

def adicionar_tarefas(descricao, prioridade):
    try:
        colecao.insert_one({"descricao": descricao, "prioridade": prioridade})
        print("Tarefa Adicionada!")
    except Exception as error:
        print(f'Erro {error} ao adicionar tarefa!')

def listar_tarefas():
    tarefas = list(colecao.find())
    for tarefa in tarefas:
        print(f"Descrição: {tarefa['descricao']}\nPrioridade: {tarefa['prioridade']}")

