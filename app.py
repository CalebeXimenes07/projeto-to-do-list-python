"""
Inicializador da aplicação: ponto único de entrada para a UI.
"""

from interface import ToDoApp


def run_app():
    app = ToDoApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()