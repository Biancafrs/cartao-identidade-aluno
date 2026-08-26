import datetime

import aluno.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('aluno', '0003_alter_aluno_bio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aluno',
            old_name='criado_em',
            new_name='matriculado_em',
        ),
        migrations.AlterField(
            model_name='aluno',
            name='matriculado_em',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='aluno',
            name='email_institucional',
            field=models.EmailField(
                default='aluno@fepi.edu.br',
                max_length=254,
                validators=[aluno.models.validar_email_institucional],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aluno',
            name='cpf',
            field=models.CharField(default='', max_length=14),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aluno',
            name='endereco',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aluno',
            name='data_nascimento',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
            preserve_default=False,
        ),
    ]
