/** Sessão. Toda leitura de dado e toda server action passa por aqui.
 *
 * O middleware já barra quem não está logado, mas ele protege *rotas*.
 * Server action é um endpoint HTTP: dá para chamá-la sem passar por página
 * nenhuma. Por isso a checagem é repetida dentro da action.
 */

import "server-only";
import { auth, currentUser } from "@clerk/nextjs/server";
import {
  clerkConfigurado,
  ehProducao,
  emailPermitido,
  emailsPermitidos,
} from "./config";

export async function exigirSessao(): Promise<string> {
  if (!clerkConfigurado()) {
    // Em desenvolvimento, antes de existir conta de Clerk, a tela roda sem
    // login para a pessoa ver o resultado. Em produção isso seria uma
    // aplicação interna aberta na internet — então nem sobe.
    if (ehProducao) {
      throw new Error(
        "Login não está configurado. Preencha as chaves do Clerk no .env antes de publicar.",
      );
    }
    return "sem-login-ainda";
  }

  const { userId } = await auth();
  if (!userId) {
    throw new Error("Sessão expirada. Entre de novo para continuar.");
  }

  // Logado não é o mesmo que autorizado. Qualquer pessoa pode criar uma conta
  // no Clerk; só quem está em EMAILS_PERMITIDOS entra nesta aplicação.
  if (emailsPermitidos().length === 0) {
    throw new Error(
      "Ninguém tem acesso liberado ainda. Preencha EMAILS_PERMITIDOS no arquivo .env com o seu e-mail.",
    );
  }

  // `currentUser()` em vez de ler o e-mail do token: o Clerk só põe o e-mail no
  // token se alguém configurar um claim customizado no painel, e passo de painel
  // esquecido aqui vira aplicação aberta. Esta chamada é cacheada por requisição.
  const usuario = await currentUser();
  if (!emailPermitido(usuario?.primaryEmailAddress?.emailAddress)) {
    throw new Error(
      "Seu e-mail não tem acesso a esta aplicação. Peça a quem criou para incluir você em EMAILS_PERMITIDOS.",
    );
  }

  return userId;
}
