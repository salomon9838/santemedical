from django.urls import path
from . import views  # Vues de l'application sante

urlpatterns = [
    # API Endpoints (JSON pour JavaFX / mobile)
    path('patients/', views.patients_api, name='patients_api'),
    path('consultations/', views.consultations_api, name='consultations_api'),
    path('pathologies/', views.pathologies_api, name='pathologies_api'),
    path('prescriptions/', views.prescriptions_api, name='prescriptions_api'),
    path('registre-api/', views.registre_maladies_api, name='registre_api'),

    # Pages Web (Templates HTML)
    path('', views.solution, name='solution'),
    path('nouvelle/', views.nouvelle_consultation, name='nouvelle'),
    path('ancienne/', views.ancienne_consultation, name='ancienne'),
    path('registre/', views.registre_medical, name='registre'),
    path('parametres/', views.parametres, name='parametres'),
]
