/** Sessão. Toda leitura de dado e toda server action passa por aqui.
 *
 * O middleware já barra quem não está logado, mas ele protege *rotas*.
 * Server action é um endpoint HTTP: dá para chamá-la sem passar por página
 * nenhuma. Por isso a checagem é repetida dentro da action.
 */

import "server-only";
import { auth } from "@/auth";
import { authConfigurado, ehProducao, emailPermitido, emailsPermitidos } from "./config";

export async function exigirSessao(): Promise<string> {
  if (!authConfigurado()) {
    // Em desenvolvimento, antes de existir o cliente OAuth do Google, a tela
    // roda sem login para a pessoa ver o resultado. Em produção isso seria uma
    // aplicação interna aberta na internet — então nem sobe.
    if (ehProducao) {
      throw new Error(
        "Login não está configurado. Preencha AUTH_GOOGLE_ID, AUTH_GOOGLE_SECRET e AUTH_SECRET no .env antes de publicar.",
      );
    }
    return "sem-login-ainda";
  }

  const sessao = await auth();
  if (!sessao?.user?.email) {
    throw new Error("Sessão expirada. Entre de novo para continuar.");
  }

  if (emailsPermitidos().length === 0) {
    throw new Error(
      "Ninguém tem acesso liberado ainda. Preencha EMAILS_PERMITIDOS no arquivo .env com o seu e-mail.",
    );
  }

  // Repetido de propósito, mesmo o callback `signIn` do `auth.ts` já tendo
  // conferido na hora de entrar: quem sai da lista precisa perder o acesso na
  // requisição seguinte, não só no próximo login. O e-mail já vem no cookie da
  // sessão — não há segunda chamada de rede aqui.
  if (!emailPermitido(sessao.user.email)) {
    throw new Error(
      "Seu e-mail não tem acesso a esta aplicação. Peça a quem criou para incluir você em EMAILS_PERMITIDOS.",
    );
  }

  return sessao.user.email;
}
