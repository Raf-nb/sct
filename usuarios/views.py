# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm
from .models import Log


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                # Registrar log de login
                Log.objects.create(
                    usuario=user,
                    acao='Login',
                    tabela_afetada='',
                    detalhes=f"Usuário {user.username} fez login no sistema"
                )

                # Redirecionar para a página solicitada ou para o dashboard
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('dashboard')
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    # Registrar log de logout
    Log.objects.create(
        usuario=request.user,
        acao='Logout',
        tabela_afetada='',
        detalhes=f"Usuário {request.user.username} fez logout do sistema"
    )

    logout(request)
    return redirect('login')


@login_required
def register_user(request):
    # Verificar se o usuário tem permissão para registrar novos usuários
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para registrar novos usuários.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Registrar log de criação de usuário
            Log.objects.create(
                usuario=request.user,
                acao='Criar Usuário',
                tabela_afetada='User',
                registro_id=str(user.id),
                detalhes=f"Criado usuário: {user.username}"
            )

            messages.success(request, f'Usuário {user.username} criado com sucesso!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'usuarios/register.html', {'form': form})