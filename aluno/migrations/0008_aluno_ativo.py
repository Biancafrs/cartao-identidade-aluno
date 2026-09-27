from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('aluno', '0007_finalizar_relacao_aluno_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
