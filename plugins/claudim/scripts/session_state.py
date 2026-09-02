#!/usr/bin/env python3
"""SessionStart.

Nao e banner de boas-vindas. Injeta o estado do projeto no contexto para o
modelo nao perguntar o que da para descobrir sozinho.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _shared import eh_projeto_greenfield, estado_projeto, ler_evento, raiz_projeto  # noqa: E402

RE_ITEM = re.compile(r"^\s*[-*]\s*\[( |x|X)\]\s+(.*)$")


def passos_do_plano(plano: Path) -> tuple[int, int, list[str]]:
    abertos, feitos, titulos = 0, 0, []
    for linha in plano.read_text(encoding="utf-8", errors="replace").splitlines():
        m = RE_ITEM.match(linha)
        if not m:
            continue
        if m.group(1).lower() == "x":
            feitos += 1
        else:
            abertos += 1
            if len(titulos) < 3:
                titulos.append(m.group(2).strip())
    return abertos, feitos, titulos


def git(raiz: Path, *args: str) -> str:
    if not shutil.which("git"):
        return ""
    try:
        r = subprocess.run(
            ["git", "-C", str(raiz), *args], capture_output=True, text=True, timeout=5
        )
        return r.stdout.strip()
    except Exception:
        return ""


def main() -> None:
    raiz = raiz_projeto(ler_evento())
    if not eh_projeto_greenfield(raiz):
        return

    estado = estado_projeto(raiz)
    linhas = ["## Estado do projeto (claudim)", ""]
    linhas.append(f"- Projeto: **{estado.get('nome', raiz.name)}**")
    if estado.get("objetivo"):
        linhas.append(f"- Objetivo declarado no /comecar: {estado['objetivo']}")
    if estado.get("fase") == "scaffold":
        linhas.append(
            "- **O /comecar nao foi concluido.** Termine o scaffold antes de qualquer "
            "outra coisa e grave `fase: pronto` em `.greenfield/state.json`."
        )

    plano = raiz / "PLANO.md"
    if plano.is_file():
        abertos, feitos, titulos = passos_do_plano(plano)
        linhas.append(f"- PLANO.md existe — {feitos} passo(s) concluido(s), {abertos} em aberto.")
        for t in titulos:
            linhas.append(f"  - proximo: {t}")
        if abertos == 0 and feitos > 0:
            linhas.append("  - Todos os passos foram marcados. Sugira `/revisar`.")
    else:
        linhas.append(
            "- **Nao existe PLANO.md.** O hook de escrita vai bloquear qualquer codigo. "
            "Se o usuario pedir para construir algo, rode `/planejar` primeiro."
        )

    branch = git(raiz, "rev-parse", "--abbrev-ref", "HEAD")
    sujo = git(raiz, "status", "--porcelain")
    if branch:
        linhas.append(f"- Branch: `{branch}`" + (" — com alteracoes nao salvas em commit." if sujo else " — tudo commitado."))

    if estado.get("dado_sensivel"):
        linhas.append(
            "- **Este projeto foi marcado como 'lida com dado sensivel' (LGPD Art. 11).** "
            "Invoque a skill `dados-sensiveis` em qualquer codigo que toque CPF, "
            "carteirinha, beneficiario, diagnostico, tracking ou URL."
        )

    print("\n".join(linhas))


if __name__ == "__main__":
    main()
