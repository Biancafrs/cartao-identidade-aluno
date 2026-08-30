# Cartao de Identidade Academica

Projeto desenvolvido com Django para exibir cartoes de identidade academica dos alunos da FEPI.

## Requisitos Atendidos

- Uso do framework Django.
- Modelo `Aluno` com oito campos obrigatórios.
- Data e hora da matrícula registradas automaticamente.
- Validação de e-mail institucional `@fepi.edu.br`.
- Busca por nome ou CPF e filtro por curso.
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
    matriculado_em = models.DateTimeField(auto_now_add=True)
    email_institucional = models.EmailField()
    cpf = models.CharField(max_length=14)
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField()
```

## Como Cadastrar Alunos

1. Acesse `http://127.0.0.1:8000/admin/`.
2. Entre com o usuario administrador.
3. Clique em `Alunos`.
4. Preencha os campos obrigatórios do aluno.
5. Salve o registro.
6. Acesse `/aluno/` para visualizar os cartoes.

## Prints do projeto

<img width="1886" height="847" alt="image" src="https://github.com/user-attachments/assets/9989f783-c2ce-4028-a0a7-7ece3a4b8ccd" />

<img width="1886" height="847" alt="image" src="https://github.com/user-attachments/assets/84c7fc61-9707-4643-b4e7-b5f3b7f8cf53" />

<img width="1886" height="847" alt="image" src="https://github.com/user-attachments/assets/9d9923bc-4aea-42da-8ab3-6e733cff455c" />


## Observacao Sobre Uso de IA

Ferramentas de IA foram usadas de forma moderada para apoio e aprendizagem do desenvolvimento front-end.
