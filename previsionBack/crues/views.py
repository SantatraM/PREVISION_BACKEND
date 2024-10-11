from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .modeles.hauteur_Debit import Hauteurdebitcrues

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
