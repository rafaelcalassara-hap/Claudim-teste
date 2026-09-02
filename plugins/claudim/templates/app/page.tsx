/** {{NOME_DO_PROJETO}} — {{OBJETIVO}}
 *
 * Server Component: busca no servidor e manda HTML pronto. Não tem
 * "use client" aqui, então nada deste arquivo vai para o navegador — só o
 * resultado já mascarado.
 */

import { ExportarCsv } from "@/components/exportar-csv";
import { exigirSessao } from "@/lib/auth";
import { bancoConfigurado, db } from "@/lib/db";
import { tabelaExemplo } from "@/lib/dados-sinteticos";
import { mascararRegistros } from "@/lib/pii";

// Esta tela lê a sessão e o banco a cada acesso — não dá para gerar no build.
export const dynamic = "force-dynamic";

const PERIODOS = [7, 30, 90, 180];

async function carregar(dias: number) {
  // Troque o corpo desta função pela consulta real quando o banco estiver
  // configurado. Enquanto não estiver, a tela roda com dado sintético.
  // Passa pelo mesmo mascaramento do caminho real: o dado é falso, mas o
  // código que a tela exercita tem que ser o de produção.
  if (!bancoConfigurado()) return mascararRegistros(tabelaExemplo(200));

  const desde = new Date(Date.now() - dias * 86_400_000);
  const linhas = await db.evento.findMany({
    where: { criadoEm: { gte: desde } },
    select: { id: true, criadoEm: true, canal: true, uf: true, valorCentavos: true },
    orderBy: { criadoEm: "desc" },
    take: 1000, // sempre um teto: tabela de fato sem limite derruba a página
  });

  // O banco guarda centavos (inteiro); a tela mostra reais. Converta aqui, na
  // saída — não deixe a coluna `valorCentavos` chegar crua na tabela, senão a
  // pessoa lê 1990 onde deveria ler R$ 19,90.
  const paraTela = linhas.map(({ valorCentavos, ...resto }) => ({
    ...resto,
    valor: (valorCentavos / 100).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    }),
  }));

  return mascararRegistros(paraTela);
}

export default async function Pagina({
  searchParams,
}: {
  searchParams: Promise<{ dias?: string }>;
}) {
  await exigirSessao();

  const { dias: diasBruto } = await searchParams;
  const dias = PERIODOS.includes(Number(diasBruto)) ? Number(diasBruto) : 30;

  let dados: Record<string, string | number>[];
  try {
    dados = await carregar(dias);
  } catch (erro) {
    return (
      <div className="rounded-padrao border border-alerta/40 bg-alerta/5 p-4">
        <p className="font-medium text-alerta">Não consegui carregar os dados.</p>
        <p className="mt-1 text-sm text-texto-suave">
          Avise o time de dados. Detalhe técnico: {(erro as Error).name}
        </p>
      </div>
    );
  }

  const colunas = dados.length > 0 ? Object.keys(dados[0]) : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">{"{{NOME_DO_PROJETO}}"}</h1>
        <p className="text-texto-suave">{"{{OBJETIVO}}"}</p>
      </div>

      {!bancoConfigurado() && (
        <p className="rounded-padrao border border-borda bg-marca-suave p-3 text-sm">
          Mostrando <strong>dados de exemplo</strong>, gerados na hora. Para ver dados de
          verdade, preencha <code>DATABASE_URL</code> no arquivo <code>.env</code>.
        </p>
      )}

      {/* Filtro por link: o servidor refaz a busca. Sem estado no navegador. */}
      <nav className="flex gap-2">
        {PERIODOS.map((p) => (
          <a
            key={p}
            href={`/?dias=${p}`}
            className={
              p === dias
                ? "rounded-padrao bg-marca px-3 py-1.5 text-sm text-white"
                : "rounded-padrao border border-borda px-3 py-1.5 text-sm hover:bg-marca-suave"
            }
          >
            {p} dias
          </a>
        ))}
      </nav>

      {dados.length === 0 ? (
        <p className="rounded-padrao border border-borda p-6 text-center text-texto-suave">
          Nenhum resultado para esse filtro. Tente um período maior.
        </p>
      ) : (
        <>
          <div className="flex items-center justify-between">
            <p className="text-sm text-texto-suave">
              {dados.length.toLocaleString("pt-BR")} registro(s) nos últimos {dias} dias
            </p>
            <ExportarCsv linhas={dados} nomeArquivo="dados.csv" />
          </div>

          <div className="overflow-x-auto rounded-padrao border border-borda">
            <table className="w-full text-sm">
              <thead className="bg-marca-suave text-left">
                <tr>
                  {colunas.map((c) => (
                    <th key={c} className="px-3 py-2 font-medium">{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {dados.slice(0, 200).map((linha, i) => (
                  <tr key={i} className="border-t border-borda">
                    {colunas.map((c) => (
                      <td key={c} className="px-3 py-2">{String(linha[c])}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
