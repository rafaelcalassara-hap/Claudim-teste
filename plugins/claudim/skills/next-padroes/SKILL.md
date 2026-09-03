---
name: next-padroes
description: Padrões obrigatórios de código Next.js neste stack — App Router, Server Components, server actions com zod e checagem de sessão, Tailwind v4, shadcn/ui, exportação CSV, tratamento de erro legível para quem não é técnico. Use ao criar ou alterar qualquer tela, componente ou action da aplicação.
---

# Next.js — como escrevemos aqui

Um stack só: Next.js (App Router), React com Tailwind v4 e shadcn/ui,
next-auth com a conta Google da empresa, Prisma sobre SQLite — o banco é o
arquivo `prisma/dev.db`, dentro do projeto. Não discuta alternativa com o
usuário, não instale framework novo, não troque de biblioteca de UI e não
troque de banco.

## Estrutura

```
app/page.tsx          # a tela — Server Component
app/acoes.ts          # server actions desta rota ("use server" no topo)
app/globals.css       # tokens do tema, no bloco @theme
app/<rota>/page.tsx   # telas extras
app/<rota>/acoes.ts   # as actions daquela rota, junto dela
app/entrar/           # a tela de entrada — rota pública
app/api/auth/         # o retorno do Google — a outra rota pública
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

## Buscar dado

Busque no servidor, com `await`. Nada de `useEffect` + `fetch` para dado da
própria aplicação — é uma volta a mais e vaza para o navegador o que não
precisava sair do servidor.

Mas a página não chama o Prisma. **Consulta mora em `lib/dados/<tabela>.ts`**,
um arquivo por tabela, com toda leitura e toda escrita daquela tabela:

```ts
// lib/dados/eventos.ts
import "server-only";

const TETO = 1000;

export async function listarEventos({ dias }: { dias: number }) {
  if (!bancoConfigurado()) return mascararRegistros(exemploFormatado());

  const linhas = await db.evento.findMany({
    where: { criadoEm: { gte: new Date(Date.now() - dias * 86_400_000) } },
    select: { id: true, criadoEm: true, canal: true, uf: true, valorCentavos: true },
    orderBy: { criadoEm: "desc" },
    take: TETO,
  });

  return mascararRegistros(linhas.map(paraTela));
}
```

```tsx
// app/page.tsx — sessão, filtro, e o que aparece. Só isso.
export default async function Pagina({ searchParams }) {
  await exigirSessao();
  const { dias } = await searchParams;
  return <Tabela linhas={await listarEventos({ dias: Number(dias) || 30 })} />;
}
```

**Por que esse arquivo existe.** Quatro regras deste projeto vivem juntas nele:
`take`, `select` explícito, mascaramento antes de sair do servidor, e centavos
virando reais. Espalhadas por página e action, as quatro dependem de alguém
lembrar de cada uma toda vez. Num arquivo por tabela, é um lugar só para
conferir — e é onde o `/revisar` olha.

**O que ele não é.** Funções `async` exportadas, e pronto. Sem classe, sem
`BaseRepository`, sem interface, sem par entidade/DTO, sem mapper. O que a
função devolve é exatamente o que a tela mostra — já mascarado, já formatado.
Como o mascaramento é obrigatório, só existe uma forma de saída legal, e é essa;
por isso não há camada de conversão para inventar. Tabela nova é **arquivo
novo**, nunca camada nova.

MVC e MVVM não se aplicam aqui: um Server Component já é a view e o controller
ao mesmo tempo, uma action já é o controller de escrita, e o Prisma já é o
model. Não crie `controllers/`, `models/`, `services/` nem `viewmodels/`.

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
    await criarEvento(entrada.data);   // lib/dados/eventos.ts — nunca db.* aqui
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

A action é o portão: zod, sessão, banco, mensagem de erro. Quem fala com a
tabela é `lib/dados/`. E cada rota tem o seu `app/<rota>/acoes.ts` — não empilhe
as actions do projeto inteiro em `app/acoes.ts`.

## Quem pode entrar

Toda aplicação deste plugin nasce fechada. Três camadas, e nenhuma é opcional:

1. **`middleware.ts`** — só `/entrar` e `/api/auth` são públicas. Toda outra
   rota redireciona para `/entrar` sem sessão.
2. **`exigirSessao()`** em toda página e toda action, porque o middleware
   protege rota e action não é rota.
3. **`EMAILS_PERMITIDOS`** no `.env` — a lista de quem entra, conferida no
   callback `signIn` do `auth.ts` (na hora de entrar) e de novo no
   `exigirSessao()` (a cada requisição, para quem sai da lista perder o acesso
   sem esperar o cookie vencer).

A terceira é a que costuma faltar. Ter conta Google não é ter acesso a esta
aplicação. Quem autoriza é a lista. Lista vazia não libera geral — não libera
ninguém. O parâmetro `hd` na tela do Google é só uma dica de qual conta usar:
dá para tirar da URL e não protege nada sozinho.

**Não existe tela de criar conta.** Acesso é concedido por quem criou a
aplicação, editando `EMAILS_PERMITIDOS`, não pedido por um formulário público.
Não recrie `/criar-conta`, não adicione formulário de cadastro, e não ponha
rota nova no `PUBLICO` do middleware para "facilitar o teste".

**Senha nunca passa por este código.** Cadastro, troca e recuperação de senha
são da conta Google da empresa. Não adicione o provider `Credentials` do
next-auth — é ele que traz a senha de volta para cá. Não escreva tela de
"esqueci minha senha", não crie tabela de usuário no `schema.prisma`, não
guarde hash de senha, não gere token de recuperação e não mande e-mail. Se o
pedido do `PLANO.md` parece exigir isso, o que ele quer é liberar mais gente —
e isso é uma linha no `.env`.

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

## Rodar

`npm run dev` e abra http://localhost:3000. Depois de mudar qualquer tela,
suba, confirme que abre, e rode `npm run checar` (`tsc --noEmit` + `eslint .`).

## Formatação e lint

Não rode prettier nem eslint à mão a cada arquivo: um hook do plugin já passa os
dois sozinho depois de cada escrita, e devolve para você o que o `--fix` não
resolveu. Quando isso chegar, **corrija o código** — não silencie a regra com
`eslint-disable`, e não leve o assunto para o usuário: ele é de marketing e
erro de lint não é decisão dele.

Prettier decide a forma, eslint decide o que é erro. Não discuta aspas, ponto e
vírgula ou largura de linha com nenhum dos dois: `.prettierrc` já decidiu.
