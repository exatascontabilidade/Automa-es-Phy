import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env (se existir)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path, verbose=True, override=True)

# Configurações do e-mail (obtidas de variáveis de ambiente)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"
SAVE_PATH = "boletos"

if os.path.exists(dotenv_path):
    print(f"✅ Arquivo .env encontrado em: {dotenv_path}")
else:
    print("❌ Arquivo .env não encontrado!")

print("EMAIL_USER:", EMAIL_USER)
print("EMAIL_PASS:", "******" if EMAIL_PASS else None)

def connect_email():
    try:
        print(f"Conectando com o usuário: {EMAIL_USER}")  # Depuração
        if not EMAIL_USER or not EMAIL_PASS:
            raise ValueError("Credenciais de e-mail não foram carregadas corretamente.")
        
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        return mail
    except Exception as e:
        print(f"Erro ao conectar ao e-mail: {e}")
        return None

def search_emails(mail):
    try:
        today = datetime.today().strftime('%d-%b-%Y')
        query = f'(SINCE "{today}" SUBJECT "boleto")'
        status, messages = mail.search(None, query)
        return messages[0].split()
    except Exception as e:
        print(f"Erro ao buscar e-mails: {e}")
        return []

def download_attachments(mail, messages):
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    
    for msg_id in messages:
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                for part in msg.walk():
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            filepath = os.path.join(SAVE_PATH, filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f'📥 Boleto baixado: {filepath}')

def main():
    mail = connect_email()
    if not mail:
        return
    
    messages = search_emails(mail)
    
    if messages:
        print(f'📧 {len(messages)} e-mails encontrados.')
        download_attachments(mail, messages)
    else:
        print('❌ Nenhum boleto encontrado para hoje.')
    
    mail.logout()

if __name__ == '__main__':
    main()
