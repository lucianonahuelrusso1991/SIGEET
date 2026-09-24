from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
import os
import zipfile

class Command(BaseCommand):
    help = 'Crea un backup JSON de la base de datos y lo envia por correo electrónico'

    def handle(self, *args, **options):
        # El email de destino se toma de las variables de entorno o usamos el host por defecto
        destinatario = os.getenv('BACKUP_EMAIL_DEST', settings.EMAIL_HOST_USER)
        if not destinatario:
            self.stdout.write(self.style.ERROR('No hay EMAIL_HOST_USER configurado para enviar el backup.'))
            return

        fecha_str = datetime.now().strftime('%Y-%m-%d_%H-%M')
        json_file = f'/tmp/backup_sigeet_{fecha_str}.json'
        zip_file = f'/tmp/backup_sigeet_{fecha_str}.zip'

        self.stdout.write(f"Creando backup en {json_file}...")
        
        # Excluimos contenttypes y permissions para evitar errores si se restaura en otra DB
        with open(json_file, 'w', encoding='utf-8') as f:
            call_command('dumpdata', exclude=['auth.permission', 'contenttypes'], indent=2, stdout=f)
            
        self.stdout.write(f"Comprimiendo archivo...")
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(json_file, os.path.basename(json_file))
            
        self.stdout.write(f"Enviando correo a {destinatario}...")
        try:
            email = EmailMessage(
                subject=f'Backup Automático SIGEET - {fecha_str}',
                body='Adjunto el backup automático de la base de datos generado por el sistema SIGEET.',
                from_email=settings.EMAIL_HOST_USER,
                to=[destinatario],
            )
            email.attach_file(zip_file)
            email.send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f'Backup enviado con éxito a {destinatario}.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error enviando el correo: {str(e)}'))
        
        # Limpiar temporales
        if os.path.exists(json_file):
            os.remove(json_file)
        if os.path.exists(zip_file):
            os.remove(zip_file)