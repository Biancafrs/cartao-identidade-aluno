from django import forms

from .models import Aluno, somente_numeros


class AlunoForm(forms.ModelForm):
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
            'cpf': 'Insira o seu CPF.',
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
