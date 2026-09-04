# Quem pode entrar

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

Um hook bloqueia cada um desses casos na hora da escrita. Se o bloqueio chegar,
ele está certo: leia o próximo passo que a mensagem dá e faça aquilo.

## Ligar o login

O login é a conta Google da empresa, e ligá-lo exige um cliente OAuth
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
