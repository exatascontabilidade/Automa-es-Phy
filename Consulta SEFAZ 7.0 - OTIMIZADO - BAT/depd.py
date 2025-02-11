import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import sys
import threading
import os

# Lista de bibliotecas necessárias
REQUIRED_LIBS = [
    "pandas",
    "selenium",
    "webdriver_manager",
    "openpyxl", 
    "sys",
    "subprocess",
    "threading"
]

def check_and_install_libs(log_widget):
    """
    Verifica e instala as bibliotecas necessárias.
    """
    log_widget.insert(tk.END, "Verificando dependências...\n")
    log_widget.see(tk.END)
    for lib in REQUIRED_LIBS:
        try:
            __import__(lib)
            log_widget.insert(tk.END, f"[Info] Biblioteca '{lib}' já está instalada.\n")
        except ImportError:
            log_widget.insert(tk.END, f"[Info] Biblioteca '{lib}' não encontrada. Instalando...\n")
            log_widget.see(tk.END)
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                log_widget.insert(tk.END, f"[Info] Biblioteca '{lib}' instalada com sucesso.\n")
            except Exception as e:
                log_widget.insert(tk.END, f"[ERRO] Falha ao instalar '{lib}': {e}\n")
        log_widget.see(tk.END)
    log_widget.insert(tk.END, "Verificação completa.\n")
    log_widget.see(tk.END)

def run_dependency_check():
    check_and_install_libs(log_text)

# Cria a janela principal
root = tk.Tk()
root.title("Launcher - Consulta SEFAZ Automática")
root.geometry("600x400")

# Área de texto com scroll para exibir logs
log_text = scrolledtext.ScrolledText(root, width=70, height=20)
log_text.pack(pady=10)

# Botão para verificar dependências
check_button = tk.Button(root, text="Verificar Dependências", 
                         command=lambda: threading.Thread(target=run_dependency_check, daemon=True).start())
check_button.pack(pady=5)
root.mainloop()
