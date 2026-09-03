#!/usr/bin/env python3
"""Gera o tema e o showcase a partir do DESIGN.md.

DESIGN.md é a única fonte dos valores de tema. Este script escreve os
derivados: o bloco @theme do Tailwind e a página de showcase. Não edite os
derivados à mão — a próxima execução sobrescreve.

    python3 docs/design-system/gerar-tema.py            # escreve os derivados
    python3 docs/design-system/gerar-tema.py --checar   # verifica, exit 1 se divergiu

O --checar responde duas perguntas: (1) os derivados correspondem ao DESIGN.md?
(2) toda utilitária de tema usada em .tsx tem token no DESIGN.md? A segunda
pega a classe inventada — `bg-azul`, `bg-blue-600` — antes de virar paleta.
"""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
DESIGN = AQUI / "DESIGN.md"
GLOBALS = RAIZ / "app" / "globals.css"
SHOWCASE = AQUI / "showcase.html"

# YAML -> custom property. O nome do token é o do DESIGN.md; o prefixo é
# exigido pelo Tailwind v4 para gerar a utilitária (--color-primary -> bg-primary).
PREFIXO = {"colors": "--color-", "rounded": "--radius-", "elevation": "--shadow-"}
GRUPOS_COR = ("brand", "surface", "status", "chart", "line")


def ler_frontmatter(texto):
    m = re.match(r"^---\n(.*?)\n---", texto, re.S)
    if not m:
        raise SystemExit("DESIGN.md sem frontmatter YAML")
    import yaml

    return yaml.safe_load(m.group(1))


def tokens(spec):
    """Achata o YAML em [(custom-property, valor, grupo)] na ordem de declaração."""
    saida = []
    for grupo in GRUPOS_COR:
        for nome, valor in spec["colors"].get(grupo, {}).items():
            saida.append((f"--color-{nome}", valor, grupo))
    for nome, valor in spec.get("rounded", {}).items():
        saida.append((f"--radius-{nome}", valor, "rounded"))
    for nome, valor in spec.get("spacing", {}).items():
        saida.append((f"--spacing-{nome}", valor, "spacing"))
    for nome, valor in spec.get("elevation", {}).items():
        if nome == "overlay":  # não é sombra, é cor de fundo do overlay
            saida.append(("--color-overlay", valor, "overlay"))
        else:
            saida.append((f"--shadow-{nome}", valor, "elevation"))
    tipo = spec.get("typography", {})
    for chave, prop in (("sans", "--font-sans"), ("display", "--font-display")):
        if chave in tipo:
            familia = tipo[chave]["fontFamily"]
            if " " in familia:  # família com espaço precisa de quotes em CSS
                familia = f'"{familia}"'
            saida.append((prop, familia + FALLBACK_SANS, "typography"))
    return saida


FALLBACK_SANS = ', ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif'

TITULO = {
    "brand": "marca",
    "surface": "superfícies",
    "status": "estado",
    "chart": "gráfico (paleta categórica)",
    "line": "linhas e foco",
    "rounded": "raio",
    "spacing": "espaçamento",
    "elevation": "elevação",
    "typography": "tipografia",
    "overlay": "overlay",
}


def montar_css(spec):
    linhas = [
        "/* GERADO por docs/design-system/gerar-tema.py — não edite à mão.",
        "   A fonte dos valores é docs/design-system/DESIGN.md.",
        "   Mudou o tema? Muda lá e roda o gerador.",
        "",
        "   Tailwind v4: cada token vira utilitária — --color-primary gera",
        "   bg-primary e text-primary; --radius-lg gera rounded-lg. */",
        '@import "tailwindcss";',
        "",
        "@theme {",
    ]
    grupo_atual = None
    for prop, valor, grupo in tokens(spec):
        if grupo != grupo_atual:
            if grupo_atual is not None:
                linhas.append("")
            linhas.append(f"  /* {TITULO.get(grupo, grupo)} */")
            grupo_atual = grupo
        linhas.append(f"  {prop}: {valor};")
    linhas += [
        "}",
        "",
        "@layer base {",
        "  body {",
        "    background-color: var(--color-background);",
        "    color: var(--color-foreground);",
        "    font-family: var(--font-sans);",
        "  }",
        "",
        "  /* O DS exige foco visível em tudo que recebe teclado. */",
        "  :focus-visible {",
        "    outline: none;",
        "    box-shadow: var(--shadow-focus);",
        "  }",
        "}",
        "",
    ]
    return "\n".join(linhas)


def swatch(prop, valor):
    escuro = prop in (
        "--color-background",
        "--color-card",
        "--color-popover",
        "--color-secondary",
        "--color-muted",
        "--color-soft",
        "--color-highlight",
        "--color-ring",
        "--color-warning",
        "--color-primary-foreground",
        "--color-accent-foreground",
        "--color-destructive-foreground",
    )
    cor_texto = "#2D2D2D" if escuro else "#FFFFFF"
    return (
        f'<figure class="sw"><div class="chip" style="background:var({prop})">'
        f'<span style="color:{cor_texto}">{valor}</span></div>'
        f'<figcaption><code>{prop}</code><small>{prop.split("-", 2)[-1]}</small>'
        f"</figcaption></figure>"
    )


def montar_showcase(spec):
    grupos = {}
    for prop, valor, grupo in tokens(spec):
        grupos.setdefault(grupo, []).append((prop, valor))

    # Os valores aparecem UMA vez, aqui no :root. Todo o resto da pagina usa
    # var(--token) — a pagina consome o proprio design system que exibe.
    raiz = "\n".join(f"  {p}: {v};" for p, v, _ in tokens(spec))

    secoes = []
    for grupo in GRUPOS_COR:
        if grupo not in grupos:
            continue
        chips = "\n      ".join(swatch(p, v) for p, v in grupos[grupo])
        secoes.append(
            f'    <h3>{TITULO[grupo].capitalize()}</h3>\n'
            f'    <div class="grid">\n      {chips}\n    </div>'
        )
    cores = "\n".join(secoes)

    raios = "\n      ".join(
        f'<div class="box" style="border-radius:var({p})">{p}<small>{v}</small></div>'
        for p, v in grupos.get("rounded", [])
    )
    sombras = "\n      ".join(
        f'<div class="box sh" style="box-shadow:var({p})">{p}</div>'
        for p, v in grupos.get("elevation", [])
    )
    fontes = "\n      ".join(
        f'<p class="amostra" style="font-family:var({p})">{p}'
        f'<small>{v.split(",")[0]}</small></p>'
        for p, v in grupos.get("typography", [])
    )

    nome = spec.get("name", "Design System")
    versao = spec.get("version", "")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{nome} — tokens</title>
<style>
/* GERADO por gerar-tema.py a partir de DESIGN.md — nao edite a mao.
   Os valores estao declarados uma unica vez, no :root abaixo. O resto da
   folha usa var(--token): esta pagina consome o design system que exibe. */
:root {{
  color-scheme: light;
{raiz}
}}
* {{ box-sizing: border-box }}
body {{ margin:0; font-family:var(--font-sans); font-size:16px; line-height:1.6;
       color:var(--color-foreground); background:var(--color-background) }}
.wrap {{ max-width:1040px; margin:0 auto; padding:40px }}
header {{ background:var(--color-primary); color:var(--color-primary-foreground);
         padding:48px 40px }}
header h1 {{ margin:0 0 6px; font-size:2.4rem; font-family:var(--font-display) }}
header p {{ margin:0; opacity:.85; font-size:.95rem }}
h2 {{ font-size:1.5rem; margin:48px 0 4px; padding-bottom:8px;
     border-bottom:2px solid var(--color-primary) }}
h3 {{ font-size:.95rem; text-transform:uppercase; letter-spacing:.06em;
     color:var(--color-muted-foreground); margin:28px 0 12px }}
code {{ font-family:ui-monospace, SFMono-Regular, Menlo, monospace }}
.grid {{ display:grid; gap:14px; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)) }}
.sw {{ margin:0; border:1px solid var(--color-border-muted);
      border-radius:var(--radius-lg); overflow:hidden }}
.chip {{ height:76px; display:flex; align-items:flex-end; padding:8px }}
.chip span {{ font-weight:600; font-size:.7rem;
             font-family:ui-monospace, SFMono-Regular, Menlo, monospace }}
figcaption {{ padding:9px 11px }}
figcaption code {{ font-weight:700; font-size:.76rem; display:block }}
figcaption small {{ color:var(--color-muted-foreground); font-size:.72rem }}
.box {{ border:1px solid var(--color-primary); height:80px; display:flex;
       flex-direction:column; align-items:center; justify-content:center; gap:3px;
       font-size:.72rem; font-family:ui-monospace, SFMono-Regular, Menlo, monospace }}
.box.sh {{ border:none; border-radius:var(--radius-lg);
          background:var(--color-card) }}
.box small {{ color:var(--color-muted-foreground) }}
.amostra {{ font-size:1.5rem; margin:0 0 10px }}
.amostra small {{ display:block; font-size:.7rem; font-family:var(--font-sans);
                 color:var(--color-muted-foreground) }}
.note {{ background:var(--color-secondary); border-left:3px solid var(--color-accent);
        padding:12px 16px; font-size:.85rem; margin-top:18px;
        border-radius:var(--radius-sm) }}
footer {{ margin:56px 0 0; padding-top:20px;
         border-top:1px solid var(--color-border-muted);
         color:var(--color-muted-foreground); font-size:.78rem }}
</style>
</head>
<body>
<header>
  <h1>{nome}</h1>
  <p>Tokens gerados de <code>DESIGN.md</code> · versao {versao}</p>
</header>
<div class="wrap">

  <section>
    <h2>Cores</h2>
{cores}
    <div class="note">Nunca use hex em componente. A utilitaria vem do token:
      <code>--color-primary</code> gera <code>bg-primary</code> e
      <code>text-primary</code>.</div>
  </section>

  <section>
    <h2>Raio</h2>
    <div class="grid">
      {raios}
    </div>
  </section>

  <section>
    <h2>Elevacao</h2>
    <div class="grid">
      {sombras}
    </div>
  </section>

  <section>
    <h2>Tipografia</h2>
      {fontes}
    <div class="note">A familia de display nao e uma fonte publica; o navegador
      cai no fallback do stack.</div>
  </section>

<footer>
  Pagina gerada por <code>docs/design-system/gerar-tema.py</code>.
  Para mudar um valor, edite <code>DESIGN.md</code> e rode o gerador —
  editar esta pagina a mao nao muda o design system.
</footer>
</div>
</body>
</html>
"""


# escala e palavra-chave nativas do Tailwind: nao sao token de tema
NATIVAS = {
    "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "base", "xs", "full",
    "none", "t", "b", "l", "r", "x", "y", "left", "center", "right", "justify",
    "white", "black", "transparent", "current", "inherit", "offset",
    "medium", "semibold", "bold", "normal", "wrap", "nowrap", "balance",
}


def classes_orfas(spec):
    """Classe de tema usada em .tsx que nao tem token no DESIGN.md."""
    cores = {"overlay"}
    for grupo in GRUPOS_COR:
        cores |= set(spec["colors"].get(grupo, {}))
    valido = {
        "bg": cores, "text": cores, "border": cores, "outline": cores,
        "ring": cores, "divide": cores,
        "rounded": set(spec.get("rounded", {})),
        "shadow": {k for k in spec.get("elevation", {}) if k != "overlay"},
        "p": set(spec.get("spacing", {})), "px": set(spec.get("spacing", {})),
        "py": set(spec.get("spacing", {})), "m": set(spec.get("spacing", {})),
        "gap": set(spec.get("spacing", {})),
        "font": {"sans", "display"},
    }
    achados = []
    for arquivo in sorted(RAIZ.rglob("*")):
        if arquivo.suffix not in (".tsx", ".ts") or "design-system" in str(arquivo):
            continue
        texto = arquivo.read_text(encoding="utf-8")
        for pre, nome in re.findall(
            r"\b(bg|text|border|outline|ring|divide|rounded|shadow|font)-([a-z][a-z-]*?)(?:/\d+)?\b",
            texto,
        ):
            if nome in NATIVAS or nome in valido[pre]:
                continue
            achados.append((arquivo.relative_to(RAIZ), f"{pre}-{nome}"))
    return achados


def main():
    checar = "--checar" in sys.argv
    spec = ler_frontmatter(DESIGN.read_text(encoding="utf-8"))
    saidas = {GLOBALS: montar_css(spec), SHOWCASE: montar_showcase(spec)}

    if checar:
        falhou = False
        for caminho, esperado in saidas.items():
            atual = caminho.read_text(encoding="utf-8") if caminho.exists() else None
            if atual != esperado:
                print(f"DIVERGIU: {caminho.relative_to(RAIZ)} não corresponde ao DESIGN.md")
                falhou = True
        if falhou:
            print("\nRode: python3 docs/design-system/gerar-tema.py")

        orfas = classes_orfas(spec)
        for arquivo, classe in orfas:
            print(f"SEM TOKEN: {arquivo} usa `{classe}`, que não existe no DESIGN.md")
        if orfas:
            print("\nAdicione o token no DESIGN.md ou use um que já existe.")
            falhou = True

        if falhou:
            return 1
        print(f"ok — {len(saidas)} derivados conferem com o DESIGN.md, "
              "nenhuma classe de tema sem token")
        return 0

    for caminho, conteudo in saidas.items():
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(conteudo, encoding="utf-8")
        print(f"escrito: {caminho.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
