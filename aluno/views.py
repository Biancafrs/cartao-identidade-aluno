from django.shortcuts import get_object_or_404, redirect, render

from .models import Aluno


def lista(request):
    alunos = Aluno.objects.all()
    return render(request, 'lista.html', {'alunos': alunos})


def detalhe(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'detalhe.html', {'aluno': aluno})


def criar_aluno(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        curso = request.POST['curso']
        bio = request.POST.get('bio', '')
        Aluno.objects.create(nome=nome, curso=curso, bio=bio)
        return redirect('alunos:lista')

    return render(request, 'form_aluno.html', {'titulo': 'Novo Aluno'})


def editar_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)

    if request.method == 'POST':
        aluno.nome = request.POST['nome']
        aluno.curso = request.POST['curso']
        aluno.bio = request.POST.get('bio', '')
        aluno.save()
        return redirect('alunos:lista')

    return render(
        request,
        'form_aluno.html',
        {'aluno': aluno, 'titulo': f'Editar: {aluno.nome}'},
    )


def excluir_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)

    if request.method == 'POST':
        aluno.delete()
        return redirect('alunos:lista')

    return render(request, 'confirmar_exclusao.html', {'aluno': aluno})
