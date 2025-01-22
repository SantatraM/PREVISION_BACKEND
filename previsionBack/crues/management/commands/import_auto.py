# crues/management/commands/import_auto.py
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.core.management.base import BaseCommand
from ...modeles.hauteur_Debit import Hauteurdebitcrues
from ...modeles.pluie import Pluiecrues

class Command(BaseCommand):
    help = 'Surveille un dossier et insère les nouveaux fichiers CSV dans la base de données'

    def handle(self, *args, **kwargs):
        class Watcher:
            DIRECTORY_TO_WATCH = "/home/hp/Stage/import_auto"  # Chemin à surveiller

            def __init__(self):
                self.observer = Observer()

            def run(self):
                event_handler = Handler()
                self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
                self.observer.start()
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    self.observer.stop()
                self.observer.join()

        class Handler(FileSystemEventHandler):
            @staticmethod
            def process(event):
                if event.is_directory:
                    return None
                elif event.event_type == 'created':
                    file_path = event.src_path
                    print(f"chemin : {file_path}")
                    file_name = os.path.basename(file_path)
                    print(f"Fichier détecté : {file_name}")
                    # Vérifiez si le fichier correspond aux types attendus
                    if "Debit" in file_name:
                        print(f"Debit ita")
                        Hauteurdebitcrues.import_auto_hauteur_debit(file_name , file_path)
                    elif "Pluvio" in file_name:
                        Pluiecrues.import_auto_pluie(file_name,file_path)

            def on_created(self, event):
                self.process(event)

        watcher = Watcher()
        watcher.run()
