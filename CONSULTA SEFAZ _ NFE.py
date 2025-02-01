import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


# Configuração do navegador
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--mute-audio")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])


# Instalação do ChromeDriver
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)

# Acessar o site
navegador.get("https://www.sefaz.se.gov.br/SitePages/acesso_usuario.aspx")

# Aguarda o carregamento da página
wait = WebDriverWait(navegador, 3)

#--------------------------------------------------------------------------------LOGIN NA PAGINA--------------------------------------------------------------------------------------------------------------------------------------------------
try:
    # Aguarda e clica no botão "Aceitar", se existir
    try:
        accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'accept-button')))
        accept_button.click()
        print("Botão 'Aceitar' clicado.")
    except:
        print("Botão 'Aceitar' não encontrado. Continuando sem clicar.")

    time.sleep(1)

    # 🔎 **Encontra todos os iframes**
    iframes = navegador.find_elements(By.TAG_NAME, "iframe")
    print(f"Número de iframes encontrados: {len(iframes)}")

    # 🔀 **Troca para o primeiro iframe, onde pode estar o dropdown**
    navegador.switch_to.frame(iframes[0])
    print("Trocado para o primeiro iframe.")

    # 1️⃣ **Aguarda e seleciona a opção "Contabilista" no dropdown**
    dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'acessoRapido')))
    dropdown.click()
    time.sleep(2)

    option_contabilista = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value='https://security.sefaz.se.gov.br/internet/portal/contabilista/atoAcessoContabilista.jsp']")))
    option_contabilista.click()
    print("Selecionado Contabilista")

    # 2️⃣ **Clica em outro elemento para fechar o menu dropdown**
    time.sleep(1)
    body = navegador.find_element(By.TAG_NAME, "body")
    body.click()
    print("Dropdown fechado.")

    time.sleep(1)

    # 3️⃣ **Encontra e troca para o iframe do login**
    try:
        iframe_login = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'atoAcessoContribuinte.jsp')]")))
        navegador.switch_to.frame(iframe_login)
    except:
        print("❌ Erro: O iframe do login NÃO foi encontrado!")
        raise Exception("Iframe do login não localizado!")
    
    # 4️⃣ **Busca a tabela de login dentro do iframe**
    try:
        tabela_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tabelaVerde")))
    except:
        raise Exception("Tabela de login não localizada!")

    # 5️⃣ **Busca os campos de login dentro da tabela**
    try:
        usuario = tabela_login.find_element(By.NAME, "UserName")
        senha = tabela_login.find_element(By.NAME, "Password")
        botao_login = tabela_login.find_element(By.NAME, "submit")  # Botão "OK"
    except:
        raise Exception("Campos de login não localizados!")

    # 6️⃣ **Clica e preenche os campos**
    usuario.click()
    usuario.send_keys("SE007829")

    senha.click()
    senha.send_keys("Exatas2024@")

    # 7️⃣ **Clica no botão "OK" para fazer login**
    botao_login.click()
    print("🎉 Login realizado com sucesso!")
except Exception as e:
    print(f"Erro ao localizar os campos de login: {e}")



#-----------------------------------------------------------------------------------SOLICITAR XML-------------------------------------------------------------------------------------------------------------------------------------------------


time.sleep(3)
navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")

body = navegador.find_element(By.TAG_NAME, "body")
body.send_keys(Keys.TAB)
body.send_keys(Keys.ENTER)

wait = WebDriverWait(navegador, 5)
time.sleep(1)

print("🔍 Tentando clicar em um campo aleatório...")

# 🔹 **Tenta clicar em um elemento qualquer na página principal**
try:
    elementos = navegador.find_elements(By.TAG_NAME, "a")  # Tenta encontrar links na página principal
    if elementos:
        elementos[0].click()  # Clica no primeiro link encontrado
        print("✅ Clique aleatório realizado para desbloquear a página!")
    else:
        print("❌ Nenhum link encontrado para clicar.")

except Exception as e:
    print(f"❌ Erro ao clicar em um campo aleatório: {e}")

try:
    print("🔍 Procurando a opção 'NFE/DOCUMENTOS ELETRÔNICOS'...")

    # Localiza a opção pelo texto
    menu_nfe = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'NFE/DOCUMENTOS ELETRONICOS')]")))

    # Clica na opção do menu
    menu_nfe.click()
    print("✅ Opção 'NFE/DOCUMENTOS ELETRÔNICOS' acessada com sucesso!")

    time.sleep(2)  # Pequena pausa para garantir o carregamento

    # Agora tenta clicar em "Solicitar Arquivos XML"
    print("🔍 Procurando a opção 'Solicitar Arquivos XML'...")
    solicitar_xml = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Solicitar Arquivos XML')]")))

    solicitar_xml.click()
    print("✅ Opção 'Solicitar Arquivos XML' acessada com sucesso!")

    #NOVO XML
    print("⏳ Aguardando carregamento da página...")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)  # Aguarde mais um pouco para evitar falhas

    # Localiza o elemento específico dentro da nova página carregada
    print("🔍 Procurando o novo link desejado na página carregada...")
    novo_elemento = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr > td > table:nth-child(6) > tbody > tr > td:nth-child(1) > a")))

    # Clica no novo elemento
    novo_elemento.click()
    print("✅ Novo elemento clicado com sucesso!")

except Exception as e:
    print(f"❌ Erro ao localizar e clicar na opção: {e}")



#-----------------------------------------------------------------------------------SELEÇÃO EMPRESA------------------------------------------------------------------------------------------------------------------------------------------

print("Acessando o menu de empresas...")
time.sleep(3)

try:
    # 🔍 Aguarda a página carregar completamente
    wait.until(EC.presence_of_element_located((By.ID, "cdPessoaContribuinte")))
    print("✅ Página carregada com sucesso!")

    # 🔍 Aguarda a presença do select das empresas
    select_empresas = wait.until(EC.presence_of_element_located((By.ID, "cdPessoaContribuinte")))
    select = Select(select_empresas)

    # 📌 Lista todas as empresas disponíveis (sem duplicação de código)
    empresas_disponiveis = {}
    for opcao in select.options:
        valor = opcao.get_attribute("value").strip()
        texto = opcao.text.strip()
        if valor and texto:
            empresas_disponiveis[valor] = texto.replace(f"{valor} - ", "")  # Remove código duplicado do nome

    while True:  # 🔄 Loop para garantir que o usuário selecione corretamente
        print("\n📌 Empresas disponíveis para seleção:")
        for codigo, nome in empresas_disponiveis.items():
            print(f"➡ {codigo} - {nome}")

        # 🔹 Pergunta ao usuário qual empresa selecionar
        codigo_empresa = input("\n📝 Digite os primeiros números da empresa desejada: ").strip()

        # 🔎 Busca a empresa correspondente
        empresa_selecionada = None
        for valor in empresas_disponiveis.keys():
            if valor.startswith(codigo_empresa):
                empresa_selecionada = valor
                break

        # ✅ Se a empresa for encontrada, seleciona no dropdown
        if empresa_selecionada:
            select.select_by_value(empresa_selecionada)
            print(f"✅ Empresa '{empresas_disponiveis[empresa_selecionada]}' selecionada com sucesso!")

            # 🔹 Aguarda o botão OK estar disponível e clica nele
            try:
                botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
                botao_ok.click()
                print("🟢 Consulta iniciada com sucesso! 🖱️")
                break  # 🔄 Sai do loop pois a seleção foi bem-sucedida

            except Exception as e:
                print(f"❌ Erro ao clicar no botão OK: {e}")
                break  # Sai do loop mesmo se houver erro no botão OK

        else:
            print("❌ Empresa não encontrada. Tente novamente digitando um número válido.")

except Exception as e:
    print(f"❌ Erro ao localizar ou selecionar a empresa: {e}")




#-----------------------------------------------------------------------------------SELEÇÃO TIPO DE ARQUIVO----------------------------------------------------------------------------------------------------------------------------------
print("-------Seleção de arquivo")
try:
    # 🔍 Aguarda a presença do campo de seleção de tipo de arquivo
    select_tipo_arquivo = wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
    
    # 🔹 Pergunta ao usuário qual tipo de arquivo deseja selecionar
    tipo_arquivo = input("\n📌 Escolha o tipo de arquivo (NFE, CTE, NFC): ").strip().upper()

    # 🔎 Busca a opção correspondente e seleciona
    select = Select(select_tipo_arquivo)
    opcoes_disponiveis = [op.text.strip().upper() for op in select.options]

    if tipo_arquivo in opcoes_disponiveis:
        select.select_by_visible_text(tipo_arquivo)
        print(f"✅ Tipo de arquivo '{tipo_arquivo}' selecionado com sucesso!")
        
        # 🔘 Aguarda e clica no botão "OK"
        botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
        botao_ok.click()
        print("✅ Botão 'OK' clicado, prosseguindo com a consulta...")
    else:
        print("❌ Tipo de arquivo inválido. Tente novamente.")
    
except Exception as e:
    print(f"❌ Erro ao selecionar o tipo de arquivo: {e}")

time.sleep(10)