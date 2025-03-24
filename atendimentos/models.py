# atendimentos/manage.py
from django.db import models
from territorios.models import Imovel, Unidade


class Atendimento(models.Model):
    imovel = models.ForeignKey(
        Imovel,
        on_delete=models.CASCADE,
        related_name='atendimentos',
        null=True,
        blank=True,
        verbose_name="Imóvel"
    )
    unidade = models.ForeignKey(
        Unidade,
        on_delete=models.CASCADE,
        related_name='atendimentos',
        null=True,
        blank=True,
        verbose_name="Unidade"
    )
    data = models.DateField(verbose_name="Data")
    hora = models.TimeField(verbose_name="Hora")
    RESULTADO_CHOICES = [
        ('atendido', 'Atendido'),
        ('ausente', 'Ausente'),
        ('recusado', 'Recusado'),
        ('retornar', 'Retornar Depois'),
    ]
    resultado = models.CharField(
        max_length=15,
        choices=RESULTADO_CHOICES,
        verbose_name="Resultado"
    )
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    registrado_por = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='atendimentos',
        verbose_name="Registrado por"
    )

    def clean(self):
        # Validar que pelo menos um dos campos imovel ou unidade esteja preenchido
        from django.core.exceptions import ValidationError
        if not self.imovel and not self.unidade:
            raise ValidationError("É necessário especificar um imóvel ou uma unidade.")

        # Garantir que não haja ambos preenchidos ao mesmo tempo
        if self.imovel and self.unidade:
            raise ValidationError("Não é possível especificar um imóvel e uma unidade ao mesmo tempo.")

    def __str__(self):
        if self.imovel:
            return f"Atendimento em {self.imovel} - {self.data.strftime('%d/%m/%Y')}"
        return f"Atendimento em {self.unidade} - {self.data.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"
        ordering = ['-data', '-hora']