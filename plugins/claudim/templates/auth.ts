/** Configuração da sessão. Login pelo Google da empresa, e nada além disso.
 *
 * Sem `adapter`: a sessão é um cookie assinado (JWT), não uma linha no banco.
 * É de propósito — esta aplicação não tem tabela de usuário, não guarda senha
 * e não cria conta. A conta é a do Google Workspace; aqui só se decide quem
 * entra.
 *
 * Também é o que faz o login funcionar antes do banco existir: o `/comecar`
 * sobe a tela no primeiro minuto, e sessão em banco quebraria isso.
 */

import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import { emailPermitido } from "@/lib/config";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Google({
      authorization: {
        params: {
          // `hd` só faz a tela do Google já sugerir a conta da empresa. É uma
          // dica, não uma tranca: dá para tirar da URL. Quem barra de verdade
          // é o callback `signIn` abaixo. Nunca confie no `hd` sozinho.
          hd: process.env.DOMINIO_GOOGLE,
          prompt: "select_account",
        },
      },
    }),
  ],

  session: { strategy: "jwt" },
  pages: { signIn: "/entrar" },

  callbacks: {
    /** A porta. Quem não está na lista não chega a ter sessão nenhuma.
     *
     * `email_verified` junto porque o e-mail é a identidade aqui: é ele que a
     * lista compara. E-mail não verificado seria alguém dizendo ser outra
     * pessoa.
     */
    signIn({ profile }) {
      return profile?.email_verified === true && emailPermitido(profile.email);
    },
  },
});
