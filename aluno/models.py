from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


def validar_email_institucional(email):
    if not email.lower().endswith('@fepi.edu.br'):
        raise ValidationError('Use um e-mail institucional terminado em @fepi.edu.br.')


class Curso(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    carga_horaria = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name='disciplinas',
    )

    class Meta:
        ordering = ('nome', 'codigo')
        constraints = [
            models.CheckConstraint(
                condition=models.Q(carga_horaria__gte=1),
                name='disciplina_carga_horaria_positiva',
            ),
        ]

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Turma(models.Model):
    class Semestre(models.IntegerChoices):
        PRIMEIRO = 1, '1º semestre'
        SEGUNDO = 2, '2º semestre'

    codigo = models.CharField(max_length=20, unique=True)
    ano = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    semestre = models.PositiveSmallIntegerField(choices=Semestre.choices)
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.PROTECT,
        related_name='turmas',
    )

    class Meta:
        ordering = ('-ano', 'semestre', 'codigo')
        constraints = [
            models.CheckConstraint(
                condition=models.Q(ano__gte=1),
                name='turma_ano_positivo',
            ),
            models.CheckConstraint(
                condition=models.Q(semestre__in=(1, 2)),
                name='turma_semestre_valido',
            ),
        ]

    def __str__(self):
        return f'{self.codigo} - {self.ano}/{self.semestre}'


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name='alunos',
    )
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
