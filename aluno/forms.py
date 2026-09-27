from django import forms
from django.db.models import Q

from .models import Aluno, Curso


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
            'bio',
            'curso',
            'email_institucional',
            'cpf',
            'endereco',
            'data_nascimento',
        )
        labels = {
            'bio': 'Biografia',
            'email_institucional': 'E-mail institucional',
            'cpf': 'CPF',
            'endereco': 'Endereço',
            'data_nascimento': 'Data de nascimento',
        }
        help_texts = {
            'bio': 'Até 280 caracteres.',
            'email_institucional': 'Use um endereço terminado em @fepi.edu.br.',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'},
            ),
        }
