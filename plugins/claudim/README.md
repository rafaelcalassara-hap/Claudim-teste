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

**PreToolUse · Write/Edit** (`guard_ds.py`)
- cor escrita direto no componente: `bg-[#0055ff]`, hex em `style={{...}}`
- cor da paleta genérica do Tailwind: `bg-blue-600`, `text-gray-500`
- classe de tema sem token no `DESIGN.md` — a utilitária nem existiria
- editar `app/globals.css`, que é arquivo gerado

*Só age em projeto que tem `docs/design-system/DESIGN.md`. Sem design system,
não atrapalha.*

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

Uma fonte de verdade por coisa. Aqui a coisa é tema, e a fonte é
`docs/design-system/DESIGN.md` — cor, tipografia, raio, sombra e espaçamento
vivem lá e em nenhum outro lugar.

| Arquivo | Responde | Não responde |
|---|---|---|
| `docs/design-system/DESIGN.md` | **qual é o valor.** YAML com cor, tipografia, raio, sombra, espaçamento, receita de componente | como usar |
| `docs/design-system/DS-ACME.md` | **como usar.** Anatomia de 22 componentes, variantes, estados, faça/não faça, acessibilidade | valor — cita token por nome, nunca por hex |
| `docs/design-system/gerar-tema.py` | lê o `DESIGN.md` e escreve os derivados |
| `app/globals.css` | **gerado** — o `@theme` do Tailwind |
| `docs/design-system/showcase.html` | **gerado** — os tokens renderizados |

Cada instrução do plugin aponta os dois pela pergunta que respondem: "preciso
de uma cor" → `DESIGN.md`; "vou montar um card" → `DS-ACME.md` §7. Um agente
que lê só o primeiro pega o hex certo e monta o header do jeito que quiser —
foi o furo que este arranjo fecha.

O nome da utilitária é o nome do token, sem tradução no meio:
`--color-primary` gera `bg-primary`. Não existe um segundo vocabulário, e
`page.tsx` e `button.tsx` não conhecem hex — trocar o tema é editar o
`DESIGN.md` e rodar o gerador.

Dois níveis de verificação, porque guardrail que só avisa não serve:

- **`guard_ds.py` bloqueia na hora da escrita** — cor literal, cor do Tailwind,
  classe sem token, edição do `globals.css` gerado. Exit 2, com o token certo
  na mensagem.
- **`gerar-tema.py --checar` fecha a rodada** — pega o que o hook não vê, como
  derivado que ficou fora de sincronia. Roda no `/construir`, no `/revisar` e
  no checklist de release.

Design system que ninguém verifica vira documento morto: antes deste arranjo o
guia citava um `--color-high-contrast` que nunca existiu e o showcase tinha
três cores inventadas na mão.

A marca é fictícia e existe para ser trocada.

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
