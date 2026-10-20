from django.urls import path

from . import curso_views

app_name = 'cursos'

urlpatterns = [
    path('', curso_views.lista, name='lista'),
    path('novo/', curso_views.criar, name='criar'),
    path('<int:pk>/editar/', curso_views.editar, name='editar'),
    path('<int:pk>/excluir/', curso_views.excluir, name='excluir'),
]
