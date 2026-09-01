from django.db import migrations


def remover_mascara_dos_cpfs(apps, schema_editor):
    Aluno = apps.get_model('aluno', 'Aluno')

    for aluno in Aluno.objects.all().only('pk', 'cpf'):
        cpf_sem_mascara = ''.join(
            caractere for caractere in aluno.cpf if caractere.isdigit()
        )
        if cpf_sem_mascara != aluno.cpf:
            Aluno.objects.filter(pk=aluno.pk).update(cpf=cpf_sem_mascara)


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0006_alter_aluno_cpf'),
    ]

    operations = [
        migrations.RunPython(remover_mascara_dos_cpfs, migrations.RunPython.noop),
    ]
