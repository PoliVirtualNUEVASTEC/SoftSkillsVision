from googleapiclient.discovery import build
from google.oauth2 import service_account

#Cargando credenciales

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'C:/Users/carta/IdeaProjects/SoftSkillsVision/SoftSkillsVision/credentials.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,scopes = SCOPES
)

#Crear servicio de Google Drive
service = build('drive', 'v3', credentials = creds)

#ID de la carpeta en Google Drive
folder_id = "1SIiUPEmfQCwFfO3JIqGRlWjIKkQBqQkw"


#Listando los archivos en la carpeta
query =  f"'{folder_id}' in parents and trashed=false"
results = service.files().list(q=query, fields="files(id, name)").execute()
files = results.get('files', [])

if not files:
    print("No hay archivos en la carpeta.")
else:
    for file in files:
        print(f"Nombre: {file['name']} - ID: {file['id']}")