from google_auth_oauthlib.flow import InstalledAppFlow

# Escopo necessário apenas para enviar e-mail
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gerar_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        './usuarios/credentials.json', SCOPES
    )
    creds = flow.run_local_server(port=0)  # Abre navegador para login
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("✅ token.json gerado com sucesso!")

if __name__ == "__main__":
    gerar_token()
