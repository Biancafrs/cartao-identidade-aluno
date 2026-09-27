from django.contrib import admin
from django.urls import include, path

from aluno import views as aluno_views

urlpatterns = [
    path('', aluno_views.dashboard, name='home'),
    path('admin/', admin.site.urls),
    path('aluno/', include('aluno.urls')),
]
