"use server";

/** Server actions.
 *
 * Uma action é um endpoint HTTP com outra cara: qualquer pessoa logada — ou
 * não — pode chamá-la direto, sem passar pela sua tela. Por isso toda action
 * repete as duas verificações, nesta ordem:
 *
 *   1. zod valida a entrada (o que chega do navegador é texto, não é confiável);
 *   2. a sessão é checada, antes de qualquer efeito no banco;
 *   3. o banco é conferido — a tela cai para dado de exemplo quando ele não
 *      está configurado, mas gravar não tem como cair para lugar nenhum.
 */

import { revalidatePath } from "next/cache";
import { z } from "zod";
import { exigirSessao } from "@/lib/auth";
import { bancoConfigurado, db } from "@/lib/db";

const EntradaEvento = z.object({
  canal: z.string().min(1, "Escolha um canal.").max(60),
  uf: z.string().length(2, "UF tem duas letras."),
  valor: z.coerce.number().positive("O valor precisa ser maior que zero."),
});

export type Resultado = { ok: true } | { ok: false; erro: string };

export async function registrarEvento(_anterior: unknown, form: FormData): Promise<Resultado> {
  const entrada = EntradaEvento.safeParse(Object.fromEntries(form));
  if (!entrada.success) {
    return { ok: false, erro: entrada.error.issues[0].message };
  }

  const usuarioId = await exigirSessao();

  // A tela lê de `dados-sinteticos` enquanto o banco não está configurado, mas
  // não existe equivalente sintético para gravar: sem banco, salvar estoura com
  // erro de conexão. Diga isso em português, antes de tentar.
  if (!bancoConfigurado()) {
    return {
      ok: false,
      erro:
        "Ainda não dá para salvar: esta aplicação está rodando com dados de " +
        "exemplo. Para salvar de verdade, preencha DATABASE_URL no arquivo .env.",
    };
  }

  try {
    await db.evento.create({
      // Centavos, inteiro: o schema não guarda número quebrado. Ver schema.prisma.
      data: {
        canal: entrada.data.canal,
        uf: entrada.data.uf,
        valorCentavos: Math.round(entrada.data.valor * 100),
      },
    });
  } catch (erro) {
    // Banco configurado, mas fora do ar. O nome do erro vai como detalhe —
    // stack trace na tela não ajuda quem vai ler.
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
