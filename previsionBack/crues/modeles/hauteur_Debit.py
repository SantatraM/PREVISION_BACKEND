from django.db import models
from formule.modeles.formule import Formuledebit
import pandas as pd
from previsionBack.utils import requete
from previsionBack.utils import insertion
from rest_framework.response import Response
from station.modeles.station import Station
from django.db import connection

class Hauteurdebitcrues(models.Model):
    id = models.CharField(primary_key=True)
    idstation = models.ForeignKey(Station, models.DO_NOTHING, db_column='idstation', blank=True, null=True)
    datecrues = models.DateTimeField(blank=True, null=True)
    hauteur = models.FloatField(blank=True, null=True)
    debit = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hauteurdebitcrues'

    def calcul_debit_with_condition_by_id_station(self,hauteur,idstation):
        try:
            formuledebit = Formuledebit()
            result = formuledebit.get_formule_debit_with_condition(hauteur,idstation)
            formule = result.get('formulefinal')
            print("formule = "+formule)
            h = hauteur
            debit = eval(formule)
            return debit
        except Exception as e:
            raise Exception(f"error: {e}")
        
    def calcul_debit_without_condition_by_id_station(self,hauteur,idstation):
        try:
            formuledebit = Formuledebit()
            result = formuledebit.get_formule_debit_without_condition(hauteur,idstation)
            formule = result.get('formulefinal')
            print("formule = "+formule)
            h = hauteur
            debit = eval(formule)
            return debit
        except Exception as e:
            raise Exception(f"error: {e}")
    
    def import_hauteur_debit(self, file, station, condition):
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
                    hauteur = row.get('Hauteur')
                    
                    if pd.isnull(hauteur):
                        hauteur = None
                        debit = None
                    else:
                        if condition == '1':
                            debit = self.calcul_debit_with_condition_by_id_station(hauteur, station)
                        else:
                            debit = self.calcul_debit_without_condition_by_id_station(hauteur, station)
                    insertion("hauteurdebitimport", [station, dateCrues, hauteur, str(debit) if debit is not None else None])
            requete("select dispatchHauteur()")
            requete("truncate table hauteurdebitimport")
            return True
        except Exception as e:
            raise Exception(f"error: {e}")
        
    def update_hauteur_debit(self,hauteur,debit):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE hauteurdebitcrues set hauteur= %s , debit = %s where id = %s"
                cursor.execute(sql,[hauteur,debit,self.id])
                return True
        except Exception as e:
            raise Exception(f"Error updating hauteur_debit: {e}")
        
    def import_auto_hauteur_debit(filename,filepath):
        try:
            code_station = filename[:6]
            print(f"code_station { code_station }")
            station = Station(code=code_station)
            idstation = station.get_station_by_code() 
            if not idstation:
                raise Exception(f"Aucune station trouvée pour le code: {code_station}")
            print(f"idstation = {idstation}")
            if filepath.endswith('.csv'):
                data = pd.read_csv(filepath)
            elif filepath.endswith('.xls') or filepath.endswith('.xlsx'):
                data = pd.read_excel(filepath)
            else:
                raise Exception("Format de fichier non pris en charge. Utilisez un fichier CSV ou Excel.")
            
            for _, row in data.iterrows():
                datecrues = row.get('DATE')
                hauteur = row.get('HAUTEUR')
                debit = row.get('DEBIT')
                insertion("hauteurdebitimport",[idstation, datecrues, hauteur,debit])
            requete("SELECT dispatchHauteur()")
            requete("TRUNCATE TABLE hauteurdebitimport")
            return True
        except Exception as e:
            raise Exception(f"Erreur lors de l'import automatique de l'hauteur et debit : {e}")
            