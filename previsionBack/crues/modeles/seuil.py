from django.db import models
from station.modeles.station import Station
from django.db import connection
from previsionBack.utils import dispatchall

class Seuil(models.Model):
    idseuil = models.CharField(primary_key=True)
    idstation = models.ForeignKey(Station, models.DO_NOTHING, db_column='idstation', blank=True, null=True)
    rouge = models.FloatField(blank=True, null=True)
    jaune = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seuil'

    def get_seuil(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_seuil"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_seuil_by_id_station(self,idstation):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_seuil where idstation = %s"
                cursor.execute(sql)
                result = dispatchall(cursor,[idstation])
            return result[0] if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
            
    def insert_seuil(self,idstation):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO seuil (idstation,rouge,jaune) VALUES (%s,%s,%s)"
                cursor.execute(sql, [idstation,self.rouge,self.jaune])
                return True
        except Exception as e:
            raise Exception(f"Error inserting seuil: {e}")
        
    def update_seuil(self):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE seuil set rouge= %s , jaune = %s where idseuil = %s"
                cursor.execute(sql,[self.rouge,self.jaune,self.idseuil])
                return True
        except Exception as e:
            raise Exception(f"Error updating seuil: {e}")
        
    def delete_seuil(self):
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM seuil where idseuil= %s"
                cursor.execute(sql,[self.idseuil])
                return True
        except Exception as e:
            raise Exception(f"Error deleting seuil: {e}")
        
        