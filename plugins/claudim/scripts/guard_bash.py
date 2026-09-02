#!/usr/bin/env python3
"""PreToolUse | Bash.

Bloqueia o que o publico deste plugin nao sabe desfazer: push em main,
apagar arquivo em massa, e DDL/DML destrutiva em banco.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _shared import bloquear, ler_evento, raiz_projeto, sair_ok  # noqa: E402

RE_PUSH = re.compile(r"\bgit\s+push\b")
RE_PUSH_MAIN = re.compile(r"\bgit\s+push\b[^|;&]*\b(main|master|origin\s+(main|master))\b")

REGRAS = [
    (
        None,  # tratado por rm_destrutivo()
        "Apagar arquivos em massa (`rm -rf`).",
        "Esse comando apaga pasta inteira sem lixeira e sem confirmacao. "
        "Se pegar a pasta errada, nao tem como voltar.",
        "Me diga em portugues o que precisa sumir ('apaga a pasta de dados antigos') "
        "que eu apago um item por vez, mostrando cada um antes.",
    ),
    (
        re.compile(r"\b(DROP\s+(TABLE|DATABASE|SCHEMA)|TRUNCATE\s+(TABLE\s+)?\w)", re.I),
        "Comando que destroi dados no banco.",
        "DROP e TRUNCATE apagam a tabela inteira e nao dao para desfazer. "
        "O acesso desta aplicacao deveria ser somente leitura.",
        "Se a intencao era so olhar os dados, use SELECT — posso montar a consulta. "
        "Se precisa mesmo mexer na estrutura do banco, isso passa pelo time de dados.",
    ),
    (
        re.compile(r"\bDELETE\s+FROM\s+\w+\s*(;|$)", re.I),
        "DELETE sem WHERE.",
        "Isso apaga todas as linhas da tabela.",
        "Se era para apagar so um pedaco, diga qual filtro (ex.: 'so os registros de 2023') "
        "que eu escrevo o WHERE.",
    ),
    (
        re.compile(r"\bgit\s+(reset\s+--hard|clean\s+-[a-z]*f|checkout\s+--\s+\.)"),
        "Comando de git que joga fora o que voce escreveu.",
        "Esses comandos descartam alteracoes que ainda nao foram salvas em commit. "
        "Nao tem 'desfazer'.",
        "Se a ideia era voltar atras em algo, me diga o que quer desfazer que eu faco "
        "um commit de seguranca antes.",
    ),
    (
        re.compile(r"\bprisma\s+migrate\s+reset\b|\bdb\s+push\b[^|;&]*--force-reset", re.I),
        "Comando que apaga o banco inteiro.",
        "`prisma migrate reset` e `db push --force-reset` derrubam todas as tabelas "
        "e recriam do zero. Todo dado que estava la some, sem lixeira.",
        "Se a migracao deu conflito, me mostre a mensagem de erro que eu resolvo sem "
        "apagar nada. Se voce quer mesmo comecar o banco do zero, isso passa pelo "
        "time de dados.",
    ),
    (
        re.compile(r"\brm\b[^|;&]*\.(db|sqlite|db-journal)\b", re.I),
        "Apagar o arquivo do banco.",
        "`prisma/dev.db` e o banco inteiro desta aplicacao — tudo que foi salvo "
        "esta ali dentro. Apagar o arquivo nao tem lixeira nem desfazer.",
        "Se a ideia era recomecar com dados de exemplo, eu faco isso sem apagar "
        "nada seu: me diga 'recomeca o banco de exemplo' que eu rodo o seed. "
        "Se voce quer mesmo zerar tudo, confirme por escrito que pode perder o "
        "que ja foi salvo.",
    ),
    (
        re.compile(r"\bvercel\b[^|;&]*(--prod\b|\bpromote\b)", re.I),
        "Publicar direto em producao.",
        "Isso coloca a versao atual no ar para todo mundo, sem ninguem ter revisado. "
        "Nesta versao do plugin a aplicacao roda na sua maquina; publicar ainda nao "
        "faz parte do processo.",
        "Rode `/revisar` primeiro. Para mostrar a tela para alguem, `vercel` sem "
        "`--prod` gera um link de preview — posso fazer isso.",
    ),
    (
        re.compile(r"\bgit\s+push\b[^|;&]*(--force|-f\b)"),
        "Push forcado.",
        "Push forcado reescreve o historico remoto e pode apagar trabalho de outra pessoa.",
        "Nao precisa disso aqui. Se o push normal reclamou, me mostre a mensagem "
        "que eu resolvo.",
    ),
]


def rm_destrutivo(comando: str) -> bool:
    """`rm` com recursivo E forcado, em qualquer ordem de flag."""
    for segmento in re.split(r"[|;&\n]", comando):
        tokens = segmento.split()
        if "rm" not in tokens[:2]:
            continue
        flags = "".join(t for t in tokens if t.startswith("-")).lower()
        if ("r" in flags and "f" in flags) or (
            "--recursive" in segmento and "--force" in segmento
        ):
            return True
    return False


def branch_atual(raiz: Path) -> str:
    if not shutil.which("git"):
        return ""
    try:
        r = subprocess.run(
            ["git", "-C", str(raiz), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip()
    except Exception:
        return ""


def main() -> None:
    evento = ler_evento()
    comando = (evento.get("tool_input") or {}).get("command") or ""
    if not comando:
        sair_ok()

    for padrao, titulo, motivo, passo in REGRAS:
        acionou = rm_destrutivo(comando) if padrao is None else bool(padrao.search(comando))
        if acionou:
            bloquear(titulo, motivo, passo)

    if RE_PUSH.search(comando):
        alvo_main = bool(RE_PUSH_MAIN.search(comando))
        na_main = branch_atual(raiz_projeto(evento)) in {"main", "master"}
        if alvo_main or na_main:
            bloquear(
                "Enviar codigo direto para a branch principal.",
                "A branch `main` e a versao que os outros usam. Enviando direto para ela, "
                "um erro seu vira o problema de todo mundo — e voltar atras exige git "
                "que voce nao precisa aprender.",
                "Vou criar uma branch com o seu nome e abrir um Pull Request. "
                "Diga 'pode abrir o PR' que eu faco os dois passos.",
            )

    sair_ok()


if __name__ == "__main__":
    main()
