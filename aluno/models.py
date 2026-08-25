from django.db import models
from django.utils import timezone


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    bio = models.TextField(max_length=280)
    criado_em = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nome
