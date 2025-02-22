from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.common.action_chains import ActionChains


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
    """Simula um clique aleatório em um elemento não interativo para desbloquear a interface."""
    try:
        elementos = navegador.find_elements(By.TAG_NAME, "div")  # Seleciona apenas <div>s
        elementos_filtrados = [el for el in elementos if el.is_displayed() and el.get_attribute("onclick") is None]
        
        if elementos_filtrados:
            elemento_aleatorio = random.choice(elementos_filtrados)
            navegador.execute_script("arguments[0].click();", elemento_aleatorio)
            print("✅ Clique aleatório realizado em um elemento seguro.")
        else:
            print("⚠️ Nenhum elemento seguro encontrado para clique aleatório.")
    except Exception as e:
        print(f"⚠️ Erro ao tentar clicar aleatoriamente: {e}")

def listar_todos_emails(navegador):
    """Lista todos os e-mails paginando até o final."""
    wait = WebDriverWait(navegador, 15)

    while True:
        try:
            print("\n🔍 Buscando e-mails na página atual...")

            # Aguarda os e-mails carregarem
            email_elementos = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[role='main'] [role='row'].zA"))
            )

            if email_elementos:
                print(f"✅ {len(email_elementos)} e-mail(s) encontrado(s) nesta página!\n")

                for email_elemento in email_elementos:
                    try:
                        # 🔹 Captura o nome do remetente
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
                print("⚠️ Nenhum e-mail encontrado nesta página!")

            # 🛑 Verifica se há uma próxima página de e-mails
            try:
                botao_proxima_pagina = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "amJ"))
                )
                
                if botao_proxima_pagina.is_displayed() and botao_proxima_pagina.is_enabled():
                    print("➡️ Indo para a próxima página...\n")
                    navegador.execute_script("arguments[0].scrollIntoView();", botao_proxima_pagina)
                    random_sleep(1, 2)
                    
                    action = ActionChains(navegador)
                    action.move_to_element(botao_proxima_pagina).click().perform()
                    random_sleep(2, 4)  # Aguarda o carregamento da nova página
                else:
                    print("✅ Todas as páginas foram percorridas.")
                    break
            
            except Exception as e:
                print(f"🚫 Erro ao tentar clicar no botão 'Próxima Página': {e}. Finalizando...")
                break

        except Exception as e:
            print(f"⚠️ Erro ao buscar e-mails: {e}")
            break

    input("\n🚀 Pressione Enter para fechar o navegador...")
    navegador.quit()
