#!/usr/bin/env python3
"""PreToolUse | Write, Edit, MultiEdit, NotebookEdit.

LGPD Art. 11: dado de saude e dado sensivel. Este hook bloqueia tres coisas:

  1. CPF ou CNS com digito verificador valido escrito dentro do codigo.
     Numero valido em fixture quase sempre e dado real de gente real.
  2. Nome de condicao de saude em arquivo de fixture / seed / dados de exemplo.
  3. Condicao de saude dentro de chamada de tracking (pixel, dataLayer, gtag).
     `/planos/oncologia` chegando num pixel e incidente, nao hipotese.
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
    eh_arquivo_de_dados_teste,
    ler_evento,
    sair_ok,
)

# --------------------------------------------------------------------------- #
# CPF
# --------------------------------------------------------------------------- #

RE_CPF = re.compile(r"(?<![\d.\-/])(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})(?![\d.\-/])")


def cpf_valido(bruto: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", bruto)]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    for tamanho in (9, 10):
        peso_inicial = tamanho + 1
        soma = sum(d[i] * (peso_inicial - i) for i in range(tamanho))
        digito = (soma * 10) % 11 % 10
        if digito != d[tamanho]:
            return False
    return True


# --------------------------------------------------------------------------- #
# CNS (Cartao Nacional de Saude)
# --------------------------------------------------------------------------- #

RE_CNS = re.compile(r"(?<!\d)([1279]\d{14})(?!\d)")


def cns_valido(bruto: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", bruto)]
    if len(d) != 15 or len(set(d)) == 1:
        return False
    soma = sum(d[i] * (15 - i) for i in range(15))
    return soma % 11 == 0


# --------------------------------------------------------------------------- #
# Condicao de saude
# --------------------------------------------------------------------------- #

TERMOS_SAUDE = [
    "oncolog", "cancer", "câncer", "quimioterap", "radioterap", "hiv", "aids",
    "soropositiv", "diabet", "hemodialis", "dialise", "diálise", "transplant",
    "psiquiatr", "depress", "esquizofren", "bipolar", "autis", "tea ",
    "gestante", "gravidez", "pre-natal", "pré-natal", "obstetric", "obstétric",
    "cardiopat", "obesidade", "bariatric", "bariátric", "alzheimer", "parkinson",
    "epilep", "hepatite", "tuberculose", "cid-10", "cid10", "diagnostic",
    "diagnóstic", "comorbidade", "doenca preexistente", "doença preexistente",
]

RE_TRACKING = re.compile(
    r"(gtag\s*\(|fbq\s*\(|dataLayer\s*\.\s*push|ttq\s*\.|analytics\s*\.\s*track|"
    r"mixpanel\s*\.\s*track|rudderanalytics|posthog\s*\.\s*capture|utm_|"
    r"event_name|conversion|pixel|track_event|send_event)",
    re.IGNORECASE,
)


def termos_saude_em(texto: str) -> list[str]:
    baixo = texto.lower()
    return sorted({t.strip() for t in TERMOS_SAUDE if t in baixo})


# --------------------------------------------------------------------------- #

def main() -> None:
    evento = ler_evento()
    caminho = caminho_alvo(evento)
    conteudo = conteudo_escrito(evento)
    if caminho is None or not conteudo:
        sair_ok()

    # 1. CPF / CNS validos
    for achado in RE_CPF.findall(conteudo):
        if cpf_valido(achado):
            bloquear(
                "Tem um CPF real no texto que eu ia gravar.",
                f"O numero `{achado}` passa na validacao de digito verificador — "
                "isso quase sempre significa dado de uma pessoa de verdade. "
                "CPF de beneficiario nao pode entrar em codigo nem em arquivo de exemplo "
                "(LGPD, e piora porque aqui e operadora de saude).",
                "Use o gerador que ja veio no projeto: `import { cpfFicticio } from "
                "\"@/lib/dados-sinteticos\"` — ele produz numeros com a cara certa e sem dono. "
                "Se o CPF precisa vir do banco, ele fica no banco e nunca no arquivo.",
            )
    for achado in RE_CNS.findall(conteudo):
        if cns_valido(achado):
            bloquear(
                "Tem um numero de carteirinha (CNS) real no texto.",
                f"O numero `{achado}` e um CNS valido. Numero de carteirinha identifica "
                "beneficiario e e dado sensivel de saude (LGPD Art. 11).",
                "Use `import { cnsFicticio } from \"@/lib/dados-sinteticos\"`. "
                "Dado de beneficiario de verdade so em consulta ao banco, em tempo de execucao.",
            )

    # 2. Condicao de saude em fixture / seed
    if eh_arquivo_de_dados_teste(caminho):
        termos = termos_saude_em(conteudo)
        if termos:
            bloquear(
                "Condicao de saude num arquivo de dados de exemplo.",
                f"`{caminho.name}` parece arquivo de fixture/seed e contem: "
                f"{', '.join(termos[:5])}. Dado de saude atrelado a pessoa e sensivel; "
                "arquivo de exemplo costuma nascer de um export de producao.",
                "Duas saidas: (a) tire a coluna de condicao do exemplo — a tela nao precisa "
                "dela para ser construida; ou (b) troque por rotulos neutros "
                "(`condicao_a`, `condicao_b`) e faca o de-para so em memoria. Me diga qual.",
            )

    # 3. Condicao de saude vazando em tracking
    for linha in conteudo.splitlines():
        if RE_TRACKING.search(linha) and termos_saude_em(linha):
            bloquear(
                "Condicao de saude indo para uma ferramenta de tracking.",
                "Essa linha manda para pixel/analytics um valor que revela condicao de "
                "saude. Mandar isso para terceiro (Meta, Google) e incidente de LGPD "
                "Art. 11, mesmo sem CPF junto — o nome do evento ou a URL ja denuncia.\n"
                f"    {linha.strip()[:160]}",
                "Mande um identificador opaco no lugar (`produto_id=17`) e resolva o nome "
                "no seu proprio banco, nunca no destino. Se o valor vem da URL, "
                "mascare antes de enviar. Posso reescrever assim — confirme.",
            )

    sair_ok()


if __name__ == "__main__":
    main()
