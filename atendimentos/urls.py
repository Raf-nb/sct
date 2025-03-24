# atendimentos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Atendimentos
    path('', views.atendimento_list, name='atendimento_list'),
    path('imovel/<int:imovel_id>/', views.imovel_atendimentos, name='imovel_atendimentos'),
    path('unidade/<int:unidade_id>/', views.unidade_atendimentos, name='unidade_atendimentos'),
    # atendimentos/urls.py (adicionar)
    path('edificio/<int:edificio_id>/unidade/criar/', views.unidade_create, name='unidade_create'),
    # Prédios e Vilas
    path('predios-vilas/', views.predios_vilas_list, name='predios_vilas_list'),
    path('edificio/<int:pk>/', views.edificio_detail, name='edificio_detail'),
]