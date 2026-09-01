from django.contrib import admin
from .models import Aluno


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso', 'periodo', 'ativo', 'cpf', 'email_institucional', 'matriculado_em')
    search_fields = ('nome', 'cpf')
    list_filter = ('curso', 'periodo', 'ativo')
    readonly_fields = ('matriculado_em',)
