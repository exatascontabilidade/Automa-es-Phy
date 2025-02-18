import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime

# Configurações do e-mail
EMAIL_USER = "financeiroexatas136@gmail.com"
EMAIL_PASS = "Exatas1010@"
IMAP_SERVER = "imap.gmail.com"
SAVE_PATH = "boletos"

# Função para conectar ao e-mail
def connect_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    return mail

# Função para buscar e-mails com boletos
def search_emails(mail):
    today = datetime.today().strftime('%d-%b-%Y')
    query = f'(SINCE "{today}" SUBJECT "boleto")'
    status, messages = mail.search(None, query)
    return messages[0].split()

# Função para baixar anexos
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

# Definir fluxo principal
def main():
    mail = connect_email()
    messages = search_emails(mail)
    
    if messages:
        print(f'📧 {len(messages)} e-mails encontrados.')
        download_attachments(mail, messages)
    else:
        print('❌ Nenhum boleto encontrado para hoje.')
    mail.logout()

if __name__ == '__main__':
    main()
