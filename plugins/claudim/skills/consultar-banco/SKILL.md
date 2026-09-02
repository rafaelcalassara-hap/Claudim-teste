---
name: consultar-banco
description: Como usar o Prisma sobre SQLite neste stack — o banco é um arquivo do projeto, o que a aplicação pode escrever, tipos permitidos, dinheiro em centavos, teto de linhas, migração, e PII mascarada antes de sair do servidor. Use ao escrever qualquer consulta, alterar o schema.prisma ou rodar migração.
---

# Consultar o banco

Prisma sobre **SQLite**. O banco é o arquivo `prisma/dev.db`, dentro do próprio
projeto: sem conta, sem servidor, sem senha, nada no `.env`. O cliente é
`lib/db.ts` e só existe no servidor — arquivo com `"use client"` que importe
daqui quebra o build, e é para quebrar mesmo.

Consequências que mudam o que você escreve:

- **Nada de tipo nativo.** `@db.Decimal`, `@db.VarChar`, `@db.Uuid` e afins não
  existem no SQLite e o Prisma recusa o schema inteiro. Use os tipos do Prisma
  puros: `String`, `Int`, `Float`, `Boolean`, `DateTime`, `BigInt`, `Bytes`.
- **Dinheiro é `Int` em centavos.** SQLite não tem decimal; `19.90` guardado
  como número quebrado erra o arredondamento na soma. Divida por 100 só para
  mostrar na tela.
- **Sem `enum`.** SQLite não suporta. Use `String` e valide com zod.
- **Um escritor por vez.** Dá de sobra para uma aplicação interna na máquina de
  uma pessoa. Não é banco para muita gente gravando ao mesmo tempo — se o
  `PLANO.md` pedir isso, avise o usuário antes de construir.

## O que pode escrever, o que não pode

- **Tabelas do `prisma/schema.prisma`:** esta aplicação é dona delas. Pode
  `create`, `update`, `delete`.
- **Dado de sistema corporativo** (beneficiário, contrato, atendimento): a
  aplicação **não se conecta** ao banco da empresa. O SQLite é um arquivo local
  e não enxerga nada além dele.

Então de onde vem o dado corporativo? De um CSV exportado pelo time de dados e
importado para uma tabela desta aplicação. Isso significa duas coisas, e as
duas precisam ser ditas ao usuário: o dado é uma **cópia** com a data da
exportação, não o valor de agora; e a cópia mora no arquivo do projeto, então
CSV com CPF ou condição de saúde cai nas regras da skill `dados-sensiveis`
antes de ser importado.

Se a tarefa parece exigir consulta ao vivo no sistema corporativo, pare e diga
ao usuário: isso não existe nesta versão e passa pelo time de dados.

Toda escrita passa antes por `bancoConfigurado()` — que aqui é literalmente
"o arquivo `prisma/dev.db` existe". Se alguém apagou, gravar devolve a frase em
português e para, em vez de estourar. O recipe completo está em `next-padroes`.

## Como escrever a consulta

- **Sempre `take`.** Padrão 1000 na tela. Sem teto, uma tabela de fato derruba
  a página e o DBA aparece.
- **Sempre `select` explícito.** Sem ele o Prisma traz todas as colunas —
  inclusive a de CPF que você não pediu e que vai vazar no payload.
- Filtre por data no `where`, não em JavaScript. Trazer o ano inteiro para
  filtrar em memória é o erro clássico aqui.
- Agregou? Use `groupBy` / `aggregate` do Prisma. Somar 200 mil linhas no
  servidor Node é desperdício — o banco faz isso melhor, mesmo sendo arquivo.
- Precisou de SQL cru: `db.$queryRaw` com *template tag*
  (`` db.$queryRaw`SELECT ... WHERE mes = ${mes}` ``), que parametriza sozinho.
  Nunca `$queryRawUnsafe` com valor vindo do usuário.
- Nada de N+1: uma consulta dentro de `map` vira 200 consultas. Use `include`
  ou um `findMany` com `where: { id: { in: ids } }`.

## Schema e migração

- Alterou o `schema.prisma`? Rode `npx prisma migrate dev --name <o-que-mudou>`
  e faça commit da pasta `prisma/migrations/`.
- `prisma migrate reset` e `db push --force-reset` **apagam o banco**. O hook
  bloqueia, e com razão. Apagar o arquivo `.db` na mão é a mesma coisa, e o hook
  bloqueia também. Se a migração deu conflito, mostre o erro que eu resolvo sem
  apagar nada.
- Depois de mudar o schema, `npx prisma generate` — senão o TypeScript ainda
  enxerga o modelo antigo.
- Popular de novo com dado de exemplo: `npx prisma db seed`. Isso acrescenta,
  não substitui.

## Descobrir o que existe no banco

`npx prisma studio` abre uma tela para olhar os dados — use para conferir. O
schema completo está em `prisma/schema.prisma`; como o banco é deste projeto e
só dele, o arquivo é a fonte da verdade, não o contrário.

## PII

Coluna de CPF, CNS, nome de beneficiário, e-mail ou telefone: passe por
`mascararRegistros` de `lib/pii.ts` **antes** de o resultado sair do Server
Component. Não deixe a coluna crua circular pelo código "só por enquanto" — a
fronteira servidor → navegador leva o objeto inteiro.

Coluna de diagnóstico, CID ou condição: só traga se o `PLANO.md` disser
explicitamente que a aplicação precisa. Se precisar, invoque `dados-sensiveis`.

## Explicar resultado

Quem lê o resultado não sabe SQL. Junto da tabela, escreva em uma linha o que
a consulta filtrou ("leads de julho, excluindo teste interno").
