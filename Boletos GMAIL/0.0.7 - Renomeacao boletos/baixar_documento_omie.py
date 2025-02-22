import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Obtém o diretório onde o script está localizado
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define o diretório de download como uma subpasta "temp" dentro do diretório atual
DOWNLOAD_DIR = os.path.join(current_dir, "temp")

def trocar_para_nova_janela(navegador):
    """Troca o foco do Selenium para a última janela aberta."""
    time.sleep(3)  # Espera a nova aba carregar completamente
    janelas = navegador.window_handles  # Obtém todas as janelas abertas
    navegador.switch_to.window(janelas[-1])  # Muda para a última aba/janela
    print("✅ Alternado para a nova aba com sucesso!")

def carregar_elemento(navegador, by, valor, timeout=10):
    """Aguarda dinamicamente um elemento estar presente na página."""
    return WebDriverWait(navegador, timeout).until(EC.presence_of_element_located((by, valor)))

def fechar_popup(navegador):
    """Fecha o popup se ele estiver presente."""
    try:
        popup = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MuiDialog-container"))
        )
        
        if popup.is_displayed():
            print("🔍 Popup detectado! Tentando fechar...")
            try:
                botao_fechar = popup.find_element(By.XPATH, ".//button[contains(@class, 'MuiButtonBase-root')]")
                botao_fechar.click()
                print("✅ Popup fechado com sucesso!")
                time.sleep(2)
            except:
                print("⚠️ Nenhum botão de fechar encontrado, tentando clicar fora.")
                navegador.execute_script("document.querySelector('.MuiDialog-container').click();")
                time.sleep(2)
    except Exception:
        print("⚠️ Nenhum popup detectado ou erro ao tentar fechá-lo.")

def listar_elementos_tabela(navegador):
    """Lista todas as linhas da tabela para entender a estrutura dos elementos."""
    try:
        print("📌 Listando estrutura da tabela...")
        linhas = navegador.find_elements(By.XPATH, "//tr")
        for i, linha in enumerate(linhas):
            celulas = linha.find_elements(By.XPATH, ".//*")  # Pegando todos os elementos dentro da linha    
    except Exception as e:
        print(f"❌ Erro ao listar elementos da tabela: {e}")

def esperar_download(download_dir, timeout=60, arquivos_iniciais=None):
    """
    Aguarda que um novo arquivo seja baixado no diretório especificado.
    Retorna o caminho completo do arquivo baixado.
    """
    if arquivos_iniciais is None:
        arquivos_iniciais = set(os.listdir(download_dir))
    start_time = time.time()
    while True:
        time.sleep(1)
        arquivos_atual = set(os.listdir(download_dir))
        novos = arquivos_atual - arquivos_iniciais
        if novos:
            for arquivo in novos:
                # Verifica se o arquivo não está em processo de download (Chrome usa a extensão .crdownload)
                if not arquivo.endswith(".crdownload"):
                    return os.path.join(download_dir, arquivo)
        if time.time() - start_time > timeout:
            raise TimeoutError("Download não completado em tempo hábil.")

def baixar_boletos_atrasados(navegador):
    # Troca para a nova janela e fecha popup, se houver
    trocar_para_nova_janela(navegador)
    fechar_popup(navegador)
    
    try:
        print("🔍 Buscando parcelas em atraso...")
        # Buscar todas as linhas da tabela (exceto o cabeçalho)
        linhas_parcelas = navegador.find_elements(By.XPATH, "//tr")[1:]  # Ignora a primeira linha (cabeçalho)
        encontrou_atraso = False  # Flag para verificar se alguma parcela foi encontrada

        for linha in linhas_parcelas:
            try:
                celulas = linha.find_elements(By.XPATH, ".//td")
                if len(celulas) < 2:
                    print("⚠️ Linha sem informações suficientes, pulando...")
                    continue

                situacao = celulas[1].text.strip()  # Segunda célula contém a situação

                if "Em aberto" in situacao or "Vencida" in situacao:
                    encontrou_atraso = True
                    print(f"⚠️ Parcela em atraso encontrada: {situacao}")

                    # Buscar o botão de download dentro da linha
                    try:
                        botao_download = linha.find_element(By.XPATH, ".//button[contains(@class, 'MuiButtonBase-root') and contains(@class, 'MuiIconButton-root')]")
                        if botao_download:
                            print("📥 Clicando no botão de download...")
                            
                            # Lista os arquivos presentes antes do download
                            arquivos_antes = set(os.listdir(DOWNLOAD_DIR))
                            
                            navegador.execute_script("arguments[0].click();", botao_download)
                            time.sleep(3)  # Tempo para iniciar o download
                            
                            # Aguarda o download concluir
                            arquivo_baixado = esperar_download(DOWNLOAD_DIR, timeout=60, arquivos_iniciais=arquivos_antes)
                            print(f"✅ Arquivo baixado: {arquivo_baixado}")
                    except Exception as e:
                        print(f"⚠️ Erro ao tentar clicar no botão de download: {e}")

            except Exception as e:
                print(f"⚠️ Erro ao processar uma linha da tabela: {e}")

        if not encontrou_atraso:
            print("✅ Nenhuma parcela em atraso encontrada.")

    except Exception as e:
        print(f"❌ Erro ao localizar parcelas em atraso: {e}")

    print("✅ Processo concluído!")
    # Fecha a janela atual (a nova aba) e retorna para a janela original
    navegador.close()  # Fecha a aba onde ocorreu o download
    if navegador.window_handles:
        navegador.switch_to.window(navegador.window_handles[0])
