import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os
from login import download_dir

   
def clicar_botao_download_navegador(navegador):
    """Clica no botão de download do navegador"""
    try:
        print("📥 Clicando no botão de download do navegador...")
        botao_download = navegador.find_element(By.XPATH, "//button[contains(@class, 'MuiIconButton-root')]")
        navegador.execute_script("arguments[0].click();", botao_download)
    except Exception as e:
        print(f"⚠️ Erro ao clicar no botão de download do navegador: {e}")

def aguardar_download():
    """Aguarda o arquivo ser baixado na pasta correta"""
    print("⏳ Aguardando conclusão do download...")
    tempo_maximo = 30  # Segundos
    tempo_inicial = time.time()

    while time.time() - tempo_inicial < tempo_maximo:
        arquivos = os.listdir(download_dir)
        arquivos_baixados = [f for f in arquivos if f.endswith(".pdf")]

        if arquivos_baixados:
            print(f"✅ Download concluído: {arquivos_baixados[0]}")
            return arquivos_baixados[0]  # Retorna o nome do arquivo baixado

        time.sleep(1)

    print("⚠️ Tempo de espera esgotado! Nenhum arquivo encontrado.")
    return None

def renomear_arquivo_baixado():
    """Renomeia o arquivo baixado com um nome padrão"""
    arquivo_baixado = aguardar_download()
    
    if arquivo_baixado:
        novo_nome = "Boleto_Atualizado.pdf"
        caminho_antigo = os.path.join(download_dir, arquivo_baixado)
        caminho_novo = os.path.join(download_dir, novo_nome)

        try:
            os.rename(caminho_antigo, caminho_novo)
            print(f"✅ Arquivo renomeado para: {novo_nome}")
        except Exception as e:
            print(f"⚠️ Erro ao renomear o arquivo: {e}")
    else:
        print("❌ Nenhum arquivo foi baixado para renomeação!")