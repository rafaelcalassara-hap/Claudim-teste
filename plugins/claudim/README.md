# claudim

Plugin para pessoas de **áreas não-técnicas** construírem aplicações internas.

Todo o resto do desenho sai dessa frase: quem usa não sabe depurar, não escolhe
stack, não sabe git e não escreve teste. Por isso guardrail que só avisa não
serve — tem que bloquear.

## Os quatro comandos

| Comando | Quando |
|---|---|
| `/comecar` | uma vez, em pasta vazia — cria o projeto |
| `/planejar` | define o que construir; grava `PLANO.md` |
| `/construir` | implementa o plano e sobe a aplicação |
| `/revisar` | auditoria read-only de compliance e do que ficou faltando |

O laço normal é `/construir` → `/revisar` até ficar bom.

## O que os hooks bloqueiam

Bloqueio = exit code 2, mensagem em português, sempre com o próximo passo.

**PreToolUse · Write/Edit** (`guard_write.py`)
- escrever `.env`, `*.pem`, `*.key`, `credentials*`, chave de service account
- senha, chave de API ou token colados dentro do código
- segredo atrás de `NEXT_PUBLIC_` — esse prefixo publica o valor no navegador
- escrever qualquer código-fonte antes de existir `PLANO.md` *(só em projeto
  criado pelo `/comecar` — fora dele, não atrapalha)*

**PreToolUse · Write/Edit** (`guard_pii.py`)
- CPF ou CNS com dígito verificador **válido** dentro de arquivo
- condição de saúde em fixture, seed ou CSV de exemplo
- condição de saúde dentro de chamada de tracking/pixel/dataLayer

**PreToolUse · Write/Edit** (`guard_auth.py`)
- recriar tela de autocadastro: rota `criar-conta`/`sign-up`, `<SignUp />`
- coluna de senha, hash de senha (`bcrypt`, `argon2`) ou token de recuperação
- biblioteca de e-mail junto de assunto de senha — o e-mail de recuperação é do
  Clerk
- outra biblioteca de sessão (`next-auth`, `better-auth`, `lucia`, `iron-session`)
- rota nova no `createRouteMatcher` do `middleware.ts` — só `/entrar` é pública
- `exigirSessao()` reescrito sem a checagem de `emailPermitido()`

**PreToolUse · Bash** (`guard_bash.py`)
- `git push` para `main`/`master`, e push forçado
- `rm -rf`, `git reset --hard`, `git clean -f`
- `DROP TABLE`, `DROP DATABASE`, `TRUNCATE`, `DELETE FROM` sem `WHERE`
- `prisma migrate reset` e `db push --force-reset` (apagam o banco inteiro)
- `vercel --prod` e `vercel promote` — publicar não faz parte do processo ainda
- `rm` de arquivo `.db` — isso é o banco inteiro da aplicação

**PostToolUse · Write/Edit** (`post_format.py`)
- `prettier --write` em `.ts/.tsx/.css/.json/.md`, usando o prettier do próprio
  projeto. Silencioso. Nunca bloqueia.

**SessionStart** (`session_state.py`)
- injeta estado: passos abertos do `PLANO.md`, branch, alterações não
  commitadas, flag de dado sensível. Não é banner.

## Skills

| Skill | Assunto |
|---|---|
| `escrever-plano` | transformar pedido vago em `PLANO.md` com critério de negócio |
| `dados-sensiveis` | LGPD Art. 11, vazamento por URL/evento, ANS |
| `next-padroes` | server/client, server action com zod e sessão, Tailwind v4, design system, CSV, erro legível |
| `consultar-banco` | Prisma: o que pode escrever, teto de linhas, migração, PII mascarada |

## Subagents

O valor está na restrição de ferramentas, não na persona.

- `revisor` — `Read, Grep, Glob, Bash`. Não corrige enquanto revisa. Audita
  também desvio do design system: hex solto, cor arbitrária, token órfão.
- `analista-dados` — mesma coisa, para pergunta sobre dado. Nunca imprime PII
  identificada no chat.

Não existe subagent "implementador": isso é o agente principal.

## Acesso

Toda aplicação nasce fechada, e não há tela de criar conta. Quem criou a
aplicação concede acesso editando uma linha do `.env`:

```
EMAILS_PERMITIDOS=@empresa.com.br,pessoa@parceiro.com
```

Três camadas: `middleware.ts` deixa pública só `/entrar`; `exigirSessao()` roda
em toda página e toda action, porque action não é rota; e a lista acima decide
quem passa. Ter conta no Clerk não é ter acesso — o Clerk autentica qualquer um
que se cadastre, a lista é quem autoriza. **Lista vazia não libera ninguém**, de
propósito: o erro caro aqui é a aplicação interna abrir para a internet.

Senha, cadastro e recuperação são telas do Clerk. Esta aplicação nunca guarda
senha, não tem tabela de usuário e não manda e-mail. A instância do Clerk fica
em "Restricted" no painel — sem isso, autocadastro continua aberto.

## Stack fixo

Next.js (App Router) · React + Tailwind v4 + shadcn/ui · Clerk para sessão ·
Prisma + SQLite. O plugin não pergunta e não oferece alternativa.

Três consequências que valem dizer em voz alta:

- **Tem build e tem Node.** É mais peso do que o público-alvo carregava antes.
  O `/comecar` verifica o Node e faz o `npm install` sozinho; se faltar Node,
  ele para e manda pedir ao TI, em vez de tentar instalar.
- **O banco é um arquivo.** `prisma/dev.db`, dentro do projeto: sem conta, sem
  servidor, sem senha, nada a preencher no `.env`. Foi a escolha deliberada
  contra Postgres hospedado e contra container — nenhum dos dois o público-alvo
  consegue provisionar sozinho, e a aplicação hoje roda na máquina de quem
  criou. Custo aceito: dinheiro vira `Int` em centavos, nada de tipo nativo
  (`@db.Decimal`) e um escritor por vez.
- **Não há conexão com o banco da empresa.** Dado corporativo entra por CSV
  exportado pelo time de dados — é uma cópia, com a data da exportação. Consulta
  ao vivo em sistema corporativo não existe nesta versão.

O scaffold sobe com 200 registros de exemplo já no banco e sem exigir login
enquanto o `.env` estiver vazio — a pessoa vê a tela cheia no primeiro minuto,
e gravar funciona de verdade desde o começo. `exigirSessao()` recusa rodar sem
login em produção, então isso não vira uma aplicação interna aberta na internet.

## Design system

O scaffold nasce com um design system em `docs/design-system/`, e o `@theme` do
`app/globals.css` é o espelho dele — cada token traz o de-para em comentário
(`--color-marca` ↔ `DS --primary`).

| Arquivo | Leitor | O que tem |
|---|---|---|
| `docs/design-system/DESIGN.md` | agente | YAML com paleta, tipografia, raio, sombra, espaçamento e a receita de cada componente |
| `docs/design-system/DS-ACME.md` | pessoa | anatomia de componente, do/don't, acessibilidade |
| `app/globals.css` | Tailwind | os mesmos valores com nome em português, virando utilitária |

Duas perguntas diferentes, dois arquivos: *qual é o valor* é pergunta de
máquina, *como eu uso* é pergunta de gente. Num arquivo só, o agente gasta
contexto lendo prosa e a pessoa caça a regra no meio de uma tabela de tokens.

O que isso muda na prática: o `/construir` lê o `DESIGN.md` antes de escrever
tela, e o `/revisar` reprova hex solto na classe, cor arbitrária do Tailwind
(`bg-blue-600`) e token novo no `@theme` sem par no DS — que é como nasce uma
segunda paleta. Design system que ninguém verifica vira documento morto.

A marca é fictícia, e é para ser trocada. Empresa com DS próprio substitui os
dois arquivos e ajusta o `@theme`. Nenhum componente muda: `page.tsx` e
`button.tsx` não conhecem hex, só utilitária de token.

## Escopo que falta

- **Deploy.** Hoje a aplicação roda na máquina de quem criou. `/publicar` é v2
  — o hook bloqueia `vercel --prod` até lá. Quando existir, o SQLite não vai
  junto: serverless não guarda arquivo, então deploy significa migrar para
  Postgres, e o histórico do Prisma é por provider (é regerar, não repetir).
- **Contas.** Quem provisiona o projeto no Clerk e como a pessoa recebe as
  chaves. Dependência de infra. O banco saiu dessa lista: é arquivo.
- **Dado corporativo.** Hoje só por CSV exportado à mão. Quem exporta, com que
  frequência, e por onde o arquivo trafega.
- **Suporte.** Quem responde quando o hook bloqueia e a pessoa não entende.
