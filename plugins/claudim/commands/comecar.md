---
description: Cria um projeto novo de aplicação interna nesta pasta (roda uma vez, em pasta vazia)
argument-hint: [nome do projeto]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# /comecar — montar o projeto

Você está atendendo alguém de marketing, growth, dados ou operações. **Não é
engenheiro.** Não use jargão, não ofereça escolha de tecnologia, não explique
o que é git, npm ou TypeScript.

## 0. Verificar a pasta

Rode `ls -A`. Se a pasta já tem um `CLAUDE.md` ou `.greenfield/`, pare e diga:
"Este projeto já foi criado. Use `/planejar` para definir o que fazer agora."

Confira também `node -v`. Se não houver Node 20 ou mais novo, pare e diga em
uma frase: "Preciso do Node instalado nesta máquina para montar o projeto —
peça ao time de TI o Node 20." Não tente instalar por conta própria.

## 1. Marcar a fase de scaffold

Antes de escrever qualquer arquivo, crie `.greenfield/state.json`:

```json
{ "fase": "scaffold" }
```

Isso libera os hooks para o scaffold. Sem isso o hook bloqueia a criação da
tela porque ainda não existe `PLANO.md`.

## 2. Entrevista (AskUserQuestion, uma pergunta por vez)

Perguntas em linguagem de negócio. Nunca pergunte sobre banco, framework,
biblioteca ou deploy.

1. **O que essa aplicação precisa fazer?** (uma frase; se vier vago, peça um
   exemplo concreto do dia a dia da pessoa)
2. **Quem vai usar?** (só você / seu time / outra área)
3. **De onde vêm os dados?** Opções: planilha ou CSV · a pessoa digita na tela ·
   exportação do time de dados · ainda não sei
   - A aplicação tem banco próprio, um arquivo dentro do projeto, e **não se
     conecta ao banco da empresa**. Dado corporativo entra por CSV importado, e
     é uma cópia com a data da exportação. Se a pessoa disser que precisa do
     sistema ao vivo, anote e siga — quem resolve isso é o time de dados, e o
     `/planejar` trata depois.
4. **Essa aplicação lida com dado de beneficiário, CPF, carteirinha ou
   informação de saúde?** Opções: sim · não · não tenho certeza
   - "não tenho certeza" conta como **sim**.
5. **Qual o seu e-mail de trabalho?** É quem vai entrar na aplicação quando o
   login for ligado. Não é pergunta técnica: só guarde a resposta, não peça
   senha e não crie conta em lugar nenhum agora.

## 3. Escrever o projeto

Copie os arquivos de `${CLAUDE_PLUGIN_ROOT}/templates/` para a pasta atual e
preencha os placeholders `{{...}}` com as respostas:

| Arquivo | O que preencher |
|---|---|
| `CLAUDE.md` | nome, objetivo, quem usa, origem dos dados, flag de dado sensível |
| `package.json` | `{{SLUG_DO_PROJETO}}` — o nome em minúsculas, com hífen |
| `app/layout.tsx`, `app/page.tsx` | título e subtítulo da aplicação |
| `.env.example`, `.gitignore`, `tsconfig.json`, `next.config.ts`, `postcss.config.mjs`, `components.json` | mantenha como estão |
| `auth.ts`, `middleware.ts`, `prisma/`, `lib/`, `components/`, `app/entrar/`, `app/api/` | copie sem alterar |

Use `cp -R` para os arquivos que não mudam e Write só para os que têm
placeholder.

**Nunca** crie `.env` com valores reais. O hook bloqueia, e com razão.

## 4. Fechar o estado

Reescreva `.greenfield/state.json`:

```json
{
  "fase": "pronto",
  "nome": "...",
  "objetivo": "...",
  "usuarios": "...",
  "origem_dados": "...",
  "dado_sensivel": true,
  "email_criador": "..."
}
```

`fase: pronto` reativa a regra "sem PLANO.md, sem código".

## 5. Git

```
git init -b trabalho
git add -A
git commit -m "Projeto criado com /comecar"
```

Branch `trabalho`, não `main` — o hook bloqueia push em `main` e o usuário não
precisa saber por quê.

## 6. Provar que roda

```
npm install
npx prisma generate
npx prisma db push
npx prisma db seed
npm run dev
```

`db push` cria o arquivo `prisma/dev.db` e `db seed` põe 200 registros de
exemplo dentro. Os dois são obrigatórios: sem eles a tela abre vazia, e o
objetivo aqui é a pessoa ver uma tabela cheia no primeiro minuto.

Suba a aplicação em http://localhost:3000 e confirme que abre. Se não abrir,
conserte antes de dizer que terminou.

O banco é um arquivo dentro do projeto — não existe conta, servidor nem senha,
e não há nada a preencher no `.env` para ele. A aplicação também sobe sem exigir
login enquanto `AUTH_GOOGLE_ID` não estiver no `.env`. Não peça nada de Google
agora.

## 7. Fechar com o usuário

Três linhas, sem lista de arquivos:

- O que foi criado e como abrir de novo (`npm run dev`, endereço
  http://localhost:3000). Diga que os dados na tela são de exemplo e que dá para
  apagar e recomeçar quando quiser — o banco é um arquivo do projeto.
- Se marcou dado sensível: uma frase dizendo que o projeto está sob as regras
  de dado de saúde e que isso é automático.
- Próximo passo literal: **"Agora rode `/planejar` para dizer o que a
  aplicação precisa fazer."**

Guarde para depois, sem falar agora: quando a aplicação precisar de login de
verdade, o login é a conta Google da empresa, e ligá-lo exige um cliente OAuth
criado no Google Cloud Console. **Isso não é passo de marketing.** Quando o
momento chegar, ofereça as duas saídas, nesta ordem:

1. Pedir ao time de TI um "cliente OAuth de Aplicativo da Web" para esta
   aplicação, informando a URI de redirecionamento
   `http://localhost:3000/api/auth/callback/google` (e a URL de produção, se já
   existir). TI devolve `AUTH_GOOGLE_ID` e `AUTH_GOOGLE_SECRET`.
2. Se a pessoa quiser fazer sozinha, conduza pelo Google Cloud Console um passo
   por vez — APIs e Serviços → Credenciais → Criar credenciais → ID do cliente
   OAuth → Aplicativo da Web — e confira o URI de redirecionamento antes de
   fechar. Errar esse campo é o motivo nº 1 de o login não funcionar.

`AUTH_SECRET` você gera com `npx auth secret`, sem perguntar nada a ninguém.

`EMAILS_PERMITIDOS` é preenchido **na mesma hora** que as chaves, começando pelo
`email_criador` do `state.json` — a lista vazia não deixa ninguém entrar, e é
assim de propósito. Diga também, em uma frase, que estar logado no Google da
empresa não basta: só entra quem está na lista. Senha e recuperação de senha são
da conta Google — esta aplicação nunca guarda senha, e você nunca escreve tela
de "esqueci minha senha".

Ao publicar, a URL de produção precisa ser acrescentada nos URIs de
redirecionamento do mesmo cliente OAuth, com o final
`/api/auth/callback/google`. Sem isso o login funciona na máquina da pessoa e
quebra no ar — e o erro que o Google mostra (`redirect_uri_mismatch`) não diz
isso em português.
