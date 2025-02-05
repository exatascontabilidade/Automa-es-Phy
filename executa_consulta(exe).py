import pandas as pd
import subprocess
import time
import os
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

# Verifica e instala dependências automaticamente
required_packages = ["pandas", "tkinter", "openpyxl", "selenium", "webdriver_manager"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} não encontrado. Instalando...")
        subprocess.run(["pip", "install", package], check=True)

os.environ["PYTHONUTF8"] = "1"

# Interface Gráfica
root = tk.Tk()
root.title("Consulta SEFAZ Automática")
root.geometry("600x400")

pasta_selecionada = tk.StringVar()
processo_ativo = None 

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
os.chdir(diretorio_atual)

def selecionar_pasta():
    caminho = filedialog.askdirectory(title="Selecione a pasta com as planilhas")
    if caminho:
        pasta_selecionada.set(caminho)
        log_mensagem_threadsafe(f"📂 Pasta selecionada: {caminho}")
        print(f"📂 Caminho da pasta selecionada: {pasta_selecionada.get()}")

def log_mensagem_threadsafe(mensagem):
    root.after(0, log_mensagem, mensagem)

def log_mensagem(mensagem):
    log_output.insert(tk.END, mensagem + "\n")
    log_output.yview(tk.END)

def carregar_empresas(arquivo):
    try:
        if not os.path.exists(arquivo):
            log_mensagem_threadsafe("❌ Erro: Arquivo da planilha não encontrado!")
            return None
        
        df = pd.read_excel(arquivo, dtype=str)  # Converte tudo para string

        colunas_necessarias = ["Inscrição Municipal", "Tipo de Arquivo", "Pesquisar Por", "Data Inicial", "Data Final"]
        colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]

        if colunas_faltando:
            log_mensagem_threadsafe(f"❌ Erro: Colunas ausentes na planilha: {', '.join(colunas_faltando)}")
            return None
        
        return df
    except Exception as e:
        log_mensagem_threadsafe(f"❌ Erro ao carregar a planilha: {e}")
        return None

def executar_consulta():
    global processo_ativo
    caminho_pasta = pasta_selecionada.get()

    if not caminho_pasta:
        messagebox.showwarning("Erro", "Nenhuma pasta selecionada!")
        return

    arquivos_planilhas = [os.path.join(caminho_pasta, f) for f in os.listdir(caminho_pasta) if f.endswith(('.xlsx', '.xls'))]

    if not arquivos_planilhas:
        messagebox.showerror("Erro", "Nenhuma planilha encontrada na pasta selecionada.")
        return

    log_mensagem_threadsafe("\n🔄 Iniciando consultas...\n")

    for arquivo in arquivos_planilhas:
        df_empresas = carregar_empresas(arquivo)

        if df_empresas is None or df_empresas.empty:
            log_mensagem_threadsafe(f"⚠️ Nenhuma empresa válida encontrada no arquivo: {arquivo}")
            continue

        for index, row in df_empresas.iterrows():
            if processo_ativo is None:
                log_mensagem_threadsafe("⛔ Processo interrompido pelo usuário!")
                return

            inscricao_municipal = str(row.get("Inscrição Municipal", "")).strip()
            tipo_arquivo = str(row.get("Tipo de Arquivo", "")).strip().upper()
            pesquisar_por = str(row.get("Pesquisar Por", "")).strip().capitalize()
            data_inicial = str(row.get("Data Inicial", "")).strip()
            data_final = str(row.get("Data Final", "")).strip()

            if not inscricao_municipal:
                log_mensagem_threadsafe(f"⚠️ Linha {index + 2}: Inscrição Municipal ausente. Pulando...")
                continue

            log_mensagem_threadsafe(f"\n🔍 Consultando Inscrição Municipal: {inscricao_municipal}...")

            try:
                caminho_script = os.path.join(diretorio_atual, "consulta_sefaz.py")
                if not os.path.exists(caminho_script):
                    log_mensagem_threadsafe("❌ Erro: Arquivo consulta_sefaz.py não encontrado!")
                    continue

                processo_ativo = subprocess.Popen(
                    ["python", caminho_script, inscricao_municipal, tipo_arquivo, pesquisar_por, data_inicial, data_final],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"
                )
                
                stdout, stderr = processo_ativo.communicate()
                log_mensagem_threadsafe(stdout)

                if stderr:
                    log_mensagem_threadsafe(f"⚠️ Erros: {stderr}")

            except Exception as e:
                log_mensagem_threadsafe(f"❌ Erro ao executar a consulta: {e}")

            time.sleep(3)

    processo_ativo = None
    log_mensagem_threadsafe("\n✅ Todas as consultas foram concluídas!\n")
    messagebox.showinfo("Concluído", "Todas as consultas foram processadas!")

def executar_consulta_thread():
    global processo_ativo
    processo_ativo = threading.Thread(target=executar_consulta, daemon=True)
    processo_ativo.start()

def encerrar_processo():
    global processo_ativo
    if processo_ativo:
        processo_ativo = None
        log_mensagem_threadsafe("⛔ Processo interrompido pelo usuário!")
        messagebox.showinfo("Encerrado", "Processo interrompido com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Nenhum processo está em execução!")

# Interface gráfica
frame = tk.Frame(root)
frame.pack(pady=10)

btn_selecionar = tk.Button(frame, text="Selecionar Pasta", command=selecionar_pasta)
btn_selecionar.pack(side=tk.LEFT, padx=5)

btn_executar = tk.Button(frame, text="Executar Consultas", command=executar_consulta_thread)
btn_executar.pack(side=tk.LEFT, padx=5)

btn_encerrar = tk.Button(frame, text="Encerrar Processo", command=encerrar_processo, fg="white", bg="red")
btn_encerrar.pack(side=tk.LEFT, padx=5)

log_output = scrolledtext.ScrolledText(root, height=15, width=70)
log_output.pack(pady=10)

root.mainloop()
