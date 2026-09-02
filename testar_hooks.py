#!/usr/bin/env python3
"""Smoke test dos hooks. Rode antes de publicar uma versao do plugin:

    python3 testar_hooks.py

Cada caso alimenta o script de hook com o JSON que o Claude Code enviaria e
confere o exit code (2 = bloqueado, 0 = liberado).
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).parent / "plugins" / "claudim" / "scripts"


def rodar(script: str, evento: dict) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        input=json.dumps(evento), capture_output=True, text=True, timeout=20,
    )
    return r.returncode, (r.stderr or r.stdout).strip()


def escrita(cwd: str, caminho: str, conteudo: str = "const x = 1;") -> dict:
    return {
        "hook_event_name": "PreToolUse", "tool_name": "Write", "cwd": cwd,
        "tool_input": {"file_path": caminho, "content": conteudo},
    }


def bash(cwd: str, comando: str) -> dict:
    return {
        "hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": cwd,
        "tool_input": {"command": comando},
    }


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="greenfield-teste-"))
    projeto = tmp / "projeto"
    (projeto / ".greenfield").mkdir(parents=True)
    (projeto / ".greenfield" / "state.json").write_text('{"fase": "pronto"}')
    p = str(projeto)

    # CPF valido gerado na hora (nao fica escrito neste arquivo).
    def digito(ds):
        peso = len(ds) + 1
        return (sum(d * (peso - i) for i, d in enumerate(ds)) * 10) % 11 % 10
    base = [5, 2, 9, 9, 8, 2, 2, 4, 7]
    base += [digito(base)]
    base += [digito(base)]
    cpf_valido = "".join(map(str, base))

    casos = [
        # (nome, script, evento, deve_bloquear)
        ("segredo: escrever .env", "guard_write", escrita(p, f"{p}/.env", "SENHA=1"), True),
        ("segredo: .env.example liberado", "guard_write", escrita(p, f"{p}/.env.example", "X="), False),
        ("segredo: chave .pem", "guard_write", escrita(p, f"{p}/chave.pem", "----"), True),
        ("segredo: senha na string de conexao", "guard_write",
         escrita(p, f"{p}/lib/db.ts", 'const URL="postgresql://user:s3nha@host/db"'), True),
        ("segredo: chave do cliente OAuth do Google em codigo", "guard_write",
         escrita(p, f"{p}/auth.ts", 'const k = "GOCSPX-aBcDeFgHiJkLmNoPqRsTuVwX";'), True),
        ("segredo: NEXT_PUBLIC_ com segredo", "guard_write",
         escrita(p, f"{p}/lib/config.ts", 'process.env.NEXT_PUBLIC_AUTH_GOOGLE_SECRET'), True),
        # Fora do projeto greenfield: isola a regra de segredo da regra de PLANO.md.
        ("segredo: NEXT_PUBLIC_ publico liberado", "guard_write",
         escrita(str(tmp), f"{tmp}/config.ts", 'process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY'), False),
        ("processo: .tsx sem PLANO.md", "guard_write", escrita(p, f"{p}/app/page.tsx"), True),
        ("processo: package.json liberado", "guard_write",
         escrita(p, f"{p}/package.json", '{"name": "x"}'), False),
        ("processo: markdown liberado", "guard_write", escrita(p, f"{p}/notas.md", "oi"), False),
        ("processo: fora de projeto greenfield", "guard_write",
         escrita(str(tmp), f"{tmp}/qualquer.tsx"), False),
        ("pii: CPF valido em codigo", "guard_pii",
         escrita(p, f"{p}/prisma/seed.ts", f'const CPF = "{cpf_valido}";'), True),
        ("pii: CPF invalido liberado", "guard_pii",
         escrita(p, f"{p}/prisma/seed.ts", 'const CPF = "11111111111";'), False),
        ("pii: condicao de saude em fixture", "guard_pii",
         escrita(p, f"{p}/prisma/seed.ts", 'const L = [{ cond: "oncologia" }];'), True),
        ("pii: condicao de saude em tracking", "guard_pii",
         escrita(p, f"{p}/app/page.tsx", 'gtag("event", "lead_oncologia")'), True),
        ("pii: codigo normal liberado", "guard_pii",
         escrita(p, f"{p}/app/page.tsx", 'export default function P() { return <h1>Leads</h1>; }'), False),
        ("bash: git push main", "guard_bash", bash(p, "git push origin main"), True),
        ("bash: rm -rf", "guard_bash", bash(p, "rm -rf ./dados"), True),
        ("bash: rm -f simples liberado", "guard_bash", bash(p, "rm -f temp.txt"), False),
        ("bash: DROP TABLE", "guard_bash", bash(p, 'psql -c "DROP TABLE leads"'), True),
        ("bash: TRUNCATE", "guard_bash", bash(p, "TRUNCATE TABLE eventos;"), True),
        ("bash: git reset --hard", "guard_bash", bash(p, "git reset --hard HEAD~1"), True),
        ("bash: git push --force", "guard_bash", bash(p, "git push --force origin trabalho"), True),
        ("bash: prisma migrate reset", "guard_bash", bash(p, "npx prisma migrate reset"), True),
        ("bash: db push --force-reset", "guard_bash",
         bash(p, "npx prisma db push --force-reset"), True),
        ("bash: deploy em producao", "guard_bash", bash(p, "vercel --prod"), True),
        ("bash: SELECT liberado", "guard_bash", bash(p, 'psql -c "SELECT 1 LIMIT 1"'), False),
        ("bash: npm run dev liberado", "guard_bash", bash(p, "npm run dev"), False),
        ("bash: prisma migrate dev liberado", "guard_bash",
         bash(p, "npx prisma migrate dev --name eventos"), False),
        ("bash: preview da vercel liberado", "guard_bash", bash(p, "vercel"), False),
        ("bash: apagar o arquivo do banco", "guard_bash", bash(p, "rm prisma/dev.db"), True),
        ("bash: apagar .sqlite", "guard_bash", bash(p, "rm -f dados.sqlite"), True),
        ("bash: db seed liberado", "guard_bash", bash(p, "npx prisma db seed"), False),
        ("bash: db push liberado", "guard_bash", bash(p, "npx prisma db push"), False),
        # --- acesso: a aplicacao nasce fechada e nao tem tela de criar conta ---
        ("auth: rota de criar conta", "guard_auth",
         escrita(p, f"{p}/app/criar-conta/page.tsx", "export default function P() {}"), True),
        ("auth: componente SignUp", "guard_auth",
         escrita(p, f"{p}/app/entrar/page.tsx", "return <SignUp />;"), True),
        ("auth: coluna de senha no schema", "guard_auth",
         escrita(p, f"{p}/prisma/schema.prisma",
                 "model Usuario {\n  senhaHash String @map(\"senha_hash\")\n}"), True),
        ("auth: hash de senha com bcrypt", "guard_auth",
         escrita(p, f"{p}/lib/login.ts", 'import bcrypt from "bcrypt";'), True),
        ("auth: token de recuperacao", "guard_auth",
         escrita(p, f"{p}/prisma/schema.prisma", "model PasswordReset { resetToken String }"), True),
        ("auth: e-mail de recuperacao de senha", "guard_auth",
         escrita(p, f"{p}/lib/email.ts",
                 'import nodemailer from "nodemailer";\nexport const assunto = "Recuperar senha";'), True),
        ("auth: outra biblioteca de login", "guard_auth",
         escrita(p, f"{p}/lib/auth.ts", 'import { clerkMiddleware } from "@clerk/nextjs/server";'), True),
        ("auth: better-auth", "guard_auth",
         escrita(p, f"{p}/lib/auth.ts", 'import { betterAuth } from "better-auth";'), True),
        ("auth: next-auth liberado", "guard_auth",
         escrita(p, f"{p}/auth.ts",
                 'import NextAuth from "next-auth";\nimport Google from "next-auth/providers/google";\n'
                 'export const { auth } = NextAuth({ callbacks: { signIn({ profile }) '
                 '{ return emailPermitido(profile.email); } } });'), False),
        ("auth: provider Credentials", "guard_auth",
         escrita(p, f"{p}/auth.ts",
                 'import Credentials from "next-auth/providers/credentials";'), True),
        ("auth: config do NextAuth sem a lista", "guard_auth",
         escrita(p, f"{p}/auth.ts",
                 'export const { auth } = NextAuth({ providers: [Google] });'), True),
        ("auth: rota publica nova no middleware", "guard_auth",
         escrita(p, f"{p}/middleware.ts",
                 'const PUBLICO = ["/entrar", "/api/auth", "/relatorio"];'), True),
        ("auth: middleware so com as duas portas liberado", "guard_auth",
         escrita(p, f"{p}/middleware.ts",
                 'const PUBLICO = ["/entrar", "/api/auth"];'), False),
        ("auth: exigirSessao sem a lista", "guard_auth",
         escrita(p, f"{p}/lib/auth.ts",
                 "export async function exigirSessao() {\n  const sessao = await auth();\n  return sessao.user.email;\n}"), True),
        ("auth: exigirSessao com a lista liberado", "guard_auth",
         escrita(p, f"{p}/lib/auth.ts",
                 "export async function exigirSessao() {\n  if (!emailPermitido(e)) throw new Error();\n  return e;\n}"), False),
        ("auth: tela comum liberada", "guard_auth",
         escrita(p, f"{p}/app/page.tsx", "export default function P() { return <h1>Leads</h1>; }"), False),
        ("auth: tabela Usuario sem senha liberada", "guard_auth",
         escrita(p, f"{p}/prisma/schema.prisma", "model Usuario { id String @id\n  email String }"), False),
        ("auth: fora de projeto greenfield", "guard_auth",
         escrita(str(tmp), f"{tmp}/app/criar-conta/page.tsx", "return <SignUp />;"), False),
    ]

    # Este caso so vale depois que o PLANO.md existir; roda por ultimo.
    def criar_plano():
        (projeto / "PLANO.md").write_text("- [ ] 1. tela")

    casos.append((criar_plano, None, None, None))
    casos.append(("processo: .tsx com PLANO.md", "guard_write",
                  escrita(p, f"{p}/app/page.tsx"), False))

    falhas = 0
    total = 0
    for nome, script, evento, deve_bloquear in casos:
        if callable(nome):
            nome()
            continue
        total += 1
        codigo, saida = rodar(f"{script}.py", evento)
        bloqueou = codigo == 2
        ok = bloqueou == deve_bloquear
        falhas += not ok
        marca = "ok  " if ok else "FALHA"
        esperado = "bloquear" if deve_bloquear else "liberar"
        print(f"[{marca}] {nome}  (esperado: {esperado}, exit={codigo})")
        if not ok and saida:
            print("        " + saida.splitlines()[0][:120])

    print(f"\n{total - falhas}/{total} passaram.")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
