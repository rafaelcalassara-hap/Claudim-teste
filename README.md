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

O `claudim` nasce com um design system em
[`plugins/claudim/templates/docs/design-system/`](./plugins/claudim/templates/docs/design-system/):
`DESIGN.md` é a única fonte dos valores de tema, e o `@theme` do Tailwind e o
showcase HTML são gerados dele. Um gate no plugin reprova classe de tema sem
token. A marca é fictícia e existe para ser trocada pela da empresa.

## Antes de publicar uma versão

```
python3 testar_hooks.py
cd plugins/claudim/templates && python3 docs/design-system/gerar-tema.py --checar
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
