"use client";

/** Botão de exportar CSV.
 *
 * É "use client" porque o download acontece no navegador. Cuidado: tudo que
 * este componente recebe por prop viaja para o navegador. Passe só linhas que
 * já saíram do `mascararRegistros`.
 */

import { Button } from "@/components/ui/button";

type Linha = Record<string, string | number>;

function paraCsv(linhas: Linha[]): string {
  const colunas = Object.keys(linhas[0] ?? {});
  const escapar = (v: unknown) => `"${String(v ?? "").replace(/"/g, '""')}"`;
  return [
    colunas.join(";"),
    ...linhas.map((linha) => colunas.map((c) => escapar(linha[c])).join(";")),
  ].join("\n");
}

export function ExportarCsv({
  linhas,
  nomeArquivo,
}: {
  linhas: Linha[];
  nomeArquivo: string;
}) {
  function baixar() {
    // BOM na frente: sem ele o Excel abre acento errado.
    const blob = new Blob(["﻿" + paraCsv(linhas)], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = nomeArquivo;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <Button variant="outline" onClick={baixar} disabled={linhas.length === 0}>
      Baixar em CSV
    </Button>
  );
}
