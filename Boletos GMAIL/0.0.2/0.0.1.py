import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Escopo de leitura de e-mails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def autenticar_gmail():
    """Autentica e retorna um serviço Gmail API"""
    creds = None
    # O arquivo token.pickle armazena o token de acesso do usuário e é
    # criado automaticamente quando o fluxo de autorização é completado pela primeira vez.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Se não temos credenciais válidas, faça o login do usuário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Salva as credenciais para o próximo uso
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Construa o serviço Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service

def listar_mensagens(service):
    """Lista as mensagens da caixa de entrada"""
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    if not messages:
        print('Nenhuma mensagem encontrada.')
    else:
        print('Mensagens:')
        for message in messages[:5]:  # Lista as 5 primeiras mensagens
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(f"Mensagem ID: {msg['id']}")
            print(f"Assunto: {msg['payload']['headers'][0]['value']}")

def main():
    # Autentica e obtém o serviço da API Gmail
    service = autenticar_gmail()

    # Lista as mensagens na caixa de entrada
    listar_mensagens(service)

if __name__ == '__main__':
    main()
