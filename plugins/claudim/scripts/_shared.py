"""Utilidades comuns aos hooks do plugin claudim.

Nada aqui fala com o usuário final. Quem fala é cada guard, em português,
sempre dizendo o proximo passo.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Entrada / saida de hook
# --------------------------------------------------------------------------- #

def ler_evento() -> dict:
    """Le o JSON do hook em stdin. Nunca levanta excecao: hook quebrado nao
    pode virar bloqueio acidental."""
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def bloquear(titulo: str, motivo: str, proximo_passo: str) -> None:
    """Exit 2 = o Claude Code cancela a ferramenta e devolve o stderr ao modelo."""
    print(
        f"\n[BLOQUEADO] {titulo}\n\n"
        f"Motivo: {motivo}\n\n"
        f"O que fazer agora: {proximo_passo}\n",
        file=sys.stderr,
    )
    sys.exit(2)


def sair_ok() -> None:
    sys.exit(0)


# --------------------------------------------------------------------------- #
# Leitura do tool_input
# --------------------------------------------------------------------------- #

def caminho_alvo(evento: dict) -> Path | None:
    ti = evento.get("tool_input") or {}
    alvo = ti.get("file_path") or ti.get("notebook_path") or ti.get("path")
    return Path(alvo) if alvo else None


def conteudo_escrito(evento: dict) -> str:
    """Todo texto que essa chamada tenta gravar no arquivo."""
    ti = evento.get("tool_input") or {}
    partes = [
        ti.get("content") or "",
        ti.get("new_string") or "",
        ti.get("new_source") or "",
    ]
    for edicao in ti.get("edits") or []:
        if isinstance(edicao, dict):
            partes.append(edicao.get("new_string") or "")
    return "\n".join(p for p in partes if p)


# --------------------------------------------------------------------------- #
# Projeto
# --------------------------------------------------------------------------- #

def raiz_projeto(evento: dict) -> Path:
    return Path(evento.get("cwd") or os.getcwd())


def eh_projeto_greenfield(raiz: Path) -> bool:
    """Os hooks do plugin rodam em toda sessao do usuario. Regras de processo
    (exigir PLANO.md) so valem em projeto criado pelo /comecar."""
    return (raiz / ".greenfield").is_dir()


def estado_projeto(raiz: Path) -> dict:
    caminho = raiz / ".greenfield" / "state.json"
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except Exception:
        return {}


def gravar_estado(raiz: Path, **campos) -> dict:
    pasta = raiz / ".greenfield"
    pasta.mkdir(parents=True, exist_ok=True)
    estado = estado_projeto(raiz)
    estado.update(campos)
    (pasta / "state.json").write_text(
        json.dumps(estado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return estado


# --------------------------------------------------------------------------- #
# Classificacao de arquivo
# --------------------------------------------------------------------------- #

EXTENSOES_CODIGO = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".prisma", ".sql",
    ".css", ".html", ".py", ".sh", ".toml", ".yaml", ".yml", ".json", ".ipynb",
}

# Documento e configuracao declarativa nao exigem PLANO.md.
NOMES_LIVRES = {
    "PLANO.md", "CLAUDE.md", "README.md", ".env.example", ".gitignore",
    "state.json",
    # Configuracao do scaffold Next.js — nada de logica de produto mora aqui.
    "package.json", "package-lock.json", "tsconfig.json", "next.config.ts",
    "postcss.config.mjs", "components.json", "next-env.d.ts", "eslint.config.mjs",
    "eslint.config.revisao.mjs", ".prettierrc", ".prettierignore", "vercel.json",
}


def eh_codigo_fonte(caminho: Path) -> bool:
    if caminho.name in NOMES_LIVRES:
        return False
    if ".greenfield" in caminho.parts:
        return False
    return caminho.suffix.lower() in EXTENSOES_CODIGO


PADRAO_DADOS_TESTE = re.compile(
    r"(fixture|seed|mock|sample|amostra|dados_?teste|test_data|exemplo|demo|"
    r"tests?/|/data/|\.csv$|\.json$|\.sql$)",
    re.IGNORECASE,
)


def eh_arquivo_de_dados_teste(caminho: Path) -> bool:
    return bool(PADRAO_DADOS_TESTE.search(str(caminho).replace(os.sep, "/")))
