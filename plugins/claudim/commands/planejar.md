---
description: Entrevista você e grava o PLANO.md com o que a aplicação precisa fazer
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Skill
---

# /planejar — decidir o que construir

Invoque a skill **escrever-plano** e siga o roteiro dela.

Contexto obrigatório antes de perguntar qualquer coisa:

- Leia `CLAUDE.md` e `.greenfield/state.json` — objetivo, público e flag de
  dado sensível já foram respondidos no `/comecar`. **Não pergunte de novo.**
- Se já existe `PLANO.md`, leia. Você está adicionando escopo, não recomeçando:
  mostre o que já está lá e pergunte o que muda.

Regras que não são negociáveis:

- O critério de pronto é escrito em linguagem de negócio ("consigo filtrar por
  mês e exportar CSV"), nunca técnica ("endpoint retorna 200").
- Nada de estimativa de tempo. O usuário não tem base para avaliar.
- **Mostre o plano e peça confirmação antes de gravar.** Se pedir mudança,
  ajuste e mostre de novo.
- Se a pessoa pedir mais do que cabe numa primeira versão, corte e diga o que
  ficou para depois — numa seção "Fora desta versão". Não silencie o corte.

Se o projeto está marcado como dado sensível, a skill `dados-sensiveis` decide
o que entra na seção de compliance do plano.

Termine com: **"Pronto. Agora rode `/construir`."**
