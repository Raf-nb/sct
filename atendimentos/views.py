# atendimentos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Atendimento
from .forms import AtendimentoImovelForm, AtendimentoUnidadeForm
from territorios.models import Territorio, Imovel, Edificio, Unidade
from usuarios.models import Log


@login_required
def atendimento_list(request):
    # Filtros
    tipo_imovel = request.GET.get('tipo_imovel', '')
    status = request.GET.get('status', '')

    # Buscar territórios com informações sobre atendimentos
    territorios = Territorio.objects.all()

    # Adicionar informações de atendimento para cada território
    for territorio in territorios:
        # Contar imóveis no território
        territorio.total_imoveis = Imovel.objects.filter(rua__territorio=territorio).count()

        # Contar imóveis atendidos
        territorio.imoveis_atendidos = Imovel.objects.filter(
            rua__territorio=territorio
        ).annotate(
            atendimentos_count=Count('atendimentos')
        ).filter(atendimentos_count__gt=0).count()

        # Calcular percentual de atendimento
        if territorio.total_imoveis > 0:
            territorio.percentual_atendido = (territorio.imoveis_atendidos / territorio.total_imoveis) * 100
        else:
            territorio.percentual_atendido = 0

    context = {
        'territorios': territorios,
        'tipo_imovel': tipo_imovel,
        'status': status,
    }

    return render(request, 'atendimentos/atendimento_list.html', context)


@login_required
def imovel_atendimentos(request, imovel_id):
    imovel = get_object_or_404(Imovel, pk=imovel_id)
    atendimentos = Atendimento.objects.filter(imovel=imovel).order_by('-data', '-hora')

    # Criar novo atendimento
    if request.method == 'POST':
        form = AtendimentoImovelForm(request.POST)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.imovel = imovel
            atendimento.registrado_por = request.user
            atendimento.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Registrar Atendimento',
                tabela_afetada='Atendimento',
                registro_id=str(atendimento.id),
                detalhes=f"Registrado atendimento para o imóvel {imovel.endereco_completo}"
            )

            messages.success(request, 'Atendimento registrado com sucesso!')
            return redirect('imovel_atendimentos', imovel_id=imovel.id)
    else:
        form = AtendimentoImovelForm(initial={'imovel': imovel})

    context = {
        'imovel': imovel,
        'atendimentos': atendimentos,
        'form': form,
    }

    return render(request, 'atendimentos/imovel_atendimentos.html', context)


@login_required
def unidade_atendimentos(request, unidade_id):
    unidade = get_object_or_404(Unidade, pk=unidade_id)
    atendimentos = Atendimento.objects.filter(unidade=unidade).order_by('-data', '-hora')

    # Criar novo atendimento
    if request.method == 'POST':
        form = AtendimentoUnidadeForm(request.POST)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.unidade = unidade
            atendimento.registrado_por = request.user
            atendimento.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Registrar Atendimento',
                tabela_afetada='Atendimento',
                registro_id=str(atendimento.id),
                detalhes=f"Registrado atendimento para unidade {unidade} do edificio {unidade.edificio.nome}"
            )

            messages.success(request, 'Atendimento registrado com sucesso!')
            return redirect('unidade_atendimentos', unidade_id=unidade.id)
    else:
        form = AtendimentoUnidadeForm(initial={'unidade': unidade})

    context = {
        'unidade': unidade,
        'edificio': unidade.edificio,
        'atendimentos': atendimentos,
        'form': form,
    }

    return render(request, 'atendimentos/unidade_atendimentos.html', context)


@login_required
def predios_vilas_list(request):
    # Filtros
    tipo = request.GET.get('tipo', '')
    status = request.GET.get('status', '')

    # Consulta base
    query = Edificio.objects.all().select_related('imovel', 'imovel__rua')

    # Aplicar filtros
    if tipo:
        query = query.filter(imovel__tipo=tipo)

    edificios = query.order_by('nome')

    context = {
        'edificios': edificios,
        'tipo_selecionado': tipo,
        'status': status,
    }

    return render(request, 'atendimentos/predios_vilas_list.html', context)


@login_required
def edificio_detail(request, pk):
    edificio = get_object_or_404(Edificio, pk=pk)
    unidades = edificio.unidades.all().order_by('bloco', 'andar', 'numero')

    # Contar unidades atendidas
    total_unidades = unidades.count()
    unidades_atendidas = 0

    for unidade in unidades:
        unidade.tem_atendimento = Atendimento.objects.filter(unidade=unidade).exists()
        if unidade.tem_atendimento:
            unidades_atendidas += 1

    # Calcular percentual de atendimento
    percentual_atendido = (unidades_atendidas / total_unidades * 100) if total_unidades > 0 else 0

    context = {
        'edificio': edificio,
        'unidades': unidades,
        'total_unidades': total_unidades,
        'unidades_atendidas': unidades_atendidas,
        'percentual_atendido': percentual_atendido,
    }

    return render(request, 'atendimentos/edificio_detail.html', context)


# atendimentos/views.py (adicionar)
@login_required
def unidade_create(request, edificio_id):
    edificio = get_object_or_404(Edificio, pk=edificio_id)

    if request.method == 'POST':
        form = UnidadeForm(request.POST)
        if form.is_valid():
            unidade = form.save(commit=False)
            unidade.edificio = edificio
            unidade.save()

            # Incrementar o contador de total_unidades do edificio
            edificio.total_unidades = edificio.unidades.count()
            edificio.save()

            # Registrar log
            Log.objects.create(
                usuario=request.user,
                acao='Criar Unidade',
                tabela_afetada='Unidade',
                registro_id=str(unidade.id),
                detalhes=f"Criada unidade {unidade.numero} no edifício {edificio.nome}"
            )

            messages.success(request, f'Unidade {unidade.numero} criada com sucesso!')
            return redirect('edificio_detail', pk=edificio.id)
    else:
        form = UnidadeForm()

    context = {
        'form': form,
        'edificio': edificio,
    }

    return render(request, 'atendimentos/unidade_form.html', context)
