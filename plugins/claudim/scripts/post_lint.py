#!/usr/bin/env python3
"""PostToolUse | Write, Edit, MultiEdit.

Roda o eslint no arquivo que acabou de ser escrito, conserta o que da para
consertar sozinho e devolve o resto para o modelo.

O ponto todo esta em para quem a mensagem vai. Exit 2 num PostToolUse manda o
stderr para o Claude, nao para a tela do usuario: quem le "no-explicit-any" e
quem sabe o que fazer com isso. O usuario deste plugin e de marketing e nao
tem que ver erro de lint nunca.

Nunca bloqueia por conta propria: sem eslint instalado, sem config, ou eslint
quebrado, sai 0 calado. Ferramenta de estilo travando o trabalho e pior do que
codigo mal formatado.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _shared import caminho_alvo, ler_evento, raiz_projeto  # noqa: E402

EXTENSOES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
MAX_ACHADOS = 8


def eslint(raiz: Path) -> list[str] | None:
    """So o eslint do proprio projeto. Sem node_modules nao ha config nem
    plugin, e um eslint global rodaria com outras regras."""
    local = raiz / "node_modules" / ".bin" / "eslint"
    return [str(local)] if local.is_file() else None


def tem_config(raiz: Path) -> bool:
    return any(
        (raiz / nome).is_file()
        for nome in ("eslint.config.mjs", "eslint.config.js", "eslint.config.ts")
    )


def erros(saida: str) -> list[str]:
    """Só severidade 2. Aviso nao interrompe ninguem."""
    try:
        relatorio = json.loads(saida)
    except Exception:
        return []
    achados = []
    for arquivo in relatorio:
        for m in arquivo.get("messages", []):
            if m.get("severity") != 2:
                continue
            regra = m.get("ruleId") or "erro de sintaxe"
            achados.append(f"  linha {m.get('line', '?')}: {m.get('message', '')} [{regra}]")
    return achados


def lintar(evento: dict) -> None:
    caminho = caminho_alvo(evento)
    if caminho is None or caminho.suffix.lower() not in EXTENSOES or not caminho.is_file():
        return
    raiz = raiz_projeto(evento)
    comando = eslint(raiz)
    if not comando or not tem_config(raiz):
        return

    try:
        r = subprocess.run(
            [
                *comando,
                "--fix",
                "--cache",
                "--cache-location",
                str(raiz / "node_modules" / ".cache" / "eslint-claudim"),
                "--format",
                "json",
                str(caminho),
            ],
            capture_output=True, text=True, timeout=40, cwd=str(raiz),
        )
    except Exception:
        return

    restantes = erros(r.stdout)
    if not restantes:
        return

    mostrados = restantes[:MAX_ACHADOS]
    sobra = len(restantes) - len(mostrados)
    print(
        f"\n[LINT] Sobrou erro em {caminho.name} depois do --fix automatico:\n\n"
        + "\n".join(mostrados)
        + (f"\n  (+{sobra} outro(s))" if sobra else "")
        + "\n\nCorrija agora, no proximo edit, antes de seguir para outro arquivo.\n"
        "Nao mostre isso ao usuario e nao peca confirmacao: e regra de codigo do\n"
        "projeto, nao decisao dele. Se a regra parecer errada para este caso, e o\n"
        "codigo que muda — nao ponha eslint-disable para calar.\n",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    lintar(ler_evento())
