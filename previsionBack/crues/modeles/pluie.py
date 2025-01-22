from django.db import models
from station.modeles.station import Station
import pandas as pd
from rest_framework.response import Response
from previsionBack.utils import requete
from previsionBack.utils import insertion
from django.db import connection

class Pluiecrues(models.Model):
    id = models.CharField(primary_key=True)
    idstation = models.ForeignKey(Station, models.DO_NOTHING, db_column='idstation', blank=True, null=True)
    datecrues = models.DateTimeField(blank=True, null=True)
    pluie = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pluiecrues'

    def import_pluie(self,file,station):
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)  
                dfs = [df]
            elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
                xls = pd.ExcelFile(file)  
                dfs = [xls.parse(sheet_name) for sheet_name in xls.sheet_names]
            else:
                return Response({'error': 'Type de fichier non supporté.'}, status=201)
            
            for df in dfs:
                for _, row in df.iterrows():
                    dateCrues = row.get('Date')
                    pluie = row.get('Pluie')
                    
                    insertion("pluieimport", [station, dateCrues, pluie])
            requete("select dispatchPluie()")
            requete("truncate table pluieimport")
            return True               
        except Exception as e:
            raise Exception(f"error: {e}")
        
    # def import_auto_pluie(filename,filepath):
    #     try:
    #         code_station = filename[:6]
    #         station = Station(code=code_station)
    #         idstation = station.get_station_by_code()
            
    #         if not idstation:
    #             raise Exception(f"Aucune station trouvée pour le code: {code_station}")

    #         if filepath.endswith('.csv'):
    #             data = pd.read_csv(filepath)
    #         elif filepath.endswith('.xls') or filepath.endswith('.xlsx'):
    #             data = pd.read_excel(filepath)
    #         else:
    #             raise Exception("Format de fichier non pris en charge. Utilisez un fichier CSV ou Excel.")
            
    #         if 'DATE' not in data.columns or 'VALEUR' not in data.columns:
    #             raise Exception("Le fichier doit contenir les colonnes 'DATE' et 'VALEUR'.")
            
    #         data['DATE'] = pd.to_datetime(data['DATE'], format='%d/%m/%Y %H:%M')

    #         # Regrouper les données par heure et sommer les valeurs de pluie
    #         data['DATE_HOUR'] = data['DATE'].dt.strftime('%d/%m/%Y %H:00')  # Garde uniquement la date et l'heure
    #         print(f"date : {data['DATE_HOUR']}")
    #         hourly_data = data.groupby('DATE_HOUR')['VALEUR'].sum().reset_index()


    #         for _, row in hourly_data.iterrows():
    #             datecrues = row['DATE_HOUR']
    #             pluie = row['VALEUR']
    #             insertion("pluieimport", [idstation, datecrues, pluie])

    #         # Appeler la fonction de traitement et vider la table temporaire
    #         requete("SELECT dispatchPluie()")  # Remplacez avec votre logique métier
    #         requete("TRUNCATE TABLE pluieimport")
            
    #         return True
    #     except Exception as e:
    #         raise Exception(f"Erreur lors de l'import automatique de pluie : {e}")
            
    def update_pluie(self,pluie):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE pluiecrues set pluie= %s where id = %s"
                cursor.execute(sql,[pluie,self.id])
                return True
        except Exception as e:
            raise Exception(f"Error updating pluie: {e}")
        
        
    def import_auto_pluie(filename, filepath):
        try:
            code_station = filename[:6]
            station = Station(code=code_station)
            idstation = station.get_station_by_code()
            
            if not idstation:
                raise Exception(f"Aucune station trouvée pour le code: {code_station}")

            # Charger le fichier
            if filepath.endswith('.csv'):
                data = pd.read_csv(filepath)
            elif filepath.endswith('.xls') or filepath.endswith('.xlsx'):
                data = pd.read_excel(filepath)
            else:
                raise Exception("Format de fichier non pris en charge. Utilisez un fichier CSV ou Excel.")

            # Vérifier les colonnes
            if 'DATE' not in data.columns or 'VALEUR' not in data.columns:
                raise Exception("Le fichier doit contenir les colonnes 'DATE' et 'VALEUR'.")

            # Convertir les dates
            data['DATE'] = pd.to_datetime(data['DATE'], format='%d/%m/%Y %H:%M')

            # Arrondir les dates à l'heure suivante
            data['DATE_HOUR'] = data['DATE'].dt.ceil('H')  # Arrondit au plafond de l'heure

            # Cumuler les valeurs par heure
            hourly_data = data.groupby('DATE_HOUR')['VALEUR'].sum().reset_index()

            # Insérer les données dans la base
            for _, row in hourly_data.iterrows():
                datecrues = row['DATE_HOUR'].strftime('%d/%m/%Y %H:00')
                pluie = row['VALEUR']
                insertion("pluieimport", [idstation, datecrues, pluie])

            # Appeler la fonction de traitement et vider la table temporaire
            requete("SELECT dispatchPluie()")  # Remplacez avec votre logique métier
            requete("TRUNCATE TABLE pluieimport")

            return True
        except Exception as e:
            raise Exception(f"Erreur lors de l'import automatique de pluie : {e}")
