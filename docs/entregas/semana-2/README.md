# Entrega da semana 2 — CRUD de alunos

Tag prevista: `semana-2`.

## Checklist

- [x] Listagem consulta os alunos do banco e mostra acesso a cadastro, detalhes, edição e exclusão.
- [x] Cadastro usa `AlunoForm` (`ModelForm`), valida os campos e persiste o novo aluno.
- [x] Edição carrega os dados existentes, valida, atualiza o mesmo registro e não duplica alunos.
- [x] Exclusão identifica o aluno, apresenta confirmação e só remove após envio por `POST`.
- [x] Sucesso e erros de validação são informados na interface; mensagens de sucesso desaparecem após cinco segundos.
- [x] Relação com `Curso`, dashboard, busca, filtros e detalhes permanecem funcionais.
- [x] Persistência verificada por testes com banco SQLite de teste; 31 testes aprovados.
- [x] Fluxo completo executado no navegador com banco temporário: 4 alunos iniciais, 5 após cadastro, 5 após edição e 4 após exclusão; dashboard atualizado.
- [x] `manage.py check`, `makemigrations --check --dry-run` e `git diff --check` aprovados.
- [ ] Criar os commits, a tag `semana-2` e publicar a tag.

Os testes foram executados com Python 3.10.12 e Django 5.2.18. O `requirements.txt` declara Django 6.1; a validação nessa versão permanece pendente.

## Prints

As imagens foram capturadas no navegador com dados fictícios gerados pelo comando `popular_demo` em um banco de teste.

| Operação | Evidência |
| --- | --- |
| Listagem | [Print da listagem](listagem.png) |
| Cadastro | [Print do formulário de cadastro](cadastro.png) |
| Edição | [Print do formulário preenchido para edição](edicao.png) |
| Exclusão | [Print da confirmação de exclusão](exclusao.png) |

As ações concluídas e suas mensagens também estão registradas nos prints de [cadastro realizado](cadastro-sucesso.png), [edição realizada](edicao-sucesso.png) e [exclusão realizada](exclusao-sucesso.png).

## Como conferir

No ambiente virtual do projeto, execute:

```bash
python manage.py migrate
python manage.py test aluno
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` para conferir o dashboard e `http://127.0.0.1:8000/aluno/` para conferir a listagem. Se o banco estiver vazio, cadastre um curso em `/admin/` ou execute `python manage.py popular_demo` para inserir dados fictícios. Na listagem, crie um aluno, abra sua edição para alterar e salvar os dados, consulte o detalhe e use o ícone de lixeira para abrir a confirmação de exclusão. Após cada ação, confira a mensagem e o resultado na listagem.

Após concluir e registrar a entrega em commit, a tag deve apontar para esse commit:

```bash
git tag -a semana-2 -m "Entrega semana 2"
git push origin semana-2
```
