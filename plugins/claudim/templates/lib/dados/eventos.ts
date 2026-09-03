/** Tudo que lê ou escreve na tabela `eventos`.
 *
 * Uma tabela, um arquivo. A tela não fala com o Prisma e a server action
 * também não — as duas chamam daqui. É isso que mantém num lugar só as quatro
 * regras que este projeto não abre mão:
 *
 *   1. `take` — toda leitura de lista tem teto de linhas;
 *   2. `select` — colunas explícitas, para PII não vir junto sem ninguém pedir;
 *   3. mascaramento antes de o dado sair do servidor;
 *   4. centavos viram reais só na saída.
 *
 * Espalhadas por página e action, essas quatro dependem de alguém lembrar.
 * Aqui, é um arquivo só para conferir — e é onde o `/revisar` vai olhar.
 *
 * **Não transforme isso num framework.** São funções `async` exportadas, nada
 * mais: sem classe, sem repositório genérico, sem interface, sem par
 * entidade/DTO. O que a função devolve é o que a tela mostra. Tabela nova é
 * arquivo novo com o nome da tabela, não uma camada nova.
 */

import "server-only";
import { bancoConfigurado, db } from "@/lib/db";
import { tabelaExemplo } from "@/lib/dados/sinteticos";
import { mascararRegistros } from "@/lib/pii";

/** Teto de linhas. Tabela grande sem limite derruba a página. */
const TETO = 1000;

/** O que a tela recebe: mascarado, formatado, sem Date e sem centavos crus. */
export type EventoNaTela = Record<string, string | number>;

/** O banco guarda centavos (inteiro); a tela mostra reais. A conversão mora
 *  aqui, na saída — se a coluna `valorCentavos` chegar crua na tabela, a pessoa
 *  lê 1990 onde deveria ler R$ 19,90. */
const emReais = (centavos: number) =>
  (centavos / 100).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export async function listarEventos({ dias }: { dias: number }): Promise<EventoNaTela[]> {
  // Sem banco a tela ainda abre, com dado falso — e passando pelo mesmo
  // mascaramento e pela mesma formatação do caminho real. O dado é de mentira;
  // o código que a tela exercita tem que ser o de produção.
  if (!bancoConfigurado()) {
    return mascararRegistros(
      tabelaExemplo(200).map(({ valor, ...resto }) => ({
        ...resto,
        valor: emReais(Math.round(valor * 100)),
      })),
    );
  }

  const desde = new Date(Date.now() - dias * 86_400_000);
  const linhas = await db.evento.findMany({
    where: { criadoEm: { gte: desde } },
    select: { id: true, criadoEm: true, canal: true, uf: true, valorCentavos: true },
    orderBy: { criadoEm: "desc" },
    take: TETO,
  });

  return mascararRegistros(
    linhas.map(({ valorCentavos, ...resto }) => ({ ...resto, valor: emReais(valorCentavos) })),
  );
}

/** Grava um evento. Quem chama é a server action, e é lá que ficam o zod, a
 *  checagem de sessão e o `bancoConfigurado()` — nesta ordem, antes daqui. */
export async function criarEvento(dados: {
  canal: string;
  uf: string;
  valor: number;
}): Promise<void> {
  await db.evento.create({
    data: {
      canal: dados.canal,
      uf: dados.uf,
      // Centavos, inteiro: o schema não guarda número quebrado. Ver schema.prisma.
      valorCentavos: Math.round(dados.valor * 100),
    },
  });
}
