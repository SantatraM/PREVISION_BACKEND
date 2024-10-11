from django.db import models
from formule.modeles.formule import Formuledebit
import pandas as pd
from previsionBack.utils import requete
from previsionBack.utils import insertion
from rest_framework.response import Response
from station.modeles.station import Station

class Crues(models.Model):
    
    def insert_crues(self,hauteur,debit,pluie,station,datecrues):
        try:
            insertion("hauteurdebitcrues(idstation,datecrues,hauteur,debit)",[station,datecrues,hauteur,debit])
            insertion("pluiecrues(idstation,datecrues,pluie)",[station,datecrues,pluie])
            return True
        except Exception as e:
            raise Exception(f"Error inserting mesure: {e}")