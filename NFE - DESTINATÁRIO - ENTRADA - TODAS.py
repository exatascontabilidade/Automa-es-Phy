import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do navegador
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--mute-audio")

# Instalação do ChromeDriver
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)

# Acessar o site
navegador.get("https://www.sefaz.se.gov.br/SitePages/acesso_usuario.aspx")

# Aguarda o carregamento da página
wait = WebDriverWait(navegador, 10)

try:
    # 1️⃣ Aguarda e seleciona a opção "Contabilista" no dropdown
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'id_do_select')))  # Substitua pelo ID real do <select>
    dropdown.click()
    
    option_contabilista = wait.until(EC.element_to_be_clickable((By.ID, 'id_da_opcao_contabilista')))  # Substitua pelo ID real da opção
    option_contabilista.click()
    print("Selecionado Contabilista")

    # 2️⃣ Aguarda os campos de login
    usuario = wait.until(EC.presence_of_element_located((By.ID, 'id_usuario')))  # Substitua pelo ID real do campo de usuário
    senha = wait.until(EC.presence_of_element_located((By.ID, 'id_senha')))  # Substitua pelo ID real do campo de senha

    # 3️⃣ Clica nos campos antes de preencher
    usuario.click()
    usuario.send_keys("SE007829")

    senha.click()
    senha.send_keys("Exatas2024@")

    print("Login preenchido com sucesso!")

except Exception as e:
    print(f"Erro ao localizar os campos de login: {e}")

# Aguarda para visualizar o preenchimento antes de fechar
time.sleep(3)

# Pressione Enter para fechar o navegador
input("Pressione Enter para fechar o navegador...")
navegador.quit()
