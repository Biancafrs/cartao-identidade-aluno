from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlunoForm
from .models import Aluno, Curso, Disciplina, Turma


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
        alunos = alunos.filter(Q(nome__icontains=busca) | Q(cpf__icontains=busca))
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
    return render(request, 'detalhe.html', {'aluno': aluno})


def criar_aluno(request):
    form = AlunoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('alunos:lista')

    return render(request, 'form_aluno.html', {'form': form, 'titulo': 'Novo aluno'})


def editar_aluno(request, pk):
    aluno = get_object_or_404(Aluno.objects.select_related('curso'), pk=pk)
    form = AlunoForm(request.POST or None, instance=aluno)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('alunos:lista')

    return render(
        request,
        'form_aluno.html',
        {'aluno': aluno, 'form': form, 'titulo': f'Editar: {aluno.nome}'},
    )


def excluir_aluno(request, pk):
    aluno = get_object_or_404(Aluno.objects.select_related('curso'), pk=pk)

    if request.method == 'POST':
        aluno.delete()
        return redirect('alunos:lista')

    return render(request, 'confirmar_exclusao.html', {'aluno': aluno})
