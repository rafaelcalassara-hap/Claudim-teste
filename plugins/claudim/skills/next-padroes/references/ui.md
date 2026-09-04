# Tela: Tailwind, shadcn/ui, erro, vazio, CSV

## Tailwind v4

O tema está em `app/globals.css`, no bloco `@theme` — **não existe
`tailwind.config.js` neste projeto**. Token vira utilitário: `--color-primary`
gera `bg-primary` e `text-primary`; `--radius-lg` gera `rounded-lg`;
`--spacing-container-md` gera `px-container-md`.

- Cor nova, espaçamento novo: o token entra no `DESIGN.md` e o `@theme` é
  regerado. Nunca direto no `globals.css` — ele é arquivo gerado.
- Não escreva hex solto na classe (`bg-[#0055ff]`) nem CSS em arquivo à parte.
  Um hook bloqueia os dois.
- Não instale `tailwind.config.js`, plugin de tema, nem outra lib de CSS.

## Design system

Dois arquivos, duas perguntas. Saber qual abrir é metade do trabalho:

| Sua intenção | Abra |
| --- | --- |
| Preciso de uma cor, raio, sombra, espaçamento, fonte | `docs/design-system/DESIGN.md` — o valor está lá, e só lá |
| Vou criar ou alterar botão, card, input, alert, header, badge | `docs/design-system/DS-ACME.md` §7 — anatomia, variantes, estados |
| Qual variante uso aqui? (primário vs secundário, card com hover…) | `DS-ACME.md` §7 do componente + §10 referência rápida |
| Como sinalizo erro, sucesso, aviso, vazio | `DS-ACME.md` §7.19 e §8 — estado nunca é só cor |
| Isso está acessível? | `DS-ACME.md` §8 |
| Posso fazer X? | `DS-ACME.md` §9 — faça / não faça |
| Container, grid, margem por breakpoint | `DS-ACME.md` §5 — e os tokens `--spacing-*` no `DESIGN.md` |
| O DS não tem o que preciso | `DS-ACME.md` §11 — a ordem para estender sem quebrar a fonte única |

**`DESIGN.md` é a única fonte dos valores.** Cor, tipografia, raio, sombra e
espaçamento vivem no YAML do topo dele, e em nenhum outro lugar. **`DS-ACME.md`
é a única fonte do uso.** Como montar, quando usar, o que não fazer. Um cita
o outro por nome; nenhum repete o que o outro tem.

O `app/globals.css` é **gerado** do `DESIGN.md`:

```
python3 docs/design-system/gerar-tema.py
```

- **Não edite o `globals.css` à mão.** Um hook bloqueia a escrita, e a próxima
  execução do gerador sobrescreveria de qualquer forma.
- O nome da utilitária é o nome do token, sem tradução no meio. Não existe um
  segundo vocabulário.
- Cor que **não** existe no DS: não invente token nem classe. Diga ao usuário
  qual valor falta e por quê — tema é decisão de design, não de implementação.
- `bg-primary` para identidade, `bg-accent` para o botão que a pessoa deve
  clicar. Errar isso deixa a tela com dois primários brigando.
- Estado nunca é só cor. Vermelho sem ícone e sem rótulo não passa em
  daltonismo — combine cor com texto ou ícone, sempre.
- Contraste mínimo 4,5:1 para texto. Sobre `bg-primary` e `bg-accent`, use
  `text-primary-foreground` / `text-accent-foreground`. Sobre `bg-warning` e
  `bg-highlight`, texto escuro (`text-foreground`).

Antes de fechar o passo, `python3 docs/design-system/gerar-tema.py --checar`
— falha se o `globals.css` divergiu do `DESIGN.md` ou se algum `.tsx` usa
classe de tema sem token.

Não existe classe `.ds-*`, não existe `packages/ui`, não existe Storybook
neste projeto. Se um documento citar isso, está desatualizado — o que existe é
`components/ui/` do shadcn e utilitária de token.

## shadcn/ui

Precisa de um componente novo (dialog, table, select)?
`npx shadcn@latest add <nome>` — ele grava o código em `components/ui/`, e a
partir daí o código é seu, pode editar. Não instale MUI, Chakra, Ant, nem
importe componente pronto de outra biblioteca.

## Erro em português

Nunca deixe stack trace na tela. Em página, `try/catch` com mensagem e o nome
do erro como detalhe:

```tsx
catch (erro) {
  return <Aviso titulo="Não consegui carregar os dados. Avise o time de dados."
                detalhe={(erro as Error).name} />;
}
```

## Estado vazio

Toda lista precisa do caso "não veio nada": uma frase explicando, não uma
tabela vazia sem cabeçalho.

## Sempre dê saída em CSV

Esse público quer levar o dado para a planilha; se não tiver botão, ele copia
da tela. Use `components/exportar-csv.tsx` — com BOM na frente, senão o Excel
abre acento errado. O CSV sai do dado **já mascarado**, igual à tela.
