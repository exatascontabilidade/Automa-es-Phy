import json
import time
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from baixar_documento_omie import baixar_boletos_atrasados, trocar_para_nova_janela

# Nome do arquivo onde estão armazenados os e-mails
ARQUIVO_EMAILS = "emails_encontrados.json"

def carregar_emails():
    """Carrega a lista de e-mails armazenados."""
    if not os.path.exists(ARQUIVO_EMAILS):
        print("❌ Nenhum e-mail armazenado para processar!")
        return []
    
    with open(ARQUIVO_EMAILS, "r", encoding="utf-8") as f:
        return json.load(f)

def baixar_boletos(navegador):
    """Processa apenas um e-mail armazenado e clica no botão de visualização."""
    emails = carregar_emails()
    if not emails:
        return

    wait = WebDriverWait(navegador, 15)
    
    email = emails[0]  # Processar apenas o primeiro e-mail para teste
    remetente = email["remetente"]
    assunto = email["assunto"]
    
    print(f"🔍 Pesquisando e-mail de {remetente} sobre '{assunto}'")
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    
    # Pesquisar pelo e-mail específico no Gmail
    search_box.clear()
    search_box.send_keys(f"from:{remetente} {assunto}")
    search_box.send_keys(Keys.RETURN)
    time.sleep(random.uniform(2, 3))
    
    try:
        # Aguardar a exibição do primeiro e-mail na lista
        email_item = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='main'] [role='row'].zA")))
        email_item.click()
        time.sleep(random.uniform(2, 4))
        
        # Tentar encontrar o botão "Visualizar o Documento no Portal Omie"
        botao_omie = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Visualizar o Documento no Portal Omie')]"))
        )
        navegador.execute_script("arguments[0].scrollIntoView();", botao_omie)
        time.sleep(random.uniform(1, 2))
        
        action = ActionChains(navegador)
        action.move_to_element(botao_omie).click().perform()
        time.sleep(random.uniform(3, 5))
        
        print(f"✅ Botão do Omie clicado! Abrindo o Portal Omie...")
        
        # 🔄 **Troca para a nova aba antes de tentar baixar o documento**
        trocar_para_nova_janela(navegador)

        # 🟢 **Chama a função de download do documento já na nova aba**
        baixar_boletos_atrasados(navegador)

    except Exception as e:
        print(f"⚠️ Erro ao tentar clicar no botão do Omie: {e}")
    
    aguardar_fechamento()

def aguardar_fechamento():
    """Aguarda o usuário pressionar Enter antes de fechar o navegador."""
    input("🔴 Pressione ENTER para fechar o navegador...")
