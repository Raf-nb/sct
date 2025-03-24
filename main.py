# main.py
# !/usr/bin/env python
"""
Ponto de entrada principal para o Sistema de Controle de Territórios.
Este arquivo facilita a execução em ambientes como Gunicorn, PythonAnywhere, etc.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configurar o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_territorios.settings')


# Esta função de aplicação é usada por servidores WSGI
def get_wsgi_application():
    from django.core.wsgi import get_wsgi_application
    return get_wsgi_application()


# Esta função de aplicação é usada por servidores ASGI (para WebSockets)
def get_asgi_application():
    from django.core.asgi import get_asgi_application
    return get_asgi_application()


# Para execução direta deste arquivo
if __name__ == "__main__":
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar Django. Verifique se está instalado e "
            "disponível na variável de ambiente PYTHONPATH. Você esqueceu "
            "de ativar um ambiente virtual?"
        ) from exc

    # Executar o servidor de desenvolvimento se nenhum argumento for fornecido
    if len(sys.argv) == 1:
        sys.argv.append('runserver')

    execute_from_command_line(sys.argv)

# Exportar a aplicação WSGI para servidores web
application = get_wsgi_application()