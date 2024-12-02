from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .modeles.formule import Formuledebit
from . modeles.variable import Variableformule
from station.modeles.station import Station

@api_view(['GET'])
def find_formule_by_id_station(request, idstation):
    try:
        formule_instance = get_object_or_404(Formuledebit, idstation=idstation)
        details = formule_instance.get_formule_by_id_station()
        return Response({'data': details}, status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500) 
    
@api_view(['GET'])
def find_formule(request):
    try:
        formule = Formuledebit()
        results = formule.get_formule()
        return Response({'data': results},status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)} , status=500)
    
@api_view(['POST'])
def create_formule(request):
    try:
        idstation = request.data.get('idstation')
        condition = float(request.data.get('condition'))
        formule = request.data.get('formule')
        new_formule = Formuledebit(condition = condition , formule = formule)
        new_formule.insert_formule(idstation)
        return Response({'message': 'formule created successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)
    
# variable formule 
@api_view(['GET'])
def find_variable_by_id_formule(request, idformule):
    try:
        variable_instance = get_object_or_404(Variableformule, idformule=idformule)
        details = variable_instance.get_variable_by_formule()
        return Response({'data': details}, status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500) 
    
@api_view(['POST'])
def create_variable_formule(request):
    try:
        idformule = request.data.get('idformule')
        valeur = float(request.data.get('valeur'))
        variable = request.data.get('variable')
        new_variable = Variableformule(idformule=idformule,variable = variable , valeur = valeur)
        new_variable.insert_variable_formule()
        return Response({'message': 'variable created successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def find_formule_with_variable(request):
    try:
        formule  = Formuledebit()
        results = formule.get_formule_with_variable()
        return Response({'data': results},status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)},status=500)
    
@api_view(['GET'])
def find_formule_with_condition(request):
    try:
        formule = Formuledebit()
        result = formule.get_formule_debit_with_condition(hauteur=1.3,idstation='STAT1')
        print(result.get('idformule'))
        return Response({'data':result},status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)},status=500)
    
@api_view(['GET'])
def find_formule_without_condition(request):
    try:
        formule = Formuledebit()
        result = formule.get_formule_debit_without_condition(hauteur=1.3,idstation='STAT1')
        return Response({'data':result},status=200)
    except Exception as e:
        print(e)
        return Response({'error': str(e)},status=500)