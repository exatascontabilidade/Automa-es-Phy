import pandas as pd
import subprocess
import time
import os
os.environ["PYTHONUTF8"] = "1"

# 🔹 Nome do arquivo da planilha com a lista de empresas
arquivo_planilha = "consulta_empresas.xlsx"  # Alterar se necessário

def carregar_empresas(arquivo):
    """Lê a planilha e retorna os dados necessários para consulta."""
    try:
        df = pd.read_excel(arquivo, dtype=str)  # Converte tudo para string para evitar erros
        
        # 🔎 Verifica se todas as colunas necessárias existem na planilha
        colunas_necessarias = ["Inscrição Municipal", "Tipo de Arquivo", "Pesquisar Por", "Data Inicial", "Data Final"]
        colunas_faltando = [coluna for coluna in colunas_necessarias if coluna not in df.columns]

        if colunas_faltando:
            print(f"❌ Erro: As seguintes colunas não foram encontradas na planilha: {', '.join(colunas_faltando)}")
            return None
        
        return df  # Retorna o DataFrame com os dados
    
    except Exception as e:
        print(f"❌ Erro ao carregar a planilha: {e}")
        return None

# 📌 Carregar a planilha
df_empresas = carregar_empresas(arquivo_planilha)

if df_empresas is None or df_empresas.empty:
    print("❌ Nenhuma empresa encontrada para processar. Verifique a planilha.")
else:
    for index, row in df_empresas.iterrows():
        inscricao_municipal = str(row.get("Inscrição Municipal", "")).strip()
        tipo_arquivo = str(row.get("Tipo de Arquivo", "")).strip().upper()
        pesquisar_por = str(row.get("Pesquisar Por", "")).strip().capitalize()
        data_inicial = str(row.get("Data Inicial", "")).strip()  # Converte para string e remove espaços
        data_final = str(row.get("Data Final", "")).strip()  # Converte para string e remove espaços

        if not inscricao_municipal:
            print(f"⚠️ Linha {index + 2}: Inscrição Municipal ausente. Pulando essa empresa...")
            continue  # Pula para a próxima empresa

        print(f"\n🔄 Iniciando consulta para Inscrição Municipal: {inscricao_municipal}")

        try:
            # 🏁 Executa o script de consulta passando os argumentos
            resultado = subprocess.run([
                "python", "consulta_sefaz.py", 
                inscricao_municipal, tipo_arquivo, pesquisar_por, data_inicial, data_final
            ], capture_output=True, text=True, encoding="utf-8")

            # 🖨️ Exibir a saída do script
            print(resultado.stdout)
            print("⚠️ Erros:", resultado.stderr if resultado.stderr else "Nenhum")

        except Exception as e:
            print(f"❌ Erro ao executar a consulta para {inscricao_municipal}: {e}")

        # ⏳ Aguarda alguns segundos antes da próxima consulta para evitar bloqueios no sistema
        time.sleep(5)  # Ajuste conforme necessário
    
    print("\n✅ Todas as consultas foram concluídas com sucesso!")
