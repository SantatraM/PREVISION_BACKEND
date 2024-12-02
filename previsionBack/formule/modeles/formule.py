from django.db import models
from django.db import connection
from previsionBack.utils import dispatchall
import re
from station.modeles.station import Station

class Formuledebit(models.Model):
    id = models.CharField(primary_key=True)
    idstation = models.ForeignKey(Station, on_delete=models.CASCADE) 
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
        
    def insert_formule(self,idstation):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO formuledebit (idstation,condition,formule) VALUES (%s,%s,%s)"
                cursor.execute(sql, [idstation,self.condition,self.formule])
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
      
    def format_formule(self,formule, variables_valeurs):
        """Remplace les variables dans la formule par leurs valeurs."""
        if variables_valeurs:
            for variable_valeur in variables_valeurs.split(','):
                if '=' in variable_valeur:
                    variable, valeur = variable_valeur.split('=')
                    formule = re.sub(r'\b{}\b'.format(variable.strip()), valeur.strip(), formule)
        return formule
      
    def get_formule_with_variable(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_formule_variable"
                cursor.execute(sql)
                result = dispatchall(cursor)
                for item in result:
                    formule = item['formule']
                    variables_valeurs = item.get('variables_valeurs', '')
                    formule_finale = self.format_formule(formule, variables_valeurs)
                    item['formulefinal'] = formule_finale
                return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")   

    def get_formule_debit_with_condition(self,hauteur,idstation):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_formule_variable where %s <= condition and idstation= %s order by condition asc"
                cursor.execute(sql,[hauteur,idstation])
                print(sql)
                result = dispatchall(cursor)
                for item in result:
                    formule = item['formule']
                    variables_valeurs = item.get('variables_valeurs','')
                    formule_finale = self.format_formule(formule,variables_valeurs)
                    item['formulefinal'] = formule_finale
                return result[0] if result else []
        except Exception as e:
            raise Exception(f"error: {e}")
        
    def get_formule_debit_without_condition(self,hauteur,idstation):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_formule_variable where %s <= condition and idstation= %s order by condition desc"
                cursor.execute(sql,[hauteur,idstation])
                print(sql)
                result = dispatchall(cursor)
                for item in result:
                    formule = item['formule']
                    variables_valeurs = item.get('variables_valeurs','')
                    formule_finale = self.format_formule(formule,variables_valeurs)
                    item['formulefinal'] = formule_finale
                return result[0] if result else []
        except Exception as e:
            raise Exception(f"error: {e}")