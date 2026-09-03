# {{NOME_DO_PROJETO}}

## O que essa aplicação faz

{{OBJETIVO}}

- **Quem usa:** {{USUARIOS}}
- **De onde vêm os dados:** {{ORIGEM_DADOS}}
- **Lida com dado sensível (CPF, carteirinha, beneficiário, saúde):** {{DADO_SENSIVEL}}

## Stack

Next.js (App Router) · React + Tailwind v4 + shadcn/ui · Clerk para sessão ·
Prisma + SQLite. Não troque, não adicione framework, não troque de banco.

O banco é o arquivo `prisma/dev.db`, dentro deste projeto: sem conta, sem
servidor, sem senha, nada a preencher no `.env`. Ele não se conecta ao banco da
empresa — dado corporativo entra por CSV importado, e é uma cópia com a data da
exportação.

| Onde | O que fica |
|---|---|
| `app/page.tsx` | a tela (Server Component: busca no servidor) |
| `app/acoes.ts` | server actions — zod valida, depois checa a sessão |
| `app/globals.css` | tokens de tema do Tailwind v4, no bloco `@theme` — espelho do design system |
| `docs/design-system/` | o design system: `DESIGN.md` tem os valores, `DS-ACME.md` a anatomia |
| `components/` | componentes React seus |
| `components/ui/` | primitivos do shadcn/ui (`npx shadcn@latest add ...`) |
| `lib/config.ts` | login configurado no `.env` + quem pode entrar |
| `lib/db.ts` | cliente do Prisma + `bancoConfigurado()` |
| `lib/auth.ts` | `exigirSessao()` — usada em toda página e toda action |
| `lib/pii.ts` | mascaramento e hash de dado pessoal |
| `lib/dados-sinteticos.ts` | gerador de dado falso para exemplo e teste |
| `prisma/schema.prisma` | as tabelas desta aplicação |
| `prisma/dev.db` | o banco — um arquivo, fora do git |
| `middleware.ts` | quais rotas exigem login (só `/entrar` é pública) |
| `PLANO.md` | o que está sendo construído e o que falta |
| `.env` | segredos — nunca vai para o git |

Rodar: `npm run dev` (abre em http://localhost:3000)

Recomeçar o banco com dado de exemplo: `npx prisma db push && npx prisma db seed`

## Quando invocar qual skill

| Situação | Skill |
|---|---|
| Escrever ou alterar tela, componente ou server action | `next-padroes` |
| Escolher cor, raio, sombra, espaçamento ou classe Tailwind | `next-padroes` + `docs/design-system/DESIGN.md` |
| Qualquer consulta, schema ou migração do Prisma | `consultar-banco` |
| CPF, carteirinha, beneficiário, diagnóstico, tracking, URL de campanha, copy de plano | `dados-sensiveis` |
| Definir ou revisar escopo | `escrever-plano` |

## Regras do projeto

- **Esta aplicação é dona das tabelas do `schema.prisma`** — nelas pode ler e
  escrever. Ela não alcança nenhum outro banco.
- **Nada de tipo nativo no schema** (`@db.Decimal`, `@db.VarChar`): SQLite não
  tem, e o Prisma recusa o schema inteiro. Dinheiro é `Int` em centavos.
- **Quem entra está em `EMAILS_PERMITIDOS`**, no `.env`. Não existe tela de
  criar conta, e senha é do Clerk — esta aplicação nunca guarda uma.
- Toda página e toda server action chamam `exigirSessao()`. O middleware
  protege rotas; server action não é rota.
- Toda entrada de server action passa por `zod` antes de virar efeito.
- Segredo vem de `process.env`. Valor literal em código é bloqueado por hook.
- **Nada com `NEXT_PUBLIC_` guarda segredo** — esse prefixo publica o valor no
  navegador de quem abrir a página.
- Dado de pessoa real não entra em arquivo. Use `lib/dados-sinteticos.ts`.
- PII é mascarada **no servidor**, antes de atravessar para componente
  `"use client"`. O que vai por prop, vai inteiro no payload da página.
- Toda consulta de lista tem `take` (teto de linhas).
- Erro na tela em português, sem stack trace.
- **Cor, raio e sombra saem de `docs/design-system/DESIGN.md`** — nunca de hex
  na classe nem de cor arbitrária do Tailwind. O `@theme` do `globals.css` é o
  espelho dele; os dois mudam no mesmo passo.
