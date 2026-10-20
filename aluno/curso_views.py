from django.contrib import messages
from django.db.models import Count
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CursoForm
from .models import Curso


def lista(request):
    cursos = Curso.objects.annotate(
        total_alunos=Count('alunos', distinct=True),
        total_disciplinas=Count('disciplinas', distinct=True),
    )
    return render(request, 'curso_lista.html', {'cursos': cursos})


def criar(request):
    form = CursoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        curso = form.save()
        messages.success(request, f'Curso {curso.nome} cadastrado com sucesso.')
        return redirect('cursos:lista')

    return render(request, 'curso_form.html', {'form': form, 'titulo': 'Novo curso'})


def editar(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    form = CursoForm(request.POST or None, instance=curso)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Curso {curso.nome} atualizado com sucesso.')
        return redirect('cursos:lista')

    return render(request, 'curso_form.html', {
        'form': form, 'titulo': f'Editar: {curso.nome}'
    })


def excluir(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    total_alunos = curso.alunos.count()
    total_disciplinas = curso.disciplinas.count()
    if request.method == 'POST':
        try:
            nome = curso.nome
            curso.delete()
        except ProtectedError:
            messages.error(
                request,
                'Não é possível excluir um curso com alunos ou disciplinas vinculados.',
            )
        else:
            messages.success(request, f'Curso {nome} excluído com sucesso.')
        return redirect('cursos:lista')

    return render(request, 'curso_confirmar_exclusao.html', {
        'curso': curso,
        'total_alunos': total_alunos,
        'total_disciplinas': total_disciplinas,
    })
