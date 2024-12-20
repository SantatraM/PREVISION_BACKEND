from django.db import models
from django.db import connection
from previsionBack.utils import dispatchall


class Station(models.Model):
    idstation = models.CharField(primary_key=True)
    site = models.CharField(max_length=50, blank=True, null=True)
    idsousbassin = models.ForeignKey('Sousbassin', models.DO_NOTHING, db_column='idsousbassin', blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    idmesure = models.ForeignKey('Mesure', models.DO_NOTHING, db_column='idmesure', blank=True, null=True)
    code = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'station'

    def get_station_by_id(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_station where idstation= %s"
                cursor.execute(sql,[self.idstation])
                result = dispatchall(cursor)
            return result[0] if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_station_by_code(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT idstation FROM station WHERE code = %s"
                cursor.execute(sql, [self.code])
                result = cursor.fetchone() 
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la station avec le code '{self.code}': {e}")
        
    def get_station(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_station"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_station_without_seuil(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_station_sans_seuil"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def insert_station(self,idsousbassin,idmesure):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO station (site,idsousbassin,longitude,latitude,idmesure,code) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, [self.site,idsousbassin,self.longitude,self.latitude,idmesure,self.code])
                return True
        except Exception as e:
            raise Exception(f"Error inserting station: {e}")
    
    def update_station(self,idsousbassin,idmesure):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE station set site= %s , idsousbassin = %s , longitude = %s , latitude = %s , idmesure = %s , code = %s where idstation = %s"
                cursor.execute(sql,[self.site,idsousbassin,self.longitude,self.latitude,idmesure,self.code,self.idstation])
                return True
        except Exception as e:
            raise Exception(f"Error updating station: {e}")
        