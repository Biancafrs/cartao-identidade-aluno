from django.db import models
from django.core.exceptions import ValidationError


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
    cpf = models.CharField(max_length=14)
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome
