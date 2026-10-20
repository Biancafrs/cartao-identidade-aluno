from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone


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
    turmas = models.ManyToManyField(
        Turma,
        through='InscricaoTurma',
        related_name='alunos',
        blank=True,
    )

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


class CarteiraAcademica(models.Model):
    aluno = models.OneToOneField(
        Aluno,
        on_delete=models.CASCADE,
        related_name='carteira',
    )
    numero = models.CharField(max_length=30, unique=True)
    emitida_em = models.DateField()
    valida_ate = models.DateField()

    def clean(self):
        super().clean()
        if self.emitida_em and self.valida_ate and self.valida_ate < self.emitida_em:
            raise ValidationError({
                'valida_ate': 'A validade deve ser igual ou posterior à emissão.'
            })

    def __str__(self):
        return f'Carteira {self.numero} — {self.aluno.nome}'

    class Meta:
        ordering = ('aluno__nome',)
        verbose_name = 'Carteira acadêmica'
        verbose_name_plural = 'Carteiras acadêmicas'


class InscricaoTurma(models.Model):
    class Situacao(models.TextChoices):
        ATIVA = 'ATIVA', 'Ativa'
        CONCLUIDA = 'CONCLUIDA', 'Concluída'
        CANCELADA = 'CANCELADA', 'Cancelada'

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name='inscricoes',
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.PROTECT,
        related_name='inscricoes',
    )
    inscrito_em = models.DateField(default=timezone.localdate)
    situacao = models.CharField(
        max_length=10,
        choices=Situacao.choices,
        default=Situacao.ATIVA,
    )

    def __str__(self):
        return f'{self.aluno.nome} — {self.turma.codigo}'

    class Meta:
        ordering = ('-inscrito_em', 'turma__codigo')
        verbose_name = 'Inscrição em turma'
        verbose_name_plural = 'Inscrições em turmas'
        constraints = [
            models.UniqueConstraint(
                fields=('aluno', 'turma'),
                name='inscricao_aluno_turma_unica',
            ),
        ]
