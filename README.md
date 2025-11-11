# 🚀 Gerenciador de Tarefas (To-Do List) - Interface Gráfica (Tkinter)

Aplicação GUI para gerenciamento de tarefas com **CustomTkinter**, seleção de datas via **TKcalendar** e persistência em **MongoDB**.

**Status do Projeto:** ✅ Em uso

## 📝 Sobre o Projeto

Este projeto fornece um gerenciador de tarefas moderno com interface gráfica, suporte a filtros, edição, conclusão e exclusão de tarefas. O prazo pode ser selecionado facilmente via calendário.

## ✨ Funcionalidades Principais

* **Sistema de Tarefas Completo:**
    * Adicionar novas tarefas com descrição.
    * Categorizar por prioridade (Alta, Média, Baixa).
    * Definir prazos (opcional).
* **Operações de Gerenciamento (CRUD):**
    * **Create:** Adicionar novas tarefas.
    * **Read:** Visualizar tarefas com filtros avançados.
    * **Update:** Editar tarefas existentes e marcar como concluídas.
    * **Delete:** Remover tarefas.
* **Filtros Avançados:**
    * Visualizar todas as tarefas.
    * Visualizar apenas tarefas pendentes.
    * Visualizar apenas tarefas concluídas.
    * Filtrar por prioridade (Alta, Média ou Baixa).
* **Estatísticas e Progresso:**
    * Contador de tarefas totais.
    * Contador de tarefas pendentes e concluídas.
    * Cálculo do progresso geral em porcentagem (%).

## 🛠️ Requisitos Técnicos Aplicados

* **Interface:** GUI com CustomTkinter e TKcalendar.
* **Banco de Dados:** MongoDB Atlas via PyMongo.
* **Arquitetura:** Separação em camadas (UI, Serviços, Banco e Inicializador).
* **Linguagem:** **Python**

## 🧱 Arquitetura (Clean Code)

- `interface.py`: Interface gráfica (GUI) e interação com o usuário.
- `services.py`: Lógica de negócio e orquestração das operações de tarefas.
- `database.py`: Acesso ao banco (MongoDB): conectar, inserir, atualizar, deletar, listar e estatísticas.
- `app.py`: Inicializador da aplicação (`run_app`).
- `main.py`: Entry-point simples que chama `run_app`.

Essa divisão simplifica manutenção, testes e evolução do projeto.

## 🏁 Como Executar o Projeto

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/CalebeXimenes07/projeto-to-do-list.git](https://github.com/CalebeXimenes07/projeto-to-do-list.git)
    ```

2.  Navegue até o diretório do projeto:
    ```bash
    cd projeto-to-do-list
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  Execute o programa:
    ```bash
    python main.py
    ```

5.  Interaja com a interface gráfica. Use o botão 📅 para escolher prazos.

## 👨‍💻 Autor

Feito por **Calebe Ximenes e Iuri Costa**

* **GitHub:** [CalebeXimenes07](https://github.com/CalebeXimenes07)
* **GitHub:** [Iurizero](https://github.com/Iurizero)
