import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configurações do Chrome
options = Options()
options.add_argument("--disable-gpu")  # Desabilita aceleração de GPU
options.add_argument("--mute-audio")  # Silencia o áudio

# Instalação e configuração do ChromeDriver
servico = Service(ChromeDriverManager().install())

# Inicia o navegador com as opções e o serviço configurado
navegador = webdriver.Chrome(service=servico, options=options)

# Acessa o site do YouTube
navegador.get("https://www.youtube.com/")

try:
    # Aguarda até o campo de pesquisa estar visível e interagível
    pesquisa = WebDriverWait(navegador, 2).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="center"]/yt-searchbox/div[1]/form/input'))
    )

    time.sleep(1)  # Pequena pausa para garantir estabilidade

    # Insere o texto de pesquisa
    pesquisa.send_keys("FELIPE AMORIM CD 2025 - FELIPE AMORIM JANEIRO 2025 [ REPERTÓRIO NOVO ] FELIPE AMORIM MEDLEYS MOVOS")
    time.sleep(1)

    # Envia a pesquisa
    pesquisa.submit()

    # Aguarda carregar os resultados da pesquisa e clica no primeiro vídeo
    video = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='video-title']"))
    )
    navegador.execute_script("arguments[0].click();", video)

    time.sleep(5)  # Aguarda o início do vídeo

except TimeoutException:
    print("⏳ Tempo de espera esgotado ao tentar interagir com o YouTube.")

except ElementNotInteractableException:
    print("⚠️ Elemento encontrado, mas não pode ser interagido no momento.")

except NoSuchElementException:
    print("❌ Elemento não encontrado na página.")

except Exception as e:
    print(f"🚨 Erro inesperado: {e}")

def youtube_skip_adds(navegador):
    max_attempts = 10  # Define o número máximo de tentativas
    attempt = 0
    
    while attempt < max_attempts:
        try:
            # Tenta encontrar diferentes variações do botão "Pular Anúncio"
            possible_xpaths = [
                '//button[contains(@class, "ytp-ad-skip-button")]',  # XPath mais comum
                '//div[contains(@class, "ytp-ad-text ytp-ad-skip-button-text")]',  # Algumas variações do botão
                '//button[@aria-label="Pular anúncios"]',
                '//*[@id="skip-button:v"]', # Teste de botão com label acessível
            ]
            
            for xpath in possible_xpaths:
                try:
                    pular_anuncio = WebDriverWait(navegador, 3).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    navegador.execute_script("arguments[0].click();", pular_anuncio)  # Força o clique
                    print("✅ Anúncio pulado com sucesso!")
                    return  # Sai da função após clicar
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                    continue  # Tenta o próximo XPath se este não for encontrado

            # Se nenhum botão for encontrado, aguarda e tenta novamente
            print("⏳ Nenhum botão de pular anúncio encontrado. Tentando novamente...")
            time.sleep(2)
            attempt += 10  # Incrementa o número de tentativas

        except Exception as e:
            print(f"🚨 Erro inesperado ao tentar pular anúncio: {e}")
            break  # Sai do loop em caso de erro crítico

    print("❌ Nenhum anúncio ignorável foi encontrado ou tempo esgotado.")

# Chamando a função após iniciar o vídeo no YouTube
youtube_skip_adds(navegador)

# Aguarda interação antes de fechar
input("Pressione Enter para fechar o navegador...")
navegador.quit()
