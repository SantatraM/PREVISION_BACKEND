from django.urls import path
from station.views import find_sous_bassin_by_id
from station.views import find_sous_bassin
from station.views import create_sous_bassin
from station.views import update_sous_bassin
from station.views import delete_sous_bassin
from station.views import find_mesure_by_id
from station.views import find_mesure
from station.views import create_mesure
from station.views import update_mesure
from station.views import delete_mesure
from station.views import find_station_by_id
from station.views import find_station
from station.views import create_station
from station.views import update_station
from formule.views import find_formule_with_variable
from formule.views import find_formule_with_condition
from crues.views import import_hauteur_debit

urlpatterns = [
    path('sousbassin/<str:idsousbassin>/', find_sous_bassin_by_id, name='find_sous_bassin_by_id'),
    path('sousbassins/', find_sous_bassin, name='find_sous_bassin'),
    path('createSousBassin/', create_sous_bassin, name='create_sous_bassin'),
    path('updateSousBassin/',update_sous_bassin,name='update_sous_bassin'),
    path('deleteSousBassin/<str:idsousbassin>/',delete_sous_bassin,name='delete_sous_bassin'),

    path('mesure/<str:idmesure>/', find_mesure_by_id, name='find_mesure_by_id'),
    path('mesures/', find_mesure, name='find_mesure'),
    path('createMesure/', create_mesure, name='create_mesure'),
    path('updateMesure/',update_mesure,name='update_mesure'),
    path('deleteMesure/<str:idmesure>/',delete_mesure,name='delete_mesure'),

    path('station/<str:idstation>/', find_station_by_id, name='find_station_by_id'),
    path('stations/', find_station, name='find_station'),
    path('createStation/', create_station, name='create_station'),
    path('updateStation/',update_station,name='update_station'),
    
    path('formules/',find_formule_with_variable,name='find_formule_with_variable'),
    path('formule/',find_formule_with_condition,name='find_formule_with_condition'),
    
    path('importHauteurDebit/',import_hauteur_debit,name='import_hauteur_debit'),
]
