# territorios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Territórios
    path('territorios/', views.territorio_list, name='territorio_list'),
    path('territorios/criar/', views.territorio_create, name='territorio_create'),
    path('territorios/<int:pk>/', views.territorio_detail, name='territorio_detail'),
    path('territorios/<int:pk>/editar/', views.territorio_update, name='territorio_update'),

    # Ruas
    path('territorios/<int:territorio_id>/rua/criar/', views.rua_create, name='rua_create'),

    # Imóveis
    path('rua/<int:rua_id>/imovel/criar/', views.imovel_create, name='imovel_create'),

    # Edifícios
    path('imovel/<int:imovel_id>/edificio/criar/', views.edificio_create, name='edificio_create'),

    # Saídas de Campo
    path('saidas-campo/', views.saida_campo_list, name='saida_campo_list'),
    path('saidas-campo/criar/', views.saida_campo_create, name='saida_campo_create'),

    # Designações
    path('designacoes/', views.designacao_list, name='designacao_list'),
    path('designacoes/criar/', views.designacao_create, name='designacao_create'),

    # Território do Dia
    path('territorio-do-dia/', views.territorio_dia, name='territorio_dia'),
]