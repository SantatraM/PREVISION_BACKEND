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
                    
                    insertion("hauteurdebitimport", [station, dateCrues, pluie])
            requete("select dispatchPluie()")
            requete("truncate table pluieimport")
            return True               
        except Exception as e:
            raise Exception(f"error: {e}")
        
    def update_pluie(self,pluie):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE pluiecrues set pluie= %s where id = %s"
                cursor.execute(sql,[pluie,self.id])
                return True
        except Exception as e:
            raise Exception(f"Error updating pluie: {e}")
        