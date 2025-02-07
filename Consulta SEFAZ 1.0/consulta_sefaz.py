import sys
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime

# ✅ Captura a Inscrição Municipal passada pelo script executa_consulta.py
if len(sys.argv) > 1:
    inscricao_municipal = sys.argv[1]
    print(f"\n🔍 Iniciando consulta para a Inscrição Municipal: {inscricao_municipal}")
else:
    print("❌ Nenhuma Inscrição Municipal informada. Encerrando o script.")
    sys.exit(1)

# ✅ Carregar a planilha com os dados da consulta
arquivo_planilha = "consulta_empresas.xlsx"
try:
    df = pd.read_excel(arquivo_planilha)
    empresa_dados = df[df["Inscrição Municipal"] == int(inscricao_municipal)].iloc[0]  # Pega os dados correspondentes

except Exception as e:
    print(f"❌ Erro ao carregar a planilha: {e}")
    sys.exit(1)

# ✅ Configuração do navegador
options = Options()
options.add_argument("--headless=new") 
options.add_argument("--disable-gpu")
options.add_argument("--mute-audio")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])


# ✅ Instalação do ChromeDriver
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)
driver = navegador


# ✅ Acessar o site
navegador.get("https://www.sefaz.se.gov.br/SitePages/acesso_usuario.aspx")
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
    time.sleep(1)

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
    usuario.send_keys("---")

    senha.click()
    senha.send_keys("---")

    # 7️⃣ **Clica no botão "OK" para fazer login**
    botao_login.click()
    print("🎉 Login realizado com sucesso!")
except Exception as e:
    print(f"Erro ao localizar os campos de login: {e}")

#-----------------------------------------------------------------------------------SOLICITAR XML-------------------------------------------------------------------------------------------------------------------------------------------------

navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")

body = navegador.find_element(By.TAG_NAME, "body")
body.send_keys(Keys.TAB)
body.send_keys(Keys.ENTER)

wait = WebDriverWait(navegador, 2)
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

    time.sleep(1)  # Pequena pausa para garantir o carregamento

    # Agora tenta clicar em "Solicitar Arquivos XML"
    print("🔍 Procurando a opção 'Solicitar Arquivos XML'...")
    solicitar_xml = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Solicitar Arquivos XML')]")))

    solicitar_xml.click()
    print("✅ Opção 'Solicitar Arquivos XML' acessada com sucesso!")

    #NOVO XML
    print("⏳ Aguardando carregamento da página...")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)  # Aguarde mais um pouco para evitar falhas

    # Localiza o elemento específico dentro da nova página carregada
    print("🔍 Procurando o novo link desejado na página carregada...")
    novo_elemento = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr > td > table:nth-child(6) > tbody > tr > td:nth-child(1) > a")))

    # Clica no novo elemento
    novo_elemento.click()
    print("✅ Novo elemento clicado com sucesso!")

except Exception as e:
    print(f"❌ Erro ao localizar e clicar na opção: {e}")


#-----------------------------------------------------------------------------------SELEÇÃO EMPRESA------------------------------------------------------------------------------------------------------------------------------------------
try:
    select_empresas = wait.until(EC.presence_of_element_located((By.ID, "cdPessoaContribuinte")))
    select = Select(select_empresas)
    select.select_by_value(str(inscricao_municipal))  # Seleciona pelo valor correto

    botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
    botao_ok.click()
    print(f"✅ Empresa '{inscricao_municipal}' selecionada!")

except Exception as e:
    print(f"❌ Erro ao selecionar empresa: {e}")
    navegador.quit()
    sys.exit(1)

#-------------------------------------- SELEÇÃO DO TIPO DE ARQUIVO --------------------------------------#
try:
    # ✅ Obtém o tipo de arquivo correspondente à Inscrição Municipal da planilha
    tipo_arquivo = empresa_dados["Tipo de Arquivo"].strip().upper()  # Obtém e padroniza o texto

    # ✅ Aguarda o campo de seleção estar disponível na página
    select_tipo_arquivo_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
    select_tipo_arquivo = Select(select_tipo_arquivo_element)

    # ✅ Obtém as opções disponíveis no dropdown
    opcoes_disponiveis = [op.text.strip().upper() for op in select_tipo_arquivo.options]

    # ✅ Verifica se o tipo de arquivo está na lista de opções e seleciona
    if tipo_arquivo in opcoes_disponiveis:
        select_tipo_arquivo.select_by_visible_text(tipo_arquivo)
        print(f"✅ Tipo de arquivo '{tipo_arquivo}' selecionado com sucesso!")
    else:
        print(f"❌ Tipo de arquivo '{tipo_arquivo}' não encontrado. Opções disponíveis: {opcoes_disponiveis}")
        sys.exit(1)  # Encerra o script se o tipo de arquivo for inválido

    # ✅ Clica no botão OK para continuar
    botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
    botao_ok.click()
    print("✅ Botão 'OK' clicado, prosseguindo...")

except Exception as e:
    print(f"❌ Erro ao selecionar o tipo de arquivo: {e}")
    sys.exit(1)  # Encerra o script em caso de erro

#----------------------------------VALIDAR DATA----------------------------------------------
def validar_data(data):
    """Verifica se a data está no formato correto DD/MM/AAAA."""
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# ----------------------------------------------------------------------------------- CASO SEJA NFE ----------------------------------------------------------------------------------------------------------------#
if tipo_arquivo == "NFE":
    try:
        # ✅ Obtém o tipo de pesquisa da planilha
        pesquisar_por = empresa_dados["Pesquisar Por"].strip()

        tipo_pesquisa_element = wait.until(EC.presence_of_element_located((By.ID, "tipoPesquisa")))
        print("✅ Campo de pesquisa encontrado!")

        select_pesquisa = Select(tipo_pesquisa_element)
        
        # 🔍 Exibe as opções disponíveis para validação
        print("📌 Opções disponíveis para pesquisa:")
        opcoes_validas = {option.text.strip(): option.get_attribute('value').strip() for option in select_pesquisa.options}

        if pesquisar_por in opcoes_validas:
            select_pesquisa.select_by_visible_text(pesquisar_por)
            print(f"✅ Tipo de pesquisa '{pesquisar_por}' selecionado com sucesso!")
        else:
            print(f"❌ Tipo de pesquisa inválido na planilha: {pesquisar_por}")
            sys.exit(1)  # Encerra o script se houver erro

    #---------------------------MENSAGEM DE ERRO ------------------------------------------------
    except Exception as e:
        print(f"❌ Erro ao selecionar o tipo de pesquisa: {e}")
        sys.exit(1)



# -------------------------------------- PREENCHIMENTO DE DATAS --------------------------------------#
    try:
        # ✅ Obtém as datas da planilha
        data_inicial = empresa_dados["Data Inicial"]
        data_final = empresa_dados["Data Final"]

        # 🔍 Converte para string e valida o formato
        data_inicial = data_inicial.strftime("%d/%m/%Y") if isinstance(data_inicial, pd.Timestamp) else str(data_inicial).strip()
        data_final = data_final.strftime("%d/%m/%Y") if isinstance(data_final, pd.Timestamp) else str(data_final).strip()

        if not (validar_data(data_inicial) and validar_data(data_final)):
            print("❌ Formato de data inválido na planilha. Corrija e tente novamente.")
            sys.exit(1)  # Encerra o script se houver erro

        # ⏳ Aguarda os campos de data estarem disponíveis
        campo_data_inicial = wait.until(EC.presence_of_element_located((By.ID, "dtInicio")))
        campo_data_final = wait.until(EC.presence_of_element_located((By.ID, "dtFinal")))

        # ✏️ Preenche os campos de data
        campo_data_inicial.clear()
        campo_data_inicial.send_keys(data_inicial)

        campo_data_final.clear()
        campo_data_final.send_keys(data_final)

        print(f"✅ Datas preenchidas: {data_inicial} até {data_final}")

        # 🔘 Clica no botão OK para continuar
        botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
        botao_ok.click()
        print("✅ Consulta iniciada!")

    except Exception as e:
        print(f"❌ Erro ao preencher as datas: {e}")
        sys.exit(1)
    try:
        # Aguarda e verifica se alguma mensagem de erro aparece na página
        mensagem_erro_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fontMessageError")))
        mensagem_erro = mensagem_erro_element.text.strip()
        if mensagem_erro:
            print(f"⚠️ Mensagem de erro detectada: {mensagem_erro}")
    except:
        print("✅ Nenhuma mensagem de erro detectada.")





# -----------------------------------------------------------------------------------CASO SEJA NFC --------------------------------------------------------------------------------------------------------------------#
if tipo_arquivo == "NFC":
    try:
        # ✅ Obtém o tipo de pesquisa da planilha
        pesquisar_por = empresa_dados["Pesquisar Por"].strip()

        tipo_pesquisa_element = wait.until(EC.presence_of_element_located((By.ID, "tipoPesquisa")))
        print("✅ Campo de pesquisa encontrado!")

        select_pesquisa = Select(tipo_pesquisa_element)
        
        # 🔍 Exibe as opções disponíveis para validação
        print("📌 Opções disponíveis para pesquisa:")
        opcoes_validas = {option.text.strip(): option.get_attribute('value').strip() for option in select_pesquisa.options}

        if pesquisar_por in opcoes_validas:
            select_pesquisa.select_by_visible_text(pesquisar_por)
            print(f"✅ Tipo de pesquisa '{pesquisar_por}' selecionado com sucesso!")
        else:
            print(f"❌ Tipo de pesquisa inválido na planilha: {pesquisar_por}")
            sys.exit(1)  # Encerra o script se houver erro

    except Exception as e:
        print(f"❌ Erro ao selecionar o tipo de pesquisa: {e}")
        sys.exit(1)

# -------------------------------------- PREENCHIMENTO DE DATAS --------------------------------------#
    try:
        # ✅ Obtém as datas da planilha
        data_inicial = empresa_dados["Data Inicial"]
        data_final = empresa_dados["Data Final"]

        # 🔍 Converte para string e valida o formato
        data_inicial = data_inicial.strftime("%d/%m/%Y") if isinstance(data_inicial, pd.Timestamp) else str(data_inicial).strip()
        data_final = data_final.strftime("%d/%m/%Y") if isinstance(data_final, pd.Timestamp) else str(data_final).strip()

        if not (validar_data(data_inicial) and validar_data(data_final)):
            print("❌ Formato de data inválido na planilha. Corrija e tente novamente.")
            sys.exit(1)  # Encerra o script se houver erro

        # ⏳ Aguarda os campos de data estarem disponíveis
        campo_data_inicial = wait.until(EC.presence_of_element_located((By.ID, "dtInicio")))
        campo_data_final = wait.until(EC.presence_of_element_located((By.ID, "dtFinal")))

        # ✏️ Preenche os campos de data
        campo_data_inicial.clear()
        campo_data_inicial.send_keys(data_inicial)

        campo_data_final.clear()
        campo_data_final.send_keys(data_final)

        print(f"✅ Datas preenchidas: {data_inicial} até {data_final}")

        # 🔘 Clica no botão OK para continuar
        botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
        botao_ok.click()
        print("✅ Consulta iniciada!")

    except Exception as e:
        print(f"❌ Erro ao preencher as datas: {e}")
        sys.exit(1)

    #---------------------------MENSAGEM DE ERRO ------------------------------------------------

    try:
        # Aguarda e verifica se alguma mensagem de erro aparece na página
        mensagem_erro_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fontMessageError")))
        mensagem_erro = mensagem_erro_element.text.strip()
        if mensagem_erro:
            print(f"⚠️ Mensagem de erro detectada: {mensagem_erro}")
    except:
        print("✅ Nenhuma mensagem de erro detectada.")

# -----------------------------------------------------------------------------------CASO SEJA CTE --------------------------------------------------------------------------------------------------------------------#
if tipo_arquivo == "CTE":
    print("✅ Script rodando...")
    try:
        # ✅ Obtém o tipo de pesquisa da planilha
        pesquisar_por = empresa_dados["Pesquisar Por"].strip()

        # Dicionário mapeando os tipos de pesquisa aos IDs dos checkboxes
        mapeamento_pesquisa = {
            "Remetente": "Remetente",
            "Expedidor": "Expedidor",
            "Recebedor": "Recebedor",
            "Destinatário": "Destinatario",
            "Emitente": "Emitente",
            "Outros": "Outros"
        }

        if pesquisar_por in mapeamento_pesquisa:
            campo_id = mapeamento_pesquisa[pesquisar_por]

            # ✅ Aguarda o campo estar disponível
            campo_elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, campo_id))
            )

            # 🔘 Se o checkbox não estiver marcado, clique nele
            if not campo_elemento.is_selected():
                campo_elemento.click()
                print(f"✅ Tipo de pesquisa '{pesquisar_por}' selecionado com sucesso!")
            else:
                print(f"ℹ️ O tipo de pesquisa '{pesquisar_por}' já estava selecionado.")

        else:
            print(f"❌ Tipo de pesquisa inválido na planilha: {pesquisar_por}")
            sys.exit(1)  # Encerra o script se houver erro

    except Exception as e:
        print(f"❌ Erro ao selecionar o tipo de pesquisa: {e}")
        sys.exit(1)
    
    # -------------------------------------- PREENCHIMENTO DE DATAS --------------------------------------#
    try:
        # ✅ Obtém as datas da planilha
        data_inicial = empresa_dados["Data Inicial"]
        data_final = empresa_dados["Data Final"]

        # 🔍 Converte para string e valida o formato
        data_inicial = data_inicial.strftime("%d/%m/%Y") if isinstance(data_inicial, pd.Timestamp) else str(data_inicial).strip()
        data_final = data_final.strftime("%d/%m/%Y") if isinstance(data_final, pd.Timestamp) else str(data_final).strip()

        if not (validar_data(data_inicial) and validar_data(data_final)):
            print("❌ Formato de data inválido na planilha. Corrija e tente novamente.")
            sys.exit(1)  # Encerra o script se houver erro

        # ⏳ Aguarda os campos de data estarem disponíveis
        campo_data_inicial = wait.until(EC.presence_of_element_located((By.ID, "dtInicio")))
        campo_data_final = wait.until(EC.presence_of_element_located((By.ID, "dtFinal")))

        # ✏️ Preenche os campos de data
        campo_data_inicial.clear()
        campo_data_inicial.send_keys(data_inicial)

        campo_data_final.clear()
        campo_data_final.send_keys(data_final)

        print(f"✅ Datas preenchidas: {data_inicial} até {data_final}")

        # 🔘 Clica no botão OK para continuar
        botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
        botao_ok.click()
        print("✅ Consulta iniciada!")

    except Exception as e:
        print(f"❌ Erro ao preencher as datas: {e}")
        sys.exit(1)

    #---------------------------MENSAGEM DE ERRO ------------------------------------------------

    try:
        # Aguarda e verifica se alguma mensagem de erro aparece na página
        mensagem_erro_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fontMessageError")))
        mensagem_erro = mensagem_erro_element.text.strip()
        if mensagem_erro:
            print(f"⚠️ Mensagem de erro detectada: {mensagem_erro}")
    except:
        print("✅ Nenhuma mensagem de erro detectada.")
