from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def random_sleep(min_seconds=1, max_seconds=2):
    time.sleep(random.uniform(min_seconds, max_seconds))

def obter_datas():
    """
    Pergunta ao usuário as datas para a busca.
    Retorna as datas formatadas para a pesquisa do Gmail.
    """
    data_inicio = input("📅 Digite a data inicial (AAAA/MM/DD): ")
    data_fim = input("📅 Digite a data final (AAAA/MM/DD): ")

    # Monta o filtro de busca com as datas informadas
    filtro_busca = f"label:financeiroexatas@exatascontabilidade.com.br recibo de honorários after:{data_inicio} before:{data_fim}"
    return filtro_busca

def buscar_emails(navegador):
    """
    Função para buscar e-mails no Gmail no mesmo navegador já logado.
    """
    # 🗓️ Pergunta as datas ao usuário antes de buscar
    filtro_busca = obter_datas()

    print(f"[INFO] - Buscando e-mails com o filtro: {filtro_busca}")

    # Aguarda a barra de pesquisa aparecer
    wait = WebDriverWait(navegador, 20)
    navegador.get("https://mail.google.com/mail/u/0/#inbox")
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

    # Insere o termo de busca
    search_box.clear()
    search_box.send_keys(filtro_busca)
    random_sleep()
    search_box.send_keys(Keys.RETURN)

    # Aguarda os resultados carregarem
    random_sleep(5)

def random_sleep(min_seconds=1, max_seconds=2):
    """Aguarda um tempo aleatório para simular comportamento humano."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def clicar_aleatoriamente(navegador):
    """Simula um clique aleatório na página para desbloquear a interface."""
    try:
        elementos = navegador.find_elements(By.XPATH, "//*")
        if elementos:
            elemento_aleatorio = random.choice(elementos)
            navegador.execute_script("arguments[0].click();", elemento_aleatorio)
            print("✅ Clique aleatório realizado para desbloqueio.")
        else:
            print("⚠️ Nenhum elemento encontrado para clique aleatório.")
    except Exception as e:
        print(f"⚠️ Erro ao tentar clicar aleatoriamente: {e}")

def listar_elemento_especifico(navegador):
    """Lista um elemento específico na página (exemplo da imagem)."""
    wait = WebDriverWait(navegador, 15)
    try:
        print("\n🔍 Buscando e-mail específico...")

        # 🔹 Aguarda a página carregar completamente
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Clicar aleatoriamente para desbloquear interface
        clicar_aleatoriamente(navegador)

        # Localiza a linha do e-mail na tabela do Gmail
        email_elemento = navegador.find_element(By.XPATH, "//tr[contains(@class, 'zA zE')]")

        if email_elemento:
            print("✅ E-mail encontrado!")

            # Obtém detalhes do e-mail
            remetente = email_elemento.find_element(By.XPATH, ".//span[@class='zF']").text
            assunto = email_elemento.find_element(By.XPATH, ".//span[@class='bqe']").text
            data = email_elemento.find_element(By.XPATH, ".//span[@class='bq3']").text

            print(f"📧 Remetente: {remetente}")
            print(f"📌 Assunto: {assunto}")
            print(f"📅 Data: {data}")

            # Clica para abrir o e-mail
            navegador.execute_script("arguments[0].click();", email_elemento)
            print("✅ E-mail aberto!")

        else:
            print("⚠️ Nenhum e-mail encontrado!")


    except Exception as e:
        print(f"⚠️ Erro ao buscar elemento específico: {e}")
        
    finally:
        # 🔴 Evita que o navegador feche automaticamente
        input("\n🚀 Pressione Enter para fechar o navegador...")

# 🚀 Agora chamamos as funções corretamente após abrir o navegador
# listar_elemento_especifico(navegador)