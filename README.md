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
| `claudim` | marketing, growth, dados, operações | cria aplicações internas em Next.js + Prisma + SQLite, com login pela conta Google da empresa, design system tokenizado e guardrails de LGPD e ANS impostos por hook |

## Design system

O `claudim` nasce com um design system em
[`plugins/claudim/templates/docs/design-system/`](./plugins/claudim/templates/docs/design-system/):
`DESIGN.md` é a única fonte dos valores de tema, `DS-ACME.md` é o guia de uso,
e o `@theme` do Tailwind e o showcase HTML são gerados do primeiro. Um guard
reprova hex, cor do Tailwind e classe de tema sem token. A marca é fictícia e
existe para ser trocada pela da empresa.

## Antes de publicar uma versão

```
python3 testar_hooks.py
cd plugins/claudim/templates && python3 docs/design-system/gerar-tema.py --checar
```

69 casos cobrindo bloqueio de segredo, `NEXT_PUBLIC_` com segredo, PII,
tracking, git, SQL destrutivo, reset de banco, deploy em produção, o modelo de
acesso (autocadastro, senha no projeto, rota pública nova, lista de quem entra)
e o design system (hex na classe, cor do Tailwind, classe sem token, `globals.css`
editado à mão).
Hook que não bloqueia é o modo de falha caro aqui: o público-alvo não percebe
que passou.

Os quatro últimos casos são o contrário: os hooks de formatação e lint têm que
sair **calados** quando o projeto não tem as ferramentas instaladas. Estilo
travando o trabalho é um modo de falha próprio.

## Estado

MVP. O que existe hoje corresponde às semanas 1–2 do rollout mais o `/revisar`
(semana 4), que já está incluído. O que **não** existe: `/publicar` (deploy na
Vercel — o hook bloqueia `--prod` de propósito), provisionamento de banco e do
cliente OAuth do Google, canal de suporte definido.
