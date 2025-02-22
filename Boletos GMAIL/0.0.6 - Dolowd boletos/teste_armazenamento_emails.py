from listar_emails_storage import obter_emails_encontrados
import json
import os

ARQUIVO_EMAILS = "emails_encontrados.json"

def carregar_emails():
    """Carrega os e-mails armazenados do arquivo JSON."""
    if not os.path.exists(ARQUIVO_EMAILS):
        print("❌ Nenhum e-mail armazenado!")
        return []

    with open(ARQUIVO_EMAILS, "r", encoding="utf-8") as f:
        return json.load(f)

def testar_armazenamento_emails():
    """Função de teste para verificar se os e-mails estão armazenados corretamente."""
    emails = carregar_emails()
    
    if not emails:
        print("❌ Nenhum e-mail armazenado!")
        return
    
    print("✅ E-mails armazenados:")
    emails_por_remetente = {}
    
    for email in emails:
        remetente = email["remetente"]
        assunto = email["assunto"]
        data = email["data"]
        
        if remetente not in emails_por_remetente:
            emails_por_remetente[remetente] = []
        
        emails_por_remetente[remetente].append({"assunto": assunto, "data": data})
    
    for remetente, mensagens in emails_por_remetente.items():
        print(f"📧 Remetente: {remetente}")
        for msg in mensagens:
            print(f"   📌 Assunto: {msg['assunto']}")
            print(f"   📅 Data: {msg['data']}")
            print("-" * 75)
        print("-" * 100)

if __name__ == "__main__":
    testar_armazenamento_emails()
