from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify


# Importe seus modelos
# from .models import Territorio, Regiao, Municipio, Bairro

@receiver(pre_save, sender='territorios.Territorio')
def gerar_slug_territorio(sender, instance, **kwargs):
    """
    Gera automaticamente um slug para o território antes de salvar.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que será salva
        **kwargs: Argumentos adicionais
    """
    if not instance.slug:
        base_slug = slugify(instance.nome)
        slug = base_slug
        counter = 1

        # Verifica se o slug já existe e adiciona um contador se necessário
        while sender.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        instance.slug = slug


@receiver(post_save, sender='territorios.Territorio')
def atualizar_regioes_relacionadas(sender, instance, **kwargs):
    """
    Atualiza informações em regiões relacionadas quando um território é modificado.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que foi salva
        **kwargs: Argumentos adicionais
    """
    # Exemplo: atualizar status ou contadores em regiões relacionadas
    # if hasattr(instance, 'regioes'):
    #     for regiao in instance.regioes.all():
    #         regiao.recalcular_estatisticas()
    #         regiao.save()
    pass


@receiver(post_delete, sender='territorios.Regiao')
def limpar_referencias_regiao(sender, instance, **kwargs):
    """
    Limpa referências quando uma região é excluída.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que foi excluída
        **kwargs: Argumentos adicionais
    """
    # Exemplo: limpar referências ou atualizar contadores
    # Municipio.objects.filter(regiao_id=instance.id).update(regiao=None)
    pass


@receiver(pre_save, sender='territorios.Municipio')
def validar_municipio(sender, instance, **kwargs):
    """
    Realiza validações adicionais antes de salvar um município.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que será salva
        **kwargs: Argumentos adicionais
    """
    # Exemplo: normalizar o código IBGE
    if hasattr(instance, 'codigo_ibge') and instance.codigo_ibge:
        instance.codigo_ibge = instance.codigo_ibge.strip()

    # Exemplo: garantir que o nome esteja em maiúsculas
    if instance.nome:
        instance.nome = instance.nome.upper()


@receiver(post_save, sender='territorios.Bairro')
def atualizar_dados_geograficos(sender, instance, created, **kwargs):
    """
    Atualiza dados geográficos quando um bairro é criado ou modificado.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que foi salva
        created: Booleano indicando se este é um novo registro
        **kwargs: Argumentos adicionais
    """
    # Exemplo: atualizar dados geográficos do bairro
    # if created and instance.coordenadas:
    #     # Calcula área, perímetro, ou outros dados geográficos
    #     with transaction.atomic():
    #         instance.area = calcular_area(instance.coordenadas)
    #         instance.perimetro = calcular_perimetro(instance.coordenadas)
    #         instance.save(update_fields=['area', 'perimetro'])
    pass