from django.db import models
from django.db import connection
from previsionBack.utils import dispatchall

class Commune(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_region = models.CharField(max_length=40, blank=True, null=True)
    nom_distri = models.CharField(max_length=40, blank=True, null=True)
    nom_commun = models.CharField(max_length=30, blank=True, null=True)
    nb_menages = models.FloatField(blank=True, null=True)
    pop_hommes = models.FloatField(blank=True, null=True)
    pop_femmes = models.FloatField(blank=True, null=True)
    pop_ensemb = models.FloatField(blank=True, null=True)
    taille_moy = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commune'

    def get_commune(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT c.id,ST_AsGeoJSON(c.geom) as geom, c.nom_commun FROM v_commune_analamanga c left join communeStation cs ON cs.idCommune = c.id where cs.idcommune is null"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_All_Commune(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * from v_commune_Analamanga"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def insert_commune_station(self,idStation,idCommune):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO communeStation values(default, %s , %s)"
                cursor.execute(sql, [idStation,idCommune])
                return True
        except Exception as e:
            raise Exception(f"Error inserting station: {e}")
        
    def get_commune_with_vigilence(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * from v_vigilence_commune"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_commune_with_alert(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * from v_vigilence_commune where couleur != 'grey'"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
            
    def get_nombre_commune_sous_vigilence(self):
        with connection.cursor() as cursor:
            sql = "SELECT total FROM v_nombre_commune_sous_vigilence"
            cursor.execute(sql)
            result = cursor.fetchone()  
            return result[0] 

    def get_nombre_population_sous_vigilence_rouge(self):
        with connection.cursor() as cursor:
            sql = "select COALESCE(SUM(pop_ensemb), 0) AS total_population from v_vigilence_commune where couleur='red'"
            cursor.execute(sql)
            result = cursor.fetchone()  
            return result[0] 
        
    def get_nombre_population_sous_vigilence_jaune(self):
        with connection.cursor() as cursor:
            sql = "select COALESCE(SUM(pop_ensemb), 0) AS total_population from v_vigilence_commune where couleur='yellow'"
            cursor.execute(sql)
            result = cursor.fetchone()  
            return result[0] 
    
    def get_pourcentage_commune_alerteRouge(self): 
        with connection.cursor() as cursor:
            sql = "select pourcentage from v_pourcentage_communes_alertes where couleur='red'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
        
    def get_pourcentage_commune_alerteJaune(self): 
        with connection.cursor() as cursor:
            sql = "select pourcentage from v_pourcentage_communes_alertes where couleur='yellow'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
    
    def get_pourcentage_commune_without_alert(self): 
        with connection.cursor() as cursor:
            sql = "select pourcentage from v_pourcentage_communes_alertes where couleur='grey'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]