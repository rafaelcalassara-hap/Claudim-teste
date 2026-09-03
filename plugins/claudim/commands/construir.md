---
description: Implementa o PLANO.md passo a passo e sobe a aplicação para você ver
allowed-tools: Read, Write, Edit, MultiEdit, Bash, Glob, Grep, Skill, TodoWrite
---

# /construir — implementar o plano

## Antes de escrever código

1. Leia `PLANO.md`. Se não existir, pare: "Ainda não há plano. Rode `/planejar`."
2. Leia `CLAUDE.md` e `.greenfield/state.json`.
3. Pegue o primeiro passo **não marcado**. Um passo por vez.

## Enquanto constrói

- Siga a skill `next-padroes` para qualquer tela, componente ou action.
- Vai criar tela, componente, cor ou classe Tailwind? Leia
  `docs/design-system/DESIGN.md` **antes** de escrever, não depois. Valor de
  cor, raio e sombra sai de lá — não do seu gosto.
- Toque em CPF, carteirinha, beneficiário, diagnóstico, URL ou tracking?
  Invoque `dados-sensiveis` **antes** de escrever, não depois.
- Consulta, schema ou migração: skill `consultar-banco`. Tabela de sistema
  corporativo é leitura, sempre.
- Ao concluir um passo, marque `- [x]` no `PLANO.md` na hora. Não deixe para
  o fim — sessão longa perde o fio.

Vibe-coding é permitido aqui. Improvisar *dentro* de um passo do plano é ok;
inventar um passo que não está no plano não é. Se descobrir que falta algo,
diga ao usuário e ofereça `/planejar` para incluir.

## Se um hook bloquear

O bloqueio está certo por padrão. Não contorne, não tente outro caminho para
fazer a mesma coisa. Leia a mensagem, faça o que ela manda, e explique ao
usuário em uma frase o que aconteceu — sem jargão.

## Terminar de verdade

"Terminei" sem aplicação rodando não conta. Ao fim de cada rodada:

1. `npx tsc --noEmit` — erro de tipo aqui é bug, não chatice do TypeScript.
2. `npm run dev` (siga a skill `run` se disponível) e abra
   http://localhost:3000. Confirme que a tela abre e que o passo entregue está
   visível nela.
3. Se quebrar, conserte antes de falar com o usuário.
4. `git add -A && git commit -m "..."` descrevendo o passo em português.

## Fechar

- Uma frase sobre o que apareceu de novo na tela.
- O que ainda falta do plano (quantos passos).
- Próximo passo: `/construir` de novo, ou `/revisar` se o plano acabou.
