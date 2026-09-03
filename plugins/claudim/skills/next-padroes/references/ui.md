# Tela: Tailwind, shadcn/ui, erro, vazio, CSV

## Tailwind v4

O tema está em `app/globals.css`, no bloco `@theme` — **não existe
`tailwind.config.js` neste projeto**. Token vira utilitário: `--color-marca`
gera `bg-marca` e `text-marca`; `--radius-padrao` gera `rounded-padrao`.

- Cor nova, espaçamento novo: adicione um token no `@theme` e use o utilitário.
- Não escreva hex solto na classe (`bg-[#0055ff]`) nem CSS em arquivo à parte.
- Não instale `tailwind.config.js`, plugin de tema, nem outra lib de CSS.

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
