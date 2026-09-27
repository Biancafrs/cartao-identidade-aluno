import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('aluno', '0004_aluno_campos_obrigatorios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={'ordering': ('nome',)},
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('carga_horaria', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='disciplinas', to='aluno.curso')),
            ],
            options={'ordering': ('nome', 'codigo')},
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('ano', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('semestre', models.PositiveSmallIntegerField(choices=[(1, '1º semestre'), (2, '2º semestre')])),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='turmas', to='aluno.disciplina')),
            ],
            options={'ordering': ('-ano', 'semestre', 'codigo')},
        ),
        migrations.AddField(
            model_name='aluno',
            name='curso_novo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='alunos_em_migracao', to='aluno.curso'),
        ),
        migrations.AddConstraint(
            model_name='disciplina',
            constraint=models.CheckConstraint(condition=models.Q(('carga_horaria__gte', 1)), name='disciplina_carga_horaria_positiva'),
        ),
        migrations.AddConstraint(
            model_name='turma',
            constraint=models.CheckConstraint(condition=models.Q(('ano__gte', 1)), name='turma_ano_positivo'),
        ),
        migrations.AddConstraint(
            model_name='turma',
            constraint=models.CheckConstraint(condition=models.Q(('semestre__in', (1, 2))), name='turma_semestre_valido'),
        ),
    ]
