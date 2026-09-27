from django.contrib import admin
from .models import Aluno, Curso, Disciplina, Turma


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso', 'ativo', 'cpf', 'email_institucional', 'matriculado_em')
    search_fields = ('nome', 'cpf', 'curso__nome')
    list_filter = ('ativo', 'curso')
    readonly_fields = ('matriculado_em',)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'curso', 'carga_horaria')
    list_filter = ('curso',)
    search_fields = ('codigo', 'nome', 'curso__nome')


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'disciplina', 'ano', 'semestre')
    list_filter = ('ano', 'semestre', 'disciplina__curso')
    search_fields = ('codigo', 'disciplina__nome', 'disciplina__codigo')
