import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import { clerkConfigurado } from "@/lib/config";

// Aplicação interna: tudo exige sessão, menos a tela de entrada.
// Uma porta pública só. Não existe tela de criar conta: quem dá acesso é quem
// criou a aplicação, pela lista EMAILS_PERMITIDOS do .env.
// Adicionar rota pública aqui é decisão consciente, não conveniência.
const publico = createRouteMatcher(["/entrar(.*)"]);

const protegido = clerkMiddleware(async (auth, req) => {
  if (!publico(req)) {
    await auth.protect();
  }
});

// Enquanto o Clerk não estiver no .env, a aplicação roda sem login para a
// pessoa ver a tela. `exigirSessao()` impede que isso chegue a produção.
export default clerkConfigurado() ? protegido : () => NextResponse.next();

export const config = {
  matcher: ["/((?!_next|.*\\..*).*)", "/(api|trpc)(.*)"],
};
