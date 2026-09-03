/** {{NOME_DO_PROJETO}} — {{OBJETIVO}}
 *
 * Server Component: busca no servidor e manda HTML pronto. Não tem
 * "use client" aqui, então nada deste arquivo vai para o navegador — só o
 * resultado já mascarado.
 *
 * Esta tela não conhece o Prisma. Ela pede a lista para `lib/dados/eventos.ts`,
 * que é quem sabe de `take`, `select`, mascaramento e centavos. Página cuida de
 * sessão, de filtro e de o que aparece na tela — só isso.
 */

import { ExportarCsv } from "@/components/exportar-csv";
import { exigirSessao } from "@/lib/auth";
import { listarEventos, type EventoNaTela } from "@/lib/dados/eventos";
import { bancoConfigurado } from "@/lib/db";

// Esta tela lê a sessão e o banco a cada acesso — não dá para gerar no build.
export const dynamic = "force-dynamic";

const PERIODOS = [7, 30, 90, 180];

export default async function Pagina({
  searchParams,
}: {
  searchParams: Promise<{ dias?: string }>;
}) {
  await exigirSessao();

  const { dias: diasBruto } = await searchParams;
  const dias = PERIODOS.includes(Number(diasBruto)) ? Number(diasBruto) : 30;

  let dados: EventoNaTela[];
  try {
    dados = await listarEventos({ dias });
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
          verdade, recrie o banco com <code>npx prisma db push</code> e{" "}
          <code>npx prisma db seed</code>.
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
                    <th key={c} className="px-3 py-2 font-medium">
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {dados.slice(0, 200).map((linha, i) => (
                  <tr key={i} className="border-t border-borda">
                    {colunas.map((c) => (
                      <td key={c} className="px-3 py-2">
                        {String(linha[c])}
                      </td>
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
