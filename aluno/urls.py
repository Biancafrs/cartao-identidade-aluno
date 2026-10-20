from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('<int:pk>/', views.detalhe, name='detalhe'),
    path('<int:pk>/carteira/', views.carteira_aluno, name='carteira_aluno'),
    path('<int:pk>/carteira/editar/', views.editar_carteira, name='editar_carteira'),
    path('<int:pk>/inscricoes/nova/', views.inscrever_turma, name='inscrever_turma'),
    path('novo/', views.criar_aluno, name='criar_aluno'),
    path('<int:pk>/editar/', views.editar_aluno, name='editar_aluno'),
    path('<int:pk>/excluir/', views.excluir_aluno, name='excluir_aluno'),
]
