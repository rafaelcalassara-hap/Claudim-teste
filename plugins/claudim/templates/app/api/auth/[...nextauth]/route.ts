/** As rotas de entrar e sair. O arquivo é só isto: quem responde é o `auth.ts`.
 *
 * É a segunda — e última — rota pública do `middleware.ts`. Sem ela o Google
 * não tem para onde devolver a pessoa depois do login.
 */

import { handlers } from "@/auth";

export const { GET, POST } = handlers;
