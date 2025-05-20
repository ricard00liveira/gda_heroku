from google_auth_oauthlib.flow import InstalledAppFlow

# Escopo necessário apenas para enviar e-mail
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def gerar_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret_819725946492-g66u5rqr6d9u7nqsidm9phrinm4mj5gb.apps.googleusercontent.com.json",
        SCOPES,
    )
    creds = flow.run_local_server(port=0)  # Abre navegador para login
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    print("✅ token.json gerado com sucesso!")


if __name__ == "__main__":
    gerar_token()
