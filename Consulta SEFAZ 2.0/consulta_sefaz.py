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
if len(sys.argv) > 1:
    inscricao_municipal = sys.argv[1]
    print(f"\n🔍 Iniciando consulta para a Inscrição Municipal: {inscricao_municipal}")
else:
    print("❌ Nenhuma Inscrição Municipal informada. Encerrando o script.")
    sys.exit(1)
arquivo_planilha = "consulta_empresas.xlsx"
try:
    df = pd.read_excel(arquivo_planilha)
    empresa_dados = df[df["Inscrição Municipal"] == int(inscricao_municipal)].iloc[0]  # Pega os dados correspondentes
except Exception as e:
    print(f"❌ Erro ao carregar a planilha: {e}")
    sys.exit(1)
options = Options()
options.add_argument("--headless=new") 
options.add_argument("--disable-gpu")
options.add_argument("--mute-audio")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)
driver = navegador
navegador.get("https://www.sefaz.se.gov.br/SitePages/acesso_usuario.aspx")
wait = WebDriverWait(navegador, 3)
#--------------------------------------------------------------------------------LOGIN NA PAGINA--------------------------------------------------------------------------------------------------------------------------------------------------
try:
    try:
        accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'accept-button')))
        accept_button.click()
    except:
        print("Botão 'Aceitar' não encontrado. Continuando sem clicar.")
    time.sleep(1)
    iframes = navegador.find_elements(By.TAG_NAME, "iframe")
    print(f"Número de iframes encontrados: {len(iframes)}")
    navegador.switch_to.frame(iframes[0])
    dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'acessoRapido')))
    dropdown.click()
    time.sleep(1)
    option_contabilista = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value='https://security.sefaz.se.gov.br/internet/portal/contabilista/atoAcessoContabilista.jsp']")))
    option_contabilista.click()
    time.sleep(1)
    body = navegador.find_element(By.TAG_NAME, "body")
    body.click()
    time.sleep(1)
    try:
        iframe_login = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'atoAcessoContribuinte.jsp')]")))
        navegador.switch_to.frame(iframe_login)
    except:
        print("❌ Erro: O iframe do login NÃO foi encontrado!")
        raise Exception("Iframe do login não localizado!")
    try:
        tabela_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tabelaVerde")))
    except:
        raise Exception("Tabela de login não localizada!")
    try:
        usuario = tabela_login.find_element(By.NAME, "UserName")
        senha = tabela_login.find_element(By.NAME, "Password")
        botao_login = tabela_login.find_element(By.NAME, "submit")
    except:
        raise Exception("Campos de login não localizados!")
    usuario.click()
    usuario.send_keys("SE007829")
    senha.click()
    senha.send_keys("Exatas2024@")
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
try:
    elementos = navegador.find_elements(By.TAG_NAME, "a") 
    if elementos:
        elementos[0].click() 
    else:
        print("❌ Nenhum link encontrado para clicar.")
except Exception as e:
    print(f"❌ Erro ao clicar em um campo aleatório: {e}")
try:
    print("🔍 Procurando a opção 'NFE/DOCUMENTOS ELETRÔNICOS'...")
    menu_nfe = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'NFE/DOCUMENTOS ELETRONICOS')]")))
    menu_nfe.click()
    time.sleep(1) 
    solicitar_xml = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Solicitar Arquivos XML')]")))
    solicitar_xml.click()
    print("✅ Opção 'Solicitar Arquivos XML' acessada com sucesso!")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)  
    novo_elemento = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr > td > table:nth-child(6) > tbody > tr > td:nth-child(1) > a")))
    novo_elemento.click()
except Exception as e:
    print(f"❌ Erro ao localizar e clicar na opção: {e}")
#-----------------------------------------------------------------------------------SELEÇÃO EMPRESA------------------------------------------------------------------------------------------------------------------------------------------
try:
    select_empresas = wait.until(EC.presence_of_element_located((By.ID, "cdPessoaContribuinte")))
    select = Select(select_empresas)
    select.select_by_value(str(inscricao_municipal))
    botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
    botao_ok.click()
    print(f"✅ Empresa '{inscricao_municipal}' selecionada!")

except Exception as e:
    print(f"❌ Erro ao selecionar empresa: {e}")
    navegador.quit()
    sys.exit(1)
try:
    tipo_arquivo = empresa_dados["Tipo de Arquivo"].strip().upper()
    select_tipo_arquivo_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
    select_tipo_arquivo = Select(select_tipo_arquivo_element)
    opcoes_disponiveis = [op.text.strip().upper() for op in select_tipo_arquivo.options]
    if tipo_arquivo in opcoes_disponiveis:
        select_tipo_arquivo.select_by_visible_text(tipo_arquivo)
        print(f"✅ Tipo de arquivo '{tipo_arquivo}' selecionado com sucesso!")
    else:
        print(f"❌ Tipo de arquivo '{tipo_arquivo}' não encontrado. Opções disponíveis: {opcoes_disponiveis}")
        sys.exit(1)
    botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
    botao_ok.click()
except Exception as e:
    print(f"❌ Erro ao selecionar o tipo de arquivo: {e}")
    sys.exit(1) 
#----------------------------------VALIDAR DATA----------------------------------------------
def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False
# ----------------------------------------------------------------------------------- CASO SEJA NFE ----------------------------------------------------------------------------------------------------------------#
if tipo_arquivo == "NFE":
    try:
        pesquisar_por = empresa_dados["Pesquisar Por"].strip()
        tipo_pesquisa_element = wait.until(EC.presence_of_element_located((By.ID, "tipoPesquisa")))
        select_pesquisa = Select(tipo_pesquisa_element)
        opcoes_validas = {option.text.strip(): option.get_attribute('value').strip() for option in select_pesquisa.options}
        if pesquisar_por in opcoes_validas:
            select_pesquisa.select_by_visible_text(pesquisar_por)
            print(f"✅ Tipo de pesquisa '{pesquisar_por}' selecionado com sucesso!")
        else:
            print(f"❌ Tipo de pesquisa inválido na planilha: {pesquisar_por}")
            sys.exit(1) 
    #---------------------------MENSAGEM DE ERRO ------------------------------------------------
    except Exception as e:
        print(f"❌ Erro ao selecionar o tipo de pesquisa: {e}")
        sys.exit(1)
# -------------------------------------- PREENCHIMENTO DE DATAS --------------------------------------#
    try:
        data_inicial = empresa_dados["Data Inicial"]
        data_final = empresa_dados["Data Final"]
        data_inicial = data_inicial.strftime("%d/%m/%Y") if isinstance(data_inicial, pd.Timestamp) else str(data_inicial).strip()
        data_final = data_final.strftime("%d/%m/%Y") if isinstance(data_final, pd.Timestamp) else str(data_final).strip()
        if not (validar_data(data_inicial) and validar_data(data_final)):
            print("❌ Formato de data inválido na planilha. Corrija e tente novamente.")
            sys.exit(1)
        campo_data_inicial = wait.until(EC.presence_of_element_located((By.ID, "dtInicio")))
        campo_data_final = wait.until(EC.presence_of_element_located((By.ID, "dtFinal")))
        campo_data_inicial.clear()
        campo_data_inicial.send_keys(data_inicial)
        campo_data_final.clear()
        campo_data_final.send_keys(data_final)
        print(f"✅ Datas preenchidas: {data_inicial} até {data_final}")
        botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
        botao_ok.click()
        print("✅ Consulta Finalizada")
    except Exception as e:
        print(f"❌ Erro ao preencher as datas: {e}")
        sys.exit(1)
    try:
        mensagem_erro_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fontMessageError")))
        mensagem_erro = mensagem_erro_element.text.strip()
        if mensagem_erro:
            print(f"⚠️ Mensagem de erro detectada: {mensagem_erro}")
    except:
        print("✅ Nenhuma mensagem de erro detectada.")
# -----------------------------------------------------------------------------------CASO SEJA NFC --------------------------------------------------------------------------------------------------------------------#
if tipo_arquivo == "NFC":
    try:
        pesquisar_por = empresa_dados["Pesquisar Por"].strip()
        tipo_pesquisa_element = wait.until(EC.presence_of_element_located((By.ID, "tipoPesquisa")))
        select_pesquisa = Select(tipo_pesquisa_element)
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
        data_inicial = empresa_dados["Data Inicial"]
        data_final = empresa_dados["Data Final"]
        data_inicial = data_inicial.strftime("%d/%m/%Y") if isinstance(data_inicial, pd.Timestamp) else str(data_inicial).strip()
        data_final = data_final.strftime("%d/%m/%Y") if isinstance(data_final, pd.Timestamp) else str(data_final).strip()
        if not (validar_data(data_inicial) and validar_data(data_final)):
            print("❌ Formato de data inválido na planilha. Corrija e tente novamente.")
            sys.exit(1)
        campo_data_inicial = wait.until(EC.presence_of_element_located((By.ID, "dtInicio")))
        campo_data_final = wait.until(EC.presence_of_element_located((By.ID, "dtFinal")))
        campo_data_inicial.clear()
        campo_data_inicial.send_keys(data_inicial)
        campo_data_final.clear()
        campo_data_final.send_keys(data_final)
        print(f"✅ Datas preenchidas: {data_inicial} até {data_final}")
        botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
        botao_ok.click()
        print("✅ Consulta Finalizada")
    except Exception as e:
        print(f"❌ Erro ao preencher as datas: {e}")
        sys.exit(1)
    #---------------------------MENSAGEM DE ERRO ------------------------------------------------
    try:
        mensagem_erro_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fontMessageError")))
        mensagem_erro = mensagem_erro_element.text.strip()
        if mensagem_erro:
            print(f"⚠️ Mensagem de erro detectada: {mensagem_erro}")
    except:
        print("✅ Nenhuma mensagem de erro detectada.")
# -----------------------------------------------------------------------------------CASO SEJA CTE --------------------------------------------------------------------------------------------------------------------#
if tipo_arquivo == "CTE":
    try:
        pesquisar_por = empresa_dados["Pesquisar Por"].strip()
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
            campo_elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, campo_id))
            )
            if not campo_elemento.is_selected():
                campo_elemento.click()
                print(f"✅ Tipo de pesquisa '{pesquisar_por}' selecionado com sucesso!")
            else:
                print(f"ℹ️ O tipo de pesquisa '{pesquisar_por}' já estava selecionado.")
        else:
            print(f"❌ Tipo de pesquisa inválido na planilha: {pesquisar_por}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao selecionar o tipo de pesquisa: {e}")
        sys.exit(1)
    # -------------------------------------- PREENCHIMENTO DE DATAS --------------------------------------#
    try:
        data_inicial = empresa_dados["Data Inicial"]
        data_final = empresa_dados["Data Final"]
        data_inicial = data_inicial.strftime("%d/%m/%Y") if isinstance(data_inicial, pd.Timestamp) else str(data_inicial).strip()
        data_final = data_final.strftime("%d/%m/%Y") if isinstance(data_final, pd.Timestamp) else str(data_final).strip()
        if not (validar_data(data_inicial) and validar_data(data_final)):
            print("❌ Formato de data inválido na planilha. Corrija e tente novamente.")
            sys.exit(1)
        campo_data_inicial = wait.until(EC.presence_of_element_located((By.ID, "dtInicio")))
        campo_data_final = wait.until(EC.presence_of_element_located((By.ID, "dtFinal")))
        campo_data_inicial.clear()
        campo_data_inicial.send_keys(data_inicial)
        campo_data_final.clear()
        campo_data_final.send_keys(data_final)
        print(f"✅ Datas preenchidas: {data_inicial} até {data_final}")
        botao_ok = wait.until(EC.element_to_be_clickable((By.ID, "okButton")))
        botao_ok.click()
        print("✅ Consulta Finalizada")
    except Exception as e:
        print(f"❌ Erro ao preencher as datas: {e}")
        sys.exit(1)
    #---------------------------MENSAGEM DE ERRO ------------------------------------------------
    try:
        mensagem_erro_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fontMessageError")))
        mensagem_erro = mensagem_erro_element.text.strip()
        if mensagem_erro:
            print(f"⚠️ Mensagem de erro detectada: {mensagem_erro}")
    except:
        print("✅ Nenhuma mensagem de erro detectada.")