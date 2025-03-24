# usuarios/admin.py
from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('acao', 'usuario', 'data', 'hora', 'tabela_afetada', 'registro_id')
    list_filter = ('acao', 'tabela_afetada', 'data', 'usuario')
    search_fields = ('acao', 'detalhes', 'usuario__username')
    readonly_fields = ('data', 'hora')