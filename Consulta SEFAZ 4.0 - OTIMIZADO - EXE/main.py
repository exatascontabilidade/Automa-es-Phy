import pandas as pd
import subprocess
import os
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import sys

os.environ["PYTHONUTF8"] = "1"
root = tk.Tk()
root.title("Consulta SEFAZ Automática")
root.geometry("600x700")
arquivo_planilha = tk.StringVar()
parar_execucao = threading.Event()

def atualizar_bibliotecas():
    """
    Atualiza todas as bibliotecas instaladas e exibe o progresso na interface Tkinter.
    """
    log_output.insert("end", "🔄 Verificando atualizações...\n")
    log_output.see("end")
    root.update()

    try:
        # Atualiza o pip primeiro
        log_output.insert("end", "🛠 Atualizando pip...\n")
        root.update()
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)

        # Obtém a lista de todas as bibliotecas instaladas
        pacotes = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout
        pacotes = [linha.split("==")[0] for linha in pacotes.split("\n") if linha]

        # Atualiza cada biblioteca e exibe na interface
        for pacote in pacotes:
            log_output.insert("end", f"🔄 Atualizando {pacote}...\n")
            root.update()
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", pacote], check=True)

        log_output.insert("end", "✅ Todas as bibliotecas foram atualizadas!\n")
        root.update()
    except Exception as e:
        log_output.insert("end", f"⚠️ Erro ao atualizar bibliotecas: {e}\n")
        root.update()
        
threading.Thread(target=atualizar_bibliotecas, daemon=True).start()
def selecionar_planilha():
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha", filetypes=[("Arquivos Excel", "*.xlsx;*.xls")]
    )
    if caminho:
        arquivo_planilha.set(caminho)
        log_output.insert("end", f"📂 Planilha selecionada: {caminho}\n")
        log_output.see("end")
def carregar_empresas(arquivo):
    colunas_necessarias = ["Inscrição Municipal", "Tipo de Arquivo", "Pesquisar Por", "Data Inicial", "Data Final"]
    try:
        df = pd.read_excel(arquivo, usecols=colunas_necessarias, dtype=str).fillna("")
        return df if not df.empty else None
    except Exception as e:
        log_output.insert("end", f"❌ Erro ao carregar a planilha: {e}\n")
        log_output.see("end")
        return None
def executar_consulta():
    if not arquivo_planilha.get():
        messagebox.showwarning("Erro", "Nenhuma planilha selecionada!")
        return
    df_empresas = carregar_empresas(arquivo_planilha.get())
    if df_empresas is None:
        messagebox.showerror("Erro", "Nenhuma empresa encontrada para processar. Verifique a planilha.")
        return
    threading.Thread(target=processar_consultas, args=(df_empresas,), daemon=True).start()
def processar_consultas(df_empresas):
    parar_execucao.clear()

    # Definir caminho correto para o executável
    script_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    
    # Agora buscamos pelo módulo correto: modulo.exe quando estiver compilado
    caminho_script = os.path.join(script_dir, "modulo.exe" if getattr(sys, 'frozen', False) else "modulo.py")

    if not os.path.exists(caminho_script):
        messagebox.showerror("Erro", "❌ Arquivo modulo.exe não encontrado!" if getattr(sys, 'frozen', False) else "❌ Arquivo modulo.py não encontrado!")
        return

    log_output.insert("end", "\n🔄 Iniciando consultas...\n")
    log_output.see("end")

    for index, row in df_empresas.iterrows():
        if parar_execucao.is_set():
            log_output.insert("end", "\n⛔ Execução interrompida pelo usuário.\n")
            log_output.see("end")
            return

        inscricao_municipal = row["Inscrição Municipal"].strip()
        if not inscricao_municipal:
            log_output.insert("end", f"⚠️ Linha {index + 2}: Inscrição Municipal ausente. Pulando...\n")
            continue

        log_output.insert("end", f"\n🔍 Consultando Inscrição Municipal: {inscricao_municipal}...\n")
        log_output.see("end")

        try:
            # Executa `modulo.exe` quando estiver empacotado, caso contrário, `modulo.py`
            resultado = subprocess.run([
                caminho_script,  # Agora chama diretamente o EXE ou PY
                inscricao_municipal, row["Tipo de Arquivo"].upper(), row["Pesquisar Por"].capitalize(),
                row["Data Inicial"], row["Data Final"], arquivo_planilha.get()
            ], capture_output=True, text=True, encoding="utf-8", timeout=30)
            
            log_output.insert("end", resultado.stdout)
            if resultado.stderr:
                log_output.insert("end", f"⚠️ Erros: {resultado.stderr}\n")

        except subprocess.TimeoutExpired:
            log_output.insert("end", f"⏳ Tempo excedido para {inscricao_municipal}. Pulando...\n")
        except Exception as e:
            log_output.insert("end", f"❌ Erro: {e}\n")

        log_output.see("end")

    log_output.insert("end", "\n✅ Todas as consultas foram concluídas!\n")
    log_output.see("end")
    messagebox.showinfo("Concluído", "Todas as consultas foram processadas!")
def encerrar_consulta():
    parar_execucao.set()
    log_output.insert("end", "\n⏹️ Interrompendo consultas...\n")
    log_output.see("end")
    messagebox.showinfo("Interrompido", "As consultas estão sendo interrompidas!")
frame = tk.Frame(root)
frame.pack(pady=10)
btn_selecionar = tk.Button(frame, text="Selecionar Planilha", command=selecionar_planilha)
btn_selecionar.pack(side=tk.LEFT, padx=5)
btn_executar = tk.Button(frame, text="Executar Consultas", command=executar_consulta)
btn_executar.pack(side=tk.LEFT, padx=5)
btn_encerrar = tk.Button(frame, text="Encerrar Consultas", command=encerrar_consulta, bg="red", fg="white")
btn_encerrar.pack(side=tk.LEFT, padx=5)
log_output = scrolledtext.ScrolledText(root, height=35, width=70)
log_output.pack(pady=10)
root.mainloop()
