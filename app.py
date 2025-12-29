import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

st.set_page_config(
    page_title="To-Do List",
)

ARQUIVO_DADOS = "tarefas.csv"

if not os.path.exists(ARQUIVO_DADOS):
    df_vazio = pd.DataFrame(columns=[
        "Atividade",
        "Prioridade",
        "Data da atividade",
        "Criado em"
    ])
    df_vazio.to_csv(ARQUIVO_DADOS, index=False)

col_esquerda, col_centro, col_direita = st.columns([1, 25, 1])

aba_cadastro, aba_dashboard = st.tabs(["Nova Tarefa", "Minhas Tarefas"])

with col_centro:

    with aba_cadastro:
        st.title("To-Do List")

        atividade = st.text_input("Atividade a ser realizada")

        prioridade = st.selectbox(
            "Prioridade",
            ("Baixa", "Média", "Alta")
        )

        data_atividade = st.date_input(
            "Data da atividade",
            value=date.today()
        )

        travar_botao = atividade.strip() == ""

        if st.button("Salvar tarefa", disabled=travar_botao):
            nova_linha = pd.DataFrame([{
                "Atividade": atividade,
                "Prioridade": prioridade,
                "Data da atividade": data_atividade.strftime("%d/%m/%Y"),
                "Criado em": datetime.now().strftime("%d/%m/%Y %H:%M")
            }])

            escrever_cabecalho = not os.path.exists(ARQUIVO_DADOS)

            nova_linha.to_csv(
                ARQUIVO_DADOS,
                mode="a",
                index=False,
                header=escrever_cabecalho
            )

            st.success("Tarefa salva com sucesso!")

        if st.button("Limpar tarefas"):
            if os.path.exists(ARQUIVO_DADOS):
                os.remove(ARQUIVO_DADOS)
                st.success("Todas as tarefas foram removidas!")
            else:
                st.info("Nenhuma tarefa para remover.")

    with aba_dashboard:
        st.title("Minhas Tarefas")

        if not os.path.exists(ARQUIVO_DADOS):
            st.warning("Nenhuma tarefa cadastrada ainda.")
            st.stop()

        df = pd.read_csv(
            ARQUIVO_DADOS,
            sep=",",
            engine="python"
        )

        if st.checkbox("Mostrar tabela"):
            st.dataframe(df, hide_index=True)

        st.divider()

        prioridade_filtro = st.selectbox(
            "Filtrar por prioridade",
            ("Todas", "Baixa", "Média", "Alta")
        )

        if prioridade_filtro == "Todas":
            df_filtrado = df
        else:
            df_filtrado = df[df["Prioridade"] == prioridade_filtro]

        contagem_prioridade = df_filtrado["Prioridade"].value_counts()

        if st.checkbox("Mostrar gráfico"):
            st.bar_chart(contagem_prioridade)
