from django.db import models
from django.db import connection
from previsionBack.utils import dispatchall

class Formuledebit(models.Model):
    id = models.CharField(primary_key=True)
    idstation = models.ForeignKey('Station', models.DO_NOTHING, db_column='idstation', blank=True, null=True)
    condition = models.FloatField(blank=True, null=True)
    formule = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formuledebit'

    def get_formule_by_id_station(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_formule where idstation = %s"
                cursor.execute(sql,[self.idstation])
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_formule():
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_formule"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def insert_formule(self):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO formule (idstation,condition,formule) VALUES (%s,%s,%s)"
                cursor.execute(sql, [self.idstation,self.condition,self.formule])
                return True
        except Exception as e:
            raise Exception(f"Error inserting formule: {e}")
        
    def update_formule(self):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE formule set idstation= %s , condition = %s , formule = %s where id = %s"
                cursor.execute(sql,[self.idstation,self.condition,self.formule,self.id])
                return True
        except Exception as e:
            raise Exception(f"Error updating formule: {e}")
        
    def delete_formule(self):
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM formule where id= %s"
                cursor.execute(sql,[self.id])
                return True
        except Exception as e:
            raise Exception(f"Error deleting formule: {e}")
        