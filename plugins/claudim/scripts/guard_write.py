#!/usr/bin/env python3
"""PreToolUse | Write, Edit, MultiEdit, NotebookEdit.

Segura duas coisas:
  1. Segredo — nada de escrever .env, chave privada ou arquivo de credencial.
  2. Processo — nao existe codigo antes de existir PLANO.md.

A regra 2 so vale em projeto criado pelo /comecar (tem pasta .greenfield/).
A regra 1 vale em qualquer lugar.
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
    eh_codigo_fonte,
    eh_projeto_greenfield,
    estado_projeto,
    ler_evento,
    raiz_projeto,
    sair_ok,
)

# --------------------------------------------------------------------------- #
# 1. Arquivos de segredo
# --------------------------------------------------------------------------- #

PADROES_SEGREDO = [
    (re.compile(r"(^|/)\.env(\.|$)(?!example)"), "arquivo de variaveis de ambiente"),
    (re.compile(r"\.(pem|key|p12|pfx|jks|keystore)$", re.I), "arquivo de chave privada"),
    (re.compile(r"(^|/)credentials?(\.|_|-|$)", re.I), "arquivo de credencial"),
    (re.compile(r"(^|/)(id_rsa|id_ed25519|\.netrc|\.pgpass)$"), "credencial de sistema"),
    (re.compile(r"service[-_]?account.*\.json$", re.I), "chave de service account"),
]

# Segredo colado direto no codigo.
PADROES_SEGREDO_INLINE = [
    (re.compile(r"postgres(ql)?://[^:\s]+:[^@\s]+@", re.I), "senha de banco na string de conexao"),
    (re.compile(r"\b(sk|rk)-[A-Za-z0-9_\-]{20,}"), "chave de API"),
    (re.compile(r"\bsk_(live|test)_[A-Za-z0-9]{20,}"), "chave secreta do Clerk"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "chave de acesso AWS"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "token do GitHub"),
    (re.compile(r"\bEAA[A-Za-z0-9]{40,}"), "token da Meta/Facebook"),
]


# Prefixo NEXT_PUBLIC_ nao e configuracao: e publicacao. Tudo que tem esse
# prefixo entra no JavaScript que vai para o navegador de quem abrir a pagina.
RE_PUBLICO_COM_SEGREDO = re.compile(
    r"NEXT_PUBLIC_[A-Z0-9_]*(SECRET|PRIVATE|PASSWORD|SENHA|TOKEN|SERVICE_ROLE|"
    r"DATABASE_URL|CLERK_SECRET)[A-Z0-9_]*", re.IGNORECASE
)


def checar_segredo(caminho: Path, conteudo: str) -> None:
    texto_caminho = str(caminho).replace("\\", "/")
    if texto_caminho.endswith(".env.example"):
        return
    for padrao, rotulo in PADROES_SEGREDO:
        if padrao.search(texto_caminho):
            bloquear(
                "Isso e um arquivo de segredo.",
                f"`{caminho.name}` e {rotulo}. Segredo nunca entra no repositorio — "
                "se vazar, o acesso precisa ser rotacionado por infra.",
                "Coloque o nome da variavel (sem o valor) no `.env.example` e peca para "
                "eu ler o valor de `process.env`. O valor real voce escreve a mao no "
                "`.env`, que ja esta no .gitignore.",
            )
    achado_publico = RE_PUBLICO_COM_SEGREDO.search(conteudo)
    if achado_publico:
        bloquear(
            "Segredo com prefixo NEXT_PUBLIC_.",
            f"`{achado_publico.group(0)}` — tudo que comeca com `NEXT_PUBLIC_` e "
            "embutido no JavaScript enviado ao navegador. Qualquer pessoa que abrir a "
            "pagina le esse valor no DevTools; nao e configuracao, e publicacao.",
            "Tire o prefixo (`CLERK_SECRET_KEY`, sem NEXT_PUBLIC_) e leia o valor em "
            "arquivo de servidor — server component, server action ou `lib/`. "
            "So identificador publico (chave `pk_`, id de pixel) pode levar o prefixo.",
        )

    for padrao, rotulo in PADROES_SEGREDO_INLINE:
        if padrao.search(conteudo):
            bloquear(
                "Tem segredo escrito dentro do codigo.",
                f"Encontrei o que parece ser {rotulo} no texto que eu ia gravar em "
                f"`{caminho.name}`.",
                "Vou trocar o valor por uma leitura de variavel de ambiente "
                "(`process.env.NOME`, em arquivo de servidor) e registrar o nome no "
                "`.env.example`. "
                "Confirme e eu refaco.",
            )


# --------------------------------------------------------------------------- #
# 2. Processo: PLANO.md antes de codigo
# --------------------------------------------------------------------------- #

def checar_plano(raiz: Path, caminho: Path) -> None:
    if not eh_projeto_greenfield(raiz):
        return
    if estado_projeto(raiz).get("fase") == "scaffold":
        return  # /comecar ainda esta montando o projeto
    if not eh_codigo_fonte(caminho):
        return
    if (raiz / "PLANO.md").is_file():
        return
    bloquear(
        "Ainda nao existe um plano para este projeto.",
        "Neste projeto o codigo so e escrito depois que existe um `PLANO.md` com o "
        "escopo e o criterio de pronto. Isso evita construir a coisa errada e ter "
        "que jogar fora.",
        "Rode `/planejar`. Sao algumas perguntas sobre o que a aplicacao precisa fazer; "
        "no fim eu gravo o PLANO.md e ai `/construir` libera a escrita de codigo.",
    )


def main() -> None:
    evento = ler_evento()
    caminho = caminho_alvo(evento)
    if caminho is None:
        sair_ok()
    raiz = raiz_projeto(evento)
    checar_segredo(caminho, conteudo_escrito(evento))
    checar_plano(raiz, caminho)
    sair_ok()


if __name__ == "__main__":
    main()
