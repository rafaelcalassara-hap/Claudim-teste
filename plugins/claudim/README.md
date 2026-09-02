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
- recriar tela de autocadastro: rota `criar-conta`/`sign-up`, formulário de
  cadastro
- coluna de senha, hash de senha (`bcrypt`, `argon2`) ou token de recuperação
- biblioteca de e-mail junto de assunto de senha — o e-mail de recuperação é da
  conta Google
- outra biblioteca de sessão (`@clerk/*`, `better-auth`, `lucia`, `iron-session`)
- provider `Credentials` do next-auth — é ele que traz a senha de volta para cá
- rota nova no `PUBLICO` do `middleware.ts` — só `/entrar` e `/api/auth` são
  públicas
- `exigirSessao()` ou o callback `signIn` reescrito sem `emailPermitido()`

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
| `next-padroes` | server/client, server action com zod e sessão, Tailwind v4, CSV, erro legível |
| `consultar-banco` | Prisma: o que pode escrever, teto de linhas, migração, PII mascarada |

## Subagents

O valor está na restrição de ferramentas, não na persona.

- `revisor` — `Read, Grep, Glob, Bash`. Não corrige enquanto revisa.
- `analista-dados` — mesma coisa, para pergunta sobre dado. Nunca imprime PII
  identificada no chat.

Não existe subagent "implementador": isso é o agente principal.

## Acesso

Toda aplicação nasce fechada, e não há tela de criar conta. Quem criou a
aplicação concede acesso editando uma linha do `.env`:

```
EMAILS_PERMITIDOS=@empresa.com.br,pessoa@parceiro.com
```

Três camadas: `middleware.ts` deixa públicas só `/entrar` e `/api/auth`;
`exigirSessao()` roda em toda página e toda action, porque action não é rota; e
a lista acima decide quem passa. Ter conta Google da empresa não é ter acesso —
a lista é quem autoriza, e ela é conferida duas vezes: no callback `signIn`, na
hora de entrar, e no `exigirSessao()`, a cada requisição, para quem sai da lista
perder o acesso sem esperar o cookie vencer. **Lista vazia não libera ninguém**,
de propósito: o erro caro aqui é a aplicação interna abrir para a internet.

Senha, cadastro e recuperação são da conta Google. Esta aplicação nunca guarda
senha, não tem tabela de usuário e não manda e-mail — a sessão é um cookie
assinado, sem `adapter` e sem linha no banco. O parâmetro `hd` na tela do Google
só sugere a conta da empresa; é a lista que barra, não ele.

## Stack fixo

Next.js (App Router) · React + Tailwind v4 + shadcn/ui · next-auth com a conta
Google da empresa · Prisma + SQLite. O plugin não pergunta e não oferece
alternativa.

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

## Escopo que falta

- **Deploy.** Hoje a aplicação roda na máquina de quem criou. `/publicar` é v2
  — o hook bloqueia `vercel --prod` até lá. Quando existir, o SQLite não vai
  junto: serverless não guarda arquivo, então deploy significa migrar para
  Postgres, e o histórico do Prisma é por provider (é regerar, não repetir).
- **Contas.** Quem cria o cliente OAuth no Google Cloud Console e como a pessoa
  recebe `AUTH_GOOGLE_ID` e `AUTH_GOOGLE_SECRET`. Dependência de infra, e a
  maior do plugin hoje: o público-alvo não faz esse passo sozinho. O `/comecar`
  manda pedir ao TI e explica o que pedir. O banco saiu dessa lista: é arquivo.
- **Dado corporativo.** Hoje só por CSV exportado à mão. Quem exporta, com que
  frequência, e por onde o arquivo trafega.
- **Suporte.** Quem responde quando o hook bloqueia e a pessoa não entende.
