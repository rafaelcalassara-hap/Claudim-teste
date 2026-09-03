# {{NOME_DO_PROJETO}}

## O que essa aplicação faz

{{OBJETIVO}}

- **Quem usa:** {{USUARIOS}}
- **De onde vêm os dados:** {{ORIGEM_DADOS}}
- **Lida com dado sensível (CPF, carteirinha, beneficiário, saúde):** {{DADO_SENSIVEL}}

## Stack

Next.js (App Router) · React + Tailwind v4 + shadcn/ui · next-auth com a conta
Google da empresa · Prisma + SQLite. Não troque, não adicione framework, não
troque de banco.

O banco é o arquivo `prisma/dev.db`, dentro deste projeto: sem conta, sem
servidor, sem senha, nada a preencher no `.env`. Ele não se conecta ao banco da
empresa — dado corporativo entra por CSV importado, e é uma cópia com a data da
exportação.

| Onde | O que fica |
|---|---|
| `app/page.tsx` | a tela (Server Component: só sessão, filtro e o que aparece) |
| `app/acoes.ts` | server actions desta rota — zod, sessão, banco, depois o efeito |
| `app/globals.css` | tokens de tema do Tailwind v4, no bloco `@theme` |
| `components/` | componentes React seus |
| `components/ui/` | primitivos do shadcn/ui (`npx shadcn@latest add ...`) |
| `lib/dados/<tabela>.ts` | **toda leitura e escrita de uma tabela** — um arquivo por tabela |
| `lib/dados/sinteticos.ts` | gerador de dado falso para exemplo e teste |
| `lib/config.ts` | login configurado no `.env` + quem pode entrar |
| `lib/db.ts` | cliente do Prisma + `bancoConfigurado()` |
| `lib/auth.ts` | `exigirSessao()` — usada em toda página e toda action |
| `lib/pii.ts` | mascaramento e hash de dado pessoal |
| `prisma/schema.prisma` | as tabelas desta aplicação |
| `prisma/dev.db` | o banco — um arquivo, fora do git |
| `auth.ts` | configuração do login pelo Google + o callback que confere a lista |
| `middleware.ts` | quais rotas exigem login (só `/entrar` e `/api/auth` são públicas) |
| `PLANO.md` | o que está sendo construído e o que falta |
| `eslint.config.mjs` | as regras de código — um hook aplica sozinho a cada arquivo salvo |
| `.prettierrc` | a formatação — idem |
| `.env` | segredos — nunca vai para o git |

Rodar: `npm run dev` (abre em http://localhost:3000)

Recomeçar o banco com dado de exemplo: `npx prisma db push && npx prisma db seed`

## Quando invocar qual skill

| Situação | Skill |
|---|---|
| Escrever ou alterar tela, componente ou server action | `next-padroes` |
| Qualquer consulta, schema ou migração do Prisma | `consultar-banco` |
| CPF, carteirinha, beneficiário, diagnóstico, tracking, URL de campanha, copy de plano | `dados-sensiveis` |
| Definir ou revisar escopo | `escrever-plano` |

## Regras do projeto

- **Esta aplicação é dona das tabelas do `schema.prisma`** — nelas pode ler e
  escrever. Ela não alcança nenhum outro banco.
- **Nada de tipo nativo no schema** (`@db.Decimal`, `@db.VarChar`): SQLite não
  tem, e o Prisma recusa o schema inteiro. Dinheiro é `Int` em centavos.
- **Quem entra está em `EMAILS_PERMITIDOS`**, no `.env`. Não existe tela de
  criar conta: a conta é a do Google da empresa e esta aplicação nunca guarda
  senha. A lista é conferida duas vezes — no `signIn` do `auth.ts` e no
  `exigirSessao()`.
- Toda página e toda server action chamam `exigirSessao()`. O middleware
  protege rotas; server action não é rota.
- Toda entrada de server action passa por `zod` antes de virar efeito.
- Segredo vem de `process.env`. Valor literal em código é bloqueado por hook.
- **Nada com `NEXT_PUBLIC_` guarda segredo** — esse prefixo publica o valor no
  navegador de quem abrir a página.
- Dado de pessoa real não entra em arquivo. Use `lib/dados/sinteticos.ts`.
- PII é mascarada **no servidor**, antes de atravessar para componente
  `"use client"`. O que vai por prop, vai inteiro no payload da página.
- Toda consulta de lista tem `take` (teto de linhas).
- **Consulta do Prisma mora em `lib/dados/<tabela>.ts`**, um arquivo por tabela,
  nunca dentro da página nem da action. É lá que ficam juntos o `take`, o
  `select`, o mascaramento e a conversão de centavos — as quatro coisas que,
  espalhadas, dependem de alguém lembrar. São funções `async` exportadas: sem
  classe, sem repositório genérico, sem DTO. Tabela nova é arquivo novo, não
  camada nova.
- Erro na tela em português, sem stack trace.

## Formatação e regras de código

Não há nada para você rodar. A cada arquivo salvo, um hook do plugin passa o
`prettier` e o `eslint --fix` sozinho, e o que não dá para consertar
automaticamente volta para o Claude corrigir antes de seguir.

Se quiser conferir tudo de uma vez: `npm run checar`.
