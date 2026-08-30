from django import forms

from .models import Aluno


class AlunoForm(forms.ModelForm):
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
