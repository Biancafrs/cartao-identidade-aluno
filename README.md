# Cartao de Identidade Academica

Projeto desenvolvido com Django para exibir cartoes de identidade academica dos alunos da FEPI.

## Requisitos Atendidos

- Uso do framework Django.
- Modelo `Aluno` com os campos obrigatorios:
  - `nome`: `CharField`
  - `curso`: `CharField`
  - `bio`: `TextField` com limite de 280 caracteres
- Front-end exibindo os cartoes dos alunos.
- Pagina de listagem dos alunos.
- Pagina de detalhes de cada aluno.
- Cadastro e gerenciamento pelo Django Admin.
- Identidade visual com cores azul e amarelo da FEPI.
- Favicon e logo da FEPI nos arquivos estaticos.

## Tecnologias

- Python 3.12
- Django 6.1
- SQLite
- HTML
- CSS

## Como Instalar e Executar

Clone o repositorio:

```bash
git clone LINK_DO_REPOSITORIO
cd cartao-identidade-aluno
```

Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute as migracoes:

```bash
python manage.py migrate
```

Crie um usuario administrador:

```bash
python manage.py createsuperuser
```

Inicie o servidor:

```bash
python manage.py runserver
```

Acesse no navegador:

```text
http://127.0.0.1:8000/
```

## Endpoints Disponiveis

| Endpoint       | Descricao                                    |
| -------------- | -------------------------------------------- |
| `/`            | Redireciona para a lista de alunos           |
| `/aluno/`      | Lista todos os cartoes de alunos cadastrados |
| `/aluno/<id>/` | Exibe os detalhes de um aluno especifico     |
| `/admin/`      | Area administrativa do Django                |

## Modelo de Dados

```python
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    bio = models.TextField(max_length=280)
    criado_em = models.DateTimeField(default=timezone.now, editable=False)
```

## Como Cadastrar Alunos

1. Acesse `http://127.0.0.1:8000/admin/`.
2. Entre com o usuario administrador.
3. Clique em `Alunos`.
4. Cadastre `nome`, `curso` e `bio`.
5. Salve o registro.
6. Acesse `/aluno/` para visualizar os cartoes.

## Prints ou Demonstracao

Adicione aqui os prints, GIF ou video curto demonstrando o funcionamento do projeto.

Sugestao de evidencias:

- Tela inicial com a lista de cartoes.
- Tela de detalhes de um aluno.
- Tela do Django Admin com alunos cadastrados.

Exemplo:

```markdown
![Lista de alunos](docs/prints/lista-alunos.png)
![Detalhe do aluno](docs/prints/detalhe-aluno.png)
```

## Observacao Sobre Uso de IA

Ferramentas de IA foram usadas de forma moderada para apoio e aprendizagem do desenvolvimento front-end.
