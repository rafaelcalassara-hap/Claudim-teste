# Acme Design System V2 — POC

Padrão de documentação de design system em dois arquivos, um para agentes e um para humanos.
POC greenfield: marca, paleta, tipografia e domínio são fictícios.

| Arquivo | Público | Formato | Para quê |
|---|---|---|---|
| [`DESIGN.md`](./DESIGN.md) | agentes e IDEs | frontmatter YAML + markdown | Fonte machine-readable dos tokens. Todo valor de cor, espaçamento, raio, sombra e a receita de cada componente. É o arquivo que um agente lê para saber *qual token usar*. |
| [`DS-ACME.md`](./DS-ACME.md) | pessoas | prosa, tabelas, anatomia | Guia de uso. Anatomia de cada componente, do/don't, exemplos, regras de acessibilidade. É o arquivo que se lê para saber *como montar a tela*. |
| [`2026-09-03-ds-acme-showcase.html`](./2026-09-03-ds-acme-showcase.html) | qualquer um | HTML autocontido | Render dos tokens e componentes. Abrir no navegador. |

## A ideia

Um design system precisa responder duas perguntas diferentes, e elas têm leitores diferentes:

- *Qual é o valor?* — pergunta de máquina. Quer dado estruturado, sem prosa. → `DESIGN.md`
- *Como eu uso?* — pergunta de pessoa. Quer contexto, exemplo e contraexemplo. → `DS-ACME.md`

Juntar as duas num arquivo só faz o agente gastar contexto lendo narrativa e a pessoa caçar
a regra no meio de uma tabela de tokens. Separar mantém os dois curtos.

## Regra de manutenção

Mudou o design system — token novo, variante nova, primitiva nova — os **dois** arquivos são
atualizados no mesmo PR, mais uma história no Storybook. Um arquivo desatualizado é pior que
arquivo nenhum: parece verdade e não é.

A fonte de verdade executável não é nenhum dos dois — é o CSS que o build compila.
Os dois `.md` são espelhos dele. Quando divergirem, o CSS ganha.

## Onde isso é usado neste repo

Esta pasta é a **vitrine do padrão**: é aqui que se lê o que ele é, e o showcase HTML
mostra os tokens aplicados.

A cópia que o plugin `claudim` distribui vive em
[`plugins/claudim/templates/docs/design-system/`](../plugins/claudim/templates/docs/design-system/).
O `/comecar` a copia para dentro de cada aplicação criada, porque o app gerado é outro
projeto — ele não enxerga esta pasta. É de lá que o `/construir` lê antes de escrever
tela, e é contra ela que o `/revisar` audita.

Os dois `.md` são iguais nos dois lugares. Mudou um, muda o outro no mesmo commit.
