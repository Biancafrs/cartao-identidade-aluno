# Entrega da semana 1

Data da verificação final: **27/09/2026**  
Prazo informado: **30/09/2026**  
Repositório: <https://github.com/Biancafrs/cartao-identidade-aluno>

## Evidências técnicas

- `python manage.py check`: nenhum problema identificado.
- `python manage.py makemigrations --check --dry-run`: nenhuma alteração faltando.
- `python manage.py migrate`: nenhuma migration pendente.
- `python manage.py test`: 24 testes aprovados.
- Migração validada em banco vazio e a partir de `aluno.0004` com alunos existentes.
- Dados anteriores comparados antes/depois da migração, sem perda de IDs ou campos.
- `popular_demo` executado duas vezes sem duplicar seus registros.
- Dashboard inspecionado em 1440 px e 500 px; o ajuste responsivo foi conferido visualmente.

## Prints

![Dashboard em desktop](dashboard.png)

![Dashboard em tela estreita](dashboard-mobile.png)

## Checklist

- [x] Ambiente instalado e execução documentada.
- [x] Quatro models próprios: Aluno, Curso, Disciplina e Turma.
- [x] Relação 1:N Curso → Aluno implementada e demonstrável.
- [x] Migrations versionadas e aplicáveis em banco vazio e existente.
- [x] Cadastros anteriores preservados na migração.
- [x] Dashboard servido na raiz `/`.
- [x] Indicadores calculados com dados persistidos e atualizados após alterações.
- [x] Dashboard vazio tratado e apresentação responsiva conferida.
- [x] CRUD, detalhe, busca, filtro e validações preservados.
- [x] Verificações e 24 testes executados com sucesso.
- [x] Dados de demonstração reproduzíveis sem versionar o SQLite.
- [x] README, diagrama e instruções atualizados.
- [x] Prints da funcionalidade salvos e incluídos na entrega.
- [x] Checklist preenchido com base no que foi verificado.
- [ ] Nome e participação do segundo integrante conferidos.
- [x] Alterações funcionais e documentação separadas em commits.
- [x] Tag anotada `semana-1` publicada no commit correto.
- [ ] Link do repositório, tag, print e checklist enviados ao professor.

## Integrantes

- Bianca Ferreira — confirmada pelo histórico do repositório.
- Segundo integrante — **nome e participação pendentes de confirmação**.

Os itens de publicação serão marcados somente depois da confirmação no GitHub. O envio ao professor depende do canal definido pela disciplina e não pode ser comprovado pelo repositório.
