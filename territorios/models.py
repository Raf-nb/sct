# territorios/manage.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Territorio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    data_criacao = models.DateField(auto_now_add=True, verbose_name="Data de Criação")
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ativo',
        verbose_name="Status"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Território"
        verbose_name_plural = "Territórios"
        ordering = ['nome']


class Rua(models.Model):
    territorio = models.ForeignKey(
        Territorio,
        on_delete=models.CASCADE,
        related_name='ruas',
        verbose_name="Território"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome")
    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    TIPO_CHOICES = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
        ('mista', 'Mista'),
    ]
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_CHOICES,
        default='residencial',
        verbose_name="Tipo"
    )

    def __str__(self):
        return f"{self.nome} - {self.territorio.nome}"

    class Meta:
        verbose_name = "Rua"
        verbose_name_plural = "Ruas"
        ordering = ['territorio', 'nome']


class Imovel(models.Model):
    rua = models.ForeignKey(
        Rua,
        on_delete=models.CASCADE,
        related_name='imoveis',
        verbose_name="Rua"
    )
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=50, blank=True, verbose_name="Complemento")
    TIPO_CHOICES = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
        ('predio', 'Prédio'),
        ('vila', 'Vila'),
    ]
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_CHOICES,
        verbose_name="Tipo"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return f"{self.numero} - {self.rua.nome}"

    @property
    def endereco_completo(self):
        complemento = f", {self.complemento}" if self.complemento else ""
        return f"{self.rua.nome}, {self.numero}{complemento}"

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"
        ordering = ['rua', 'numero']


# territorios/manage.py (continuação)

class Edificio(models.Model):
    imovel = models.OneToOneField(
        Imovel,
        on_delete=models.CASCADE,
        related_name='edificio',
        verbose_name="Imóvel"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome")
    TIPO_PORTARIA_CHOICES = [
        ('sem_portaria', 'Sem Portaria'),
        ('portaria_24h', 'Portaria 24h'),
        ('portaria_horario', 'Portaria com Horário Limitado'),
        ('porteiro_eletronico', 'Porteiro Eletrônico'),
    ]
    tipo_portaria = models.CharField(
        max_length=20,
        choices=TIPO_PORTARIA_CHOICES,
        default='sem_portaria',
        verbose_name="Tipo de Portaria"
    )
    total_unidades = models.PositiveIntegerField(default=0, verbose_name="Total de Unidades")
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Garantir que o imóvel associado seja do tipo 'predio' ou 'vila'
        if self.imovel.tipo not in ['predio', 'vila']:
            self.imovel.tipo = 'predio'
            self.imovel.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Edifício"
        verbose_name_plural = "Edifícios"
        ordering = ['nome']


class Unidade(models.Model):
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.CASCADE,
        related_name='unidades',
        verbose_name="Edifício"
    )
    numero = models.CharField(max_length=10, verbose_name="Número")
    andar = models.CharField(max_length=10, blank=True, verbose_name="Andar")
    bloco = models.CharField(max_length=10, blank=True, verbose_name="Bloco")
    STATUS_CHOICES = [
        ('ocupado', 'Ocupado'),
        ('vazio', 'Vazio'),
        ('nao_visitado', 'Não Visitado'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='nao_visitado',
        verbose_name="Status"
    )

    def __str__(self):
        if self.bloco:
            return f"Bloco {self.bloco}, Apto {self.numero}"
        return f"Apto {self.numero}"

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
        ordering = ['edificio', 'bloco', 'andar', 'numero']


# territorios/manage.py (continuação)

class SaidaCampo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    data = models.DateField(verbose_name="Data")
    dia_semana = models.CharField(max_length=15, blank=True, verbose_name="Dia da Semana")
    horario = models.TimeField(verbose_name="Horário")
    dirigente = models.CharField(max_length=100, verbose_name="Dirigente")
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='agendada',
        verbose_name="Status"
    )

    def save(self, *args, **kwargs):
        # Preencher automaticamente o dia da semana
        if self.data and not self.dia_semana:
            dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira',
                           'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
            self.dia_semana = dias_semana[self.data.weekday()]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} - {self.data.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Saída de Campo"
        verbose_name_plural = "Saídas de Campo"
        ordering = ['-data', 'horario']


class Designacao(models.Model):
    territorio = models.ForeignKey(
        Territorio,
        on_delete=models.CASCADE,
        related_name='designacoes',
        verbose_name="Território"
    )
    saida_campo = models.ForeignKey(
        SaidaCampo,
        on_delete=models.CASCADE,
        related_name='designacoes',
        verbose_name="Saída de Campo"
    )
    data_designacao = models.DateField(verbose_name="Data de Designação")
    data_devolucao = models.DateField(blank=True, null=True, verbose_name="Data de Devolução")
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='ativa',
        verbose_name="Status"
    )

    def __str__(self):
        return f"{self.territorio.nome} - {self.saida_campo.nome}"

    class Meta:
        verbose_name = "Designação"
        verbose_name_plural = "Designações"
        ordering = ['-data_designacao']