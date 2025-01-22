# crues/apps.py
from django.apps import AppConfig
from django.core.management import call_command
import threading
import os

class CruesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crues'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # Éviter de lancer plusieurs threads
            thread = threading.Thread(target=self.run_import_auto)
            thread.daemon = True  # Le thread s'arrête avec Django
            thread.start()

    def run_import_auto(self):
        try:
            call_command('import_auto')
        except Exception as e:
            print(f"Erreur : {e}")
