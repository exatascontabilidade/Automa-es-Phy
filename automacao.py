from playwright.sync_api import sync_playwright

def preencher_formulario(username, password, url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Defina True se não quiser abrir o navegador
        page = browser.new_page()
        page.goto(url)
        
        # Preencher os campos de username e password
        page.fill('input[name="UserName"]', username)
        page.fill('input[name="Password"]', password)
        
        # Clicar no botão de submit
        page.click('input[name="submit"]')
        
        # Manter a página aberta para verificação (remova se necessário)
        page.wait_for_timeout(5000)
        browser.close()

# Exemplo de uso
preencher_formulario("123.456.789-01", "minha_senha", "http://seusite.com/login")
