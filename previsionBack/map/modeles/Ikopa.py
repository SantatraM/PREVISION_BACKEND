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

class Ikopa(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.CharField(max_length=254, blank=True, null=True)
    nomrivi_re = models.CharField(db_column='nomrivi�re', max_length=25, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    long_km = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ikopa'
        
    def get_Ikopa(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id,ST_AsGeoJSON(geom) as geom , name FROM rivieres"
                print(sql)
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")