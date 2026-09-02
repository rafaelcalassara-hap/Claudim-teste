import { NextResponse } from "next/server";
import { auth } from "@/auth";
import { authConfigurado } from "@/lib/config";

// Aplicação interna: tudo exige sessão, menos duas portas — a tela de entrada
// e o retorno do Google, que precisa ser público senão o login não fecha o
// ciclo. Não existe tela de criar conta: quem dá acesso é quem criou a
// aplicação, pela lista EMAILS_PERMITIDOS do .env.
// Acrescentar rota aqui é decisão consciente, não conveniência.
const PUBLICO = ["/entrar", "/api/auth"];

const protegido = auth((req) => {
  const rota = req.nextUrl.pathname;
  if (PUBLICO.some((publica) => rota.startsWith(publica))) return NextResponse.next();
  if (!req.auth) return NextResponse.redirect(new URL("/entrar", req.url));
  return NextResponse.next();
});

// Enquanto o Google não estiver no .env, a aplicação roda sem login para a
// pessoa ver a tela. `exigirSessao()` impede que isso chegue a produção.
export default authConfigurado() ? protegido : () => NextResponse.next();

export const config = {
  matcher: ["/((?!_next|.*\\..*).*)", "/(api|trpc)(.*)"],
};
