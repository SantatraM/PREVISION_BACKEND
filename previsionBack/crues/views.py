from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .modeles.hauteur_Debit import Hauteurdebitcrues
from .modeles.crues import Crues

@api_view(['POST'])
def import_hauteur_debit(request):
    try:
        if 'file' not in request.FILES:
            return Response({'error': 'Fichier non fourni.'}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES['file']
        station = request.data.get('station')
        condition = (request.data.get('condition'))
        print("condition = " + condition)
        hauteur_debit = Hauteurdebitcrues() 
        result = hauteur_debit.import_hauteur_debit(file, station, condition)
        if result:
            return Response({'message': 'Importation réussie.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Erreur d\'importation.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_crues(request):
    try:
        idstation = request.data.get('idstation')
        datecrues = request.data.get('datecrues')
        hauteur = float(request.data.get('hauteur')) if hauteur else None
        debit = float(request.data.get('debit')) if debit else None
        pluie = float(request.data.get('pluie')) if pluie else None
        
        new_crues = Crues()
        new_crues.insert_crues(hauteur,debit,pluie,idstation,datecrues)
        return Response({'message': 'Crues created successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)
    