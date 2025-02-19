from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Função para esperar de forma aleatória
def random_sleep(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Configurações do navegador para rodar em modo headless
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--mute-audio")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Instanciando o WebDriver
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)

# Ação do mouse para mover antes de interagir com o campo
action = ActionChains(navegador)

# Abrir o Gmail
navegador.get("https://mail.google.com")

# Aguardar o carregamento da página e encontrar o campo de e-mail
wait = WebDriverWait(navegador, 20)  # Aumentando o tempo de espera
email_elem = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))

# Simular movimento do mouse e clicar no campo
action.move_to_element(email_elem).perform()
random_sleep()  # Pausa aleatória antes de interagir
email_elem.send_keys("primeirot414@gmail.com")
random_sleep()  # Pausa após digitar o e-mail
email_elem.send_keys(Keys.RETURN)

# Tentar outro método de espera para o campo de senha
password_elem = wait.until(EC.visibility_of_element_located((By.NAME, "Passwd")))

# Simular movimento do mouse e clicar no campo de senha
action.move_to_element(password_elem).perform()
random_sleep()  # Pausa aleatória antes de interagir
password_elem.send_keys("serverteste01")
random_sleep()  # Pausa após digitar a senha
password_elem.send_keys(Keys.RETURN)

# Aguardar o carregamento após o login
random_sleep(3, 5)  # Pausa aleatória após o login

# Agora você está logado e pode interagir com o Gmail via Selenium
print("Login realizado com sucesso!")

# Esperar o usuário pressionar "Enter" para fechar o navegador
input("Pressione Enter para fechar o navegador...")

# Fechar o navegador
navegador.quit()
