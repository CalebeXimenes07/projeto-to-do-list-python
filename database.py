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

def atualizar_tarefa(id_tarefa, descricao=None, prioridade=None, prazo=None, concluida=None):
    global conexao_ok
    if not conexao_ok and not conectar_bd():
        raise Exception("Não foi possível conectar ao banco de dados")
    
    try:
        update_data = {}
        if descricao is not None:
            update_data["descricao"] = descricao
        if prioridade is not None:
            update_data["prioridade"] = prioridade
        if prazo is not None:
            update_data["prazo"] = prazo
        if concluida is not None:
            update_data["concluida"] = concluida
            
        if update_data:
            resultado = colecao.update_one(
                {"_id": id_tarefa}, 
                {"$set": update_data}
            )
            if resultado.modified_count > 0:
                print("Tarefa atualizada com sucesso!")
                return True
            else:
                print("Tarefa não encontrada.")
                return False
        return False
    except Exception as error:
        print(f'Erro {error} ao atualizar tarefa!')
        conexao_ok = False
        return False

def obter_estatisticas():
    global conexao_ok
    if not conexao_ok and not conectar_bd():
        raise Exception("Não foi possível conectar ao banco de dados")
    
    try:
        total = colecao.count_documents({})
        pendentes = colecao.count_documents({"concluida": False})
        concluidas = colecao.count_documents({"concluida": True})
        
        progresso = 0
        if total > 0:
            progresso = (concluidas / total) * 100
            
        return {
            "total": total,
            "pendentes": pendentes,
            "concluidas": concluidas,
            "progresso": round(progresso, 1)
        }
    except Exception as error:
        print(f'Erro {error} ao obter estatísticas!')
        conexao_ok = False
        return {"total": 0, "pendentes": 0, "concluidas": 0, "progresso": 0}

# Tentar conectar ao iniciar
conectar_bd()

def adicionar_tarefas(descricao, prioridade, prazo=None, concluida=False):
    global conexao_ok
    if not conexao_ok and not conectar_bd():
        raise Exception("Não foi possível conectar ao banco de dados")
    
    try:
        tarefa = {
            "descricao": descricao, 
            "prioridade": prioridade,
            "prazo": prazo,
            "concluida": concluida
        }
        colecao.insert_one(tarefa)
        print("Tarefa Adicionada!")
        return True
    except Exception as error:
        print(f'Erro {error} ao adicionar tarefa!')
        conexao_ok = False
        raise

def listar_tarefas(filtro=None):
    global conexao_ok
    if not conexao_ok and not conectar_bd():
        raise Exception("Não foi possível conectar ao banco de dados")
    
    try:
        query = {}
        if filtro == "pendentes":
            query = {"concluida": False}
        elif filtro == "concluidas":
            query = {"concluida": True}
        elif filtro in ["Baixa", "Média", "Alta"]:
            query = {"prioridade": filtro}
        
        tarefas = list(colecao.find(query))
        for tarefa in tarefas:
            print(f"Descrição: {tarefa['descricao']}\nPrioridade: {tarefa['prioridade']}\nConcluída: {tarefa.get('concluida', False)}")
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

