from django.shortcuts import get_object_or_404, render
from .models import Aluno


def lista(request):
    alunos = Aluno.objects.all()
    return render(request, 'lista.html', {'alunos': alunos})


def detalhe(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'detalhe.html', {'aluno': aluno})
