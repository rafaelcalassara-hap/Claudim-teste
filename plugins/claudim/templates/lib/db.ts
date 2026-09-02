/** Cliente do Prisma.
 *
 * O banco é o arquivo `prisma/dev.db`, dentro do próprio projeto. Não há URL,
 * não há senha e não há nada a preencher no `.env`.
 *
 * Este arquivo só roda no servidor — se um componente com "use client"
 * importar daqui, o build quebra, e isso é proposital.
 */

import "server-only";
import { existsSync } from "node:fs";
import path from "node:path";
import { PrismaClient } from "@prisma/client";

const ARQUIVO_BANCO = path.join(process.cwd(), "prisma", "dev.db");

/** O banco é um arquivo, então "configurado" aqui é literalmente: ele existe.
 *
 * `/comecar` cria e popula o arquivo. Se alguém apagar, a tela cai para dado de
 * exemplo em vez de quebrar, e gravar avisa em português em vez de estourar. */
export function bancoConfigurado(): boolean {
  return existsSync(ARQUIVO_BANCO);
}

const global_ = globalThis as unknown as { prisma?: PrismaClient };

// Em desenvolvimento o Next recarrega o módulo a cada alteração. Sem este
// cache, cada recarga abre uma conexão nova e o banco derruba a aplicação.
export const db =
  global_.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["warn", "error"] : ["error"],
  });

if (process.env.NODE_ENV !== "production") global_.prisma = db;
