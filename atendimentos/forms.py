# atendimentos/forms.py
from django import forms
from .models import Atendimento

class AtendimentoImovelForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['imovel', 'data', 'hora', 'resultado', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

class AtendimentoUnidadeForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['unidade', 'data', 'hora', 'resultado', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }