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

    def test_lista_renderiza_aluno(self):
        resposta = self.client.get(reverse('alunos:lista'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.aluno.nome)
        self.assertTemplateUsed(resposta, 'lista.html')

    def test_detalhe_renderiza_aluno(self):
        resposta = self.client.get(
            reverse('alunos:detalhe', args=[self.aluno.pk])
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.aluno.curso)
        self.assertTemplateUsed(resposta, 'detalhe.html')

# Create your tests here.
