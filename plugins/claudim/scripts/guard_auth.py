#!/usr/bin/env python3
"""PreToolUse | Write, Edit, MultiEdit, NotebookEdit.

Segura o modelo de acesso da aplicacao. A regra do plugin e curta:

  * a aplicacao nasce fechada e nao tem tela de criar conta;
  * quem entra esta em EMAILS_PERMITIDOS, no .env;
  * a conta e a do Google Workspace da empresa — este codigo nunca guarda
    senha, nunca gera token de recuperacao e nunca manda e-mail.

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
        "Acesso aqui e concedido, nao pedido: a aplicacao e interna, a conta e a do "
        "Google da empresa e quem entra esta na lista `EMAILS_PERMITIDOS`. Uma tela "
        "de autocadastro deixa qualquer pessoa que descubra o endereco criar a "
        "propria conta.",
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
            f"`{achado.group(0)}` — a senha da pessoa e a da conta Google dela, e quem "
            "cuida disso e o Google. Guardar senha aqui significa escrever hash, "
            "comparacao e expiracao a mao, que e o lugar onde autenticacao caseira "
            "costuma vazar.",
            "Nao crie tabela de usuario nem coluna de senha. Quem pode entrar sai da "
            "lista `EMAILS_PERMITIDOS`; a senha e a conta ficam no Google. "
            "Uma tabela `Usuario` sem senha, so para registrar quem fez o que, pode — "
            "guarde o e-mail da sessao, nao credencial.",
        )

    achado = RE_TOKEN_RECUPERACAO.search(conteudo)
    if achado:
        bloquear(
            "Recuperacao de senha nao e desta aplicacao.",
            f"`{achado.group(0)}` — token de recuperacao precisa de expiracao, uso unico "
            "e comparacao a prova de timing. Errar um desses e conta invadida, e nada "
            "disso aparece quando voce abre a tela e ela funciona.",
            "Quem esqueceu a senha recupera na conta Google da empresa, nao aqui. Nao "
            "escreva tela de 'esqueci minha senha'.",
        )

    if RE_LIB_EMAIL.search(conteudo) and RE_CONTEXTO_SENHA.search(conteudo):
        bloquear(
            "Esta aplicacao nao manda e-mail de senha.",
            "O texto junta uma biblioteca de envio de e-mail com assunto de senha ou "
            "recuperacao. Esse e-mail e do Google, e mandar um proprio significa "
            "provisionar remetente, dominio e chave — nada disso existe no projeto.",
            "Deixe recuperacao de senha com o Google. Se a aplicacao precisa mandar "
            "outro tipo de e-mail (um relatorio, por exemplo), me diga qual — isso e "
            "outra conversa e passa pelo `/planejar`.",
        )


# --------------------------------------------------------------------------- #
# 3. Trocar o login por outra biblioteca de sessao
# --------------------------------------------------------------------------- #

RE_OUTRA_AUTH = re.compile(
    r"(['\"]@clerk/[a-z0-9/-]+['\"]|['\"]better-auth(/[a-z0-9/-]+)?['\"]|['\"]lucia['\"]|"
    r"['\"]iron-session['\"]|['\"]passport['\"]|['\"]express-session['\"]|"
    r"['\"]@supabase/auth[a-z0-9/-]*['\"]|['\"]@auth0/[a-z0-9/-]+['\"])",
    re.I,
)


def checar_outra_auth(conteudo: str) -> None:
    achado = RE_OUTRA_AUTH.search(conteudo)
    if achado:
        bloquear(
            "O login deste projeto e a conta Google da empresa, pelo next-auth.",
            f"`{achado.group(0)}` e outra biblioteca de sessao. Duas bibliotecas de "
            "login no mesmo projeto e a receita de rota que parece protegida e nao esta.",
            "Use `exigirSessao()` de `lib/auth.ts`, que ja le a sessao e ja confere a "
            "lista de quem pode entrar. " + PROXIMO_PASSO_LISTA,
        )


# --------------------------------------------------------------------------- #
# 4. Provider de senha no next-auth
# --------------------------------------------------------------------------- #

RE_PROVIDER_SENHA = re.compile(
    r"(next-auth/providers/credentials|\bCredentialsProvider\b|\bCredentials\s*\()", re.I
)


def checar_provider_credenciais(conteudo: str) -> None:
    achado = RE_PROVIDER_SENHA.search(conteudo)
    if not achado:
        return
    bloquear(
        "Provider de usuario e senha nao entra neste projeto.",
        f"`{achado.group(0)}` — o provider `Credentials` do next-auth traz a senha de "
        "volta para dentro desta aplicacao: passa a ser voce a guardar hash, comparar e "
        "expirar. O unico provider aqui e o Google da empresa.",
        "Deixe o `providers` do `auth.ts` so com `Google(...)`. Quem entra sai da lista "
        "`EMAILS_PERMITIDOS`. " + PROXIMO_PASSO_LISTA,
    )


# --------------------------------------------------------------------------- #
# 5. Afrouxar o middleware
# --------------------------------------------------------------------------- #

# As duas unicas portas publicas: a tela de entrada e o retorno do Google.
PUBLICO_PERMITIDO = ("/entrar", "/api/auth")

RE_LISTA_PUBLICO = re.compile(r"\bPUBLICO\b\s*(?::[^=]*?)?=\s*\[(.*?)\]", re.S)
RE_LITERAL = re.compile(r"['\"]([^'\"]+)['\"]")


def checar_middleware(caminho: Path, conteudo: str) -> None:
    if caminho.name != "middleware.ts":
        return
    achado = RE_LISTA_PUBLICO.search(conteudo)
    if not achado:
        return
    for rota in RE_LITERAL.findall(achado.group(1)):
        if not rota.startswith(PUBLICO_PERMITIDO):
            bloquear(
                "Rota publica nova no middleware.",
                f"`{rota}` ficaria acessivel sem login. Nesta aplicacao as unicas portas "
                "publicas sao `/entrar` e `/api/auth` — toda outra tela exige sessao. "
                "Rota publica aqui nao e conveniencia de teste, e a aplicacao interna "
                "aberta na internet.",
                "Para ver a tela sem login durante o desenvolvimento, deixe o `.env` "
                "sem `AUTH_GOOGLE_ID`: o projeto ja sobe sem login nesse caso e "
                "`exigirSessao()` impede que isso chegue a producao. " + PROXIMO_PASSO_LISTA,
            )


# --------------------------------------------------------------------------- #
# 6. Tirar a lista do exigirSessao() ou do callback signIn
# --------------------------------------------------------------------------- #

RE_DEFINE_SESSAO = re.compile(r"export\s+async\s+function\s+exigirSessao\b")
RE_CONFIG_NEXTAUTH = re.compile(r"NextAuth\s*\(\s*\{")


def checar_allowlist(conteudo: str) -> None:
    if RE_DEFINE_SESSAO.search(conteudo) and "emailPermitido" not in conteudo:
        bloquear(
            "O `exigirSessao()` perdeu a checagem de quem pode entrar.",
            "Sem `emailPermitido()`, quem foi tirado da lista continua entrando ate o "
            "cookie vencer. Estar logado no Google nao e o mesmo que ter acesso a esta "
            "aplicacao; a lista `EMAILS_PERMITIDOS` e quem autoriza, e ela precisa "
            "valer a cada requisicao.",
            "Mantenha a checagem de `emailPermitido()` depois do `auth()` em "
            "`lib/auth.ts`. " + PROXIMO_PASSO_LISTA,
        )

    if RE_CONFIG_NEXTAUTH.search(conteudo) and "emailPermitido" not in conteudo:
        bloquear(
            "A configuracao do login perdeu o callback que confere a lista.",
            "Sem `emailPermitido()` no callback `signIn`, qualquer pessoa com uma conta "
            "Google entra — inclusive de fora da empresa. O parametro `hd` da tela do "
            "Google e so uma dica: da para tirar da URL, e nao protege nada sozinho.",
            "Mantenha em `auth.ts` o callback `signIn` conferindo "
            "`profile.email_verified` e `emailPermitido(profile.email)`. "
            + PROXIMO_PASSO_LISTA,
        )


def checar(evento: dict) -> None:
    caminho = caminho_alvo(evento)
    if caminho is None:
        return
    if not eh_projeto_greenfield(raiz_projeto(evento)):
        return  # fora de projeto do /comecar o plugin nao manda no login

    conteudo = conteudo_escrito(evento)
    checar_autocadastro(caminho, conteudo)
    checar_senha(caminho, conteudo)
    checar_outra_auth(conteudo)
    checar_provider_credenciais(conteudo)
    checar_middleware(caminho, conteudo)
    checar_allowlist(conteudo)


if __name__ == "__main__":
    checar(ler_evento())
    sair_ok()
