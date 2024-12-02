from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .modeles.hauteur_Debit import Hauteurdebitcrues
from .modeles.crues import Crues
from .modeles.seuil import Seuil

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
            return Response({'error': 'Erreur d\'importation.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def create_crues(request):
    try:
        idstation = request.data.get('idstation')
        datecrues = request.data.get('datecrues')
        hauteur = request.data.get('hauteur')
        hauteur = float(hauteur) if hauteur else None
        debit =request.data.get('debit')
        debit = float(debit) if debit else None
        pluie = request.data.get('pluie')
        pluie = float(pluie) if pluie else None
        
        new_crues = Crues()
        new_crues.insert_crues(hauteur,debit,pluie,idstation,datecrues)
        return Response({'message': 'Crues created successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def find_seuil(request):
    try:
        seuils = Seuil()
        result = seuils.get_seuil()
        return Response({'data': result},status=200) 
    except Exception as e:
        return Response({'error': str(e)},status=500)
    
@api_view(['GET'])
def delete_seuil(request,idseuil):
    try:
        seuil = Seuil(idseuil = idseuil)
        seuil.delete_seuil()
        return Response({'message': 'Seuil deleted successfully.'}, status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)} , status=500)
    
@api_view(['POST'])    
def create_seuil(request):
    try:
        idstation = request.data.get('idstation')
        rouge = request.data.get('rouge')
        jaune = request.data.get('jaune')
        
        if not idstation or not rouge or not jaune:
            return Response({'error': 'Tous les champs (idstation, rouge, jaune) sont requis.'}, status=200)
        
        try:
            rougeFloat = float(rouge)
            jauneFloat = float(jaune)
        except ValueError:
            return Response({'error': 'Les valeurs de seuils doivent être des nombres.'}, status=200)

        if rougeFloat <= jauneFloat:
            return Response({'error': 'L\'alerte rouge doit être supérieure à l\'alerte jaune.'}, status=200)
        
        new_seuil = Seuil(rouge=rougeFloat, jaune=jauneFloat)
        new_seuil.insert_seuil(idstation)  
        return Response({'message': 'Seuil créé avec succès.'}, status=201)
    
    except Exception as e:
        print(e)
        return Response({'error': 'Une erreur interne est survenue.'}, status=200)
    
@api_view(['POST'])
def update_seuil(request):
    try:
        idseuil = request.data.get('idseuil')
        rouge = request.data.get('rouge')
        jaune = request.data.get('jaune')
        try:
            rougeFloat = float(rouge)
            jauneFloat = float(jaune)
        except ValueError:
            return Response({'error': 'Les valeurs de seuils doivent être des nombres.'}, status=200)

        if rougeFloat <= jauneFloat:
            return Response({'error': 'L\'alerte rouge doit être supérieure à l\'alerte jaune.'}, status=200)
        
        new_seuil = Seuil(idseuil = idseuil,rouge = rougeFloat,jaune = jauneFloat)
        new_seuil.update_seuil()
        return Response({'message': 'Seuil updated successfully.'} , status=201)
    except Exception as e:
        print(e)
        return Response({'error': str(e)},status=500)
    
    
@api_view(['GET'])
def find_crues_today(request,idstation):
    try:
        crues = Crues()
        result = crues.get_today_crues(idstation)
        return Response({'data': result},status=200)
    except Exception as e:
        return Response({'error': str(e) },status=200)
    
@api_view(['GET'])
def filtre_crues(request,datedebut,datefin,idstation):
    try:
        if datefin <= datedebut:
            return Response({'error': 'La date de fin doit être supérieure à la date de début.'}, status=200)
        crues = Crues()
        result = crues.get_crues_by_date(datedebut,datefin,idstation)
        return Response({'data': result },status=200)
    except Exception as e:
        return Response({'error':str(e) },status=200)
    
@api_view(['GET'])
def filtre_crues_by_one_date(request,datedebut,idstation):
    try:
        crues = Crues()
        result = crues.get_crues_by_one_date(datedebut,idstation)
        return Response({'data': result },status=200)
    except Exception as e:
        return Response({'error':str(e) },status=200)
