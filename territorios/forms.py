# territorios/forms.py
from django import forms
from .models import Territorio, Rua, Imovel, Edificio, Unidade, SaidaCampo, Designacao

class TerritorioForm(forms.ModelForm):
    class Meta:
        model = Territorio
        fields = ['nome', 'descricao', 'status']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class RuaForm(forms.ModelForm):
    class Meta:
        model = Rua
        fields = ['nome', 'cep', 'tipo']

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ['numero', 'complemento', 'tipo', 'ativo']

class EdificioForm(forms.ModelForm):
    class Meta:
        model = Edificio
        fields = ['nome', 'tipo_portaria', 'total_unidades', 'observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['numero', 'andar', 'bloco', 'status']

class SaidaCampoForm(forms.ModelForm):
    class Meta:
        model = SaidaCampo
        fields = ['nome', 'data', 'horario', 'dirigente', 'status']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }

class DesignacaoForm(forms.ModelForm):
    class Meta:
        model = Designacao
        fields = ['territorio', 'saida_campo', 'data_designacao', 'data_devolucao', 'status']
        widgets = {
            'data_designacao': forms.DateInput(attrs={'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'type': 'date', 'required': False}),
        }