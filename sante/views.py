from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import JsonResponse

from .models import (
    ThemeConfig,
    Patient,
    Utilisateur,
    Consultation,
    Pathologie,
    Prescription,
    RegistreMaladie
)

from .serializers import (
    PatientSerializer,
    UtilisateurSerializer,
    ConsultationSerializer,
    PathologieSerializer,
    PrescriptionSerializer,
    RegistreMaladieSerializer
)


# ========================================
# THÈME (public - pas besoin d'auth)
# ========================================
def get_theme(request):
    theme = ThemeConfig.objects.first()
    if not theme:
        # Valeurs par défaut si aucun thème n'existe
        data = {
            "primary_color": "#4361ee",
            "secondary_color": "#7209b7",
        }
    else:
        data = {
            "primary_color": theme.primary_color,
            "secondary_color": theme.secondary_color,
        }
    return JsonResponse(data)

    


# ========================================
# INSCRIPTION (REGISTER)
# ========================================
@api_view(['POST'])
@permission_classes([AllowAny])  # Accessible sans auth
def register_user(request):
    data = request.data

    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    role = data.get('role')
    service = data.get('service')

    if not all([username, password, role, service]):
        return Response({'error': 'Tous les champs obligatoires doivent être remplis'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Ce nom d\'utilisateur existe déjà'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        Utilisateur.objects.create(
            user=user,
            role=role,
            service=service
        )
        return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# PATIENTS API (protégé)
# ========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def patients_api(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# CONSULTATIONS API (protégé)
# ========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def consultations_api(request):
    if request.method == 'GET':
        consultations = Consultation.objects.all()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# PATHOLOGIES API (protégé)
# ========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pathologies_api(request):
    if request.method == 'GET':
        pathologies = Pathologie.objects.all()
        serializer = PathologieSerializer(pathologies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PathologieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# PRESCRIPTIONS API (protégé)
# ========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def prescriptions_api(request):
    if request.method == 'GET':
        prescriptions = Prescription.objects.all()
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# REGISTRE MALADIES API (protégé)
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def registre_maladies_api(request):
    registre = RegistreMaladie.objects.all()
    serializer = RegistreMaladieSerializer(registre, many=True)
    return Response(serializer.data)


# ========================================
# VUES TEMPLATES HTML (pages web)
# ========================================
def solution(request):
    return render(request, 'solution.html')

def nouvelle_consultation(request):
    return render(request, 'nouvelle_consultation.html')

def ancienne_consultation(request):
    return render(request, 'ancienne_consultation.html')

def registre_medical(request):
    return render(request, 'registre_medical.html')

def parametres(request):
    return render(request, 'parametres.html')



