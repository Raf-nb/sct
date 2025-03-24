from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings


# Importe seu modelo de perfil, se você tiver um
# from .models import Perfil

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Sinal para criar um perfil de usuário automaticamente quando um novo usuário é criado.

    Args:
        sender: O modelo que enviou o sinal (User)
        instance: A instância do modelo que foi salva
        created: Booleano indicando se este é um novo registro
        **kwargs: Argumentos adicionais
    """
    if created:
        # Se você tiver um modelo de perfil, descomente a linha abaixo
        # Perfil.objects.create(usuario=instance)
        pass


@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    """
    Sinal para salvar o perfil do usuário quando o usuário é atualizado.

    Args:
        sender: O modelo que enviou o sinal (User)
        instance: A instância do modelo que foi salva
        **kwargs: Argumentos adicionais
    """
    # Se você tiver um modelo de perfil, descomente a linha abaixo
    # instance.perfil.save()
    pass


# Exemplo de sinal pre_save para manipular dados antes de salvar
@receiver(pre_save, sender=User)
def processar_usuario_antes_de_salvar(sender, instance, **kwargs):
    """
    Sinal executado antes de salvar um usuário, pode ser usado para
    transformar ou validar dados.

    Args:
        sender: O modelo que enviou o sinal (User)
        instance: A instância do modelo que será salva
        **kwargs: Argumentos adicionais
    """
    # Exemplo: Normalizar email para minúsculas
    if instance.email:
        instance.email = instance.email.lower()