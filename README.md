# Greenfield Marketplace

Marketplace interno de plugins do Claude Code.

## Instalar

```
/plugin marketplace add git@github.com:greenfield-llc/greenfield-marketplace.git
/plugin install claudim
```

Atualizar é `git pull` neste repositório — a correção chega em quem já
instalou. É esse o motivo de ser plugin e não template repo.

## Plugins

| Plugin | Para quem | O que faz |
|---|---|---|
| `claudim` | marketing, growth, dados, operações | cria aplicações internas em Next.js + Prisma + SQLite, com sessão pelo Clerk, design system tokenizado e guardrails de LGPD e ANS impostos por hook |

## Design system

O `claudim` nasce com um design system em dois arquivos — um para agente ler,
outro para pessoa ler — e o tema do Tailwind é o espelho dele. A referência do
padrão está em [`ds-acme/`](./ds-acme/), com um showcase HTML dos tokens e
componentes. A marca é fictícia e existe para ser trocada pela da empresa.

## Antes de publicar uma versão

```
python3 testar_hooks.py
```

49 casos cobrindo bloqueio de segredo, `NEXT_PUBLIC_` com segredo, PII,
tracking, git, SQL destrutivo, reset de banco, deploy em produção e o modelo de
acesso (autocadastro, senha no projeto, rota pública nova, lista de quem entra).
Hook que não bloqueia é o modo de falha caro aqui: o público-alvo não percebe
que passou.

## Estado

MVP. O que existe hoje corresponde às semanas 1–2 do rollout mais o `/revisar`
(semana 4), que já está incluído. O que **não** existe: `/publicar` (deploy na
Vercel — o hook bloqueia `--prod` de propósito), provisionamento de banco e de
conta do Clerk, canal de suporte definido.
