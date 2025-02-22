import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def trocar_para_nova_janela(navegador):
    """Troca o foco do Selenium para a última janela aberta."""
    time.sleep(3)  # Espera a nova aba carregar completamente
    janelas = navegador.window_handles  # Obtém todas as janelas abertas
    navegador.switch_to.window(janelas[-1])  # Muda para a última aba/janela
    print("✅ Alternado para a nova aba com sucesso!")

def carregar_elemento(navegador, by, valor, timeout=10):
    """Aguarda dinamicamente um elemento estar presente na nova página."""
    return WebDriverWait(navegador, timeout).until(EC.presence_of_element_located((by, valor)))

def fechar_popup(navegador):
    """Fecha o popup se ele estiver presente."""
    # 🛑 Verifica se o popup está presente e visível antes de tentar fechá-lo
    try:
        popup = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MuiDialog-container"))
        )
        
        if popup.is_displayed():
            print("🔍 Popup detectado! Tentando fechar...")

            # ⬅️ Alternativa 1: Clicar diretamente no botão de fechar do popup, se existir
            try:
                botao_fechar = popup.find_element(By.XPATH, ".//button[contains(@class, 'MuiButtonBase-root')]")
                botao_fechar.click()
                print("✅ Popup fechado com sucesso!")
                time.sleep(2)
            except:
                print("⚠️ Nenhum botão de fechar encontrado, tentando clicar fora.")

                # ⬅️ Alternativa 2: Clicar fora do modal para fechá-lo
                navegador.execute_script("document.querySelector('.MuiDialog-container').click();")
                time.sleep(2)

    except Exception:
        print("⚠️ Nenhum popup detectado ou erro ao tentar fechá-lo.")

def carregar_elemento(navegador, by, valor, timeout=10):
    """Aguarda dinamicamente um elemento estar presente na página."""
    return WebDriverWait(navegador, timeout).until(EC.presence_of_element_located((by, valor)))


def listar_elementos_tabela(navegador):
    """Lista todas as linhas da tabela para entender a estrutura dos elementos."""
    try:
        print("📌 Listando estrutura da tabela...")
        linhas = navegador.find_elements(By.XPATH, "//tr")
        for i, linha in enumerate(linhas):
            celulas = linha.find_elements(By.XPATH, ".//*")  # Pegando todos os elementos dentro da linha    
    except Exception as e:
        print(f"❌ Erro ao listar elementos da tabela: {e}")




def baixar_boletos_atrasados(navegador):
    
    trocar_para_nova_janela(navegador)
    fechar_popup(navegador)
    
    try:
        print("🔍 Buscando parcelas em atraso...")

        # Buscar todas as linhas da tabela (exceto o cabeçalho)
        linhas_parcelas = navegador.find_elements(By.XPATH, "//tr")[1:]  # Ignora a primeira linha (cabeçalho)

        encontrou_atraso = False  # Flag para verificar se alguma parcela foi encontrada

        for linha in linhas_parcelas:
            try:
                # Buscar todas as células da linha
                celulas = linha.find_elements(By.XPATH, ".//td")

                if len(celulas) < 2:
                    print("⚠️ Linha sem informações suficientes, pulando...")
                    continue

                situacao = celulas[1].text.strip()  # Segunda célula contém a situação

                if "Em aberto" in situacao or "Vencida" in situacao:
                    encontrou_atraso = True
                    print(f"⚠️ Parcela em atraso encontrada: {situacao}")

                    # Buscar o botão de download dentro da linha
                    try:
                        botao_download = linha.find_element(By.XPATH, ".//button[contains(@class, 'MuiButtonBase-root') and contains(@class, 'MuiIconButton-root')]")

                        if botao_download:
                            print("📥 Clicando no botão de download...")
                            navegador.execute_script("arguments[0].click();", botao_download)
                            time.sleep(3)  # Tempo para abrir a nova janela

                    except Exception as e:
                        print(f"⚠️ Erro ao tentar clicar no botão de download: {e}")

            except Exception as e:
                print(f"⚠️ Erro ao processar uma linha da tabela: {e}")

        if not encontrou_atraso:
            print("✅ Nenhuma parcela em atraso encontrada.")

    except Exception as e:
        print(f"❌ Erro ao localizar parcelas em atraso: {e}")

    print("✅ Processo concluído!")