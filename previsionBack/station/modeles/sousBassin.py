from django.db import models
from django.db import connection
from previsionBack.utils import dispatchall


class Sousbassin(models.Model):
    idsousbassin = models.CharField(primary_key=True)
    sousbassin = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'sousbassin'

    def get_sous_bassin_by_id(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM sousbassin where idsousbassin= %s"
                cursor.execute(sql,[self.idsousbassin])
                result = dispatchall(cursor)
            return result[0] if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_sous_bassin(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM sousbassin"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def insert_sous_bassin(self):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO sousbassin (sousbassin) VALUES (%s)"
                cursor.execute(sql, [self.sousbassin])
                return True
        except Exception as e:
            raise Exception(f"Error inserting sous bassin: {e}")
        
    def update_sous_bassin(self):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE sousbassin set sousbassin= %s where idsousbassin = %s"
                cursor.execute(sql,[self.sousbassin,self.idsousbassin])
                return True
        except Exception as e:
            raise Exception(f"Error updating sous bassin: {e}")
        
    def delete_sous_bassin(self):
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM sousbassin where idsousbassin= %s"
                cursor.execute(sql,[self.idsousbassin])
                return True
        except Exception as e:
            raise Exception(f"Error deleting sous bassin: {e}")
        
    
