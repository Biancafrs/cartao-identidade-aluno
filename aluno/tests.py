from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .forms import AlunoForm, CarteiraAcademicaForm, CursoForm, InscricaoTurmaForm
from .models import Aluno, CarteiraAcademica, Curso, Disciplina, InscricaoTurma, Turma


class PaginasAlunoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.curso_engenharia = Curso.objects.create(nome='Engenharia de Software')
        cls.curso_direito = Curso.objects.create(nome='Direito')
        cls.curso_medicina = Curso.objects.create(nome='Medicina')
        cls.aluno = Aluno.objects.create(
            nome='Ana Silva',
            curso=cls.curso_engenharia,
            periodo=4,
            bio='Estudante e pesquisadora.',
            email_institucional='ana@fepi.edu.br',
            cpf='123.456.789-00',
            endereco='Rua das Flores, 10',
            data_nascimento=date(2000, 5, 20),
        )
        cls.outro_aluno = Aluno.objects.create(
            nome='Bruno Souza',
            curso=cls.curso_direito,
            periodo=2,
            bio='Estudante de Direito.',
            email_institucional='bruno@fepi.edu.br',
            cpf='987.654.321-00',
            endereco='Avenida Central, 20',
            data_nascimento=date(1999, 8, 10),
        )

    def dados_validos(self, **alteracoes):
        dados = {
            'nome': 'Carlos Lima',
            'curso': self.curso_medicina.pk,
            'periodo': 1,
            'bio': 'Aluno.',
            'email_institucional': 'carlos@fepi.edu.br',
            'cpf': '111.222.333-44',
            'endereco': 'Rua Principal, 30',
            'data_nascimento': '2001-03-15',
            'ativo': 'on',
        }
        dados.update(alteracoes)
        return dados

    def test_matricula_e_preenchida_automaticamente(self):
        self.assertIsNotNone(self.aluno.matriculado_em)

    def test_email_precisa_ser_institucional(self):
        form = AlunoForm(data=self.dados_validos(email_institucional='carlos@gmail.com'))
        self.assertFalse(form.is_valid())
        self.assertIn('email_institucional', form.errors)

    def test_model_tambem_valida_dominio_do_email(self):
        self.aluno.email_institucional = 'ana@gmail.com'
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_criar_aluno_com_os_campos_obrigatorios(self):
        resposta = self.client.post(reverse('alunos:criar_aluno'), self.dados_validos())
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.assertTrue(Aluno.objects.filter(nome='Carlos Lima').exists())
        self.assertContains(self.client.get(reverse('alunos:lista')), 'Carlos Lima')

    def test_cadastro_exibe_mensagem_de_sucesso(self):
        resposta = self.client.post(
            reverse('alunos:criar_aluno'), self.dados_validos(), follow=True,
        )
        self.assertContains(resposta, 'Aluno Carlos Lima cadastrado com sucesso.')

    def test_formulario_rejeita_curso_inexistente(self):
        form = AlunoForm(data=self.dados_validos(curso=999999))
        self.assertFalse(form.is_valid())
        self.assertIn('curso', form.errors)

    def test_cpf_aceita_numeros_e_salva_sem_mascara(self):
        resposta = self.client.post(
            reverse('alunos:criar_aluno'),
            self.dados_validos(cpf='11122233344'),
        )

        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.assertEqual(Aluno.objects.get(nome='Carlos Lima').cpf, '11122233344')

    def test_cpf_colado_com_mascara_e_normalizado(self):
        resposta = self.client.post(
            reverse('alunos:criar_aluno'),
            self.dados_validos(cpf='111.222.333-44'),
        )

        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.assertEqual(Aluno.objects.get(nome='Carlos Lima').cpf, '11122233344')

    def test_cpf_rejeita_quantidade_incorreta(self):
        form = AlunoForm(data=self.dados_validos(cpf='111222333'))

        self.assertFalse(form.is_valid())
        self.assertIn('Informe os 11 números do CPF.', form.errors['cpf'])

    def test_modelo_normaliza_e_mascara_cpf(self):
        self.aluno.cpf = '123.456.789-00'
        self.aluno.save()
        self.aluno.refresh_from_db()

        self.assertEqual(self.aluno.cpf, '12345678900')
        self.assertEqual(self.aluno.cpf_formatado, '123.456.789-00')
        self.assertEqual(self.aluno.cpf_mascarado, '***.456.789-**')

    def test_formulario_rejeita_campo_obrigatorio_ausente(self):
        resposta = self.client.post(reverse('alunos:criar_aluno'), self.dados_validos(cpf=''))
        self.assertEqual(resposta.status_code, 200)
        self.assertFormError(resposta.context['form'], 'cpf', 'Este campo é obrigatório.')
        self.assertContains(resposta, 'Revise os campos destacados e tente novamente.')
        self.assertFalse(Aluno.objects.filter(nome='Carlos Lima').exists())

    def test_busca_por_nome(self):
        resposta = self.client.get(reverse('alunos:lista'), {'busca': 'Ana'})
        self.assertContains(resposta, 'Ana Silva')
        self.assertNotContains(resposta, 'Bruno Souza')

    def test_busca_por_cpf(self):
        resposta = self.client.get(reverse('alunos:lista'), {'busca': '987.654'})
        self.assertContains(resposta, 'Bruno Souza')
        self.assertNotContains(resposta, 'Ana Silva')

    def test_filtro_por_curso(self):
        resposta = self.client.get(reverse('alunos:lista'), {'curso': 'Direito'})
        self.assertContains(resposta, 'Bruno Souza')
        self.assertNotContains(resposta, 'Ana Silva')

    def test_busca_e_filtro_podem_ser_combinados(self):
        resposta = self.client.get(
            reverse('alunos:lista'),
            {'busca': 'Ana', 'curso': 'Direito'},
        )
        self.assertNotContains(resposta, 'Ana Silva')
        self.assertContains(resposta, 'Nenhum aluno encontrado')

    def test_detalhe_exibe_os_dados_do_aluno(self):
        resposta = self.client.get(reverse('alunos:detalhe', args=[self.aluno.pk]))
        self.assertContains(resposta, self.aluno.email_institucional)
        self.assertContains(resposta, self.aluno.cpf_mascarado)
        self.assertNotContains(resposta, self.aluno.cpf)
        self.assertContains(resposta, self.aluno.endereco)
        self.assertContains(resposta, '4º período')
        self.assertContains(resposta, 'Ativo')

    def test_editar_aluno(self):
        total_antes = Aluno.objects.count()
        resposta = self.client.post(
            reverse('alunos:editar_aluno', args=[self.aluno.pk]),
            self.dados_validos(nome='Ana Souza', email_institucional='ana@fepi.edu.br'),
            follow=True,
        )
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.nome, 'Ana Souza')
        self.assertEqual(Aluno.objects.count(), total_antes)
        self.assertContains(resposta, 'Aluno Ana Souza atualizado com sucesso.')

    def test_edicao_invalida_preserva_dados(self):
        resposta = self.client.post(
            reverse('alunos:editar_aluno', args=[self.aluno.pk]),
            self.dados_validos(nome='Nome inválido', cpf='123'),
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Revise os campos destacados e tente novamente.')
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.nome, 'Ana Silva')

    def test_edicao_exibe_data_de_nascimento_no_campo(self):
        resposta = self.client.get(reverse('alunos:editar_aluno', args=[self.aluno.pk]))

        self.assertContains(resposta, 'value="2000-05-20"')

    def test_excluir_aluno(self):
        resposta = self.client.post(
            reverse('alunos:excluir_aluno', args=[self.aluno.pk]), follow=True,
        )
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.assertFalse(Aluno.objects.filter(pk=self.aluno.pk).exists())
        self.assertContains(resposta, 'Aluno Ana Silva excluído com sucesso.')
        self.assertNotContains(resposta, 'Ana Silva</h3>')

    def test_exclusao_exige_confirmacao(self):
        resposta = self.client.get(reverse('alunos:excluir_aluno', args=[self.aluno.pk]))
        self.assertContains(resposta, 'Tem certeza de que deseja excluir')
        self.assertTrue(Aluno.objects.filter(pk=self.aluno.pk).exists())

    def test_curso_com_aluno_nao_pode_ser_excluido(self):
        with self.assertRaises(ProtectedError):
            self.curso_engenharia.delete()

    def test_edicao_mantem_curso_inativo_disponivel(self):
        self.curso_engenharia.ativo = False
        self.curso_engenharia.save(update_fields=['ativo'])

        form = AlunoForm(instance=self.aluno)

        self.assertIn(self.curso_engenharia, form.fields['curso'].queryset)
        self.assertNotIn(self.curso_engenharia, AlunoForm().fields['curso'].queryset)


class DashboardVazioTests(TestCase):
    def test_dashboard_vazio_exibe_zeros_e_orientacao(self):
        resposta = self.client.get(reverse('home'))

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['total'], 0)
        self.assertEqual(resposta.context['ativos'], 0)
        self.assertEqual(resposta.context['inativos'], 0)
        self.assertContains(resposta, 'Nenhum curso cadastrado')


class DashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.curso_direito = Curso.objects.create(nome='Direito')
        cls.curso_computacao = Curso.objects.create(nome='Computação')
        cls.disciplina = Disciplina.objects.create(
            nome='Algoritmos',
            codigo='COMP-001',
            carga_horaria=80,
            curso=cls.curso_computacao,
        )
        Turma.objects.create(
            codigo='COMP-001-2026-1',
            ano=2026,
            semestre=1,
            disciplina=cls.disciplina,
        )
        dados_aluno = {
            'bio': 'Aluno.',
            'cpf': '000.000.000-00',
            'endereco': 'Rua Acadêmica',
            'data_nascimento': date(2000, 1, 1),
        }
        cls.aluno_ativo = Aluno.objects.create(
            nome='Aluno Ativo',
            curso=cls.curso_computacao,
            email_institucional='ativo@fepi.edu.br',
            **dados_aluno,
        )
        cls.aluno_inativo = Aluno.objects.create(
            nome='Aluno Inativo',
            curso=cls.curso_computacao,
            email_institucional='inativo@fepi.edu.br',
            ativo=False,
            **dados_aluno,
        )

    def test_dashboard_exibe_totais_reais(self):
        resposta = self.client.get(reverse('home'))

        self.assertEqual(resposta.context['total'], 2)
        self.assertEqual(resposta.context['ativos'], 1)
        self.assertEqual(resposta.context['inativos'], 1)
        self.assertEqual(resposta.context['total_cursos'], 2)
        self.assertEqual(resposta.context['total_disciplinas'], 1)
        self.assertEqual(resposta.context['total_turmas'], 1)

    def test_dashboard_agrupa_alunos_e_inclui_curso_sem_alunos(self):
        resposta = self.client.get(reverse('home'))
        distribuicao = {
            curso.nome: curso.total_alunos for curso in resposta.context['cursos']
        }

        self.assertEqual(distribuicao, {'Computação': 2, 'Direito': 0})

    def test_dashboard_atualiza_apos_alteracao(self):
        self.aluno_inativo.ativo = True
        self.aluno_inativo.save(update_fields=['ativo'])

        resposta = self.client.get(reverse('home'))

        self.assertEqual(resposta.context['ativos'], 2)
        self.assertEqual(resposta.context['inativos'], 0)

    def test_dashboard_e_listagem_sao_telas_distintas(self):
        dashboard = self.client.get(reverse('home'))
        listagem = self.client.get(reverse('alunos:lista'))

        self.assertContains(dashboard, 'Dashboard acadêmico')
        self.assertNotContains(listagem, 'Dashboard acadêmico')


class PopularDemoTests(TestCase):
    def test_comando_cria_dados_esperados_em_banco_vazio(self):
        call_command('popular_demo', verbosity=0)

        self.assertEqual(Aluno.objects.count(), 4)
        self.assertEqual(Aluno.objects.filter(ativo=True).count(), 3)
        self.assertEqual(Aluno.objects.filter(ativo=False).count(), 1)
        self.assertEqual(Curso.objects.count(), 2)
        self.assertEqual(Disciplina.objects.count(), 2)
        self.assertEqual(Turma.objects.count(), 2)
        self.assertTrue(all(curso.alunos.count() == 2 for curso in Curso.objects.all()))

    def test_comando_e_idempotente(self):
        call_command('popular_demo', verbosity=0)
        primeira_execucao = (
            Aluno.objects.count(),
            Curso.objects.count(),
            Disciplina.objects.count(),
            Turma.objects.count(),
        )

        call_command('popular_demo', verbosity=0)

        self.assertEqual(
            primeira_execucao,
            (
                Aluno.objects.count(),
                Curso.objects.count(),
                Disciplina.objects.count(),
                Turma.objects.count(),
            ),
        )

    def test_dashboard_reflete_dados_populados(self):
        call_command('popular_demo', verbosity=0)

        resposta = self.client.get(reverse('home'))

        self.assertEqual(resposta.context['total'], 4)
        self.assertEqual(resposta.context['ativos'], 3)
        self.assertEqual(resposta.context['inativos'], 1)
        self.assertEqual(resposta.context['total_cursos'], 2)
        self.assertEqual(resposta.context['total_disciplinas'], 2)
        self.assertEqual(resposta.context['total_turmas'], 2)


class Semana3Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.curso = Curso.objects.create(nome='Ciência da Computação')
        cls.disciplina = Disciplina.objects.create(
            nome='Banco de Dados', codigo='CC-101', carga_horaria=60,
            curso=cls.curso,
        )
        cls.turma = Turma.objects.create(
            codigo='CC-101-A', ano=2026, semestre=2, disciplina=cls.disciplina,
        )
        cls.outra_turma = Turma.objects.create(
            codigo='CC-101-B', ano=2026, semestre=2, disciplina=cls.disciplina,
        )
        cls.aluno = Aluno.objects.create(
            nome='Ana Costa', curso=cls.curso, periodo=2, bio='Estudante.',
            email_institucional='ana.costa@fepi.edu.br', cpf='12345678901',
            endereco='Rua Central, 1', data_nascimento=date(2002, 4, 3),
        )
        cls.outro_aluno = Aluno.objects.create(
            nome='Bruno Costa', curso=cls.curso, periodo=2, bio='Estudante.',
            email_institucional='bruno.costa@fepi.edu.br', cpf='12345678902',
            endereco='Rua Central, 2', data_nascimento=date(2002, 5, 4),
        )

    def test_curso_crud_completo(self):
        self.assertTrue(issubclass(CursoForm, forms.ModelForm))
        resposta = self.client.post(reverse('cursos:criar'), {
            'nome': 'Matemática', 'ativo': 'on',
        }, follow=True)
        self.assertContains(resposta, 'Curso Matemática cadastrado com sucesso.')
        curso = Curso.objects.get(nome='Matemática')
        self.assertContains(self.client.get(reverse('cursos:lista')), 'Matemática')
        resposta = self.client.get(reverse('cursos:editar', args=[curso.pk]))
        self.assertContains(resposta, 'value="Matemática"')
        self.client.post(reverse('cursos:editar', args=[curso.pk]), {
            'nome': 'Matemática Aplicada', 'ativo': 'on',
        })
        curso.refresh_from_db()
        self.assertEqual(curso.nome, 'Matemática Aplicada')
        self.assertEqual(Curso.objects.filter(pk=curso.pk).count(), 1)
        self.client.get(reverse('cursos:excluir', args=[curso.pk]))
        self.assertTrue(Curso.objects.filter(pk=curso.pk).exists())
        resposta = self.client.post(reverse('cursos:excluir', args=[curso.pk]), follow=True)
        self.assertContains(resposta, 'Curso Matemática Aplicada excluído com sucesso.')
        self.assertFalse(Curso.objects.filter(pk=curso.pk).exists())

    def test_curso_com_dependencias_nao_e_excluido(self):
        resposta = self.client.get(reverse('cursos:excluir', args=[self.curso.pk]))
        self.assertContains(resposta, 'Remova esses vínculos antes de excluir')
        resposta = self.client.post(
            reverse('cursos:excluir', args=[self.curso.pk]), follow=True,
        )
        self.assertContains(resposta, 'Não é possível excluir um curso')
        self.assertTrue(Curso.objects.filter(pk=self.curso.pk).exists())

    def test_carteira_um_para_um_e_tela_com_dados_reais(self):
        self.assertTrue(issubclass(CarteiraAcademicaForm, forms.ModelForm))
        self.assertIsNone(CarteiraAcademica.objects.filter(aluno=self.aluno).first())
        resposta = self.client.get(reverse('alunos:detalhe', args=[self.aluno.pk]))
        self.assertContains(resposta, 'ainda não possui carteira')
        self.assertContains(resposta, 'Cadastrar carteira')
        dados = {
            'numero': 'FEPI-2026-001', 'emitida_em': '2026-02-01',
            'valida_ate': '2027-02-01',
        }
        resposta = self.client.post(
            reverse('alunos:editar_carteira', args=[self.aluno.pk]),
            dados, follow=True,
        )
        self.assertContains(resposta, 'FEPI-2026-001')
        self.assertContains(resposta, '01/02/2027')
        self.assertContains(resposta, 'Editar carteira')
        carteira = self.aluno.carteira
        self.assertEqual(carteira.numero, 'FEPI-2026-001')
        dados['numero'] = 'FEPI-2026-002'
        self.client.post(reverse('alunos:editar_carteira', args=[self.aluno.pk]), dados)
        carteira.refresh_from_db()
        self.assertEqual(carteira.numero, 'FEPI-2026-002')
        self.assertEqual(CarteiraAcademica.objects.filter(aluno=self.aluno).count(), 1)
        segunda = CarteiraAcademica(
            aluno=self.aluno, numero='OUTRA',
            emitida_em=date(2026, 2, 1), valida_ate=date(2027, 2, 1),
        )
        with self.assertRaises(ValidationError):
            segunda.full_clean()

    def test_rota_antiga_da_carteira_aponta_para_o_detalhe(self):
        resposta = self.client.get(reverse('alunos:carteira_aluno', args=[self.aluno.pk]))
        self.assertRedirects(
            resposta,
            f"{reverse('alunos:detalhe', args=[self.aluno.pk])}#carteira",
        )

    def test_carteira_rejeita_validade_anterior_a_emissao(self):
        resposta = self.client.post(reverse('alunos:editar_carteira', args=[self.aluno.pk]), {
            'numero': 'INVALIDA', 'emitida_em': '2026-02-01',
            'valida_ate': '2026-01-01',
        })
        self.assertContains(resposta, 'A validade deve ser igual ou posterior à emissão.')
        self.assertFalse(CarteiraAcademica.objects.filter(aluno=self.aluno).exists())

    def test_inscricao_through_guarda_dados_extras_e_aparece_no_detalhe(self):
        self.assertTrue(issubclass(InscricaoTurmaForm, forms.ModelForm))
        self.assertEqual(Aluno._meta.get_field('turmas').remote_field.through, InscricaoTurma)
        resposta = self.client.post(
            reverse('alunos:inscrever_turma', args=[self.aluno.pk]),
            {'turma': self.turma.pk, 'inscrito_em': '2026-10-20', 'situacao': 'ATIVA'},
            follow=True,
        )
        self.assertContains(resposta, self.turma.codigo)
        self.assertContains(resposta, '20/10/2026')
        inscricao = InscricaoTurma.objects.get(aluno=self.aluno, turma=self.turma)
        self.assertEqual(inscricao.situacao, InscricaoTurma.Situacao.ATIVA)
        self.assertEqual(inscricao.inscrito_em, date(2026, 10, 20))
        self.assertIn(self.turma, self.aluno.turmas.all())

        InscricaoTurma.objects.create(aluno=self.aluno, turma=self.outra_turma)
        InscricaoTurma.objects.create(aluno=self.outro_aluno, turma=self.turma)
        self.assertEqual(self.aluno.turmas.count(), 2)
        self.assertEqual(self.turma.alunos.count(), 2)

        duplicada = self.client.post(reverse('alunos:inscrever_turma', args=[self.aluno.pk]), {
            'turma': self.turma.pk, 'inscrito_em': '2026-10-20', 'situacao': 'ATIVA',
        })
        self.assertEqual(duplicada.status_code, 200)
        self.assertEqual(InscricaoTurma.objects.filter(
            aluno=self.aluno, turma=self.turma,
        ).count(), 1)

    def test_dashboard_e_primeiro_crud_continuam_funcionando(self):
        self.assertContains(self.client.get(reverse('home')), 'Dashboard acadêmico')
        self.assertContains(self.client.get(reverse('alunos:lista')), self.aluno.nome)
        self.assertContains(self.client.get(reverse('alunos:detalhe', args=[self.aluno.pk])), 'Inscrições em turmas')

    def test_exclusao_de_aluno_remove_carteira_e_inscricao(self):
        CarteiraAcademica.objects.create(
            aluno=self.aluno, numero='FEPI-TESTE',
            emitida_em=date(2026, 2, 1), valida_ate=date(2027, 2, 1),
        )
        InscricaoTurma.objects.create(aluno=self.aluno, turma=self.turma)
        resposta = self.client.post(reverse('alunos:excluir_aluno', args=[self.aluno.pk]))
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.assertFalse(Aluno.objects.filter(pk=self.aluno.pk).exists())
        self.assertFalse(CarteiraAcademica.objects.filter(aluno_id=self.aluno.pk).exists())
        self.assertFalse(InscricaoTurma.objects.filter(aluno_id=self.aluno.pk).exists())
        self.assertTrue(Curso.objects.filter(pk=self.curso.pk).exists())
        self.assertTrue(Turma.objects.filter(pk=self.turma.pk).exists())
