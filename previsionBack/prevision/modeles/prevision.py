import math
from django.db import models
from django.db import connection
from datetime import timedelta
from previsionBack.utils import dispatchall
from datetime import datetime

class Prevision(models.Model):

    def get_id_station(station):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT idstation FROM station WHERE site= %s"
                cursor.execute(sql, [station])
                result = cursor.fetchone() 
                if result is not None:
                    return result[0]  
                else:
                    raise Exception("Aucun résultat trouvé.")
        except Exception as e:
            raise Exception(f"Error: {e}")

    def get_last_date(self, idstation):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT MAX(datecrues) 
                FROM v_crues 
                WHERE idstation = %s
            """, [idstation])
            result = cursor.fetchone()
            return result[0] if result else None

    def get_debit_at_time(self, idstation, time_point):
        with connection.cursor() as cursor:
            sql = "SELECT debit FROM v_crues WHERE idstation = %s AND datecrues = %s"
            # print(f"Exécution de la requête : {sql % (idstation, time_point)}")
            cursor.execute(sql, [idstation, time_point])
            result = cursor.fetchone()
            return result[0] if result else None
        
    def get_date_plus_pres(self,idstation,time_point):
        with connection.cursor() as cursor:
            sql = "SELECT datecrues FROM v_crues WHERE idstation = %s AND datecrues < %s AND debit IS NOT NULL ORDER BY datecrues desc limit 1 "
            cursor.execute(sql,[idstation,time_point])
            result = cursor.fetchone()
            return result[0] if result else None
    
    def calculer_intervalle_en_heures(self, date_debut, date_fin):
        if not isinstance(date_debut, datetime) or not isinstance(date_fin, datetime):
            raise ValueError("Les dates doivent être des objets datetime.")
            
        delta = date_fin - date_debut
        heures = delta.total_seconds() / 3600  
        return round(heures, 2)

    def get_debit_at_time_pres(self,idstation,time_point):
        with connection.cursor() as cursor:
            date_plus_pres = self.get_date_plus_pres(idstation,time_point)
            interval_temps = self.calculer_intervalle_en_heures(date_plus_pres,time_point)
            print(f"Intervalle de temps plus pres : {interval_temps} heures")
            if interval_temps > 2:
                raise Exception(f"Il est impossible de faire la prévision : l'intervalle de temps, plus près de {time_point}, est trop long.")
            else :
                sql = " SELECT debit FROM v_crues WHERE idstation = %s AND datecrues = %s "
                print(f"Exécution de la requête : {sql % (idstation, date_plus_pres)}")
                cursor.execute(sql, [idstation, date_plus_pres])
                result = cursor.fetchone()
            return result[0] if result else None       
    
    def calculate_dqprev(self, idstation):
        last_date = self.get_last_date(idstation)
        time_intervals = [0, 6, 12, 18, 24,30]
        debits = {}
        for hours in time_intervals:
            debit = self.get_debit_at_time(idstation, last_date - timedelta(hours=hours))
            if debit is None:
                debit = self.get_debit_at_time_pres(idstation, last_date - timedelta(hours=hours))
            debits[hours] = debit
        debit_diffs = {
            0: debits[0] - debits[6],
            6: debits[6] - debits[12],
            12: debits[12] - debits[18],
            18: debits[18] - debits[24],
            24: debits[24] - debits[30]
        }
        dqprev = (
            0.22 * debit_diffs[0] + 0.38 * debit_diffs[6] + 0.18 * debit_diffs[12] + 0.12 * debit_diffs[18] + 0.10 * debit_diffs[24]
        )
        return dqprev
    
    def calculate_dqprev12(self, idstation):
        last_date = self.get_last_date(idstation)
        dqprev6 = self.calculate_dqprev(idstation)
        time_intervals = [0, 6, 12, 18, 24,30]
        debits = {}
        for hours in time_intervals:
            debit = self.get_debit_at_time(idstation, last_date - timedelta(hours=hours))
            if debit is None:
                debit = self.get_debit_at_time_pres(idstation, last_date - timedelta(hours=hours))
            debits[hours] = debit
        debit_diffs = {
            0: debits[0] - debits[6],
            6: debits[6] - debits[12],
            12: debits[12] - debits[18],
            18: debits[18] - debits[24],
            24: debits[24] - debits[30]
        }
        dqprev12 = (
            0.22 * dqprev6 + 0.38 * debit_diffs[0] + 0.18 * debit_diffs[6] + 0.12 * debit_diffs[12] + 0.10 * debit_diffs[18]
        )
        
        return dqprev12
      
    def prevision12_Ambohimanambola(self, idstationAmbohimanambola, idstation):
        last_date_Ambohimanambola = self.get_last_date(idstationAmbohimanambola)
        dqPrev = self.calculate_dqprev12(idstation)
        print(f"dqprev (Station {idstation}): {dqPrev}")
        prevision6_data = self.prevision_Ambohimanambola(idstationAmbohimanambola, idstation)
        prevision6 = prevision6_data["debit"]  
        prevision = dqPrev + prevision6
        prevision_time = last_date_Ambohimanambola + timedelta(hours=12)
        
        return {
            "debit": round(prevision),
            "datecrues": prevision_time
        }
        
    def prevision_Ambohimanambola(self, idstationAmbohimanambola, idstation):
        last_date_Ambohimanambola = self.get_last_date(idstationAmbohimanambola)
        last_date_amount = self.get_last_date(idstation)
        interval_temps = self.calculer_intervalle_en_heures(last_date_amount, last_date_Ambohimanambola)

        if interval_temps >= 10:
            raise Exception("Il est impossible de faire la prévision : intervalle de temps trop long.")

        Debit_Observe = self.get_debit_at_time(idstationAmbohimanambola, last_date_Ambohimanambola)
        print(f"Debit_Observe (Station {idstationAmbohimanambola}, Date {last_date_Ambohimanambola}): {Debit_Observe}")
        dqPrev = self.calculate_dqprev(idstation)
        print(f"dqprev (Station {idstation}): {dqPrev}")
        prevision = Debit_Observe + dqPrev
        prevision_time = last_date_Ambohimanambola + timedelta(hours=6)  
        
        return {
            "debit": round(prevision),
            "datecrues": prevision_time
        }

    def get_Crues_24heures(self,idstation):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_crues where datecrues >= (SELECT MAX(datecrues) - INTERVAL '1 day' from v_crues where idstation = %s) and idstation = %s order by datecrues asc"
                cursor.execute(sql,[idstation,idstation])
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
    
    def generate_Date_Intervals(self,dernierDateCrues,previsionDate):
        diff_time = abs((previsionDate - dernierDateCrues).total_seconds())
        diff_hours = int(diff_time // 3600)
        
        labels = []
        for i in range(1, diff_hours + 1):
            new_date = dernierDateCrues + timedelta(hours=i)
            labels.append(new_date)
        return labels
    
    def generate_Debit(self,dernierDebit,previsionDebit,dernierDateCrues,previsionDate):
        diff_hours = int((previsionDate - dernierDateCrues).total_seconds() // 3600)
        print(str(diff_hours))
        # Générer les débits interpolés
        data = []
        for i in range(1, diff_hours + 1):
            current_debit = dernierDebit + ((previsionDebit - dernierDebit) / diff_hours) * i
            data.append(current_debit)

        return data
    
    def combine_debit_with_intervals(self,intervalle, debit):
        if len(intervalle) != len(debit):
            raise ValueError("Les listes 'intervalle' et 'debit' doivent avoir la même longueur.")
        
        combined_data = [
            {"datecrues": time, "debit": debit_value}
            for time, debit_value in zip(intervalle, debit)
        ]
        return combined_data

    def combine_crues_with_previsions(self,crues, intervalle):
        combined_data = []

        for crue in crues:
            combined_data.append({
                "datecrues": crue.get("datecrues").strftime('%Y-%m-%d %H:%M:%S'),  
                "debit": crue.get("debit"),
                "lenghtPrevision" : len(intervalle)
            })

        for data in intervalle:
            combined_data.append({
                "datecrues": data.get("datecrues").strftime('%Y-%m-%d %H:%M:%S'),
                "debit": data.get("debit"),
                "lenghtPrevision" : len(intervalle)
            })

        return combined_data

    def view_prevision_06h(self, idstationAmbohimanambola, idstation):
        crues = self.get_Crues_24heures(idstationAmbohimanambola)
        prevision = self.prevision_Ambohimanambola(idstationAmbohimanambola, idstation)
        dernier_date_crues = crues[-1]["datecrues"]
        dernier_debit = crues[-1]["debit"]
        intervalle = self.generate_Date_Intervals(dernier_date_crues, prevision["datecrues"])
        debit = self.generate_Debit(dernier_debit, prevision["debit"], dernier_date_crues, prevision["datecrues"])
        combined_data_intervals = self.combine_debit_with_intervals(intervalle, debit)
        final_data = self.combine_crues_with_previsions(crues, combined_data_intervals)

        return final_data
    
    def view_prevision_12h(self,idstationAmbohimanambola,idstation):
        crues = self.get_Crues_24heures(idstationAmbohimanambola)
        prevision = self.prevision12_Ambohimanambola(idstationAmbohimanambola,idstation)
        dernier_date_crues = crues[-1]["datecrues"]
        dernier_debit = crues[-1]["debit"]
        intervalle = self.generate_Date_Intervals(dernier_date_crues, prevision["datecrues"])
        debit = self.generate_Debit(dernier_debit, prevision["debit"], dernier_date_crues, prevision["datecrues"])
        combined_data_intervals = self.combine_debit_with_intervals(intervalle, debit)
        final_data = self.combine_crues_with_previsions(crues, combined_data_intervals)

        return final_data
        
    def get_stations_by_riviere(self,idriviere):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_previsionParRivieres where idriviere= %s"
                cursor.execute(sql,[idriviere])
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def get_stations_prevision(self):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM v_previsionparrivieres"
                cursor.execute(sql)
                result = dispatchall(cursor)
            return result if result else []
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    def insert_prevision_riviere(self,idriviere,stationDeDonnee,stationAPrevoir):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO previsionParRivieres values (default,%s,%s,%s)"
                cursor.execute(sql, [idriviere,stationDeDonnee,stationAPrevoir])
                return True
        except Exception as e:
            raise Exception(f"Error:{e}")
        
    def update_prevision_riviere(self,id,stationDeDonnee,stationAPrevoir):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE previsionparrivieres set stationdedonnee = %s , stationaprevoir = %s where id=%s"
                cursor.execute(sql,[stationDeDonnee,stationAPrevoir,id])
                return True
        except Exception as e:
            raise Exception(f"Error:{e}")
        
    def delete_prevision_riviere(self,id):
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM previsionparrivieres where id= %s"
                cursor.execute(sql,[id])
                return True
        except Exception as e:
            raise Exception(f"Error: {e}")