#!/usr/bin/env python3
"""PostToolUse | Write, Edit, MultiEdit.

Formata o arquivo que acabou de ser escrito, sem que o usuario veja. Nunca
bloqueia: formatador quebrado nao pode travar quem nao sabe o que e lint.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _shared import caminho_alvo, ler_evento, raiz_projeto  # noqa: E402

EXTENSOES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".css", ".json", ".md"}


def prettier(raiz: Path) -> list[str] | None:
    """Prefere o prettier instalado no projeto. Sem node_modules, nao formata:
    baixar pacote no meio de um hook seria lento e silencioso demais."""
    local = raiz / "node_modules" / ".bin" / "prettier"
    if local.is_file():
        return [str(local)]
    global_ = shutil.which("prettier")
    return [global_] if global_ else None


def formatar(evento: dict) -> None:
    caminho = caminho_alvo(evento)
    if caminho is None or caminho.suffix.lower() not in EXTENSOES or not caminho.is_file():
        return
    comando = prettier(raiz_projeto(evento))
    if not comando:
        return
    try:
        subprocess.run(
            [*comando, "--write", "--log-level", "silent", str(caminho)],
            capture_output=True, text=True, timeout=25,
        )
    except Exception:
        return


if __name__ == "__main__":
    formatar(ler_evento())
