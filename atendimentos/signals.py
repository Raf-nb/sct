from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User
from django.conf import settings
import logging

# Configure o logger para os sinais
logger = logging.getLogger(__name__)


# Importe seus modelos
# from .models import Atendimento, Encaminhamento, Agendamento, StatusAtendimento, HistoricoAtendimento

@receiver(pre_save, sender='atendimentos.Atendimento')
def pre_salvar_atendimento(sender, instance, **kwargs):
    """
    Executa ações antes de salvar um atendimento.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que será salva
        **kwargs: Argumentos adicionais
    """
    # Se for um novo registro (sem ID), defina a data de criação
    if not instance.pk:
        instance.data_criacao = timezone.now()

    # Sempre atualiza a data de modificação
    instance.data_modificacao = timezone.now()

    # Verificar se há mudança de status e registrar
    if instance.pk:
        try:
            antigo = sender.objects.get(pk=instance.pk)
            if hasattr(instance, 'status') and hasattr(antigo, 'status') and instance.status != antigo.status:
                instance.data_status = timezone.now()
                # Poderia adicionar aqui lógica para criar um registro no histórico
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='atendimentos.Atendimento')
def registrar_historico_atendimento(sender, instance, created, **kwargs):
    """
    Registra alterações no histórico quando um atendimento é criado ou modificado.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que foi salva
        created: Booleano indicando se este é um novo registro
        **kwargs: Argumentos adicionais
    """
    # from .models import HistoricoAtendimento

    # Cria um registro de histórico
    # tipo = 'criacao' if created else 'atualizacao'
    # HistoricoAtendimento.objects.create(
    #     atendimento=instance,
    #     tipo=tipo,
    #     data=timezone.now(),
    #     usuario=instance.responsavel if hasattr(instance, 'responsavel') else None,
    #     descricao=f"Atendimento {'criado' if created else 'atualizado'}"
    # )
    pass


@receiver(post_save, sender='atendimentos.Encaminhamento')
def processar_encaminhamento(sender, instance, created, **kwargs):
    """
    Processa ações necessárias quando um encaminhamento é criado ou modificado.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que foi salva
        created: Booleano indicando se este é um novo registro
        **kwargs: Argumentos adicionais
    """
    if created:
        # Atualiza o status do atendimento associado, se existir
        # if hasattr(instance, 'atendimento') and instance.atendimento:
        #     atendimento = instance.atendimento
        #     atendimento.status = 'encaminhado'
        #     atendimento.save(update_fields=['status', 'data_modificacao'])

        # Notifica o destino do encaminhamento
        # notificar_destino_encaminhamento(instance)
        pass


@receiver(pre_save, sender='atendimentos.Agendamento')
def validar_agendamento(sender, instance, **kwargs):
    """
    Valida as regras de negócio antes de salvar um agendamento.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que será salva
        **kwargs: Argumentos adicionais
    """
    # Verifica se a data do agendamento é futura
    if hasattr(instance, 'data_agendamento') and instance.data_agendamento:
        if instance.data_agendamento < timezone.now():
            logger.warning(f"Tentativa de criar agendamento com data passada: {instance.data_agendamento}")
            # Você pode levantar uma exceção aqui ou definir um valor padrão
            # raise ValueError("A data do agendamento deve ser futura")

    # Verifica disponibilidade no horário
    # verificar_disponibilidade_horario(instance)


@receiver(m2m_changed, sender='atendimentos.Atendimento.categorias.through')
def atualizar_categorias_atendimento(sender, instance, action, pk_set, **kwargs):
    """
    Atualiza informações quando as categorias de um atendimento são modificadas.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do atendimento
        action: A ação realizada (add, remove, clear, etc.)
        pk_set: Conjunto de IDs de objetos adicionados ou removidos
        **kwargs: Argumentos adicionais
    """
    if action in ('post_add', 'post_remove', 'post_clear'):
        # Atualiza estatísticas ou outras informações relacionadas às categorias
        # atualizar_estatisticas_categorias()

        # Registra a mudança no histórico
        # from .models import HistoricoAtendimento
        # HistoricoAtendimento.objects.create(
        #     atendimento=instance,
        #     tipo='alteracao_categorias',
        #     data=timezone.now(),
        #     usuario=None,  # Você precisa identificar o usuário atual de alguma forma
        #     descricao=f"Categorias do atendimento foram {action.replace('post_', '')}"
        # )
        pass


@receiver(post_delete, sender='atendimentos.Atendimento')
def registrar_exclusao_atendimento(sender, instance, **kwargs):
    """
    Registra quando um atendimento é excluído e realiza limpezas necessárias.

    Args:
        sender: O modelo que enviou o sinal
        instance: A instância do modelo que foi excluída
        **kwargs: Argumentos adicionais
    """
    # Pode criar um log em uma tabela separada para auditar exclusões
    # from .models import LogExclusao
    # LogExclusao.objects.create(
    #     modelo='Atendimento',
    #     objeto_id=instance.id,
    #     data=timezone.now(),
    #     usuario=None,  # Você precisa identificar o usuário atual de alguma forma
    #     dados=str(instance.__dict__)
    # )

    logger.info(f"Atendimento {instance.id} excluído em {timezone.now()}")