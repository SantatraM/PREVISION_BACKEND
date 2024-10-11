from django.db import models
from django.db import connection
from previsionBack.utils import dispatchall


class Mesure(models.Model):
    idmesure = models.CharField(primary_key=True)
    mesure = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mesure'

    def get_mesure_by_id(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM mesure where idmesure= %s"
                cursor.execute(sql,[self.idmesure])
                result = dispatchall(cursor)
            return result[0] if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_mesure(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM mesure"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def insert_mesure(self):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO mesure (mesure) VALUES (%s)"
                cursor.execute(sql, [self.mesure])
                return True
        except Exception as e:
            raise Exception(f"Error inserting mesure: {e}")
        
    def update_mesure(self):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE mesure set mesure= %s where idmesure = %s"
                cursor.execute(sql,[self.mesure,self.idmesure])
                return True
        except Exception as e:
            raise Exception(f"Error updating mesure: {e}")
        
    def delete_mesure(self):
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM mesure where idmesure= %s"
                cursor.execute(sql,[self.idmesure])
                return True
        except Exception as e:
            raise Exception(f"Error deleting mesure: {e}")
        
    
