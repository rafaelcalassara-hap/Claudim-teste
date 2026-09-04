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
| `app/globals.css` | **gerado** do design system — hook bloqueia edição à mão |
| `docs/design-system/` | o design system: `DESIGN.md` = **o valor** (a fonte), `DS-ACME.md` = **o uso** (anatomia, do/don't) |
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

## Regras do projeto, e onde está o porquê

Cada linha é obrigatória. A skill da direita explica o motivo e mostra como se
escreve — invoque ela antes de mexer no assunto, não depois.

| Regra | Skill |
|---|---|
| Esta aplicação só alcança as tabelas do `schema.prisma`. | `consultar-banco` |
| Nada de tipo nativo no schema. Dinheiro é `Int` em centavos. | `consultar-banco` |
| Toda consulta de lista tem `take`, e mora em `lib/dados/<tabela>.ts`. | `consultar-banco` |
| Toda página e toda action chamam `exigirSessao()`. | `next-padroes` |
| Toda entrada de action passa por `zod` antes de virar efeito. | `next-padroes` |
| Quem entra está em `EMAILS_PERMITIDOS`. Não há tela de criar conta nem senha aqui. | `next-padroes` |
| Erro na tela em português, sem stack trace. | `next-padroes` |
| Cor, raio, sombra e espaçamento saem de `docs/design-system/DESIGN.md`. Nunca hex nem cor do Tailwind — o `globals.css` é gerado. | `next-padroes` |
| Como montar botão, card, input, alert, header sai de `docs/design-system/DS-ACME.md` §7. | `next-padroes` |
| PII é mascarada no servidor, antes de ir por prop para `"use client"`. | `dados-sensiveis` |
| Dado de pessoa real não entra em arquivo — use `lib/dados/sinteticos.ts`. | `dados-sensiveis` |
| Segredo vem de `process.env`, e nunca com prefixo `NEXT_PUBLIC_`. | `dados-sensiveis` |

Definir ou revisar escopo é a skill `escrever-plano`.

Login, segredo e dado pessoal são impostos por hook, não por boa vontade: se
você errar, a escrita é bloqueada e a mensagem diz o próximo passo.

## Formatação e lint

Nada a rodar à mão: a cada arquivo salvo um hook passa `prettier` e
`eslint --fix`, e devolve ao Claude o que sobrou. Tudo de uma vez: `npm run checar`.
