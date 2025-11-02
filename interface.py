import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from database import adicionar_tarefas, listar_tarefas
import sys

# Configuração do tema customtkinter
ctk.set_appearance_mode("Dark")  # Usando tema escuro para uma aparência mais moderna
ctk.set_default_color_theme("green")  # Tema verde para destacar elementos importantes

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela principal
        self.title("Lista de Tarefas")
        self.geometry("800x600")
        self.minsize(600, 500)
        
        # Configuração do grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Criação do frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Configuração do grid do frame principal
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)  # Título
        self.main_frame.grid_rowconfigure(1, weight=0)  # Formulário
        self.main_frame.grid_rowconfigure(2, weight=1)  # Lista de tarefas
        
        # Título com estilo melhorado
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="ew")
        self.title_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="✓ Gerenciador de Tarefas", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2CC985", "#2CC985")  # Cor verde para destacar
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Subtítulo
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Organize suas tarefas de forma eficiente",
            font=ctk.CTkFont(size=14),
            text_color=("gray70", "gray70")
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        # Frame do formulário com estilo melhorado
        self.form_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.form_frame.grid(row=1, column=0, padx=20, pady=15, sticky="ew")
        
        # Configuração do grid do formulário
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(2, weight=0)
        
        # Título do formulário
        self.form_title = ctk.CTkLabel(
            self.form_frame, 
            text="✨ Nova Tarefa", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#2CC985", "#2CC985")
        )
        self.form_title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 5), sticky="w")
        
        # Campos do formulário
        self.descricao_label = ctk.CTkLabel(self.form_frame, text="📝 Descrição:", font=ctk.CTkFont(weight="bold"))
        self.descricao_label.grid(row=1, column=0, padx=15, pady=(10, 5), sticky="w")
        
        self.descricao_entry = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Digite a descrição da tarefa...",
            height=35,
            corner_radius=8,
            fg_color="#2b2b2b",  # Cor de fundo escura
            border_color="#2CC985",  # Borda verde
            text_color="white"  # Texto branco
        )
        self.descricao_entry.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        self.prioridade_label = ctk.CTkLabel(self.form_frame, text="🔔 Prioridade:", font=ctk.CTkFont(weight="bold"))
        self.prioridade_label.grid(row=1, column=1, padx=15, pady=(10, 5), sticky="w")
        
        self.prioridade_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=["Baixa", "Média", "Alta"],
            height=35,
            corner_radius=8,
            fg_color="#2b2b2b",  # Cor de fundo escura
            border_color="#2CC985",  # Borda verde
            button_color="#2CC985",  # Cor do botão dropdown
            button_hover_color="#25a06e",  # Cor do botão ao passar o mouse
            dropdown_fg_color="#2b2b2b",  # Cor de fundo do dropdown
            dropdown_hover_color="#3c3c3c",  # Cor de hover do dropdown
            dropdown_text_color="white"  # Cor do texto do dropdown
        )
        self.prioridade_combobox.set("Média")
        self.prioridade_combobox.grid(row=2, column=1, padx=15, pady=(0, 15), sticky="ew")
        
        self.adicionar_button = ctk.CTkButton(
            self.form_frame, 
            text="➕ Adicionar Tarefa", 
            command=self.adicionar_tarefa,
            fg_color="#2CC985",
            hover_color="#25a06e",
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold")
        )
        self.adicionar_button.grid(row=2, column=2, padx=15, pady=(0, 15), sticky="e")
        
        # Frame da lista de tarefas
        self.list_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.list_frame.grid(row=2, column=0, padx=20, pady=15, sticky="nsew")
        
        # Configuração do grid da lista
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=0)  # Título da lista
        self.list_frame.grid_rowconfigure(1, weight=1)  # Tabela
        
        # Cabeçalho da lista com ícone
        self.list_header = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.list_header.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")
        self.list_header.grid_columnconfigure(1, weight=1)
        
        # Ícone da lista
        self.list_icon_label = ctk.CTkLabel(
            self.list_header,
            text="📋",
            font=ctk.CTkFont(size=22)
        )
        self.list_icon_label.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="w")
        
        # Título da lista
        self.list_title = ctk.CTkLabel(
            self.list_header, 
            text="Tarefas Cadastradas", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2CC985", "#2CC985")
        )
        self.list_title.grid(row=0, column=1, padx=0, pady=0, sticky="w")
        
        # Frame para botões
        self.buttons_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="e")
        
        # Botão de atualizar
        self.refresh_button = ctk.CTkButton(
            self.buttons_frame, 
            text="🔄 Atualizar", 
            command=self.atualizar_lista,
            width=100,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold", size=12)
        )
        self.refresh_button.grid(row=0, column=0, padx=(0, 10), pady=0)
        
        # Botão de excluir
        self.delete_button = ctk.CTkButton(
            self.buttons_frame, 
            text="🗑️ Excluir", 
            command=self.excluir_tarefa_selecionada,
            fg_color="#dc3545",
            hover_color="#c82333",
            width=100,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold", size=12)
        )
        self.delete_button.grid(row=0, column=1, padx=0, pady=0)
        
        # Criação da tabela de tarefas (usando Treeview do ttk)
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Tema mais customizável
        self.style.configure("Treeview", 
                             background="#2b2b2b", 
                             foreground="white", 
                             rowheight=35,  # Linhas mais altas
                             fieldbackground="#2b2b2b")
        self.style.map('Treeview', background=[('selected', '#2CC985')])  # Cor de seleção verde
        self.style.configure("Treeview.Heading", 
                             background="#1f1f1f", 
                             foreground="#2CC985", 
                             relief="flat",
                             font=('Arial', 10, 'bold'))
        # Remover completamente o fundo branco da tabela
        self.style.configure("Treeview.Item", background="#2b2b2b")
        self.style.configure("Treeview.Cell", background="#2b2b2b")
                             
        # Configuração adicional para corrigir cores
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove bordas
        
        # Configurar cores para todos os elementos do Treeview
        self.style.map("Treeview", 
                      background=[("selected", "#2CC985")],
                      foreground=[("selected", "white")])
                      
        # Configurar cores para o cabeçalho
        self.style.map("Treeview.Heading",
                      background=[("active", "#2b2b2b"), ("!active", "#1f1f1f")],
                      foreground=[("active", "#2CC985"), ("!active", "#2CC985")])
                      
        # Configuração adicional para eliminar todas as bordas brancas
        try:
            self.option_add("*TCombobox*Listbox*Background", "#2b2b2b")
            self.option_add("*TCombobox*Listbox*Foreground", "white")
            self.option_add("*TCombobox*Listbox*selectBackground", "#2CC985")
            self.option_add("*TCombobox*Listbox*selectForeground", "white")
        except Exception:
            pass  # Ignorar erros de configuração de opções
        
        # Remover bordas brancas da tabela e configurar cores de fundo
        self.style.configure("Treeview", 
                            borderwidth=0, 
                            highlightthickness=0,
                            background="#2b2b2b",
                            fieldbackground="#2b2b2b")
        self.style.configure("Treeview.Heading", 
                            borderwidth=0, 
                            highlightthickness=0,
                            background="#1f1f1f",
                            foreground="#2CC985")
        
        # Frame para a tabela com scrollbar
        self.table_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.table_frame.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Criação da tabela
        self.tree = ttk.Treeview(self.table_frame, columns=("id", "descricao", "prioridade"), show="headings", style="dark.Treeview")
        self.tree.heading("id", text="ID")
        self.tree.heading("descricao", text="✏️ Descrição")
        self.tree.heading("prioridade", text="⚠️ Prioridade")
        self.tree.column("id", width=0, stretch=tk.NO)  # Coluna oculta para armazenar o ID
        self.tree.column("descricao", width=400)
        self.tree.column("prioridade", width=120)
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Criar estilo específico para esta tabela
        self.style.configure("dark.Treeview", 
                            background="#2b2b2b", 
                            fieldbackground="#2b2b2b", 
                            foreground="white",
                            borderwidth=0,
                            highlightthickness=0)
        
        # Aplicar tag para todas as linhas com fundo escuro
        self.tree.tag_configure('dark_bg', background='#2b2b2b')
        
        # Garantir que todas as linhas usem a tag dark_bg
        def fixar_cores(event):
            for item in self.tree.get_children():
                self.tree.item(item, tags=('dark_bg',))
        
        # Vincular eventos para garantir que as cores sejam aplicadas
        self.tree.bind('<<TreeviewOpen>>', fixar_cores)
        self.tree.bind('<<TreeviewSelect>>', fixar_cores)
        self.after(100, lambda: fixar_cores(None))
        
        # Configuração adicional para corrigir cores de fundo
        self.style.configure('Treeview', 
                            fieldbackground='#2b2b2b',  # Cor de fundo dos campos
                            background='#2b2b2b')       # Cor de fundo geral
        
        # Adicionar menu de contexto para excluir tarefas
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Excluir Tarefa", command=self.excluir_tarefa_selecionada)
        self.tree.bind("<Button-3>", self.mostrar_menu_contexto)
        
        # Scrollbar personalizada com CTkScrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.table_frame, 
            command=self.tree.yview,
            button_color="#2CC985",
            button_hover_color="#25a06e",
            fg_color="#1f1f1f"
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Carregar tarefas iniciais
        self.atualizar_lista()
    
    def adicionar_tarefa(self):
        descricao = self.descricao_entry.get()
        prioridade = self.prioridade_combobox.get()
        
        if not descricao:
            messagebox.showerror("Erro", "A descrição da tarefa não pode estar vazia!")
            return
        
        try:
            adicionar_tarefas(descricao, prioridade)
            self.descricao_entry.delete(0, tk.END)
            self.prioridade_combobox.set("Média")
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar tarefa: {e}")
    
    def mostrar_menu_contexto(self, event):
        # Selecionar o item sob o cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def on_tree_hover(self, event):
        """Adiciona efeito de hover na tabela."""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            self.tree.config(cursor="hand2")  # Muda o cursor para mão
        else:
            self.tree.config(cursor="")  # Restaura o cursor padrão
            
    def excluir_tarefa_selecionada(self):
        # Obter o item selecionado
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para excluir!")
            return
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta tarefa?"):
            try:
                # Obter o ID da tarefa selecionada
                item = selecionado[0]
                id_tarefa = self.tree.item(item, "values")[0]
                
                # Importar função de exclusão
                from database import excluir_tarefa
                from bson.objectid import ObjectId
                
                # Excluir tarefa
                if excluir_tarefa(ObjectId(id_tarefa)):
                    self.tree.delete(item)
                    messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso!")
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir a tarefa.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir tarefa: {e}")
    
    def atualizar_lista(self):
        # Limpar a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Obter tarefas do banco de dados
            from database import listar_tarefas, conectar_bd
            
            # Tentar reconectar se necessário
            try:
                tarefas = listar_tarefas()
            except Exception:
                if not conectar_bd():
                    messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados. Verifique sua conexão com a internet.")
                    return
                tarefas = listar_tarefas()
            
            # Adicionar tarefas à tabela
            for tarefa in tarefas:
                # Converter o ObjectId para string para exibição
                id_str = str(tarefa['_id'])
                self.tree.insert("", tk.END, values=(id_str, tarefa['descricao'], tarefa['prioridade']))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tarefas: {e}")

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()