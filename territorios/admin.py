# territorios/admin.py
from django.contrib import admin
from .models import Territorio, Rua, Imovel, Edificio, Unidade, SaidaCampo, Designacao

class RuaInline(admin.TabularInline):
    model = Rua
    extra = 1

@admin.register(Territorio)
class TerritorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'data_criacao')
    list_filter = ('status',)
    search_fields = ('nome', 'descricao')
    inlines = [RuaInline]

class ImovelInline(admin.TabularInline):
    model = Imovel
    extra = 1

@admin.register(Rua)
class RuaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'territorio', 'tipo', 'cep')
    list_filter = ('tipo', 'territorio')
    search_fields = ('nome', 'cep')
    inlines = [ImovelInline]

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('numero', 'complemento', 'rua', 'tipo', 'ativo')
    list_filter = ('tipo', 'ativo', 'rua__territorio')
    search_fields = ('numero', 'complemento', 'rua__nome')

class UnidadeInline(admin.TabularInline):
    model = Unidade
    extra = 1

@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'imovel', 'tipo_portaria', 'total_unidades')
    list_filter = ('tipo_portaria',)
    search_fields = ('nome', 'imovel__rua__nome')
    inlines = [UnidadeInline]

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('numero', 'andar', 'bloco', 'edificio', 'status')
    list_filter = ('status', 'edificio')
    search_fields = ('numero', 'andar', 'bloco', 'edificio__nome')

@admin.register(SaidaCampo)
class SaidaCampoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'dia_semana', 'horario', 'dirigente', 'status')
    list_filter = ('status', 'data')
    search_fields = ('nome', 'dirigente')

@admin.register(Designacao)
class DesignacaoAdmin(admin.ModelAdmin):
    list_display = ('territorio', 'saida_campo', 'data_designacao', 'data_devolucao', 'status')
    list_filter = ('status', 'data_designacao')
    search_fields = ('territorio__nome', 'saida_campo__nome')