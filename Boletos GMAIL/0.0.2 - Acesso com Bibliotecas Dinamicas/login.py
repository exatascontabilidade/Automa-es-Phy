from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Adiciona o diretório do script ao path
from busca import buscar_emails  # Importa a função de busca sem abrir outro navegador
from busca import clicar_aleatoriamente
from busca import listar_elemento_especifico
from busca import random_sleep
# Importa a função de busca sem abrir outro navegador

def random_sleep(min_seconds=1, max_seconds=2):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Configuração do navegador
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--mute-audio")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)

action = ActionChains(navegador)

# 📨 Acessar Gmail e fazer login
navegador.get("https://mail.google.com")

wait = WebDriverWait(navegador, 20)
email_elem = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))

action.move_to_element(email_elem).perform()
random_sleep()
email_elem.send_keys("financeiroexatas136@gmail.com")
random_sleep()
email_elem.send_keys(Keys.RETURN)

# Aguarda a entrada da senha
password_elem = wait.until(EC.visibility_of_element_located((By.NAME, "Passwd")))

action.move_to_element(password_elem).perform()
random_sleep()
password_elem.send_keys("Exatas1010@")
random_sleep()
password_elem.send_keys(Keys.RETURN)

random_sleep(3, 5)

print("[INFO] - Login realizado com sucesso!")
# tem que chamar as fun
# 🔍 Inicia a busca no mesmo navegador logado
buscar_emails(navegador)
clicar_aleatoriamente(navegador)
listar_elemento_especifico(navegador)