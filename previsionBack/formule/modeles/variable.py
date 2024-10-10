from django.db import models
from django.db import connection
from previsionBack.utils import dispatchall

class Variableformule(models.Model):
    id = models.CharField(primary_key=True)
    idformule = models.ForeignKey('Formuledebit', models.DO_NOTHING, db_column='idformule', blank=True, null=True)
    variable = models.CharField(max_length=5, blank=True, null=True)
    valeur = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variableformule'

    def get_variable_by_formule(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM variableformule where idformule=%s"
                cursor.execute(sql,[self.idformule])
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
    
    def insert_variable_formule(self):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO variableformule (idformule,variable,valeur) VALUES (%s,%s,%s)"
                cursor.execute(sql, [self.idformule,self.variable,self.valeur])
                return True
        except Exception as e:
            raise Exception(f"Error inserting variable formule: {e}")
    
    def update_variable_formule(self):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE variableformule set valeur= %s ,  where id = %s"
                cursor.execute(sql,[self.valeur,self.id])
                return True
        except Exception as e:
            raise Exception(f"Error updating variable formule: {e}")