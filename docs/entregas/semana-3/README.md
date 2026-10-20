# Entrega da semana 3

Tag prevista: `semana-3`.

## Checklist

- [x] Seis models de domínio: `Aluno`, `Curso`, `Disciplina`, `Turma`, `CarteiraAcademica` e `InscricaoTurma`.
- [x] Três relações 1:N preexistentes preservadas: `Curso → Aluno`, `Curso → Disciplina` e `Disciplina → Turma`.
- [x] `CarteiraAcademica.aluno` usa `OneToOneField`; a carteira é cadastrada, editada, persistida e exibida junto aos detalhes do aluno com dados do banco.
- [x] `Aluno.turmas` usa `ManyToManyField` com `through=InscricaoTurma`; a associação guarda data e situação, impede duplicação do par aluno/turma e aparece no detalhe do aluno.
- [x] CRUD 2 de `Curso`: cadastro, listagem, edição e exclusão com confirmação. Cursos com alunos ou disciplinas vinculados são protegidos.
- [x] Quatro formulários `ModelForm`: aluno, curso, carteira e inscrição em turma.
- [x] Migração `0010` aplicada no SQLite local; os quatro alunos, dois cursos, duas disciplinas e duas turmas existentes foram preservados.
- [x] Dashboard e primeiro CRUD continuam funcionais.
- [x] 39 testes aprovados com Python 3.14.8 e Django 6.1; `manage.py check` e `makemigrations --check --dry-run` aprovados.
- [x] Fluxo do CRUD de cursos, carteira, inscrição e dashboard conferido no navegador com dados fictícios.
- [ ] Registrar os commits e publicar a tag `semana-3`.
- [ ] Confirmar com o professor a divergência de prazo descrita abaixo.

## Prints

Os prints foram capturados em um banco de teste com dados fictícios. Os registros locais do projeto não foram usados nas imagens.

| Funcionalidade | Evidência |
| --- | --- |
| CRUD 2 — listagem | [Cursos cadastrados](cursos-listagem.png) |
| CRUD 2 — cadastro | [Formulário de novo curso](cursos-cadastro.png) |
| CRUD 2 — edição | [Formulário preenchido](cursos-edicao.png) |
| CRUD 2 — exclusão | [Confirmação de exclusão](cursos-exclusao.png) |
| Relacionamento 1:1 | [Carteira acadêmica nos detalhes do aluno](aluno-relacionamentos.png) |
| Relacionamento N:N | [Inscrição exibida no detalhe do aluno](aluno-relacionamentos.png) e [formulário de inscrição](inscricao-cadastro.png) |

## Como conferir

Instale as dependências e aplique as migrações:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test aluno
python manage.py runserver
```

Abra `/cursos/` para criar, listar, editar e excluir um curso sem alunos ou disciplinas vinculados. Abra `/aluno/` e escolha um aluno: a carteira aparece nos detalhes, com a opção de cadastrar ou editar seus dados; “Nova inscrição” associa o aluno a uma turma. Se o banco estiver vazio, execute `python manage.py popular_demo` para inserir dados fictícios.

## Prazo

O documento da disciplina informa aulas em **20/10 e 21/10**, mas registra **07/10/2026** como prazo da Semana 3. A data correta precisa ser confirmada com o professor.
