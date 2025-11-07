import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from tkcalendar import Calendar
from services import (
    criar_tarefa,
    obter_tarefas,
    editar_tarefa,
    remover_tarefa,
    estatisticas,
)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Lista de Tarefas")
        self.geometry("1280x720")
        self.minsize(800, 600)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Título
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="ew")
        self.title_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="Gerenciador de Tarefas", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2CC985", "#2CC985")
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Formulário
        self.form_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.form_frame.grid(row=1, column=0, padx=20, pady=15, sticky="ew")
        self.form_frame.grid_columnconfigure(0, weight=2)
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(2, weight=1)
        self.form_frame.grid_columnconfigure(3, weight=0)
        
        self.descricao_label = ctk.CTkLabel(self.form_frame, text="Descrição:", font=ctk.CTkFont(weight="bold"))
        self.descricao_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.descricao_entry = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Digite a descrição da tarefa...",
            height=35,
            corner_radius=8,
            fg_color="#2b2b2b",
            border_color="#2CC985",
            text_color="white"
        )
        self.descricao_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        self.prioridade_label = ctk.CTkLabel(self.form_frame, text="Prioridade:", font=ctk.CTkFont(weight="bold"))
        self.prioridade_label.grid(row=0, column=1, padx=15, pady=(15, 5), sticky="w")
        
        self.prioridade_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=["Baixa", "Média", "Alta"],
            height=35,
            corner_radius=8,
            fg_color="#2b2b2b",
            border_color="#2CC985",
            button_color="#2CC985",
            button_hover_color="#25a06e",
            dropdown_fg_color="#2b2b2b",
            dropdown_hover_color="#3c3c3c",
            dropdown_text_color="white"
        )
        self.prioridade_combobox.set("Média")
        self.prioridade_combobox.grid(row=1, column=1, padx=15, pady=(0, 15), sticky="ew")


            
        self.prazo_label = ctk.CTkLabel(self.form_frame, text="Prazo:", font=ctk.CTkFont(weight="bold"))
        self.prazo_label.grid(row=0, column=2, padx=15, pady=(15, 5), sticky="w")
            
        # Botão para abrir o calendário (sem campo de entrada)
        self.calendar_button = ctk.CTkButton(
            self.form_frame,
            text="Selecionar Data 📅",
            height=35,
            command=self.abrir_calendario,
            fg_color="#2CC985",
            hover_color="#25a06e",
            corner_radius=8
        )
        self.calendar_button.grid(row=1, column=2, padx=15, pady=(0, 15), sticky="ew")
        
        # Label para mostrar a data selecionada
        self.data_selecionada_label = ctk.CTkLabel(
            self.form_frame,
            text="Nenhuma data selecionada",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.data_selecionada_label.grid(row=2, column=2, padx=15, pady=(0, 5), sticky="w")
        
        self.adicionar_button = ctk.CTkButton(
            self.form_frame, 
            text="Adicionar Tarefa", 
            command=self.adicionar_tarefa,
            fg_color="#2CC985",
            hover_color="#25a06e",
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold")
        )
        self.adicionar_button.grid(row=1, column=3, padx=15, pady=(0, 15), sticky="e")
        
        # Lista de tarefas
        self.list_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.list_frame.grid(row=2, column=0, padx=20, pady=15, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(2, weight=1)
        
        # Cabeçalho com título
        self.list_header = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.list_header.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")
        self.list_header.grid_columnconfigure(0, weight=1)
        
        self.list_title = ctk.CTkLabel(
            self.list_header, 
            text="Tarefas Cadastradas", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2CC985", "#2CC985")
        )
        self.list_title.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        
        # Filtros e botões
        self.controls_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.controls_frame.grid(row=1, column=0, padx=15, pady=(5, 5), sticky="ew")
        self.controls_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para filtros
        self.filters_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.filters_frame.grid(row=0, column=0, sticky="w")
        
        self.filtro_label = ctk.CTkLabel(self.filters_frame, text="Filtrar:", font=ctk.CTkFont(weight="bold"))
        self.filtro_label.grid(row=0, column=0, padx=(0, 10), pady=0)
        
        self.filtro_combobox = ctk.CTkComboBox(
            self.filters_frame,
            values=["Todas", "Baixa", "Média", "Alta"],
            width=120,
            height=30,
            corner_radius=8,
            command=self.aplicar_filtro
        )
        self.filtro_combobox.set("Todas")
        self.filtro_combobox.grid(row=0, column=1, padx=(0, 10), pady=0)
        
        # Frame para botões de ação
        self.buttons_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=1, sticky="e")
        
        self.edit_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Editar", 
            command=self.editar_tarefa_selecionada,
            width=80,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold", size=12)
        )
        self.edit_button.grid(row=0, column=0, padx=(0, 10), pady=0)
        
        self.concluir_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Concluir", 
            command=self.marcar_concluida,
            fg_color="#28a745",
            hover_color="#218838",
            width=80,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold", size=12)
        )
        self.concluir_button.grid(row=0, column=1, padx=(0, 10), pady=0)
        
        self.refresh_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Atualizar", 
            command=self.atualizar_lista,
            width=80,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold", size=12)
        )
        self.refresh_button.grid(row=0, column=2, padx=(0, 10), pady=0)
        
        self.delete_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Excluir", 
            command=self.excluir_tarefa_selecionada,
            fg_color="#dc3545",
            hover_color="#c82333",
            width=80,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold", size=12)
        )
        self.delete_button.grid(row=0, column=3, padx=0, pady=0)
        
        # Tabela de tarefas
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", 
                             background="#2b2b2b", 
                             foreground="white", 
                             rowheight=35,
                             fieldbackground="#2b2b2b",
                             borderwidth=0,
                             highlightthickness=0)
        self.style.map('Treeview', 
                       background=[('selected', '#2CC985')],
                       foreground=[('selected', 'white')])
        self.style.configure("Treeview.Heading", 
                             background="#1f1f1f", 
                             foreground="#2CC985", 
                             relief="flat",
                             font=('Arial', 10, 'bold'))
        
        # Frame para a tabela com scrollbar
        self.table_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.table_frame.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Criação da tabela
        self.tree = ttk.Treeview(self.table_frame, columns=("id", "descricao", "prioridade", "prazo", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("prioridade", text="Prioridade")
        self.tree.heading("prazo", text="Prazo")
        self.tree.heading("status", text="Status")
        self.tree.column("id", width=0, stretch=tk.NO)
        self.tree.column("descricao", width=300, anchor="center")
        self.tree.column("prioridade", width=80, anchor="center")
        self.tree.column("prazo", width=100, anchor="center")
        self.tree.column("status", width=80, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")
        

        
        # Adicionar menu de contexto para excluir tarefas
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Excluir Tarefa", command=self.excluir_tarefa_selecionada)
        self.tree.bind("<Button-3>", self.mostrar_menu_contexto)
        
        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.table_frame, command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.atualizar_lista()
    
    def aplicar_filtro(self, filtro):
        if filtro == "Todas":
            self.atualizar_lista()
        elif filtro in ["Baixa", "Média", "Alta"]:
            self.atualizar_lista(filtro)
    
    def editar_tarefa_selecionada(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para editar!")
            return
        
        item = selecionado[0]
        valores = self.tree.item(item, "values")
        
        # Criar janela de edição
        self.janela_edicao = ctk.CTkToplevel(self)
        self.janela_edicao.title("Editar Tarefa")
        self.janela_edicao.geometry("400x300")
        self.janela_edicao.transient(self)
        self.janela_edicao.grab_set()
        
        # Campos de edição
        ctk.CTkLabel(self.janela_edicao, text="Descrição:").pack(pady=(20, 5), padx=20, anchor="w")
        self.edit_descricao = ctk.CTkEntry(self.janela_edicao)
        self.edit_descricao.pack(pady=(0, 10), padx=20, fill="x")
        self.edit_descricao.insert(0, valores[1])
        
        ctk.CTkLabel(self.janela_edicao, text="Prioridade:").pack(pady=(10, 5), padx=20, anchor="w")
        self.edit_prioridade = ctk.CTkComboBox(self.janela_edicao, values=["Baixa", "Média", "Alta"])
        self.edit_prioridade.pack(pady=(0, 10), padx=20, fill="x")
        self.edit_prioridade.set(valores[2])
        
        ctk.CTkLabel(self.janela_edicao, text="Prazo:").pack(pady=(10, 5), padx=20, anchor="w")
        
        # Botão para abrir o calendário na janela de edição (sem campo de entrada)
        self.edit_calendar_button = ctk.CTkButton(
            self.janela_edicao,
            text="Selecionar Data 📅",
            command=lambda: self.abrir_calendario_edicao(),
            fg_color="#2CC985",
            hover_color="#25a06e",
            corner_radius=8
        )
        self.edit_calendar_button.pack(pady=(0, 10), padx=20, fill="x")
        
        # Label para mostrar a data selecionada na edição
        self.edit_data_selecionada_label = ctk.CTkLabel(
            self.janela_edicao,
            text=f"Data: {valores[3]}" if valores[3] else "Nenhuma data selecionada",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.edit_data_selecionada_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Armazena a data atual da tarefa
        self.edit_data_selecionada = valores[3] if valores[3] else None
        
        # Botões
        button_frame = ctk.CTkFrame(self.janela_edicao, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkButton(
            button_frame, 
            text="Salvar", 
            command=lambda: self.salvar_edicao(item, valores[0])
        ).pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        ctk.CTkButton(
            button_frame, 
            text="Cancelar", 
            command=self.janela_edicao.destroy,
            fg_color="gray"
        ).pack(side="right", fill="x", expand=True)
    
    def salvar_edicao(self, item, id_tarefa):
        try:
            descricao = self.edit_descricao.get()
            prioridade = self.edit_prioridade.get()
            prazo = getattr(self, 'edit_data_selecionada', None)  # Usa a data armazenada
            
            if not descricao:
                messagebox.showerror("Erro", "Descrição não pode estar vazia!")
                return
            
            if editar_tarefa(
                id_tarefa, 
                descricao=descricao, 
                prioridade=prioridade, 
                prazo=prazo if prazo else None
            ):
                self.janela_edicao.destroy()
                self.atualizar_lista()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar tarefa: {e}")
    
    def marcar_concluida(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para concluir!")
            return
        
        if messagebox.askyesno("Confirmar", "Marcar esta tarefa como concluída?"):
            try:
                item = selecionado[0]
                valores = self.tree.item(item, "values")
                id_tarefa = valores[0]
                
                if editar_tarefa(id_tarefa, concluida=True):
                    self.atualizar_lista()
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao concluir tarefa: {e}")
    
    def adicionar_tarefa(self):
        descricao = self.descricao_entry.get()
        prioridade = self.prioridade_combobox.get()
        prazo = getattr(self, 'data_selecionada', None)  # Usa a data armazenada
        
        if not descricao:
            messagebox.showerror("Erro", "Descrição não pode estar vazia!")
            return
        
        try:
            criar_tarefa(descricao, prioridade, prazo if prazo else None)
            self.descricao_entry.delete(0, tk.END)
            # Limpa a data selecionada
            if hasattr(self, 'data_selecionada'):
                delattr(self, 'data_selecionada')
            self.data_selecionada_label.configure(text="Nenhuma data selecionada")
            self.prioridade_combobox.set("Média")
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar tarefa: {e}")
    
    def mostrar_menu_contexto(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
            
    def excluir_tarefa_selecionada(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para excluir!")
            return
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta tarefa?"):
            try:
                item = selecionado[0]
                id_tarefa = self.tree.item(item, "values")[0]
                
                if remover_tarefa(id_tarefa):
                    self.tree.delete(item)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir tarefa: {e}")
    
    def atualizar_lista(self, filtro=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            tarefas = obter_tarefas(filtro)
            for tarefa in tarefas:
                id_str = str(tarefa['_id'])
                prazo = tarefa.get('prazo', '') or ''
                status = "Concluída" if tarefa.get('concluida', False) else "Pendente"
                self.tree.insert("", tk.END, values=(id_str, tarefa['descricao'], tarefa['prioridade'], prazo, status))
            
            # Atualizar estatísticas
            self.atualizar_estatisticas()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tarefas: {e}")
    
    def atualizar_estatisticas(self):
        try:
            stats = estatisticas()
            
            if hasattr(self, 'stats_frame'):
                self.stats_frame.destroy()
            
            self.stats_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
            self.stats_frame.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")
            
            # Labels de estatísticas
            stats_text = f"Total: {stats['total']} | Pendentes: {stats['pendentes']} | Concluídas: {stats['concluidas']} | Progresso: {stats['progresso']}%"
            self.stats_label = ctk.CTkLabel(self.stats_frame, text=stats_text, font=ctk.CTkFont(size=12))
            self.stats_label.pack(pady=10)
            
            # Barra de progresso
            self.progress_bar = ctk.CTkProgressBar(self.stats_frame)
            self.progress_bar.set(stats['progresso'] / 100)
            self.progress_bar.pack(pady=(0, 10), padx=20, fill="x")
            
        except Exception as e:
            print(f"Erro ao atualizar estatísticas: {e}")
    
    def abrir_calendario(self):
        """Abre uma janela com calendário para selecionar a data"""
        # Criar janela de calendário
        self.calendario_janela = ctk.CTkToplevel(self)
        self.calendario_janela.title("Selecionar Data")
        self.calendario_janela.geometry("300x300")
        self.calendario_janela.transient(self)
        self.calendario_janela.grab_set()
        
        # Centralizar a janela
        self.calendario_janela.update_idletasks()
        x = (self.calendario_janela.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.calendario_janela.winfo_screenheight() // 2) - (300 // 2)
        self.calendario_janela.geometry(f"300x300+{x}+{y}")
        
        # Criar calendário
        self.calendario = Calendar(
            self.calendario_janela,
            selectmode='day',
            date_pattern='dd/mm/yyyy',
            background='#2b2b2b',
            foreground='white',
            headersbackground='#2CC985',
            headersforeground='white',
            selectbackground='#2CC985',
            selectforeground='white',
            normalbackground='#2b2b2b',
            normalforeground='white',
            weekendbackground='#2b2b2b',
            weekendforeground='white'
        )
        self.calendario.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Frame para os botões
        botoes_frame = ctk.CTkFrame(self.calendario_janela, fg_color="transparent")
        botoes_frame.pack(pady=10, padx=20, fill='x')
        
        # Botão Selecionar
        ctk.CTkButton(
            botoes_frame,
            text="Selecionar",
            command=self.selecionar_data,
            fg_color="#2CC985",
            hover_color="#25a06e"
        ).pack(side="left", padx=(0, 10), fill='x', expand=True)
        
        # Botão Cancelar
        ctk.CTkButton(
            botoes_frame,
            text="Cancelar",
            command=self.calendario_janela.destroy,
            fg_color="gray"
        ).pack(side="right", fill='x', expand=True)
    
    def selecionar_data(self):
        """Seleciona a data do calendário e atualiza o label"""
        data_selecionada = self.calendario.get_date()
        self.data_selecionada = data_selecionada  # Armazena a data selecionada
        self.data_selecionada_label.configure(text=f"Data: {data_selecionada}")
        self.calendario_janela.destroy()
    
    def abrir_calendario_edicao(self):
        """Abre o calendário para a janela de edição"""
        # Criar janela de calendário
        self.calendario_janela = ctk.CTkToplevel(self.janela_edicao)
        self.calendario_janela.title("Selecionar Data")
        self.calendario_janela.geometry("300x300")
        self.calendario_janela.transient(self.janela_edicao)
        self.calendario_janela.grab_set()
        
        # Centralizar a janela
        self.calendario_janela.update_idletasks()
        x = (self.calendario_janela.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.calendario_janela.winfo_screenheight() // 2) - (300 // 2)
        self.calendario_janela.geometry(f"300x300+{x}+{y}")
        
        # Criar calendário
        self.calendario = Calendar(
            self.calendario_janela,
            selectmode='day',
            date_pattern='dd/mm/yyyy',
            background='#2b2b2b',
            foreground='white',
            headersbackground='#2CC985',
            headersforeground='white',
            selectbackground='#2CC985',
            selectforeground='white',
            normalbackground='#2b2b2b',
            normalforeground='white',
            weekendbackground='#2b2b2b',
            weekendforeground='white'
        )
        self.calendario.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Frame para os botões
        botoes_frame = ctk.CTkFrame(self.calendario_janela, fg_color="transparent")
        botoes_frame.pack(pady=10, padx=20, fill='x')
        
        # Botão Selecionar
        ctk.CTkButton(
            botoes_frame,
            text="Selecionar",
            command=self.selecionar_data_edicao,
            fg_color="#2CC985",
            hover_color="#25a06e"
        ).pack(side="left", padx=(0, 10), fill='x', expand=True)
        
        # Botão Cancelar
        ctk.CTkButton(
            botoes_frame,
            text="Cancelar",
            command=self.calendario_janela.destroy,
            fg_color="gray"
        ).pack(side="right", fill='x', expand=True)
    
    def selecionar_data_edicao(self):
        """Seleciona a data do calendário e atualiza o label na edição"""
        data_selecionada = self.calendario.get_date()
        self.edit_data_selecionada = data_selecionada  # Armazena a data selecionada
        self.edit_data_selecionada_label.configure(text=f"Data: {data_selecionada}")
        self.calendario_janela.destroy()
            
# Inicialização movida para app.py (run_app)