# atendimentos/apps.py
from django.apps import AppConfig


class AtendimentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'atendimentos'
    verbose_name = 'Atendimentos'

    def ready(self):
        """
        Método executado quando a aplicação é inicializada.
        Pode ser usado para registrar sinais ou realizar outras inicializações.
        """
        # Import dos sinais para garantir que sejam registrados
        import atendimentos.signals