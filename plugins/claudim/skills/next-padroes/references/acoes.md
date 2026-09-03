# Server action: zod, sessão, banco — o efeito por último

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
