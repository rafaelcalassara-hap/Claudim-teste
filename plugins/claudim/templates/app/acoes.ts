"use server";

/** Server actions desta rota.
 *
 * Uma action é um endpoint HTTP com outra cara: qualquer pessoa logada — ou
 * não — pode chamá-la direto, sem passar pela sua tela, e o `middleware.ts`
 * não cobre isso. Por isso toda action repete as três verificações, nesta
 * ordem, antes de qualquer efeito:
 *
 *   1. zod valida a entrada (o que chega do navegador é texto, não é confiável);
 *   2. a sessão é checada;
 *   3. o banco é conferido — a tela cai para dado de exemplo quando ele não
 *      existe, mas gravar não tem como cair para lugar nenhum.
 *
 * O que a action **não** faz é falar com o Prisma. A escrita mora em
 * `lib/dados/eventos.ts`, junto com a leitura da mesma tabela. Aqui fica o
 * portão; lá fica a tabela.
 *
 * Rota nova ganha o seu próprio `app/<rota>/acoes.ts`. Não empilhe as actions
 * do projeto inteiro neste arquivo.
 */

import { revalidatePath } from "next/cache";
import { z } from "zod";
import { exigirSessao } from "@/lib/auth";
import { criarEvento } from "@/lib/dados/eventos";
import { bancoConfigurado } from "@/lib/db";

const EntradaEvento = z.object({
  canal: z.string().min(1, "Escolha um canal.").max(60),
  uf: z.string().length(2, "UF tem duas letras."),
  valor: z.coerce.number().positive("O valor precisa ser maior que zero."),
});

export type Resultado = { ok: true } | { ok: false; erro: string };

export async function registrarEvento(
  _anterior: unknown,
  form: FormData,
): Promise<Resultado> {
  const entrada = EntradaEvento.safeParse(Object.fromEntries(form));
  if (!entrada.success) {
    return { ok: false, erro: entrada.error.issues[0].message };
  }

  const usuarioId = await exigirSessao();

  // A tela lê de `lib/dados/sinteticos.ts` enquanto o arquivo do banco não
  // existe, mas não há equivalente sintético para gravar: sem banco, salvar
  // estoura. Diga isso em português, antes de tentar.
  if (!bancoConfigurado()) {
    return {
      ok: false,
      erro:
        "Ainda não dá para salvar: esta aplicação está rodando com dados de " +
        "exemplo. Rode `npx prisma db push` para criar o banco.",
    };
  }

  try {
    await criarEvento(entrada.data);
  } catch (erro) {
    // Banco criado, mas o arquivo sumiu ou travou. O nome do erro vai como
    // detalhe — stack trace na tela não ajuda quem vai ler.
    return {
      ok: false,
      erro: `Não consegui salvar agora. Tente de novo em instantes. Detalhe técnico: ${(erro as Error).name}`,
    };
  }

  // Log com o id da sessão, nunca com o registro inteiro.
  console.info(`evento criado por ${usuarioId}`);

  revalidatePath("/");
  return { ok: true };
}
