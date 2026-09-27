import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('aluno', '0006_migrar_cursos_dos_alunos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='curso',
        ),
        migrations.RenameField(
            model_name='aluno',
            old_name='curso_novo',
            new_name='curso',
        ),
        migrations.AlterField(
            model_name='aluno',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alunos', to='aluno.curso'),
        ),
    ]
