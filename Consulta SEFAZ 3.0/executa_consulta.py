import pandas as pd
import subprocess
import time
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import sys

os.environ["PYTHONUTF8"] = "1"  # Garante compatibilidade de caracteres

# 🔹 Criar a janela principal
root = tk.Tk()
root.title("Consulta SEFAZ Automática")
root.geometry("600x400")

# Variável para armazenar o caminho do arquivo selecionado
arquivo_planilha = tk.StringVar()
parar_execucao = False  # 🔹 Variável para controlar a interrupção das consultas

def selecionar_planilha():
    """Abre um explorador de arquivos para selecionar a planilha."""
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha",
        filetypes=[("Arquivos Excel", "*.xlsx;*.xls")]
    )
    if caminho:
        arquivo_planilha.set(caminho)  # Atualiza a variável com o caminho selecionado
        log_output.insert(tk.END, f"📂 Planilha selecionada: {caminho}\n")

def carregar_empresas(arquivo):
    """Lê a planilha e retorna os dados necessários para consulta."""
    try:
        df = pd.read_excel(arquivo, dtype=str)  # Converte tudo para string para evitar erros
        
        # 🔎 Verifica se todas as colunas necessárias existem na planilha
        colunas_necessarias = ["Inscrição Municipal", "Tipo de Arquivo", "Pesquisar Por", "Data Inicial", "Data Final"]
        colunas_faltando = [coluna for coluna in colunas_necessarias if coluna not in df.columns]

        if colunas_faltando:
            log_output.insert(tk.END, f"❌ Erro: Colunas ausentes na planilha: {', '.join(colunas_faltando)}\n")
            return None
        
        return df  # Retorna o DataFrame com os dados
    
    except Exception as e:
        log_output.insert(tk.END, f"❌ Erro ao carregar a planilha: {e}\n")
        return None

def executar_consulta():
    """Executa as consultas para cada empresa listada na planilha."""
    global parar_execucao  # 🔹 Permite alterar a variável global
    parar_execucao = False  # 🔹 Reseta a variável ao iniciar

    caminho_arquivo = arquivo_planilha.get()
    
    if not caminho_arquivo:
        messagebox.showwarning("Erro", "Nenhuma planilha selecionada!")
        return

    df_empresas = carregar_empresas(caminho_arquivo)

    if df_empresas is None or df_empresas.empty:
        messagebox.showerror("Erro", "Nenhuma empresa encontrada para processar. Verifique a planilha.")
        return

    log_output.insert(tk.END, "\n🔄 Iniciando consultas...\n")

    # 🔹 Obtém o diretório onde o executável está rodando
    if getattr(sys, 'frozen', False):  # Se estiver rodando como EXE
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    caminho_script = os.path.join(script_dir, "consulta_sefaz.py")

    print(f"🔍 Caminho do script: {caminho_script}")  # Para verificar se está correto

    if not os.path.exists(caminho_script):
        messagebox.showerror("Erro", "❌ Arquivo consulta_sefaz.py não encontrado!")
        return  # Encerra a execução

    for index, row in df_empresas.iterrows():
        if parar_execucao:  # 🔹 Se a variável for True, interrompe a execução
            log_output.insert(tk.END, "\n⛔ Execução interrompida pelo usuário.\n")
            messagebox.showinfo("Encerrado", "As consultas foram interrompidas!")
            return

        inscricao_municipal = str(row.get("Inscrição Municipal", "")).strip()
        tipo_arquivo = str(row.get("Tipo de Arquivo", "")).strip().upper()
        pesquisar_por = str(row.get("Pesquisar Por", "")).strip().capitalize()
        data_inicial = str(row.get("Data Inicial", "")).strip()
        data_final = str(row.get("Data Final", "")).strip()

        if not inscricao_municipal:
            log_output.insert(tk.END, f"⚠️ Linha {index + 2}: Inscrição Municipal ausente. Pulando...\n")
            continue  # Pula para a próxima empresa

        log_output.insert(tk.END, f"\n🔍 Consultando Inscrição Municipal: {inscricao_municipal}...\n")
        root.update_idletasks()  # Atualiza a interface enquanto roda o processo

        try:
            resultado = subprocess.run([
                sys.executable, caminho_script,  # Usa o Python correto
                inscricao_municipal, tipo_arquivo, pesquisar_por, data_inicial, data_final, caminho_arquivo  # <- Passa o caminho da planilha!
            ], capture_output=True, text=True, encoding="utf-8")

            # Exibir a saída do script no log
            log_output.insert(tk.END, resultado.stdout)
            log_output.insert(tk.END, f"⚠️ Erros: {resultado.stderr if resultado.stderr else 'Nenhum'}\n")

        except Exception as e:
            log_output.insert(tk.END, f"❌ Erro ao executar a consulta: {e}\n")

        time.sleep(5)  # Aguarda antes da próxima consulta

    log_output.insert(tk.END, "\n✅ Todas as consultas foram concluídas!\n")
    messagebox.showinfo("Concluído", "Todas as consultas foram processadas!")

def encerrar_consulta():
    """Função para interromper a execução das consultas."""
    global parar_execucao
    parar_execucao = True  # 🔹 Define a variável para interromper o loop
    log_output.insert(tk.END, "\n⏹️ Interrompendo consultas...\n")
    messagebox.showinfo("Interrompido", "As consultas estão sendo interrompidas!")

# 🔹 Criar os botões e área de log na interface
frame = tk.Frame(root)
frame.pack(pady=10)

btn_selecionar = tk.Button(frame, text="Selecionar Planilha", command=selecionar_planilha)
btn_selecionar.pack(side=tk.LEFT, padx=5)

btn_executar = tk.Button(frame, text="Executar Consultas", command=executar_consulta)
btn_executar.pack(side=tk.LEFT, padx=5)

btn_encerrar = tk.Button(frame, text="Encerrar Consultas", command=encerrar_consulta, bg="red", fg="white")
btn_encerrar.pack(side=tk.LEFT, padx=5)

log_output = scrolledtext.ScrolledText(root, height=15, width=70)
log_output.pack(pady=10)

# 🔹 Iniciar a interface gráfica
root.mainloop()
