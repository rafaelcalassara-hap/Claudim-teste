---
name: next-padroes
description: Padrões obrigatórios de código Next.js neste stack — App Router, Server Components, server actions com zod e checagem de sessão, Tailwind v4, shadcn/ui, design system tokenizado em docs/design-system, exportação CSV, tratamento de erro legível para quem não é técnico. Use ao criar ou alterar qualquer tela, componente, cor, classe Tailwind ou action da aplicação.
---

# Next.js — como escrevemos aqui

Um stack só: Next.js (App Router), React com Tailwind v4 e shadcn/ui, Clerk
para sessão, Prisma sobre SQLite — o banco é o arquivo `prisma/dev.db`, dentro
do projeto. Não discuta alternativa com o usuário, não instale framework novo,
não troque de biblioteca de UI e não troque de banco.

## Estrutura

```
app/page.tsx        # a tela — Server Component
app/acoes.ts        # server actions ("use server" no topo)
app/globals.css     # tokens do tema — GERADO do design system
prisma/dev.db       # o banco, um arquivo (fora do git)
app/entrar/         # a única rota pública — login do Clerk
docs/design-system/ # DESIGN.md: a fonte dos valores de tema
app/<rota>/page.tsx # telas extras
components/         # componentes seus
components/ui/      # primitivos do shadcn/ui
lib/db.ts           # cliente do Prisma + bancoConfigurado()
lib/auth.ts         # exigirSessao()
lib/pii.ts          # mascaramento e hash
lib/dados-sinteticos.ts
middleware.ts       # rotas protegidas
.env                # nunca no git
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

## Buscar dado

Busque dentro do Server Component, com `await`, direto no Prisma. Nada de
`useEffect` + `fetch` para dado da própria aplicação — isso é uma volta a mais
e vaza para o navegador o que não precisava sair do servidor.

```tsx
export default async function Pagina() {
  await exigirSessao();
  const linhas = await db.evento.findMany({ take: 1000, orderBy: { criadoEm: "desc" } });
  return <Tabela linhas={mascararRegistros(linhas)} />;
}
```

Filtro vai na URL (`searchParams`), não em estado de React: o servidor refaz a
busca, o link fica compartilhável e a tela funciona sem JavaScript.

## Server action: zod, sessão, banco — o efeito por último

Uma action é um endpoint HTTP. Dá para chamá-la sem passar pela sua tela, e o
`middleware.ts` não cobre isso. Toda action que escreve, sem exceção:

```ts
"use server";

export async function salvar(_anterior: unknown, form: FormData) {
  const entrada = Entrada.safeParse(Object.fromEntries(form)); // 1. zod
  if (!entrada.success) return { ok: false, erro: entrada.error.issues[0].message };

  const usuarioId = await exigirSessao();                       // 2. sessão

  if (!bancoConfigurado()) {                                    // 3. banco
    return {
      ok: false,
      erro:
        "Ainda não dá para salvar: esta aplicação está rodando com dados de " +
        "exemplo. Para salvar de verdade, preencha DATABASE_URL no arquivo .env.",
    };
  }

  try {                                                         // 4. efeito
    await db.evento.create({ data: entrada.data });
  } catch (erro) {
    return {
      ok: false,
      erro: `Não consegui salvar agora. Tente de novo em instantes. Detalhe técnico: ${(erro as Error).name}`,
    };
  }

  revalidatePath("/");
  return { ok: true };
}
```

O efeito no banco vem **depois** das três. Action que escreve antes de checar
sessão é o furo clássico deste stack.

**Leitura cai para dado de exemplo; escrita não cai para lugar nenhum.** A tela
roda sem banco porque `page.tsx` troca a consulta por `tabelaExemplo()` quando
`bancoConfigurado()` é falso. Gravar não tem esse plano B: sem a checagem, o
primeiro clique em "Salvar" estoura erro de conexão contra o host de mentira do
`.env.example`. E isso não aparece no `tsc --noEmit` nem em abrir a tela — só
quando uma pessoa clica. Por isso a checagem é obrigatória, não recomendada.

Depois dela, `try/catch` mesmo assim: banco configurado também sai do ar, e aí
a diferença entre uma frase em português e um stack trace é tudo o que esse
público tem.

Devolva erro como valor (`{ ok: false, erro }`), não como exceção: a mensagem
precisa chegar à tela em português.

## Quem pode entrar

Toda aplicação deste plugin nasce fechada. Três camadas, e nenhuma é opcional:

1. **`middleware.ts`** — só `/entrar(.*)` é pública. Toda outra rota passa por
   `auth.protect()`.
2. **`exigirSessao()`** em toda página e toda action, porque o middleware
   protege rota e action não é rota.
3. **`EMAILS_PERMITIDOS`** no `.env` — a lista de quem entra.

A terceira é a que costuma faltar. Ter conta no Clerk não é ter acesso a esta
aplicação: o Clerk autentica *qualquer* pessoa que se cadastrar. Quem autoriza
é a lista. Lista vazia não libera geral — não libera ninguém.

**Não existe tela de criar conta.** Acesso é concedido por quem criou a
aplicação, editando `EMAILS_PERMITIDOS`, não pedido por um formulário público.
Não recrie `/criar-conta`, não adicione `<SignUp />`, e não ponha rota nova no
`publico` do middleware para "facilitar o teste".

**Senha nunca passa por este código.** Cadastro, troca e recuperação de senha
são telas do Clerk. Não escreva tela de "esqueci minha senha", não crie tabela
de usuário no `schema.prisma`, não guarde hash de senha, não gere token de
recuperação e não mande e-mail. Se o pedido do `PLANO.md` parece exigir isso,
o que ele quer é liberar mais gente — e isso é uma linha no `.env`.

## Tailwind v4

O tema está em `app/globals.css`, no bloco `@theme` — **não existe
`tailwind.config.js` neste projeto**. Token vira utilitário: `--color-primary`
gera `bg-primary` e `text-primary`; `--radius-lg` gera `rounded-lg`.

- Cor nova, espaçamento novo: o token entra no `DESIGN.md` e o `@theme` é
  regerado. Nunca direto no `globals.css` — ele é arquivo gerado (ver
  **Design system**, abaixo).
- Não escreva hex solto na classe (`bg-[#0055ff]`) nem CSS em arquivo à parte.
- Não instale `tailwind.config.js`, plugin de tema, nem outra lib de CSS.

## Design system

**`docs/design-system/DESIGN.md` é a única fonte dos valores de tema.** Cor,
tipografia, raio, sombra e espaçamento vivem lá, em YAML no topo do arquivo, e
em nenhum outro lugar. Leia antes de escrever tela ou componente.

O `app/globals.css` é **gerado** dele:

```
python3 docs/design-system/gerar-tema.py
```

- **Não edite o `globals.css` à mão.** Um hook bloqueia a escrita, e a próxima
  execução do gerador sobrescreveria de qualquer forma.
- O nome da utilitária é o nome do token, sem tradução no meio:
  `--color-primary` gera `bg-primary`, `--radius-lg` gera `rounded-lg`,
  `--shadow-sm` gera `shadow-sm`. Não existe um segundo vocabulário.
- Cor que **não** existe no DS: não invente token nem classe. Diga ao usuário
  qual valor falta e por quê — tema é decisão de design, não de implementação.
- `bg-primary` para identidade, `bg-accent` para o botão que a pessoa deve
  clicar. Errar isso deixa a tela com dois primários brigando.
- Estado nunca é só cor. Vermelho sem ícone e sem rótulo não passa em
  daltonismo — combine cor com texto ou ícone, sempre.
- Contraste mínimo 4,5:1 para texto. Sobre `bg-primary` e `bg-accent`, use
  `text-primary-foreground` / `text-accent-foreground`. Sobre `bg-warning` e
  `bg-highlight`, texto escuro (`text-foreground`).

Antes de fechar o passo, rode a checagem:

```
python3 docs/design-system/gerar-tema.py --checar
```

Ela falha se o `globals.css` divergiu do `DESIGN.md` ou se algum `.tsx` usa
classe de tema sem token — `bg-azul`, `bg-blue-600`. É assim que nasce uma
segunda paleta.

`DS-ACME.md`, na mesma pasta, tem a anatomia de cada componente em prosa.
Consulte quando a dúvida for *como montar*, não *qual valor usar* — ele cita
token por nome e não repete valor, de propósito.

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

## Não faça

- Segredo com prefixo `NEXT_PUBLIC_`. Esse prefixo publica o valor no
  navegador. Chave secreta é `process.env.CHAVE`, lida em arquivo de servidor.
- `dangerouslySetInnerHTML` com texto vindo do banco.
- `useEffect` para buscar dado da própria aplicação.
- Instalar biblioteca de gráfico ou de UI nova por conta própria.
- Escrever em tabela de sistema corporativo. Esta aplicação escreve só no que
  está no `prisma/schema.prisma`.
- `any` para calar erro de tipo. O erro está apontando um bug de verdade.

## Rodar

`npm run dev` e abra http://localhost:3000. Depois de mudar qualquer tela,
suba, confirme que abre, e rode `npx tsc --noEmit` — erro de tipo aqui é a
única verificação automática que o projeto tem.
