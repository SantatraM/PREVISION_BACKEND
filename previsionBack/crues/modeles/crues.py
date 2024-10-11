from django.db import models
from previsionBack.utils import requete
from previsionBack.utils import insertion
from previsionBack.utils import dispatchall
from pluie import Pluiecrues
from hauteur_Debit import Hauteurdebitcrues
from django.db import connection

class Crues(models.Model):
    
    def insert_crues(self,hauteur,debit,pluie,station,datecrues):
        try:
            insertion("hauteurdebitcrues(idstation,datecrues,hauteur,debit)",[station,datecrues,hauteur,debit])
            insertion("pluiecrues(idstation,datecrues,pluie)",[station,datecrues,pluie])
            return True
        except Exception as e:
            raise Exception(f"Error inserting mesure: {e}")
        
    def update_crues(self,hauteur,debit,pluie,idhauteur,idpluie):
        try:
            hauteur_debit = Hauteurdebitcrues(id = idhauteur)
            pluie = Pluiecrues(id = idpluie)
            hauteur_debit.update_hauteur_debit(hauteur,debit)
            pluie.update_pluie(pluie)
            return True
        except Exception as e:
            raise Exception(f"Error updating crues: {e}")
        
    def get_crues(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_crues"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_crues_by_date(self,dateDebut,dateFin,idstation):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_crues where datecrues::date between %s and %s and idstation = %s order by datecrues asc"
                cursor.execute(sql,[dateDebut,dateFin,idstation])
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")

    def get_today_crues(self,idstation):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_crues where datecrues::date = current_date and idstation = %s order by datecrues asc"
                cursor.execute(sql,[idstation])
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def search_crues(self,idstation,hauteur,debit,pluie):
        try:
            conditions = []
            if idstation:
                conditions.append(f"idstation='{idstation}'")
            if debit:
                conditions.append(f"debit={debit}")
            if hauteur:
                conditions.append(f"hauteur={hauteur}")
            if pluie:
                conditions.append(f"pluie={pluie}")
                
            if conditions:
                sql = f"SELECT * FROM v_crues where " + " AND ".join(conditions)
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = dispatchall(cursor)
                return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
