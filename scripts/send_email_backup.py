import smtplib
from email.message import EmailMessage
import sys
import os
from datetime import datetime

# ==========================================
# CONFIGURACION DE CORREO SMTP
# ==========================================
# (Completar cuando Antonio pase los datos de Google Workspace)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "tu_correo@colegio.edu.ar"
SMTP_PASSWORD = "tu_contraseña_o_app_password"
DESTINATARIO = "admin_backups@colegio.edu.ar"
# ==========================================

def send_backup(filepath):
    if SMTP_USER == "tu_correo@colegio.edu.ar":
        print(" > ADVERTENCIA: Correo no configurado. Solo se guardo el backup local.")
        return

    filename = os.path.basename(filepath)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    msg = EmailMessage()
    msg['Subject'] = f'SIGES Backup Diario - {date_str}'
    msg['From'] = SMTP_USER
    msg['To'] = DESTINATARIO
    msg.set_content('Adjunto se encuentra el backup automatico de la base de datos de SIGES.')

    # Adjuntar el archivo
    with open(filepath, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='gzip', filename=filename)

    try:
        # Enviar via SMTP SSL
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)
        print(" > Backup enviado por correo exitosamente.")
    except Exception as e:
        print(f" > ERROR al enviar correo: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Se requiere la ruta del archivo de backup.")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: No se encontro el archivo {filepath}")
        sys.exit(1)
        
    send_backup(filepath)
