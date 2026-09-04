/** Mascaramento e hash de dado pessoal.
 *
 * LGPD Art. 11: aqui é operadora de saúde, então dado de beneficiário é
 * sensível. Mascare no servidor, antes de o dado atravessar para o navegador —
 * o que um Server Component passa para um componente "use client" viaja
 * inteiro no payload da página e aparece no DevTools de quem abrir.
 */

import "server-only";
import { createHash } from "node:crypto";

const somenteDigitos = (v: unknown) => String(v ?? "").replace(/\D/g, "");

export function mascararCpf(valor: unknown): string {
  const d = somenteDigitos(valor);
  if (d.length !== 11) return "***";
  return `***.${d.slice(3, 6)}.${d.slice(6, 9)}-**`;
}

export function mascararCns(valor: unknown): string {
  const d = somenteDigitos(valor);
  if (d.length !== 15) return "***";
  return `${d.slice(0, 3)} **** **** ${d.slice(-4)}`;
}

export function mascararNome(valor: unknown): string {
  const partes = String(valor ?? "")
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  if (partes.length === 0) return "***";
  if (partes.length === 1) return partes[0];
  return `${partes[0]} ${partes[partes.length - 1][0]}.`;
}

export function mascararEmail(valor: unknown): string {
  const texto = String(valor ?? "");
  if (!texto.includes("@")) return "***";
  const [usuario, dominio] = texto.split("@");
  return `${usuario.slice(0, 2)}***@${dominio}`;
}

export function mascararTelefone(valor: unknown): string {
  const d = somenteDigitos(valor);
  return d ? `****-${d.slice(-4)}` : "***";
}

/** Para cruzar bases sem guardar o número. Precisa de PII_SALT no .env. */
export function hashCpf(valor: unknown): string {
  const salt = process.env.PII_SALT;
  if (!salt) throw new Error("PII_SALT não configurado no .env.");
  return createHash("sha256")
    .update(`${salt}${somenteDigitos(valor)}`)
    .digest("hex");
}

const REGRAS: [RegExp, (v: unknown) => string][] = [
  [/cpf/i, mascararCpf],
  [/cns|carteirinha/i, mascararCns],
  [/e_?mail/i, mascararEmail],
  [/telefone|celular/i, mascararTelefone],
  [/nome|beneficiari/i, mascararNome],
];

/**
 * Passe o resultado da consulta por aqui antes de devolvê-lo do Server
 * Component. Devolve objetos simples (sem Decimal, sem Date), que é o que
 * atravessa a fronteira servidor → navegador sem erro de serialização.
 */
export function mascararRegistros<T extends Record<string, unknown>>(
  linhas: T[],
): Record<string, string | number>[] {
  return linhas.map((linha) => {
    const saida: Record<string, string | number> = {};
    for (const [coluna, valor] of Object.entries(linha)) {
      const regra = REGRAS.find(([padrao]) => padrao.test(coluna));
      if (regra) {
        saida[coluna] = regra[1](valor);
      } else if (valor instanceof Date) {
        saida[coluna] = valor.toISOString();
      } else if (typeof valor === "object" && valor !== null) {
        saida[coluna] = String(valor); // Decimal do Prisma cai aqui
      } else {
        saida[coluna] = valor as string | number;
      }
    }
    return saida;
  });
}
