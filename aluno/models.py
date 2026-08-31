from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validar_email_institucional(email):
    if not email.lower().endswith('@fepi.edu.br'):
        raise ValidationError('Use um e-mail institucional terminado em @fepi.edu.br.')


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    bio = models.TextField(max_length=280)
    matriculado_em = models.DateTimeField(auto_now_add=True)
    email_institucional = models.EmailField(
        max_length=254,
        validators=[validar_email_institucional],
    )
    cpf = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='Informe o CPF no formato 000.000.000-00.',
            )
        ],
    )
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField()

    @property
    def cpf_mascarado(self):
        numeros = ''.join(caractere for caractere in self.cpf if caractere.isdigit())

        if len(numeros) != 11:
            return '***.***.***-**'

        return f'***.{numeros[3:6]}.{numeros[6:9]}-**'

    def __str__(self):
        return self.nome
