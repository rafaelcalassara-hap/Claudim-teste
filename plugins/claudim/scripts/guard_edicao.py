#!/usr/bin/env python3
"""PreToolUse | Write, Edit, MultiEdit, NotebookEdit.

Porta unica dos tres guards de escrita. Antes eram tres entradas no hooks.json:
tres processos Python por edicao, cada um relendo o stdin e reimportando o
_shared. Agora e um processo que chama os tres na ordem.

Ordem importa e e esta:

  1. guard_write — segredo e a regra "sem PLANO.md nao ha codigo";
  2. guard_pii   — CPF/CNS real, condicao de saude em fixture ou em tracking;
  3. guard_auth  — modelo de acesso (so em projeto do /comecar).

O primeiro que achar problema chama bloquear(), que sai com exit 2 e leva a
mensagem para o modelo. Os seguintes nao rodam — de proposito: uma edicao
bloqueada com tres motivos de uma vez nao ajuda ninguem a consertar.

Cada guard continua rodavel sozinho (`python3 guard_pii.py < evento.json`), que
e como o testar_hooks.py exercita caso a caso.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import guard_auth  # noqa: E402
import guard_pii  # noqa: E402
import guard_write  # noqa: E402
from _shared import ler_evento, sair_ok  # noqa: E402


def main() -> None:
    evento = ler_evento()
    guard_write.checar(evento)
    guard_pii.checar(evento)
    guard_auth.checar(evento)
    sair_ok()


if __name__ == "__main__":
    main()
