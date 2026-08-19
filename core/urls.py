from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        '',
        RedirectView.as_view(pattern_name='alunos:lista', permanent=False),
        name='home',
    ),
    path('admin/', admin.site.urls),
    path('aluno/', include('aluno.urls')),
]
