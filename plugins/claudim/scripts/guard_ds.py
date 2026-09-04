#!/usr/bin/env python3
"""PreToolUse | Write, Edit, MultiEdit.

Segura o design system:
  1. Cor literal em componente (bg-[#0055ff], style com hex).
  2. Classe de tema que nao tem token no DESIGN.md (bg-blue-600, bg-azul).
  3. Edicao a mao de arquivo gerado (app/globals.css).

A fonte dos tokens e docs/design-system/DESIGN.md do proprio projeto. Sem esse
arquivo o guard nao opina — quem nao adotou design system nao e atrapalhado.

Nao depende de pyyaml: le o front matter com regex, porque hook que quebra por
falta de dependencia vira bloqueio acidental.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _shared import (  # noqa: E402
    bloquear,
    caminho_alvo,
    conteudo_escrito,
    ler_evento,
    raiz_projeto,
    sair_ok,
)

EXTENSOES = {".tsx", ".ts", ".jsx", ".js", ".css"}

# Secoes do front matter que declaram token, e o prefixo que cada uma gera.
SECOES = {
    "colors": "",          # o nome do token ja e o nome da utilitaria
    "rounded": "",
    "spacing": "",
    "elevation": "",
}

# Escala e palavra-chave nativas do Tailwind: nao sao token de tema.
NATIVAS = {
    "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl",
    "base", "xs", "full", "none", "auto", "px",
    "t", "b", "l", "r", "x", "y", "s", "e",
    "left", "center", "right", "justify", "start", "end",
    "white", "black", "transparent", "current", "inherit",
    "offset", "medium", "semibold", "bold", "normal", "light", "thin",
    "wrap", "nowrap", "balance", "pretty", "clip", "ellipsis",
    "solid", "dashed", "dotted", "double", "hidden", "collapse",
    "mono", "serif",
}

PREFIXOS = ("bg", "text", "border", "outline", "ring", "divide", "shadow",
            "rounded", "font", "from", "via", "to", "fill", "stroke", "accent",
            "decoration", "caret", "placeholder")

# Escala de cor do Tailwind: bg-blue-600, text-gray-500, border-slate-200.
FAMILIAS_TAILWIND = (
    "slate|gray|grey|zinc|neutral|stone|red|orange|amber|yellow|lime|green|"
    "emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose"
)
COR_TAILWIND = re.compile(
    rf"\b(?:{'|'.join(PREFIXOS)})-(?:{FAMILIAS_TAILWIND})-\d{{2,3}}\b"
)

# Valor literal onde deveria haver token.
COR_ARBITRARIA = re.compile(
    rf"\b(?:{'|'.join(PREFIXOS)})-\[(#[0-9a-fA-F]{{3,8}}|rgba?\(|hsla?\(|oklch\()"
)
HEX_EM_ESTILO = re.compile(r"style=\{\{[^}]*?#[0-9a-fA-F]{6}", re.S)

# Guloso de proposito: `border-border-muted` e prefixo `border` + token
# `border-muted`, nao prefixo `border` + token `border` sobrando `-muted`.
CLASSE = re.compile(rf"\b({'|'.join(PREFIXOS)})-([a-z][a-z0-9-]*)(?:/\d+)?\b")


def tokens_do_design(raiz: Path) -> set[str] | None:
    """Nomes de token declarados no front matter. None = projeto sem design system."""
    design = raiz / "docs" / "design-system" / "DESIGN.md"
    try:
        texto = design.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.match(r"^---\n(.*?)\n---", texto, re.S)
    if not m:
        return None

    nomes: set[str] = set()
    secao = None
    for linha in m.group(1).split("\n"):
        if re.match(r"^[a-z]", linha):                      # coluna 0: secao raiz
            secao = linha.split(":")[0].strip()
            continue
        if secao not in SECOES:
            continue
        # aceita "  nome: valor" (2 espacos) e "    nome: valor" (4, agrupado)
        campo = re.match(r"^ {2,6}([a-z0-9][a-z0-9-]*):\s*(.*)$", linha)
        if campo and campo.group(2).strip():                # tem valor, nao e subgrupo
            nomes.add(campo.group(1))
    nomes.add("overlay")
    nomes.update({"sans", "display"})                       # familias tipograficas
    return nomes or None


def checar_arquivo_gerado(raiz: Path, caminho: Path) -> None:
    try:
        rel = caminho.resolve().relative_to(raiz.resolve()).as_posix()
    except (ValueError, OSError):
        return
    if rel != "app/globals.css":
        return
    if not (raiz / "docs" / "design-system" / "gerar-tema.py").is_file():
        return
    bloquear(
        "O app/globals.css e um arquivo gerado.",
        "Os tokens de tema saem de docs/design-system/DESIGN.md. Editar o CSS "
        "direto cria um segundo lugar com valor de cor, e a proxima execucao do "
        "gerador apaga a sua alteracao.",
        "Edite o valor em docs/design-system/DESIGN.md e rode "
        "`python3 docs/design-system/gerar-tema.py`. O globals.css sai dele, e "
        "nenhum componente precisa mudar.",
    )


def checar_conteudo(conteudo: str, validos: set[str], caminho: Path) -> None:
    achado = COR_ARBITRARIA.search(conteudo) or HEX_EM_ESTILO.search(conteudo)
    if achado:
        bloquear(
            "Cor escrita direto no componente.",
            f"`{achado.group(0)[:40]}` fixa um valor de cor fora do design system. "
            "Quando a marca mudar, essa cor fica para tras — e ninguem lembra que "
            "ela existe.",
            "Use o token: `bg-primary`, `text-foreground`, `border-border-muted`. "
            "A lista esta em docs/design-system/DESIGN.md.",
        )

    tw = COR_TAILWIND.search(conteudo)
    if tw:
        bloquear(
            "Cor da paleta do Tailwind, nao do design system.",
            f"`{tw.group(0)}` e uma cor generica do Tailwind. O projeto tem paleta "
            "propria, e misturar as duas e como nasce uma segunda identidade visual.",
            "Troque pelo token equivalente do projeto — `bg-primary`, `bg-accent`, "
            "`bg-destructive`, `text-muted-foreground`. A lista completa esta em "
            "docs/design-system/DESIGN.md.",
        )

    for prefixo, nome in CLASSE.findall(conteudo):
        if nome in NATIVAS or nome in validos:
            continue
        if re.fullmatch(r"\d+(\.\d+)?", nome):              # escala numerica: p-4, gap-2
            continue
        # nativa com escala: outline-offset-2, ring-offset-4, border-x-2
        if re.sub(r"-\d+(\.\d+)?$", "", nome) in NATIVAS:
            continue
        bloquear(
            f"A classe `{prefixo}-{nome}` nao existe no design system.",
            f"Nenhum token chamado `{nome}` esta declarado em "
            "docs/design-system/DESIGN.md, entao essa classe nao vai gerar estilo "
            "nenhum — o Tailwind so cria a utilitaria a partir do token.",
            f"Use um token que existe, ou declare `{nome}` no DESIGN.md e rode "
            "`python3 docs/design-system/gerar-tema.py`. Tema e decisao de design: "
            "se o valor e novo mesmo, confirme com quem pediu antes de inventar.",
        )


def checar(evento: dict) -> None:
    """Chamado pelo guard_edicao.py. Nao sai do processo: quem sai e o
    bloquear(), e so quando ha o que bloquear."""
    caminho = caminho_alvo(evento)
    if caminho is None or caminho.suffix.lower() not in EXTENSOES:
        return

    raiz = raiz_projeto(evento)
    checar_arquivo_gerado(raiz, caminho)

    validos = tokens_do_design(raiz)
    if validos is None:          # projeto sem design system: o guard nao opina
        return

    checar_conteudo(conteudo_escrito(evento), validos, caminho)


if __name__ == "__main__":
    checar(ler_evento())
    sair_ok()
