from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AlunoForm, CarteiraAcademicaForm, InscricaoTurmaForm
from .models import (
    Aluno, CarteiraAcademica, Curso, Disciplina, InscricaoTurma, Turma,
    somente_numeros,
)


def dashboard(request):
    indicadores_alunos = Aluno.objects.aggregate(
        total=Count('id'),
        ativos=Count('id', filter=Q(ativo=True)),
        inativos=Count('id', filter=Q(ativo=False)),
    )
    cursos = Curso.objects.annotate(total_alunos=Count('alunos')).order_by('nome')
    contexto = {
        **indicadores_alunos,
        'total_cursos': Curso.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
        'total_turmas': Turma.objects.count(),
        'cursos': cursos,
    }
    return render(request, 'dashboard.html', contexto)


def lista(request):
    busca = request.GET.get('busca', '').strip()
    curso = request.GET.get('curso', '').strip()
    alunos = Aluno.objects.select_related('curso')

    if busca:
        filtro_busca = Q(nome__icontains=busca)
        cpf_busca = somente_numeros(busca)
        if cpf_busca:
            filtro_busca |= Q(cpf__icontains=cpf_busca)
        alunos = alunos.filter(filtro_busca)
    if curso:
        alunos = alunos.filter(curso__nome=curso)

    cursos = Curso.objects.order_by('nome')
    return render(
        request,
        'lista.html',
        {'alunos': alunos, 'busca': busca, 'curso_selecionado': curso, 'cursos': cursos},
    )


def detalhe(request, pk):
    aluno = get_object_or_404(Aluno.objects.select_related('curso'), pk=pk)
    carteira = CarteiraAcademica.objects.filter(aluno=aluno).first()
    inscricoes = InscricaoTurma.objects.filter(aluno=aluno).select_related(
        'turma__disciplina__curso'
    )
    return render(request, 'detalhe.html', {
        'aluno': aluno,
        'carteira': carteira,
        'inscricoes': inscricoes,
    })


def carteira_aluno(request, pk):
    get_object_or_404(Aluno, pk=pk)
    return redirect(f"{reverse('alunos:detalhe', args=[pk])}#carteira")


def editar_carteira(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    carteira = CarteiraAcademica.objects.filter(aluno=aluno).first()
    form = CarteiraAcademicaForm(request.POST or None, instance=carteira)
    if request.method == 'POST' and form.is_valid():
        carteira = form.save(commit=False)
        carteira.aluno = aluno
        carteira.save()
        messages.success(request, 'Carteira acadêmica salva com sucesso.')
        return redirect(f"{reverse('alunos:detalhe', args=[aluno.pk])}#carteira")

    return render(request, 'form_relacionamento.html', {
        'form': form,
        'titulo': f'Carteira acadêmica de {aluno.nome}',
        'voltar_url': f"{reverse('alunos:detalhe', args=[aluno.pk])}#carteira",
    })


def inscrever_turma(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    form = InscricaoTurmaForm(request.POST or None, aluno=aluno)
    if request.method == 'POST' and form.is_valid():
        inscricao = form.save(commit=False)
        inscricao.aluno = aluno
        inscricao.save()
        messages.success(request, 'Inscrição em turma registrada com sucesso.')
        return redirect('alunos:detalhe', pk=aluno.pk)

    return render(request, 'form_relacionamento.html', {
        'form': form,
        'titulo': f'Inscrever {aluno.nome} em uma turma',
        'voltar_url': reverse('alunos:detalhe', args=[aluno.pk]),
    })


def criar_aluno(request):
    form = AlunoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        aluno = form.save()
        messages.success(request, f'Aluno {aluno.nome} cadastrado com sucesso.')
        return redirect('alunos:lista')

    return render(request, 'form_aluno.html', {'form': form, 'titulo': 'Novo aluno'})


def editar_aluno(request, pk):
    aluno = get_object_or_404(Aluno.objects.select_related('curso'), pk=pk)
    form = AlunoForm(request.POST or None, instance=aluno)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Aluno {aluno.nome} atualizado com sucesso.')
        return redirect('alunos:lista')

    return render(
        request,
        'form_aluno.html',
        {'aluno': aluno, 'form': form, 'titulo': f'Editar: {aluno.nome}'},
    )


def excluir_aluno(request, pk):
    aluno = get_object_or_404(Aluno.objects.select_related('curso'), pk=pk)

    if request.method == 'POST':
        nome = aluno.nome
        aluno.delete()
        messages.success(request, f'Aluno {nome} excluído com sucesso.')
        return redirect('alunos:lista')

    return render(request, 'confirmar_exclusao.html', {'aluno': aluno})
