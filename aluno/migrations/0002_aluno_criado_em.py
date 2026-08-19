import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('aluno', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='criado_em',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
            ),
        ),
    ]
