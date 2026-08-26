from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import AlunoForm
from .models import Aluno


class PaginasAlunoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.aluno = Aluno.objects.create(
            nome='Ana Silva',
            curso='Engenharia de Software',
            bio='Estudante e pesquisadora.',
            email_institucional='ana@fepi.edu.br',
            cpf='123.456.789-00',
            endereco='Rua das Flores, 10',
            data_nascimento=date(2000, 5, 20),
        )
        cls.outro_aluno = Aluno.objects.create(
            nome='Bruno Souza',
            curso='Direito',
            bio='Estudante de Direito.',
            email_institucional='bruno@fepi.edu.br',
            cpf='987.654.321-00',
            endereco='Avenida Central, 20',
            data_nascimento=date(1999, 8, 10),
        )

    def dados_validos(self, **alteracoes):
        dados = {
            'nome': 'Carlos Lima',
            'curso': 'Medicina',
            'bio': 'Aluno.',
            'email_institucional': 'carlos@fepi.edu.br',
            'cpf': '111.222.333-44',
            'endereco': 'Rua Principal, 30',
            'data_nascimento': '2001-03-15',
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

    def test_formulario_rejeita_campo_obrigatorio_ausente(self):
        resposta = self.client.post(reverse('alunos:criar_aluno'), self.dados_validos(cpf=''))
        self.assertEqual(resposta.status_code, 200)
        self.assertFormError(resposta.context['form'], 'cpf', 'Este campo é obrigatório.')

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
        self.assertContains(resposta, self.aluno.cpf)
        self.assertContains(resposta, self.aluno.endereco)

    def test_editar_aluno(self):
        resposta = self.client.post(
            reverse('alunos:editar_aluno', args=[self.aluno.pk]),
            self.dados_validos(nome='Ana Souza', email_institucional='ana@fepi.edu.br'),
        )
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.nome, 'Ana Souza')

    def test_excluir_aluno(self):
        resposta = self.client.post(reverse('alunos:excluir_aluno', args=[self.aluno.pk]))
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.assertFalse(Aluno.objects.filter(pk=self.aluno.pk).exists())
