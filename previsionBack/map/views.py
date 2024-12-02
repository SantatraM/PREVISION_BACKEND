from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .modeles.commune import Commune
from .modeles.Rivieres import Rivieres

@api_view(['GET'])
def find_commune(request):
    try:
        communes = Commune()
        result = communes.get_commune()
        return Response({'data': result},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=500)
    
@api_view(['GET'])
def find_All_commune(request):
    try:
        communes = Commune()
        result = communes.get_All_Commune()
        return Response({'data': result},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=500)
    
@api_view(['GET'])
def find_Rivieres(request):
    try:
        rivieres = Rivieres()
        result = rivieres.get_Rivieres()
        return Response({'data': result},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['POST'])
def insert_Communes_Station(request):
    try:
        idstation = request.data.get('idstation')
        idcommunes = request.data.get('idcommune',[])
        for idcommune in idcommunes:
            communeStation = Commune()
            communeStation.insert_commune_station(idstation,idcommune)
        return Response({'message':'Success'},status=200)
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['GET'])
def find_commune_with_vigilence(request):
    try:
        communes = Commune()
        result = communes.get_commune_with_vigilence()
        return Response({'data': result},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=500)
    
@api_view(['GET'])
def find_commune_with_alert(request):
    try:
        communes = Commune()
        result = communes.get_commune_with_alert()
        return Response({'data': result},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=500)
    

@api_view(['GET'])
def get_nombre_commune_sous_vigilence(request):
    try:
        commune = Commune()
        total = commune.get_nombre_commune_sous_vigilence()
        return Response({'data': total},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['GET'])
def get_nombre_population_sous_vigilence_rouge(request):
    try:
        commune = Commune()
        total = commune.get_nombre_population_sous_vigilence_rouge()
        return Response({'data': total},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['GET'])
def get_nombre_population_sous_vigilence_jaune(request):
    try:
        commune = Commune()
        total = commune.get_nombre_population_sous_vigilence_jaune()
        return Response({'data': total},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['GET'])
def get_pourcentage_commune_Rouge(request):
    try:
        commune = Commune()
        total = commune.get_pourcentage_commune_alerteRouge()
        return Response({'data': total},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['GET'])
def get_pourcentage_commune_Jaune(request):
    try:
        commune = Commune()
        total = commune.get_pourcentage_commune_alerteJaune()
        return Response({'data': total},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['GET'])
def get_pourcentage_commune_without_alert(request):
    try:
        commune = Commune()
        total = commune.get_pourcentage_commune_without_alert()
        return Response({'data': total},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=200)
    
@api_view(['GET'])
def find_Riviere(request):
    try:
        rivieres = Rivieres()
        result = rivieres.get_Riviere()
        return Response({'data': result},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=200)