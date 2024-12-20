# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db import connection
from previsionBack.utils import dispatchall

class Rivieres(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    id = models.AutoField(primary_key=True)
    geom = models.TextField(blank=True, null=True) 
    name = models.CharField(max_length=254, blank=True, null=True)
    nomrivi_re = models.CharField(db_column='nomrivi�re', max_length=25, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    long_km = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rivieres'

    def get_Rivieres(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id,ST_AsGeoJSON(geom) as geom , name FROM rivieres"
                print(sql)
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
    
    def get_Riviere(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * from riviere"
                print(sql)
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_Riviere_non_prise(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * from v_riviere_non_prise"
                print(sql)
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def insert_riviere(self,nomRiviere):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM riviere WHERE  LOWER(nom) = %s", [nomRiviere])
                count = cursor.fetchone()[0]

            if count > 0:
                raise Exception("La rivière avec ce nom existe déjà.")
            
            with connection.cursor() as cursor:
                sql = "INSERT INTO riviere(nom) values (%s)"
                cursor.execute(sql, [nomRiviere])
                return True
        except Exception as e:
            raise Exception(f"Error:{e}")