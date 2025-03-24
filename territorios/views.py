# territorios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib import messages
from .models import Territorio, Rua, Imovel, Edificio, Unidade, SaidaCampo, Designacao
from .forms import (TerritorioForm, RuaForm, ImovelForm, EdificioForm,
                    UnidadeForm, SaidaCampoForm, DesignacaoForm)
from atendimentos.models import Atendimento
from usuarios.models import Log


@login_required
def dashboard(request):
    # Coletar estatísticas
    total_territorios = Territorio.objects.count()
    total_imoveis = Imovel.objects.count()

    # Contar imóveis atendidos (com pelo menos um atendimento)
    imoveis_atendidos = Imovel.objects.annotate(
        qtd_atendimentos=Count('atendimentos')
    ).filter(qtd_atendimentos__gt=0).count()

    # Calcular percentual de atendimento
    percentual_atendidos = (imoveis_atendidos / total_imoveis * 100) if total_imoveis > 0 else 0

    # Designações ativas
    designacoes_ativas = Designacao.objects.filter(status='ativa').count()

    # Território do dia (hoje)
    hoje = timezone.localdate()
    territorio_hoje = Designacao.objects.filter(
        saida_campo__data=hoje,
        status='ativa'
    ).select_related('territorio', 'saida_campo').first()

    # Próximas saídas de campo
    proximas_saidas = SaidaCampo.objects.filter(
        data__gte=hoje,
        status='agendada'
    ).order_by('data')[:5]

    # Últimas designações
    ultimas_designacoes = Designacao.objects.filter(
        status='ativa'
    ).select_related('territorio', 'saida_campo').order_by('-data_designacao')[:5]

    # Tipos de imóveis (para gráfico)
    tipos_imoveis = Imovel.objects.values('tipo').annotate(count=Count('id'))

    context = {
        'total_territorios': total_territorios,
        'total_imoveis': total_imoveis,
        'imoveis_atendidos': imoveis_atendidos,
        'percentual_atendidos': percentual_atendidos,
        'designacoes_ativas': designacoes_ativas,
        'territorio_hoje': territorio_hoje,
        'proximas_saidas': proximas_saidas,
        'ultimas_designacoes': ultimas_designacoes,
        'tipos_imoveis': tipos_imoveis,
    }

    return render(request, 'territorios/dashboard.html', context)


@login_required
def territorio_list(request):
    territorios = Territorio.objects.all()
    return render(request, 'territorios/territorio_list.html', {'territorios': territorios})


# territorios/views.py (continuação)
@login_required
def territorio_create(request):
    if request.method == 'POST':
        form = TerritorioForm(request.POST)
        if form.is_valid():
            territorio = form.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Criar Território',
                tabela_afetada='Territorio',
                registro_id=str(territorio.id),
                detalhes=f"Criado território: {territorio.nome}"
            )

            messages.success(request, f'Território "{territorio.nome}" criado com sucesso!')
            return redirect('territorio_detail', pk=territorio.id)
    else:
        form = TerritorioForm()

    return render(request, 'territorios/territorio_form.html', {'form': form, 'titulo': 'Novo Território'})


@login_required
def territorio_detail(request, pk):
    territorio = get_object_or_404(Territorio, pk=pk)
    ruas = territorio.ruas.all()

    # Contar imóveis e atendimentos por território
    total_imoveis = Imovel.objects.filter(rua__territorio=territorio).count()

    imoveis_atendidos = Imovel.objects.filter(
        rua__territorio=territorio
    ).annotate(
        atendimentos_count=Count('atendimentos')
    ).filter(atendimentos_count__gt=0).count()

    percentual_atendido = (imoveis_atendidos / total_imoveis * 100) if total_imoveis > 0 else 0

    # Buscar designações ativas para este território
    designacoes = territorio.designacoes.filter(status='ativa')

    context = {
        'territorio': territorio,
        'ruas': ruas,
        'total_imoveis': total_imoveis,
        'imoveis_atendidos': imoveis_atendidos,
        'percentual_atendido': percentual_atendido,
        'designacoes': designacoes,
    }

    return render(request, 'territorios/territorio_detail.html', context)


@login_required
def territorio_update(request, pk):
    territorio = get_object_or_404(Territorio, pk=pk)

    if request.method == 'POST':
        form = TerritorioForm(request.POST, instance=territorio)
        if form.is_valid():
            territorio = form.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Atualizar Território',
                tabela_afetada='Territorio',
                registro_id=str(territorio.id),
                detalhes=f"Atualizado território: {territorio.nome}"
            )

            messages.success(request, f'Território "{territorio.nome}" atualizado com sucesso!')
            return redirect('territorio_detail', pk=territorio.id)
    else:
        form = TerritorioForm(instance=territorio)

    return render(request, 'territorios/territorio_form.html',
                  {'form': form, 'titulo': 'Editar Território', 'territorio': territorio})


@login_required
def rua_create(request, territorio_id):
    territorio = get_object_or_404(Territorio, pk=territorio_id)

    if request.method == 'POST':
        form = RuaForm(request.POST)
        if form.is_valid():
            rua = form.save(commit=False)
            rua.territorio = territorio
            rua.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Criar Rua',
                tabela_afetada='Rua',
                registro_id=str(rua.id),
                detalhes=f"Criada rua: {rua.nome} no território {territorio.nome}"
            )

            messages.success(request, f'Rua "{rua.nome}" adicionada com sucesso ao território "{territorio.nome}"!')
            return redirect('territorio_detail', pk=territorio.id)
    else:
        form = RuaForm()

    return render(request, 'territorios/rua_form.html',
                  {'form': form, 'territorio': territorio, 'titulo': 'Nova Rua'})


@login_required
def imovel_create(request, rua_id):
    rua = get_object_or_404(Rua, pk=rua_id)

    if request.method == 'POST':
        form = ImovelForm(request.POST)
        if form.is_valid():
            imovel = form.save(commit=False)
            imovel.rua = rua
            imovel.save()

            # Se for prédio ou vila, redirecionar para criar edificio
            if imovel.tipo in ['predio', 'vila']:
                return redirect('edificio_create', imovel_id=imovel.id)

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Criar Imóvel',
                tabela_afetada='Imovel',
                registro_id=str(imovel.id),
                detalhes=f"Criado imóvel: {imovel.numero} na rua {rua.nome}"
            )

            messages.success(request, f'Imóvel nº "{imovel.numero}" adicionado com sucesso à rua "{rua.nome}"!')
            return redirect('rua_detail', pk=rua.id)
    else:
        form = ImovelForm()

    return render(request, 'territorios/imovel_form.html',
                  {'form': form, 'rua': rua, 'titulo': 'Novo Imóvel'})


@login_required
def edificio_create(request, imovel_id):
    imovel = get_object_or_404(Imovel, pk=imovel_id)

    # Verificar se já existe um edifício para este imóvel
    try:
        edificio = imovel.edificio
        messages.warning(request, f'Este imóvel já possui um edifício configurado: {edificio.nome}')
        return redirect('edificio_detail', pk=edificio.id)
    except Edificio.DoesNotExist:
        pass

    if request.method == 'POST':
        form = EdificioForm(request.POST)
        if form.is_valid():
            edificio = form.save(commit=False)
            edificio.imovel = imovel
            edificio.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Criar Edifício',
                tabela_afetada='Edificio',
                registro_id=str(edificio.id),
                detalhes=f"Criado edifício: {edificio.nome} para o imóvel {imovel.numero}"
            )

            messages.success(request, f'Edifício "{edificio.nome}" criado com sucesso!')
            return redirect('edificio_detail', pk=edificio.id)
    else:
        # Pré-preencher nome com base no imóvel
        form = EdificioForm(initial={
            'nome': f"{imovel.tipo.capitalize()} - {imovel.rua.nome}, {imovel.numero}"
        })

    return render(request, 'territorios/edificio_form.html',
                  {'form': form, 'imovel': imovel, 'titulo': 'Novo Edifício'})


@login_required
def saida_campo_list(request):
    saidas = SaidaCampo.objects.all().order_by('-data')
    return render(request, 'territorios/saida_campo_list.html', {'saidas': saidas})


@login_required
def saida_campo_create(request):
    if request.method == 'POST':
        form = SaidaCampoForm(request.POST)
        if form.is_valid():
            saida = form.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Criar Saída de Campo',
                tabela_afetada='SaidaCampo',
                registro_id=str(saida.id),
                detalhes=f"Criada saída de campo: {saida.nome} em {saida.data.strftime('%d/%m/%Y')}"
            )

            messages.success(request, f'Saída de campo "{saida.nome}" criada com sucesso!')
            return redirect('saida_campo_list')
    else:
        form = SaidaCampoForm()

    return render(request, 'territorios/saida_campo_form.html', {'form': form, 'titulo': 'Nova Saída de Campo'})


@login_required
def designacao_list(request):
    designacoes = Designacao.objects.all().select_related('territorio', 'saida_campo').order_by('-data_designacao')
    return render(request, 'territorios/designacao_list.html', {'designacoes': designacoes})


@login_required
def designacao_create(request):
    if request.method == 'POST':
        form = DesignacaoForm(request.POST)
        if form.is_valid():
            designacao = form.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Criar Designação',
                tabela_afetada='Designacao',
                registro_id=str(designacao.id),
                detalhes=f"Criada designação do território {designacao.territorio.nome} para {designacao.saida_campo.nome}"
            )

            messages.success(request, 'Designação criada com sucesso!')
            return redirect('designacao_list')
    else:
        form = DesignacaoForm()

    return render(request, 'territorios/designacao_form.html', {'form': form, 'titulo': 'Nova Designação'})


@login_required
def territorio_dia(request):
    hoje = timezone.localdate()

    # Buscar designação para hoje
    designacao = Designacao.objects.filter(
        saida_campo__data=hoje,
        status='ativa'
    ).select_related('territorio', 'saida_campo').first()

    # Buscar próximas designações
    proximas_designacoes = Designacao.objects.filter(
        saida_campo__data__gt=hoje,
        status='ativa'
    ).select_related('territorio', 'saida_campo').order_by('saida_campo__data')[:5]

    context = {
        'hoje': hoje,
        'designacao': designacao,
        'proximas_designacoes': proximas_designacoes,
    }

    return render(request, 'territorios/territorio_dia.html', context)
