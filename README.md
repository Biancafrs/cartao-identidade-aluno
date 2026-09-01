# Cartao de Identidade Academica

Projeto desenvolvido com Django para exibir cartoes de identidade academica dos alunos da FEPI.

## Requisitos Atendidos

- Uso do framework Django.
- Modelo `Aluno` com dez campos.
- Pelo menos cinco campos de texto, um campo numerico, campos de data/data-hora e um campo booleano.
- Data e hora da matrícula registradas automaticamente.
- Validação de e-mail institucional `@fepi.edu.br`.
- Busca por nome e filtro por curso.
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

### Windows

Crie e ative o ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instale as dependencias e inicie o projeto:

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Linux

Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependencias e inicie o projeto:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Crie um usuario administrador, se necessario:

```bash
python manage.py createsuperuser
```

Acesse no navegador:

```text
http://127.0.0.1:8000/
```

## Endpoints Disponiveis

| Endpoint               | Descricao                                    |
| ---------------------- | -------------------------------------------- |
| `/aluno/`              | Lista todos os cartoes de alunos cadastrados |
| `/aluno/novo/`         | Exibe o formulario para cadastrar aluno      |
| `/aluno/<id>/`         | Exibe os detalhes de um aluno especifico     |
| `/aluno/<id>/editar/`  | Exibe o formulario para editar aluno         |
| `/aluno/<id>/excluir/` | Exibe a confirmacao para excluir aluno       |
| `/admin/`              | Area administrativa do Django                |

## Modelo de Dados

```python
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    periodo = models.PositiveSmallIntegerField(default=1)
    bio = models.TextField(max_length=280)
    matriculado_em = models.DateTimeField(auto_now_add=True)
    email_institucional = models.EmailField(max_length=254)
    cpf = models.CharField(max_length=14)
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
```

Campos do model:

| Campo                 | Tipo                        | Finalidade                                                         |
| --------------------- | --------------------------- | ------------------------------------------------------------------ |
| `nome`                | `CharField`                 | Nome do aluno                                                      |
| `curso`               | `CharField`                 | Curso do aluno                                                     |
| `periodo`             | `PositiveSmallIntegerField` | Periodo atual do aluno                                             |
| `bio`                 | `TextField`                 | Breve biografia, limitada a 280 caracteres                         |
| `matriculado_em`      | `DateTimeField`             | Data e hora da matricula, preenchida automaticamente               |
| `email_institucional` | `EmailField`                | E-mail institucional do aluno, validado com dominio `@fepi.edu.br` |
| `cpf`                 | `CharField`                 | CPF do aluno, validado no formato `000.000.000-00`                 |
| `endereco`            | `CharField`                 | Endereco do aluno                                                  |
| `data_nascimento`     | `DateField`                 | Data de nascimento do aluno                                        |
| `ativo`               | `BooleanField`              | Indica se o cadastro esta ativo                                    |

O model tambem possui:

- `cpf_mascarado`: propriedade usada para exibir o CPF parcialmente oculto nas telas publicas.
- `Meta`: configura a ordenacao padrao por nome e os nomes exibidos no Django Admin.

## Como Cadastrar, Editar e Excluir Alunos

Pela interface do sistema:

1. Acesse `http://127.0.0.1:8000/aluno/`.
2. Clique em `Novo aluno`.
3. Preencha os dados do aluno.
4. Salve o cadastro para voltar para a lista de cartoes.
5. Para alterar um cadastro, clique no icone de editar no cartao do aluno.
6. Para remover um cadastro, clique no icone de excluir no cartao do aluno e confirme a exclusao.

Pelo Django Admin:

1. Acesse `http://127.0.0.1:8000/admin/`.
2. Entre com o usuario administrador.
3. Clique em `Alunos`.
4. Cadastre, edite ou exclua os registros pela area administrativa.

## Prints do projeto

<img width="1886" height="847" alt="image" src="https://github.com/user-attachments/assets/9989f783-c2ce-4028-a0a7-7ece3a4b8ccd" />

<img width="1886" height="847" alt="image" src="https://github.com/user-attachments/assets/84c7fc61-9707-4643-b4e7-b5f3b7f8cf53" />

<img width="1886" height="847" alt="image" src="https://github.com/user-attachments/assets/9d9923bc-4aea-42da-8ab3-6e733cff455c" />

## Observacao Sobre Uso de IA

Ferramentas de IA foram usadas de forma moderada para apoio e aprendizagem do desenvolvimento front-end.
