#!/usr/bin/env python3
"""PreToolUse | Write, Edit, MultiEdit, NotebookEdit.

Segura o modelo de acesso da aplicacao. A regra do plugin e curta:

  * a aplicacao nasce fechada e nao tem tela de criar conta;
  * quem entra esta em EMAILS_PERMITIDOS, no .env;
  * senha, cadastro e recuperacao sao telas do Clerk — este codigo nunca
    guarda senha, nunca gera token de recuperacao e nunca manda e-mail.

Instrucao em skill nao segura isso: quem usa o plugin nao percebe que uma tela
de autocadastro abriu a aplicacao interna para a internet. Por isso e hook.

Vale so em projeto criado pelo /comecar (tem pasta .greenfield/).
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
    eh_projeto_greenfield,
    ler_evento,
    raiz_projeto,
    sair_ok,
)

PROXIMO_PASSO_LISTA = (
    "Para liberar mais gente, acrescente o e-mail em `EMAILS_PERMITIDOS` no `.env` "
    "— uma linha, sem codigo. Se o PLANO.md pede outra coisa, me diga qual e eu "
    "explico o que da para fazer sem mexer no login."
)


# --------------------------------------------------------------------------- #
# 1. Tela de autocadastro
# --------------------------------------------------------------------------- #

RE_ROTA_CADASTRO = re.compile(r"(^|/)(criar-conta|cadastrar|cadastro|sign-?up)(/|$)", re.I)
RE_ROTA_CADASTRO_CATCHALL = re.compile(r"\[\[\.\.\.sign-?up\]\]", re.I)
RE_COMPONENTE_CADASTRO = re.compile(r"<SignUp\b|\bSignUpButton\b|useSignUp\b")


def checar_autocadastro(caminho: Path, conteudo: str) -> None:
    texto = str(caminho).replace("\\", "/")
    achou_rota = RE_ROTA_CADASTRO.search(texto) or RE_ROTA_CADASTRO_CATCHALL.search(texto)
    achou_componente = RE_COMPONENTE_CADASTRO.search(conteudo)
    if not (achou_rota or achou_componente):
        return
    bloquear(
        "Esta aplicacao nao tem tela de criar conta.",
        "Acesso aqui e concedido, nao pedido: a aplicacao e interna e quem entra "
        "esta na lista `EMAILS_PERMITIDOS`. Uma tela de autocadastro deixa qualquer "
        "pessoa que descubra o endereco criar a propria conta.",
        PROXIMO_PASSO_LISTA,
    )


# --------------------------------------------------------------------------- #
# 2. Senha, token de recuperacao e e-mail de recuperacao
# --------------------------------------------------------------------------- #

RE_COLUNA_SENHA = re.compile(
    r"\b(senha_?hash|hash_?senha|password_?hash|hash_?password|encrypted_password|"
    r"passwordDigest|senhaCriptografada)\b", re.I
)
RE_HASH_SENHA = re.compile(r"\b(bcrypt|argon2|@node-rs/argon2|scryptSync|pbkdf2Sync)\b")
RE_TOKEN_RECUPERACAO = re.compile(
    r"\b(reset_?token|token_?reset|password_?reset|reset_?password|"
    r"token_?recuperacao|recuperar_?senha|esqueci[-_]?(minha[-_]?)?senha|forgot[-_]?password)\b",
    re.I,
)
RE_LIB_EMAIL = re.compile(
    r"(nodemailer|@sendgrid/mail|['\"]postmark['\"]|mailgun|['\"]resend['\"]|"
    r"@aws-sdk/client-ses|smtp\.)", re.I
)
RE_CONTEXTO_SENHA = re.compile(r"\b(senha|password|recupera\w*|reset)\b", re.I)


def checar_senha(caminho: Path, conteudo: str) -> None:
    achado = RE_COLUNA_SENHA.search(conteudo) or RE_HASH_SENHA.search(conteudo)
    if achado:
        bloquear(
            "Esta aplicacao nao guarda senha.",
            f"`{achado.group(0)}` — senha, cadastro e troca de senha sao telas do Clerk. "
            "Guardar senha aqui significa escrever hash, comparacao e expiracao a mao, "
            "que e o lugar onde autenticacao caseira costuma vazar.",
            "Nao crie tabela de usuario nem coluna de senha. Quem pode entrar sai da "
            "lista `EMAILS_PERMITIDOS`; a senha e a conta ficam no Clerk. "
            "Uma tabela `Usuario` sem senha, so para registrar quem fez o que, pode — "
            "guarde o id da sessao do Clerk, nao credencial.",
        )

    achado = RE_TOKEN_RECUPERACAO.search(conteudo)
    if achado:
        bloquear(
            "Recuperacao de senha nao e desta aplicacao.",
            f"`{achado.group(0)}` — token de recuperacao precisa de expiracao, uso unico "
            "e comparacao a prova de timing. Errar um desses e conta invadida, e nada "
            "disso aparece quando voce abre a tela e ela funciona.",
            "O Clerk ja manda o e-mail de recuperacao, nas telas dele. Nao escreva tela "
            "de 'esqueci minha senha'.",
        )

    if RE_LIB_EMAIL.search(conteudo) and RE_CONTEXTO_SENHA.search(conteudo):
        bloquear(
            "Esta aplicacao nao manda e-mail de senha.",
            "O texto junta uma biblioteca de envio de e-mail com assunto de senha ou "
            "recuperacao. Esse e-mail e o do Clerk, e mandar um proprio significa "
            "provisionar remetente, dominio e chave — nada disso existe no projeto.",
            "Deixe recuperacao de senha com o Clerk. Se a aplicacao precisa mandar "
            "outro tipo de e-mail (um relatorio, por exemplo), me diga qual — isso e "
            "outra conversa e passa pelo `/planejar`.",
        )


# --------------------------------------------------------------------------- #
# 3. Trocar o Clerk por outra biblioteca de sessao
# --------------------------------------------------------------------------- #

RE_OUTRA_AUTH = re.compile(
    r"(['\"]next-auth['\"]|['\"]@auth/[a-z-]+['\"]|['\"]better-auth['\"]|"
    r"['\"]lucia['\"]|['\"]iron-session['\"]|['\"]passport['\"]|"
    r"['\"]express-session['\"]|['\"]@supabase/auth[a-z-]*['\"])",
    re.I,
)


def checar_outra_auth(conteudo: str) -> None:
    achado = RE_OUTRA_AUTH.search(conteudo)
    if achado:
        bloquear(
            "O login deste projeto e o Clerk.",
            f"`{achado.group(0)}` e outra biblioteca de sessao. Duas bibliotecas de "
            "login no mesmo projeto e a receita de rota que parece protegida e nao esta.",
            "Use `exigirSessao()` de `lib/auth.ts`, que ja fala com o Clerk e ja "
            "confere a lista de quem pode entrar. " + PROXIMO_PASSO_LISTA,
        )


# --------------------------------------------------------------------------- #
# 4. Afrouxar o middleware
# --------------------------------------------------------------------------- #

RE_MATCHER = re.compile(r"createRouteMatcher\(\s*\[(.*?)\]", re.S)
RE_LITERAL = re.compile(r"['\"]([^'\"]+)['\"]")


def checar_middleware(caminho: Path, conteudo: str) -> None:
    if caminho.name != "middleware.ts":
        return
    achado = RE_MATCHER.search(conteudo)
    if not achado:
        return
    for rota in RE_LITERAL.findall(achado.group(1)):
        if not rota.startswith("/entrar"):
            bloquear(
                "Rota publica nova no middleware.",
                f"`{rota}` ficaria acessivel sem login. Nesta aplicacao a unica porta "
                "publica e `/entrar` — toda outra tela exige sessao. Rota publica aqui "
                "nao e conveniencia de teste, e a aplicacao interna aberta na internet.",
                "Para ver a tela sem login durante o desenvolvimento, deixe o `.env` "
                "sem as chaves do Clerk: o projeto ja sobe sem login nesse caso e "
                "`exigirSessao()` impede que isso chegue a producao. " + PROXIMO_PASSO_LISTA,
            )


# --------------------------------------------------------------------------- #
# 5. Tirar a lista de dentro do exigirSessao()
# --------------------------------------------------------------------------- #

RE_DEFINE_SESSAO = re.compile(r"export\s+async\s+function\s+exigirSessao\b")


def checar_allowlist(conteudo: str) -> None:
    if not RE_DEFINE_SESSAO.search(conteudo):
        return
    if "emailPermitido" in conteudo:
        return
    bloquear(
        "O `exigirSessao()` perdeu a checagem de quem pode entrar.",
        "Sem `emailPermitido()`, basta ter conta no Clerk para entrar — e qualquer "
        "pessoa pode criar uma. Estar logado nao e o mesmo que ter acesso a esta "
        "aplicacao; a lista `EMAILS_PERMITIDOS` e quem autoriza.",
        "Mantenha a checagem de `emailPermitido()` depois do `auth()` em "
        "`lib/auth.ts`. " + PROXIMO_PASSO_LISTA,
    )


def main() -> None:
    evento = ler_evento()
    caminho = caminho_alvo(evento)
    if caminho is None:
        sair_ok()
    if not eh_projeto_greenfield(raiz_projeto(evento)):
        sair_ok()  # fora de projeto do /comecar o plugin nao manda no login

    conteudo = conteudo_escrito(evento)
    checar_autocadastro(caminho, conteudo)
    checar_senha(caminho, conteudo)
    checar_outra_auth(conteudo)
    checar_middleware(caminho, conteudo)
    checar_allowlist(conteudo)
    sair_ok()


if __name__ == "__main__":
    main()
