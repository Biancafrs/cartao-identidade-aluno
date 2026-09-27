from django.db import migrations


def migrar_cursos(apps, schema_editor):
    Aluno = apps.get_model('aluno', 'Aluno')
    Curso = apps.get_model('aluno', 'Curso')
    banco = schema_editor.connection.alias

    cursos_invalidos = list(
        Aluno.objects.using(banco)
        .filter(curso_novo__isnull=True)
        .values_list('id', 'curso')
    )
    cursos_invalidos = [
        (aluno_id, nome) for aluno_id, nome in cursos_invalidos
        if not nome or not nome.strip()
    ]
    if cursos_invalidos:
        ids = ', '.join(str(aluno_id) for aluno_id, _ in cursos_invalidos)
        raise RuntimeError(
            f'Alunos com curso vazio ou apenas espaços: {ids}. '
            'Corrija os dados antes de aplicar esta migration.'
        )

    for aluno in Aluno.objects.using(banco).filter(curso_novo__isnull=True).iterator():
        curso, _ = Curso.objects.using(banco).get_or_create(nome=aluno.curso)
        aluno.curso_novo_id = curso.pk
        aluno.save(update_fields=['curso_novo'], using=banco)

    if Aluno.objects.using(banco).filter(curso_novo__isnull=True).exists():
        raise RuntimeError('Nem todos os alunos foram vinculados a um curso.')


def reverter_cursos(apps, schema_editor):
    Aluno = apps.get_model('aluno', 'Aluno')
    banco = schema_editor.connection.alias

    for aluno in Aluno.objects.using(banco).select_related('curso_novo').iterator():
        if aluno.curso_novo_id:
            aluno.curso = aluno.curso_novo.nome
            aluno.curso_novo_id = None
            aluno.save(update_fields=['curso', 'curso_novo'], using=banco)


class Migration(migrations.Migration):
    dependencies = [
        ('aluno', '0005_modelagem_academica_e_curso_temporario'),
    ]

    operations = [
        migrations.RunPython(migrar_cursos, reverter_cursos),
    ]
