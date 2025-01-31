import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações do Chrome
options = Options()
options.add_argument("--disable-gpu")  # Desabilita a aceleração de GPU

# Instalação e configuração do ChromeDriver
servico = Service(ChromeDriverManager().install())

# Inicia o navegador com as opções e o serviço configurado
navegador = webdriver.Chrome(service=servico, options=options)

# Acessa o site do YouTube
navegador.get("https://www.youtube.com/")

navegador.find_element('xpath', '//*[@id="center"]/yt-searchbox/div[1]/form/input').send_keys("FELIPE AMORIM CD 2025 - FELIPE AMORIM JANEIRO 2025 [ REPERTÓRIO NOVO ] FELIPE AMORIM MEDLEYS MOVOS")
time.sleep(2)
navegador.find_element('xpath', '//*[@id="center"]/yt-searchbox/div[1]/form/input').submit()

# Espera até o elemento estar visível
elemento = WebDriverWait(navegador, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="thumbnail"]/yt-image/img'))
)

time.sleep(2)
# Forçar o clique no elemento com JavaScript
navegador.execute_script("arguments[0].click();", elemento)

# Mudar para o iframe se o botão "Pular Anúncio" estiver dentro de um iframe
try:
    iframe = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    )
    navegador.switch_to.frame(iframe)
    
    # Tenta encontrar e clicar no botão "Pular Anúncio"
    pular_anuncio = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class="ytp-ad-skip-button ytp-button"]'))
    )
    pular_anuncio.click()
    print("Anúncio pulado com sucesso!")
except Exception as e:
    print(f"Erro ao tentar pular o anúncio: {e}")

# Opcional: Pause para ver o que aconteceu antes de fechar
input("Pressione Enter para fechar o navegador...")
navegador.quit()
