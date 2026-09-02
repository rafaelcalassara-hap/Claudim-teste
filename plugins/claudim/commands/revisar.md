---
description: Revisão de compliance e qualidade por um agente que só lê, nunca altera
allowed-tools: Task, Read, Glob, Grep, Bash
---

# /revisar — auditoria antes de mostrar para alguém

Dispare o subagent **revisor** (`Task`, `subagent_type: revisor`). Ele é
read-only de propósito: revisor que conserta enquanto revisa esconde o
problema em vez de mostrar.

Passe para ele: caminho do projeto, conteúdo de `PLANO.md`, e a flag
`dado_sensivel` de `.greenfield/state.json`.

## Quando o revisor voltar

Traduza o relatório para o usuário nesta forma, nesta ordem:

**🔴 Precisa resolver antes de usar** — segredo commitado, PII/dado de saúde
em código, vazamento em tracking, copy de plano/preço/rede sem aval de
compliance.

**🟡 Ficou faltando do plano** — item do `PLANO.md` marcado como feito mas não
entregue, ou não marcado.

**⚪ Dá para melhorar** — o resto.

Regras da entrega:

- No máximo 7 itens. Se houver mais, mostre os 7 mais graves e diga quantos
  sobraram.
- Cada item em uma frase, sem jargão, com o que fazer em seguida.
- **Não corrija nada sozinho.** Pergunte: "quer que eu resolva os vermelhos?"
  Se sim, aí sim edite — mas isso é trabalho de `/construir`, não de `/revisar`.
- Se não achou nada vermelho, diga isso em uma linha. Não invente achado para
  parecer útil.
