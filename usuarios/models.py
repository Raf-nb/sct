# usuarios/manage.py
from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs',
        verbose_name="Usuário"
    )
    data = models.DateField(auto_now_add=True, verbose_name="Data")
    hora = models.TimeField(auto_now_add=True, verbose_name="Hora")
    acao = models.CharField(max_length=100, verbose_name="Ação")
    tabela_afetada = models.CharField(max_length=50, blank=True, verbose_name="Tabela Afetada")
    registro_id = models.CharField(max_length=20, blank=True, verbose_name="ID do Registro")
    detalhes = models.TextField(blank=True, verbose_name="Detalhes")

    def __str__(self):
        return f"{self.acao} por {self.usuario} em {self.data.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ['-data', '-hora']