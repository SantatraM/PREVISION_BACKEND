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
from station.views import find_station_without_seuil
from formule.views import find_formule_with_variable
from formule.views import find_formule_with_condition
from formule.views import create_formule
from crues.views import import_hauteur_debit
from crues.views import find_seuil
from crues.views import create_seuil
from crues.views import find_crues_today
from crues.views import delete_seuil
from crues.views import update_seuil
from crues.views import create_crues
from crues.views import filtre_crues
from crues.views import filtre_crues_by_one_date
from map.views import find_commune
from map.views import find_All_commune
from map.views import find_Rivieres
from map.views import find_Riviere
from prevision.views import prevision_ambohimanambola
from prevision.views import prevision12_ambohimanambola
from map.views import insert_Communes_Station
from map.views import find_commune_with_vigilence
from map.views import get_nombre_commune_sous_vigilence
from map.views import get_nombre_population_sous_vigilence_rouge
from map.views import get_nombre_population_sous_vigilence_jaune
from map.views import find_commune_with_alert
from map.views import get_pourcentage_commune_Rouge
from map.views import get_pourcentage_commune_Jaune
from map.views import get_pourcentage_commune_without_alert
from prevision.views import find_crues_24h
from prevision.views import get_prevision_ambohimanambola
from prevision.views import get_prevision12_ambohimanambola
from prevision.views import find_stations_by_riviere
from prevision.views import find_stations_previsions

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
    path('stationWithoutSeuil/', find_station_without_seuil, name='find_station_without_seuil'),
    path('createStation/', create_station, name='create_station'),
    path('updateStation/',update_station,name='update_station'),
    
    path('formules/',find_formule_with_variable,name='find_formule_with_variable'),
    path('formule/',find_formule_with_condition,name='find_formule_with_condition'),
    path('createFormule/', create_formule, name='create_formule'),
    
    path('importHauteurDebit/',import_hauteur_debit,name='import_hauteur_debit'),
    
    path('seuils/',find_seuil,name='find_seuil'),
    path('createSeuil/', create_seuil, name='create_seuil'),
    path('cruesToday/<str:idstation>/',find_crues_today,name='find_crues_today'),
    path('filtreCrues/<str:datedebut>/<str:datefin>/<str:idstation>',filtre_crues,name='filtre_crues'),
    path('filtreCrues1/<str:datedebut>/<str:idstation>/', filtre_crues_by_one_date, name='filtre_crues_by_one_date'),
    
    path('communes/',find_commune,name='find_commune'),
    path('Allcommunes/',find_All_commune,name='find_All_commune'),
    path('rivieres/',find_Rivieres,name='find_Rivieres'),
    path('riviere/',find_Riviere,name='find_Riviere'),
    path('prevision/<str:station_id_ambohimanambola>/<str:station_id>/', prevision_ambohimanambola, name='prevision_ambohimanambola'),
    path('prevision12/<str:station_id_ambohimanambola>/<str:station_id>/', prevision12_ambohimanambola, name='prevision12_ambohimanambola'),
    
    path('insertCommuneStation/', insert_Communes_Station, name='insert_Communes_Station'),
    path('communes_vigilence/',find_commune_with_vigilence,name='find_commune_with_vigilence'),
    path('nombreCommunes/',get_nombre_commune_sous_vigilence,name='get_nombre_commune_sous_vigilence'),
    path('nombrePopRouge/',get_nombre_population_sous_vigilence_rouge,name='get_nombre_population_sous_vigilence_rouge'),
    path('nombrePopJaune/',get_nombre_population_sous_vigilence_jaune,name='get_nombre_population_sous_vigilence_jaune'),
    path('communes_alert/',find_commune_with_alert,name='find_commune_with_alert'),
    path('pourcentageRouge/',get_pourcentage_commune_Rouge,name='get_pourcentage_commune_Rouge'),
    path('pourcentageJaune/',get_pourcentage_commune_Jaune,name='get_pourcentage_commune_Jaune'),
    path('pourcentageWithoutAlert/',get_pourcentage_commune_without_alert,name='get_pourcentage_commune_without_alert'),
    
    path('crues24h/<str:idstation>',find_crues_24h,name="find_crues_24h"),
    
    path('prevision06h/<str:station_id_ambohimanambola>/<str:station_id>/', get_prevision_ambohimanambola, name='get_prevision_ambohimanambola'),
    path('prevision12h/<str:station_id_ambohimanambola>/<str:station_id>/', get_prevision12_ambohimanambola, name='get_prevision12_ambohimanambola'),
    
    path('stationPrev/<str:idriviere>/', find_stations_by_riviere, name='find_stations_by_riviere'),
    path('deleteSeuil/<str:idseuil>/',delete_seuil,name='delete_seuil'),
    path('updateSeuil/',update_seuil,name='update_seuil'),
    path('createCrues/', create_crues, name='create_crues'),
    path('stationPrevision/', find_stations_previsions, name='find_stations_previsions'),
]
