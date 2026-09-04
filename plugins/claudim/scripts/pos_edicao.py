#!/usr/bin/env python3
"""PostToolUse | Write, Edit, MultiEdit.

Porta unica do que roda depois de cada escrita: prettier primeiro, eslint --fix
depois. Um processo em vez de dois, e — mais importante — a ordem fica
garantida: o eslint sempre ve o arquivo ja formatado, nunca o contrario.

Nenhum dos dois trava o trabalho por conta propria. Quem sai com exit 2 e so o
lint, quando sobra erro que o --fix nao resolve, e o texto vai para o modelo
pelo stderr — nunca para a tela de quem pediu a aplicacao.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import post_format  # noqa: E402
import post_lint  # noqa: E402
from _shared import ler_evento  # noqa: E402


def main() -> None:
    evento = ler_evento()
    post_format.formatar(evento)
    post_lint.lintar(evento)


if __name__ == "__main__":
    main()
