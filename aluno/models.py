from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator


def validar_email_institucional(email):
    if not email.lower().endswith('@fepi.edu.br'):
        raise ValidationError('Use um e-mail institucional terminado em @fepi.edu.br.')


def somente_numeros(valor):
    return ''.join(caractere for caractere in valor if caractere.isdigit())


def formatar_cpf(cpf):
    numeros = somente_numeros(cpf)
    return f'{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}'


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

    @property
    def cpf_formatado(self):
        return formatar_cpf(self.cpf)

    @property
    def cpf_mascarado(self):
        numeros = somente_numeros(self.cpf)
        if len(numeros) != 11:
            return '***.***.***-**'
        return f'***.{numeros[3:6]}.{numeros[6:9]}-**'

    def save(self, *args, **kwargs):
        self.cpf = somente_numeros(self.cpf)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
