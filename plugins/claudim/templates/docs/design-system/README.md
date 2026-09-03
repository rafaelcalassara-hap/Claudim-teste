# Design system

Uma fonte de verdade por coisa. Aqui, a coisa é **tema**: cor, tipografia,
raio, sombra, espaçamento.

| Arquivo | Papel | Editável |
|---|---|---|
| `DESIGN.md` | **a fonte.** Frontmatter YAML com todos os valores, e a receita de cada componente | sim — é aqui que se muda o tema |
| `DS-ACME.md` | o guia de uso: anatomia, do/don't, acessibilidade. Cita token por **nome**, nunca por valor | sim |
| `gerar-tema.py` | lê o `DESIGN.md` e escreve os derivados | sim |
| `showcase.html` | os tokens renderizados, para olhar | **não — gerado** |
| `../../app/globals.css` | o `@theme` do Tailwind | **não — gerado** |

## Mudar o tema

```
# 1. edite o valor em DESIGN.md
# 2. regenere os derivados
python3 docs/design-system/gerar-tema.py
```

Nenhum componente muda. `page.tsx` e `button.tsx` não conhecem hex — usam
`bg-primary`, `rounded-lg`, `text-muted-foreground`. O nome da utilitária é o
nome do token, sem tradução no meio.

## Verificar

```
python3 docs/design-system/gerar-tema.py --checar
```

Sai com 1 e diz o que fazer quando:

- um derivado foi editado à mão e não corresponde mais ao `DESIGN.md`;
- um `.tsx` usa classe de tema sem token — `bg-azul`, `bg-blue-600`. É assim
  que nasce uma segunda paleta, e é o que essa checagem existe para impedir.

## Por que dois arquivos de documentação

*Qual é o valor* é pergunta de máquina: quer dado estruturado, sem prosa.
*Como eu uso* é pergunta de gente: quer contexto, exemplo e contraexemplo.
Num arquivo só, o agente gasta contexto lendo narrativa e a pessoa caça a
regra no meio de uma tabela de tokens.

O `DS-ACME.md` não repete valor de propósito. Valor em dois lugares é valor
que vai divergir — foi o que aconteceu antes deste arranjo: o guia citava um
`--color-high-contrast` que nunca existiu, e o showcase tinha três cores
inventadas na mão.

## Trocar pelo design system da sua empresa

Substitua os valores no `DESIGN.md`, ajuste o `DS-ACME.md` e rode o gerador.
A marca aqui é fictícia e existe para ser trocada.
