/** Qual parte da infraestrutura já foi configurada no `.env`.
 *
 * O projeto sobe com a tela funcionando antes de existir cliente OAuth do
 * Google — é assim de propósito, para a pessoa ver o resultado no primeiro
 * minuto. O que não pode é isso virar produção sem login: veja `lib/auth.ts`.
 *
 * O banco não entra aqui: ele é um arquivo, e quem responde se existe é
 * `bancoConfigurado()` em `lib/db.ts` — que usa `fs` e por isso não pode ser
 * importado pelo `middleware.ts`.
 *
 * Sem `server-only` aqui: o `middleware.ts` também precisa desta checagem.
 * Nenhuma destas variáveis tem `NEXT_PUBLIC_` — com o login pelo Google não
 * existe chave que precise ir para o navegador.
 */

export function authConfigurado(): boolean {
  const id = process.env.AUTH_GOOGLE_ID ?? "";
  return id.endsWith(".apps.googleusercontent.com") && !!process.env.AUTH_SECRET;
}

/** Quem pode entrar nesta aplicação.
 *
 * Ter conta no Google da empresa não é o mesmo que ter acesso aqui. Esta lista
 * é a fronteira, e ela é consultada duas vezes: no callback `signIn` do
 * `auth.ts` (na hora de entrar) e no `exigirSessao()` (a cada requisição).
 *
 * Formato: `@dominio.com.br` libera o domínio inteiro; `pessoa@empresa.com`
 * libera uma pessoa. Separe por vírgula.
 */
export function emailsPermitidos(): string[] {
  return (process.env.EMAILS_PERMITIDOS ?? "")
    .split(",")
    .map((regra) => regra.trim().toLowerCase())
    .filter(Boolean);
}

export function emailPermitido(email: string | null | undefined): boolean {
  const regras = emailsPermitidos();
  // Lista vazia não libera geral: sem regra, ninguém entra. Falhar fechado é
  // proposital — o erro caro aqui é a aplicação interna abrir para qualquer um.
  if (regras.length === 0) return false;

  const alvo = (email ?? "").trim().toLowerCase();
  if (!alvo) return false;

  return regras.some((regra) =>
    regra.startsWith("@") ? alvo.endsWith(regra) : alvo === regra,
  );
}

export const ehProducao = process.env.NODE_ENV === "production";
