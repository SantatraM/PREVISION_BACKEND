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
        
    def get_station(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM station"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def insert_station(self):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO station (site,idsousbassin,longitude,latitude,idmesure) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sql, [self.site,self.idsousbassin,self.longitude,self.latitude,self.idmesure])
                return True
        except Exception as e:
            raise Exception(f"Error inserting station: {e}")
    
    def update_station(self):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE station set site= %s , idsousbassin = %s , longitude = %s , latitude = %s , idmesure = %s where idstation = %s"
                cursor.execute(sql,[self.site,self.idsousbassin,self.longitude,self.latitude,self.idmesure,self.idstation])
                return True
        except Exception as e:
            raise Exception(f"Error updating station: {e}")
        