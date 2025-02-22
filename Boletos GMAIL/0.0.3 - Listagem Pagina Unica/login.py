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

# ⚠️ PEGANDO E-MAIL E SENHA DE VARIÁVEIS DE AMBIENTE ⚠️
EMAIL_GMAIL = "financeiroexatas136@gmail.com" # Defina antes de rodar o script: export EMAIL_GMAIL="seu_email@gmail.com"
SENHA_GMAIL = "Exatas1010@" # Defina antes de rodar: export SENHA_GMAIL="sua_senha"

def random_sleep(min_seconds=1, max_seconds=2):
    """Aguarda um tempo aleatório para simular comportamento humano."""
    time.sleep(random.uniform(min_seconds, max_seconds))


def iniciar_navegador():
    """Configura e inicia o navegador Selenium."""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico, options=options)
    return navegador


def fazer_login(navegador):
    """Realiza login no Gmail."""
    navegador.get("https://mail.google.com")

    wait = WebDriverWait(navegador, 20)

    try:
        # 🔑 Insere o e-mail
        email_elem = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_elem.send_keys(EMAIL_GMAIL)
        random_sleep()
        email_elem.send_keys(Keys.RETURN)

        # 🔒 Aguarda a entrada da senha
        password_elem = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_elem.send_keys(SENHA_GMAIL)
        random_sleep()
        password_elem.send_keys(Keys.RETURN)

        random_sleep(3, 5)

        # ✅ Confirma que o login foi bem-sucedido
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "z0")))  # Botão "Escrever" do Gmail
        print("[INFO] - Login realizado com sucesso!")

        return True

    except Exception as e:
        print(f"⚠️ Erro ao fazer login: {e}")
        return False


if __name__ == "__main__":
    navegador = iniciar_navegador()
    if fazer_login(navegador):
        from busca import buscar_emails, clicar_aleatoriamente, listar_elemento_especifico

        # 🔍 Inicia a busca no mesmo navegador logado
        buscar_emails(navegador)
        clicar_aleatoriamente(navegador)
        listar_elemento_especifico(navegador)
    else:
        print("❌ Não foi possível fazer login. Verifique suas credenciais ou autenticação 2FA.")
        navegador.quit()
