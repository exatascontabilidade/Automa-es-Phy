from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def random_sleep(min_seconds=1, max_seconds=2):
    """Aguarda um tempo aleatório para simular comportamento humano."""
    time.sleep(random.uniform(min_seconds, max_seconds))


def obter_datas():
    """
    Pergunta ao usuário as datas para a busca.
    Retorna as datas formatadas para a pesquisa do Gmail.
    """
    data_inicio = input("📅 Digite a data inicial (AAAA/MM/DD): ")
    data_fim = input("📅 Digite a data final (AAAA/MM/DD): ")

    filtro_busca = f"label:financeiroexatas@exatascontabilidade.com.br recibo de honorários after:{data_inicio} before:{data_fim}"
    return filtro_busca


def buscar_emails(navegador):
    """
    Busca e-mails no Gmail no mesmo navegador já logado.
    """
    filtro_busca = obter_datas()
    print(f"[INFO] - Buscando e-mails com o filtro: {filtro_busca}")

    wait = WebDriverWait(navegador, 20)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

    search_box.clear()
    search_box.send_keys(filtro_busca)
    random_sleep()
    search_box.send_keys(Keys.RETURN)
    
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='main'] [role='row']")))


    random_sleep(2)  # Aguarda os resultados carregarem
    
    print("[INFO] - Resultados carregados com sucesso!")


def clicar_aleatoriamente(navegador):
    """Simula um clique aleatório para desbloquear a interface."""
    try:
        elementos = navegador.find_elements(By.XPATH, "//*")
        if elementos:
            elemento_aleatorio = random.choice(elementos)
            navegador.execute_script("arguments[0].click();", elemento_aleatorio)
            print("✅ Clique aleatório realizado.")
        else:
            print("⚠️ Nenhum elemento encontrado para clique aleatório.")
    except Exception as e:
        print(f"⚠️ Erro ao tentar clicar aleatoriamente: {e}")


def listar_elemento_especifico(navegador):
    """Lista todos os e-mails encontrados na busca, sem abrir nenhum deles."""
    wait = WebDriverWait(navegador, 15)

    try:
        print("\n🔍 Buscando e-mails específicos...")

        # Aguarda a área principal carregar completamente antes de interagir
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Aguarda os e-mails carregados na pesquisa
        email_elementos = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[role='main'] [role='row'].zA")  # Pega todos os e-mails (lidos e não lidos)
            )
        )

        if email_elementos:
            print(f"✅ {len(email_elementos)} e-mail(s) encontrado(s)!\n")

            for email_elemento in email_elementos:
                try:
                    # 🔹 Captura o nome do remetente (lido ou não lido)
                    remetente_elemento = email_elemento.find_element(By.CLASS_NAME, "yX")
                    remetente = remetente_elemento.text if remetente_elemento.text else "Desconhecido"

                    # 🔹 Captura o assunto do e-mail
                    assunto_elemento = email_elemento.find_element(By.CLASS_NAME, "bog")
                    assunto = assunto_elemento.text if assunto_elemento.text else "Sem assunto"

                    # 🔹 Captura a data do e-mail
                    data_elemento = email_elemento.find_element(By.CLASS_NAME, "xW")
                    data = data_elemento.text if data_elemento.text else "Data não disponível"

                    print(f"📧 **Remetente:** {remetente}")
                    print(f"📌 **Assunto:** {assunto}")
                    print(f"📅 **Data:** {data}")
                    print("-" * 50)  # Separador entre os e-mails

                except Exception as e:
                    print(f"⚠️ Erro ao processar um e-mail: {e}")

        else:
            print("⚠️ Nenhum e-mail encontrado!")

    except Exception as e:
        print(f"⚠️ Erro ao buscar e-mails: {e}")

    finally:
        input("\n🚀 Pressione Enter para fechar o navegador...")
        navegador.quit()