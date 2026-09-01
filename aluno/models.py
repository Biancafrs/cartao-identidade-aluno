from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validar_email_institucional(email):
    if not email.lower().endswith('@fepi.edu.br'):
        raise ValidationError('Use um e-mail institucional terminado em @fepi.edu.br.')


def formatar_cpf(cpf):
    numeros = ''.join(caractere for caractere in cpf if caractere.isdigit())
    return f'{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}'


def somente_numeros(cpf):
    return ''.join(caractere for caractere in cpf if caractere.isdigit())


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    periodo = models.PositiveSmallIntegerField(default=1)
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
                regex=r'^(?:\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2})$',
                message='Informe os 11 números do CPF.',
            )
        ],
    )
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)

    @property
    def cpf_formatado(self):
        return formatar_cpf(self.cpf)

    def save(self, *args, **kwargs):
        self.cpf = somente_numeros(self.cpf)
        super().save(*args, **kwargs)

    @property
    def cpf_mascarado(self):
        numeros = somente_numeros(self.cpf)

        if len(numeros) != 11:
            return '***.***.***-**'

        return f'***.{numeros[3:6]}.{numeros[6:9]}-**'

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
