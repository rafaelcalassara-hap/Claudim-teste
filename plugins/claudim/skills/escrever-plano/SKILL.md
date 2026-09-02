---
name: escrever-plano
description: Roteiro para transformar um pedido vago de área de negócio em um PLANO.md com escopo, passos numerados e critério de pronto em linguagem de negócio. Use quando o usuário descrever algo que quer construir, pedir para planejar, ou quando faltar PLANO.md e ele pedir para escrever código.
---

# Escrever o PLANO.md

O plano existe para uma coisa: impedir que a pessoa e você construam coisas
diferentes achando que é a mesma. Ele não é documentação.

## Como entrevistar

Uma pergunta por vez, com `AskUserQuestion` quando houver opções. Máximo 6
perguntas — depois disso a pessoa desiste.

O que você precisa arrancar:

1. **A tela.** "Quando isso estiver pronto, o que você vê na tela?" Se a
   resposta for abstrata, pergunte o que ela faz hoje no lugar disso
   (planilha? pedido para o time de dados? BI?).
2. **Os dados.** Quais campos, de onde. Se disser "do banco", pergunte o nome
   da tabela ou de um campo — e se não souber, marque para descobrir com o
   comando `/revisar` ou com o agente `analista-dados`.
3. **A ação.** Filtrar, exportar, comparar períodos, marcar como visto. Escolha
   uma como principal.
4. **O corte.** "Se só uma coisa funcionasse na primeira versão, qual seria?"

Não pergunte: framework, banco, hospedagem, autenticação, performance. Isso é
decisão sua.

## Formato do PLANO.md

```markdown
# Plano — <nome>

## O que essa aplicação faz
Uma frase. A pessoa tem que reconhecer o pedido dela aqui.

## Está pronto quando
- [ ] Consigo <ação de negócio concreta>
- [ ] Consigo <outra>
Critérios em primeira pessoa, do ponto de vista de quem usa.

## Passos
- [ ] 1. <passo>
- [ ] 2. <passo>
Cada passo produz algo visível na tela. "Criar camada de acesso a dados"
não é passo; "a tela lista os leads do mês" é.

## Dados usados
Origem, tabela/arquivo, campos.

## Compliance
Só se o projeto lida com dado sensível. Liste o que precisa de mascaramento e
o que precisa passar por compliance ANS antes de ir para alguém de fora.

## Fora desta versão
O que foi cortado, para a pessoa não achar que você esqueceu.
```

## Regras

- Entre 3 e 8 passos. Mais que isso, corte escopo — não quebre em passos menores.
- Nunca estimativa de tempo.
- Nunca critério técnico no "está pronto quando".
- Mostre o plano inteiro no chat e peça confirmação **antes** de gravar.
- Depois de gravar, uma frase: "Gravei. Rode `/construir`."
