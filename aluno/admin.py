from django.contrib import admin
from .forms import AlunoForm
from .models import Aluno


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    form = AlunoForm
    list_display = ('nome', 'curso', 'periodo', 'ativo', 'cpf_formatado', 'email_institucional', 'matriculado_em')
    search_fields = ('nome', 'cpf')
    list_filter = ('curso', 'periodo', 'ativo')
    readonly_fields = ('matriculado_em',)
