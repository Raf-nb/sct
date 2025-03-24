# atendimentos/admin.py
from django.contrib import admin
from .models import Atendimento


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('get_local', 'data', 'hora', 'resultado', 'registrado_por')
    list_filter = ('resultado', 'data')
    search_fields = ('observacoes', 'imovel__numero', 'unidade__numero')

    def get_local(self, obj):
        if obj.imovel:
            return f"Imóvel: {obj.imovel}"
        return f"Unidade: {obj.unidade}"

    get_local.short_description = 'Local'