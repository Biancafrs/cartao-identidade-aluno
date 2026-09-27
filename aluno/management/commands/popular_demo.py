from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from aluno.models import Aluno, Curso, Disciplina, Turma


class Command(BaseCommand):
    help = 'Cria ou atualiza dados fictícios para demonstração sem apagar registros.'

    @transaction.atomic
    def handle(self, *args, **options):
        cursos = {}
        for nome in ('Administração', 'Engenharia de Software'):
            curso, _ = Curso.objects.update_or_create(
                nome=nome,
                defaults={'ativo': True},
            )
            cursos[nome] = curso

        disciplinas_config = (
            {
                'codigo': 'ADM-DEMO-001',
                'nome': 'Fundamentos de Administração',
                'carga_horaria': 60,
                'curso': cursos['Administração'],
            },
            {
                'codigo': 'ES-DEMO-001',
                'nome': 'Programação Web',
                'carga_horaria': 80,
                'curso': cursos['Engenharia de Software'],
            },
        )
        disciplinas = {}
        for dados in disciplinas_config:
            codigo = dados['codigo']
            disciplina, _ = Disciplina.objects.update_or_create(
                codigo=codigo,
                defaults={chave: valor for chave, valor in dados.items() if chave != 'codigo'},
            )
            disciplinas[codigo] = disciplina

        turmas_config = (
            {
                'codigo': 'ADM-DEMO-2026-1',
                'ano': 2026,
                'semestre': 1,
                'disciplina': disciplinas['ADM-DEMO-001'],
            },
            {
                'codigo': 'ES-DEMO-2026-1',
                'ano': 2026,
                'semestre': 1,
                'disciplina': disciplinas['ES-DEMO-001'],
            },
        )
        for dados in turmas_config:
            Turma.objects.update_or_create(
                codigo=dados['codigo'],
                defaults={chave: valor for chave, valor in dados.items() if chave != 'codigo'},
            )

        alunos_config = (
            {
                'nome': 'Ana Martins',
                'email_institucional': 'ana.demo@fepi.edu.br',
                'cpf': '111.111.111-11',
                'endereco': 'Rua Acadêmica, 101',
                'data_nascimento': date(2002, 3, 12),
                'bio': 'Estudante de Administração.',
                'curso': cursos['Administração'],
                'ativo': True,
            },
            {
                'nome': 'Bruno Almeida',
                'email_institucional': 'bruno.demo@fepi.edu.br',
                'cpf': '222.222.222-22',
                'endereco': 'Rua Acadêmica, 202',
                'data_nascimento': date(2001, 7, 25),
                'bio': 'Estudante de Administração.',
                'curso': cursos['Administração'],
                'ativo': False,
            },
            {
                'nome': 'Carla Oliveira',
                'email_institucional': 'carla.demo@fepi.edu.br',
                'cpf': '333.333.333-33',
                'endereco': 'Avenida Universitária, 303',
                'data_nascimento': date(2003, 1, 8),
                'bio': 'Estudante de Engenharia de Software.',
                'curso': cursos['Engenharia de Software'],
                'ativo': True,
            },
            {
                'nome': 'Diego Santos',
                'email_institucional': 'diego.demo@fepi.edu.br',
                'cpf': '444.444.444-44',
                'endereco': 'Avenida Universitária, 404',
                'data_nascimento': date(2002, 11, 19),
                'bio': 'Estudante de Engenharia de Software.',
                'curso': cursos['Engenharia de Software'],
                'ativo': True,
            },
        )
        for dados in alunos_config:
            email = dados['email_institucional']
            aluno = Aluno.objects.filter(email_institucional=email).order_by('pk').first()
            if aluno is None:
                Aluno.objects.create(**dados)
                continue

            for campo, valor in dados.items():
                setattr(aluno, campo, valor)
            aluno.save(update_fields=tuple(dados))

        self.stdout.write(
            self.style.SUCCESS(
                'Dados de demonstração prontos: 2 cursos, 2 disciplinas, '
                '2 turmas e 4 alunos identificados por e-mail.'
            )
        )
