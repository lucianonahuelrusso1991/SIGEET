import os
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = '/app/google_credentials.json'

def test_auth():
    print("Iniciando prueba de conexion con Google Cloud...")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"[ERROR] No se encontro el archivo de credenciales en {CREDENTIALS_FILE}")
        sys.exit(1)
        
    try:
        # El alcance (scope) que necesitamos para Classroom
        SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']
        
        print(" > Leyendo archivo JSON...")
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
            
        print(" > Autenticando con Google APIs...")
        service = build('classroom', 'v1', credentials=creds)
        
        print(" > Solicitando lista de cursos de prueba (esto puede dar un error normal si el robot no fue invitado a ninguna clase aun)...")
        results = service.courses().list(pageSize=5).execute()
        courses = results.get('courses', [])
        
        print("==================================================")
        print("EXITO TOTAL: El archivo JSON es valido y el robot")
        print("ha logrado autenticarse correctamente en Google.")
        print(f"Cursos encontrados: {len(courses)}")
        print("==================================================")
        
    except Exception as e:
        print("==================================================")
        print("[ERROR] Fallo la autenticacion.")
        print(f"Detalle del error: {e}")
        print("==================================================")

if __name__ == '__main__':
    test_auth()
