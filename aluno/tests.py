from django.test import TestCase
from django.urls import reverse

from .models import Aluno


class PaginasAlunoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.aluno = Aluno.objects.create(
            nome='Ana Silva',
            curso='Engenharia de Software',
            bio='Estudante e pesquisadora.',
        )

    def test_raiz_redireciona_para_lista(self):
        resposta = self.client.get('/')
        self.assertRedirects(resposta, reverse('alunos:lista'))

    def test_listar_alunos(self):
        resposta = self.client.get(reverse('alunos:lista'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.aluno.nome)
        self.assertTemplateUsed(resposta, 'lista.html')

    def test_detalhe_renderiza_aluno(self):
        resposta = self.client.get(reverse('alunos:detalhe', args=[self.aluno.pk]))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.aluno.curso)
        self.assertTemplateUsed(resposta, 'detalhe.html')

    def test_criar_aluno_get(self):
        resposta = self.client.get(reverse('alunos:criar_aluno'))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'form_aluno.html')

    def test_criar_aluno_post(self):
        resposta = self.client.post(
            reverse('alunos:criar_aluno'),
            {'nome': 'Carlos Lima', 'curso': 'Direito', 'bio': 'Aluno.'},
        )
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.assertTrue(Aluno.objects.filter(nome='Carlos Lima').exists())

    def test_editar_aluno_get(self):
        resposta = self.client.get(reverse('alunos:editar_aluno', args=[self.aluno.pk]))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.aluno.nome)
        self.assertTemplateUsed(resposta, 'form_aluno.html')

    def test_editar_aluno_post(self):
        resposta = self.client.post(
            reverse('alunos:editar_aluno', args=[self.aluno.pk]),
            {'nome': 'Ana Souza', 'curso': 'Medicina', 'bio': 'Bio atualizada.'},
        )
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.nome, 'Ana Souza')
        self.assertEqual(self.aluno.curso, 'Medicina')

    def test_excluir_aluno_get(self):
        resposta = self.client.get(reverse('alunos:excluir_aluno', args=[self.aluno.pk]))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.aluno.nome)
        self.assertTemplateUsed(resposta, 'confirmar_exclusao.html')

    def test_excluir_aluno_post(self):
        resposta = self.client.post(reverse('alunos:excluir_aluno', args=[self.aluno.pk]))
        self.assertRedirects(resposta, reverse('alunos:lista'))
        self.assertFalse(Aluno.objects.filter(pk=self.aluno.pk).exists())
