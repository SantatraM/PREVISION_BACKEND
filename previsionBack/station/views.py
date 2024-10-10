from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .modeles.sousBassin import Sousbassin
from .modeles.mesure import Mesure
from .modeles.station import Station

@api_view(['GET'])  
def find_sous_bassin_by_id(request, idsousbassin):
    try:
        sous_bassin_instance = get_object_or_404(Sousbassin, idsousbassin=idsousbassin)
        details = sous_bassin_instance.get_sous_bassin_by_id()
        return Response({'data': details}, status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)  
    
@api_view(['GET'])
def find_sous_bassin(request):
    try:
        sousbassins = Sousbassin()
        results = sousbassins.get_sous_bassin()
        return Response({'data': results},status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)} , status=500)
    
@api_view(['POST'])
def create_sous_bassin(request):
    try:
        sousbassin = request.data.get('sousbassin')
        new_sousbassin = Sousbassin(sousbassin=sousbassin)
        new_sousbassin.insert_sous_bassin()
        return Response({'message': 'Sous bassin created successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def update_sous_bassin(request):
    try:
        idsousbassin = request.data.get('idsousbassin')
        sousbassin = request.data.get('sousbassin')
        new_sousbassin = Sousbassin(sousbassin = sousbassin , idsousbassin = idsousbassin )
        new_sousbassin.update_sous_bassin()
        return Response({'message': 'Sous bassin updated successfully.'} , status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)},status=500)
    
@api_view(['GET'])
def delete_sous_bassin(request,idsousbassin):
    try:
        sousbassin = Sousbassin(idsousbassin = idsousbassin)
        sousbassin.delete_sous_bassin()
        return Response({'message': 'Sous bassin deleted successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)} , status=500)
    
# mesure
@api_view(['GET'])  
def find_mesure_by_id(request, idmesure):
    try:
        mesure_instance = get_object_or_404(Mesure, idmesure=idmesure)
        details = mesure_instance.get_mesure_by_id()
        return Response({'data': details}, status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)  
    
@api_view(['GET'])
def find_mesure(request):
    try:
        mesures = Mesure()
        results = mesures.get_mesure()
        return Response({'data': results},status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)} , status=500)
    
@api_view(['POST'])
def create_mesure(request):
    try:
        mesure = request.data.get('mesure')
        new_mesure = Mesure(mesure=mesure)
        new_mesure.insert_mesure()
        return Response({'message': 'Mesure created successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def update_mesure(request):
    try:
        idmesure = request.data.get('idmesure')
        mesure = request.data.get('mesure')
        new_mesure = Mesure(mesure = mesure , idmesure = idmesure )
        new_mesure.update_mesure()
        return Response({'message': 'Mesure updated successfully.'} , status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)},status=500)
    
@api_view(['GET'])
def delete_mesure(request,idmesure):
    try:
        mesure = Mesure(idmesure = idmesure)
        mesure.delete_mesure()
        return Response({'message': 'Mesure deleted successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)} , status=500)

# station
@api_view(['GET'])  
def find_station_by_id(request, idstation):
    try:
        station_instance = get_object_or_404(Station, idstation=idstation)
        details = station_instance.get_station_by_id()
        return Response({'data': details}, status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)  
    
@api_view(['GET'])
def find_station(request):
    try:
        stations = Station()
        results = stations.get_station()
        return Response({'data': results},status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)} , status=500)
    
@api_view(['POST'])
def create_mesure(request):
    try:
        site = request.data.get('site')
        idsousbassin = request.data.get('idsousbassin')
        longitude = float(request.data.get('longitude'))
        latitude = float(request.data.get('latitude'))
        idmesure = request.data.get('idmesure')

        new_station = Station(site = site , idsousbassin = idsousbassin , longitude = longitude , latitude = latitude ,idmesure = idmesure)
        new_station.insert_station()
        return Response({'message': 'Station created successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def update_station(request):
    try:
        idstation = request.data.get('idstation')
        site = request.data.get('site')
        idsousbassin = request.data.get('idsousbassin')
        longitude = float(request.data.get('longitude'))
        latitude = float(request.data.get('latitude'))
        idmesure = float(request.data.get('idmesure'))

        new_station = Station(site = site ,idsousbassin = idsousbassin, longitude = longitude , latitude = latitude , idmesure = idmesure, idstation = idstation )
        new_station.update_station()
        return Response({'message': 'Station updated successfully.'} , status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)},status=500)