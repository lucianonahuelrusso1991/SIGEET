import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.rosters',
    'https://www.googleapis.com/auth/classroom.profile.emails'
]

def main():
    if not os.path.exists('client_secret.json'):
        print("ERROR: No se encontró 'client_secret.json' en la carpeta actual.")
        print("Debes descargarlo desde Google Cloud Console -> Pantalla OAuth -> Tipo Desktop.")
        return

    print("Abriendo el navegador para que inicies sesión como secretaria.alumnos@pioix.edu.ar...")
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    print("\n¡ÉXITO! Se generó el archivo 'token.json'.")
    print("Sube este archivo a tu servidor Hostinger en la carpeta /opt/sigeet/ (o en la misma carpeta del proyecto).")

if __name__ == '__main__':
    main()
