from django import forms
from django.db.models import Q

from .models import (
    Aluno, CarteiraAcademica, Curso, InscricaoTurma, Turma, somente_numeros,
)


class AlunoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cursos_disponiveis = Q(ativo=True)
        if self.instance and self.instance.curso_id:
            cursos_disponiveis |= Q(pk=self.instance.curso_id)

        campo_curso = self.fields['curso']
        campo_curso.queryset = Curso.objects.filter(cursos_disponiveis).order_by('nome')
        campo_curso.empty_label = 'Selecione um curso'
        if not campo_curso.queryset.exists():
            campo_curso.help_text = (
                'Nenhum curso ativo disponível. Cadastre um curso na área administrativa.'
            )

    class Meta:
        model = Aluno
        fields = (
            'nome',
            'curso',
            'periodo',
            'bio',
            'email_institucional',
            'cpf',
            'endereco',
            'data_nascimento',
            'ativo',
        )
        labels = {
            'periodo': 'Período',
            'bio': 'Biografia',
            'email_institucional': 'E-mail institucional',
            'cpf': 'CPF',
            'endereco': 'Endereço',
            'data_nascimento': 'Data de nascimento',
            'ativo': 'Aluno ativo',
        }
        help_texts = {
            'periodo': 'Informe o período atual do aluno.',
            'bio': 'Até 280 caracteres.',
            'email_institucional': 'Use um endereço terminado em @fepi.edu.br.',
            'cpf': 'Informe os 11 números do CPF.',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
            'cpf': forms.TextInput(
                attrs={
                    'inputmode': 'numeric',
                    'autocomplete': 'off',
                    'placeholder': 'Somente números',
                }
            ),
            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'},
            ),
        }

    def clean_cpf(self):
        return somente_numeros(self.cleaned_data['cpf'])


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'ativo')
        labels = {'ativo': 'Curso ativo'}


class CarteiraAcademicaForm(forms.ModelForm):
    class Meta:
        model = CarteiraAcademica
        fields = ('numero', 'emitida_em', 'valida_ate')
        labels = {
            'numero': 'Número da carteira',
            'emitida_em': 'Data de emissão',
            'valida_ate': 'Válida até',
        }
        widgets = {
            'emitida_em': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'valida_ate': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class InscricaoTurmaForm(forms.ModelForm):
    def __init__(self, *args, aluno, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = (
            Turma.objects.select_related('disciplina__curso')
            .exclude(inscricoes__aluno=aluno)
            .order_by('-ano', 'semestre', 'codigo')
        )
        if not self.fields['turma'].queryset.exists():
            self.fields['turma'].help_text = (
                'Nenhuma turma disponível. Cadastre uma turma na área administrativa.'
            )

    class Meta:
        model = InscricaoTurma
        fields = ('turma', 'inscrito_em', 'situacao')
        labels = {'inscrito_em': 'Data da inscrição', 'situacao': 'Situação'}
        widgets = {
            'inscrito_em': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
