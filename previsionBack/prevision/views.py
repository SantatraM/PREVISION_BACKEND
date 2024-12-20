from django.http import JsonResponse
from django.shortcuts import render
from .modeles.prevision import Prevision
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])  
def prevision_ambohimanambola(request, station_id_ambohimanambola, station_id):
    try:
        prevision_model = Prevision()
        prevision = prevision_model.prevision_Ambohimanambola(station_id_ambohimanambola, station_id)
        return Response({'data': prevision},status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=200)
    
@api_view(['GET'])  
def prevision12_ambohimanambola(request, station_id_ambohimanambola, station_id):
    try:
        prevision_model = Prevision()
        prevision = prevision_model.prevision12_Ambohimanambola(station_id_ambohimanambola, station_id)
        return Response({'data': prevision},status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=200)
    
@api_view(['GET'])
def find_crues_24h(request,idstation):
    try:
        prevision_model = Prevision()
        result = prevision_model.get_Crues_24heures(idstation)
        return Response({'data': result},status=200)
    except Exception as e:
        return Response({'error': str(e) },status=200)
    
@api_view(['GET'])
def get_prevision_ambohimanambola(request,station_id_ambohimanambola,station_id):
    try:
        prevision_model = Prevision()
        prevision = prevision_model.view_prevision_06h(station_id_ambohimanambola,station_id)
        return Response({'data':prevision},status=200)
    except Exception as e:
        return JsonResponse({'error':str(e)},status=200)
    
@api_view(['GET'])
def get_prevision12_ambohimanambola(request,station_id_ambohimanambola,station_id):
    try:
        prevision_model = Prevision()
        prevision = prevision_model.view_prevision_12h(station_id_ambohimanambola,station_id)
        return Response({'data':prevision},status=200)
    except Exception as e:
        return JsonResponse({'error':str(e)},status=200)
    
@api_view(['GET'])
def find_stations_by_riviere(request,idriviere):
    try:
        prevision_model = Prevision()
        result = prevision_model.get_stations_by_riviere(idriviere)
        return Response({'data': result},status=200)
    except Exception as e:
        return Response({'error': str(e) },status=200)
    
@api_view(['GET'])
def find_stations_previsions(request):
    try:
        prevision_model = Prevision()
        result = prevision_model.get_stations_prevision()
        return Response({'data': result},status=200)
    except Exception as e:
        return Response({'error': str(e) },status=200)
    
@api_view(['POST'])
def create_prevision_riviere(request):
    try:
        idriviere = request.data.get('idriviere')
        stationdedonnee = request.data.get('stationdedonnee')
        stationaprevoir = request.data.get('stationaprevoir')
        if stationdedonnee == stationaprevoir:
            return Response({'error': 'Les deux stations doivent être différentes.'},status=200)
        prevision = Prevision()
        result = prevision.insert_prevision_riviere(idriviere,stationdedonnee,stationaprevoir)
        return Response({'message': 'success.'}, status=200)
    except Exception as e:
        print(e)
        return Response({'error':str(e)},status=200)

@api_view(['POST'])
def update_prevision_riviere(request):
    try:
        id = request.data.get('id')
        stationdedonnee = request.data.get('stationdedonnee')
        stationaprevoir = request.data.get('stationaprevoir')
        if stationdedonnee == stationaprevoir:
            return Response({'error': 'Les deux stations doivent être différentes.'},status=200)
        
        prevision = Prevision()
        prevision.update_prevision_riviere(id,stationdedonnee,stationaprevoir)
        return Response({'message':'success'},status=200)
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['GET'])
def delete_prevision_riviere(request,id):
    try:
        print(id)
        prevision = Prevision()
        prevision.delete_prevision_riviere(id)
        return Response({'message': 'success.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)} , status=200)
    