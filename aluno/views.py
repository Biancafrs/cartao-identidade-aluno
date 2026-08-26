from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlunoForm
from .models import Aluno


def lista(request):
    busca = request.GET.get('busca', '').strip()
    curso = request.GET.get('curso', '').strip()
    alunos = Aluno.objects.all()

    if busca:
        alunos = alunos.filter(Q(nome__icontains=busca) | Q(cpf__icontains=busca))
    if curso:
        alunos = alunos.filter(curso=curso)

    cursos = (
        Aluno.objects.order_by('curso')
        .values_list('curso', flat=True)
        .distinct()
    )
    return render(
        request,
        'lista.html',
        {'alunos': alunos, 'busca': busca, 'curso_selecionado': curso, 'cursos': cursos},
    )


def detalhe(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'detalhe.html', {'aluno': aluno})


def criar_aluno(request):
    form = AlunoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('alunos:lista')

    return render(request, 'form_aluno.html', {'form': form, 'titulo': 'Novo aluno'})


def editar_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
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
    aluno = get_object_or_404(Aluno, pk=pk)

    if request.method == 'POST':
        aluno.delete()
        return redirect('alunos:lista')

    return render(request, 'confirmar_exclusao.html', {'aluno': aluno})
