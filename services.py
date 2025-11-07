"""
Camada de serviços: contém a lógica de negócio da aplicação de tarefas,
fazendo ponte entre a interface e o acesso ao banco (database.py).

Responsabilidades:
- Normalizar dados vindos da UI
- Orquestrar chamadas ao banco
- Fornecer uma API simples para a interface
"""

from typing import List, Optional, Dict, Any
from bson.objectid import ObjectId

from database import (
    adicionar_tarefas,
    listar_tarefas,
    atualizar_tarefa,
    excluir_tarefa,
    obter_estatisticas,
)


def criar_tarefa(descricao: str, prioridade: str, prazo: Optional[str] = None) -> bool:
    """Cria uma tarefa com validação mínima de dados."""
    descricao = descricao.strip()
    prioridade = prioridade.strip()
    prazo = prazo.strip() if prazo else None

    if not descricao:
        raise ValueError("Descrição não pode estar vazia")
    if prioridade not in {"Baixa", "Média", "Alta"}:
        raise ValueError("Prioridade inválida")

    return adicionar_tarefas(descricao, prioridade, prazo)


def obter_tarefas(filtro: Optional[str] = None) -> List[Dict[str, Any]]:
    """Obtém tarefas do repositório aplicando filtro opcional."""
    return listar_tarefas(filtro)


def editar_tarefa(
    id_tarefa,
    descricao: Optional[str] = None,
    prioridade: Optional[str] = None,
    prazo: Optional[str] = None,
    concluida: Optional[bool] = None,
) -> bool:
    """Atualiza uma tarefa existente."""
    if prioridade is not None and prioridade not in {"Baixa", "Média", "Alta"}:
        raise ValueError("Prioridade inválida")
    if descricao is not None:
        descricao = descricao.strip()
    if prazo is not None:
        prazo = prazo.strip()

    # Garantir que o ID seja do tipo ObjectId
    oid = ObjectId(id_tarefa) if not isinstance(id_tarefa, ObjectId) else id_tarefa
    return atualizar_tarefa(oid, descricao, prioridade, prazo, concluida)


def remover_tarefa(id_tarefa) -> bool:
    """Remove uma tarefa pelo ID."""
    oid = ObjectId(id_tarefa) if not isinstance(id_tarefa, ObjectId) else id_tarefa
    return excluir_tarefa(oid)


def estatisticas() -> Dict[str, Any]:
    """Retorna estatísticas agregadas das tarefas."""
    return obter_estatisticas()