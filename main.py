from database import adicionar_tarefas
from database import listar_tarefas

print("Testando código")
entrada_descricao = input("Insira a descrição do sua tarefa: ")
entrada_prioridade = input("Insira a prioridade da sua tarefa: ")

adicionar_tarefas(entrada_descricao, entrada_prioridade)

print("Lista das Tarefas inseridas:\n")

listar_tarefas()
