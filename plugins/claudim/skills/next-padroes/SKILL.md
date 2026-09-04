---
name: next-padroes
description: Padrões obrigatórios de código Next.js neste stack — App Router, Server Components, server actions com zod e checagem de sessão, Tailwind v4, shadcn/ui, design system tokenizado em docs/design-system, exportação CSV, tratamento de erro legível para quem não é técnico. Use ao criar ou alterar qualquer tela, componente ou action da aplicação.
---

# Next.js — como escrevemos aqui

Um stack só: Next.js (App Router), React com Tailwind v4 e shadcn/ui,
next-auth com a conta Google da empresa, Prisma sobre SQLite — o banco é o
arquivo `prisma/dev.db`, dentro do projeto. Não discuta alternativa com o
usuário, não instale framework novo, não troque de biblioteca de UI e não
troque de banco.

## Leia o detalhe do que você vai mexer

Esta página é o que vale sempre. Antes de escrever, leia **só** o arquivo da
parte que você vai tocar — nesta mesma pasta:

| Vou mexer em | Leia |
|---|---|
| consulta, `lib/dados/`, o que a página busca | `references/dados.md` |
| server action, formulário, qualquer escrita | `references/acoes.md` |
| `auth.ts`, `middleware.ts`, `lib/auth.ts`, login, quem entra | `references/acesso.md` |
| cor, raio, sombra, espaçamento, botão, card, alert, header — qualquer coisa visual; Tailwind, shadcn/ui, erro, vazio, CSV | `references/ui.md` |

Mais de uma linha se aplica? Leia as duas. Nenhuma se aplica? O que está aqui
basta.

## Estrutura

```
app/page.tsx          # a tela — Server Component
app/acoes.ts          # server actions desta rota ("use server" no topo)
app/globals.css       # tokens do tema — GERADO de docs/design-system/DESIGN.md
app/<rota>/page.tsx   # telas extras
app/<rota>/acoes.ts   # as actions daquela rota, junto dela
app/entrar/           # a tela de entrada — rota pública
app/api/auth/         # o retorno do Google — a outra rota pública
docs/design-system/   # DESIGN.md = o valor (fonte); DS-ACME.md = o uso
components/           # componentes seus
components/ui/        # primitivos do shadcn/ui
lib/dados/<tabela>.ts # TODA leitura e escrita daquela tabela
lib/dados/sinteticos.ts
lib/db.ts             # cliente do Prisma + bancoConfigurado()
lib/auth.ts           # exigirSessao()
lib/pii.ts            # mascaramento e hash
prisma/dev.db         # o banco, um arquivo (fora do git)
auth.ts               # configuração do login (provider Google + allowlist)
middleware.ts         # rotas protegidas
eslint.config.mjs     # regras de código (hook aplica sozinho)
.prettierrc           # formatação (idem)
.env                  # nunca no git
```

## Server por padrão, client por exceção

Componente sem `"use client"` roda **só no servidor**: ele busca no banco e
manda HTML pronto. É o padrão aqui.

Só marque `"use client"` quando a coisa precisa mesmo do navegador: clique que
muda estado local, `onChange`, download de arquivo, `window`. E quando marcar,
mantenha o componente pequeno — a folha da árvore, não a raiz.

**A fronteira é o ponto de vazamento.** Tudo que um Server Component passa por
prop para um componente `"use client"` viaja para o navegador e aparece no
DevTools de quem abrir a página — inclusive o campo que você não renderizou.
Passe só o que a tela mostra, já mascarado por `lib/pii.ts`.

## Não faça

- Segredo com prefixo `NEXT_PUBLIC_`. Esse prefixo publica o valor no
  navegador. Chave secreta é `process.env.CHAVE`, lida em arquivo de servidor.
- `dangerouslySetInnerHTML` com texto vindo do banco.
- `useEffect` para buscar dado da própria aplicação.
- Instalar biblioteca de gráfico ou de UI nova por conta própria.
- Escrever em tabela de sistema corporativo. Esta aplicação escreve só no que
  está no `prisma/schema.prisma`.
- `any` para calar erro de tipo. O erro está apontando um bug de verdade.
- `eslint-disable` para calar uma regra. Conserte o código.
- `db.*` dentro de `page.tsx` ou de `acoes.ts`. Consulta é `lib/dados/<tabela>.ts`.
- Pasta `controllers/`, `models/`, `services/` ou `viewmodels/`. O App Router já
  tem camadas; essas só duplicariam o que `page.tsx` e `acoes.ts` já são.

## Rodar, formatar, conferir

`npm run dev` e abra http://localhost:3000. Depois de mudar qualquer tela,
suba, confirme que abre, e rode `npm run checar` (`tsc --noEmit` + `eslint .`).

Não rode prettier nem eslint à mão a cada arquivo: um hook do plugin já passa os
dois sozinho depois de cada escrita e devolve o que o `--fix` não resolveu.
Quando isso chegar, **corrija o código** — não silencie a regra e não leve o
assunto ao usuário: ele é de marketing e erro de lint não é decisão dele.
