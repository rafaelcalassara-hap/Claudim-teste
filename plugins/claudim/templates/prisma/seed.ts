/** Popula o banco com dado de exemplo, para a tela ter o que mostrar.
 *
 * Rode com: npx prisma db seed
 *
 * Regra que não muda: o que entra aqui é gerado por `lib/dados/sinteticos.ts`.
 * Dado de pessoa real não entra em arquivo — nem neste. O hook do plugin
 * bloqueia CPF ou carteirinha de verdade, e condição de saúde em seed.
 */

import { PrismaClient } from "@prisma/client";
import { tabelaExemplo } from "../lib/dados/sinteticos";

const db = new PrismaClient();

async function main() {
  const linhas = tabelaExemplo(200);
  await db.evento.createMany({
    data: linhas.map((l) => ({
      criadoEm: new Date(l.criadoEm),
      canal: l.canal,
      uf: l.uf,
      // Centavos, inteiro — ver o comentário no schema.
      valorCentavos: Math.round(l.valor * 100),
    })),
  });
  console.info(`${linhas.length} eventos de exemplo criados.`);
}

main()
  .catch((erro) => {
    console.error("Não consegui popular o banco:", (erro as Error).message);
    process.exit(1);
  })
  .finally(() => db.$disconnect());
