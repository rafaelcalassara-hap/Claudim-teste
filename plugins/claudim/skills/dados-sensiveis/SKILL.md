---
name: dados-sensiveis
description: Regras da casa para dado de beneficiário e dado de saúde (LGPD Art. 11) e para publicidade de plano de saúde (ANS). Use SEMPRE antes de escrever código que toque CPF, carteirinha/CNS, nome de beneficiário, diagnóstico, CID, condição de saúde, tracking, pixel, evento de analytics, URL de campanha, ou texto que fale de cobertura, rede credenciada ou preço de plano.
---

# Dado sensível — o que é obrigatório aqui

Contexto: operadora de saúde. Dado de saúde é **dado sensível** pela LGPD
Art. 11 — regime mais restrito que dado pessoal comum. Um erro aqui é
incidente reportável, não bug.

## 1. Coleta: mascare na entrada, não na saída

Mascaramento em política escrita não vale nada. Faça na camada que coleta.

- CPF: guarde e exiba mascarado — `***.456.789-**`. Se precisar cruzar com
  outra base, use hash (SHA-256 com salt do `.env`), nunca o número puro.
- Carteirinha/CNS: mesma regra.
- Nome de beneficiário em tela compartilhada: primeiro nome + inicial.
- Log: nunca logue o registro inteiro. Logue o id interno.

Use `lib/pii.ts` do projeto (`mascararCpf`, `hashCpf`, `mascararNome`,
`mascararRegistros`).

**Onde mascarar neste stack:** no servidor, antes de o dado atravessar para o
navegador. Um Server Component que passa o registro do Prisma por prop para um
componente `"use client"` manda o objeto **inteiro** no payload da página —
inclusive a coluna que ele não renderizou. Ela aparece no DevTools de quem
abrir a tela. Mascare no Server Component, nunca no componente de tela.

## 2. Nada de dado real em arquivo

Fixture, seed, CSV de exemplo, notebook: **zero** dado de gente real. O hook
`guard_pii` bloqueia CPF e CNS com dígito verificador válido, e condição de
saúde em arquivo de exemplo.

Gere com `lib/dados-sinteticos.ts`. Isso vale também para `prisma/seed.ts` e
para qualquer migração com `INSERT` de exemplo. Se precisar de um caso real
para reproduzir um problema, consulte o banco em tempo de execução — não copie
para arquivo.

## 3. Vazamento por URL e por evento

O incidente mais comum e o mais fácil de cometer. Uma URL como
`/planos/oncologia` que chega num pixel do Meta revela condição de saúde de
quem navegou — e você mandou para terceiro sem base legal.

Regra: **nada que revele condição de saúde sai da nossa infraestrutura.**
Isso inclui:

- caminho de URL e query string enviados a pixel, GTM, GA4, Meta, TikTok;
- nome de evento (`lead_oncologia` → `lead_produto_17`);
- nome de audiência ou segmento em plataforma de mídia;
- parâmetro customizado de evento;
- título da página (`document.title` vai junto no pixel por padrão) — no Next,
  isso é o `metadata.title` da rota;
- rota do App Router. `app/planos/oncologia/page.tsx` vira a URL
  `/planos/oncologia`, que o pixel captura sozinho a cada navegação. O nome da
  pasta é decisão de compliance, não de organização de arquivo.

**Variável `NEXT_PUBLIC_`.** Tudo com esse prefixo é embutido no JavaScript
enviado ao navegador. ID de pixel público pode; chave secreta, mapa de
de-para clínico ou qualquer coisa que revele condição, não.

Como resolver: mande identificador opaco e resolva o significado no nosso
banco. Se a URL já é pública e falante, redija antes de enviar o evento.

Isso vale para deduplicação também: o `event_id` compartilhado entre browser e
servidor não pode carregar informação clínica.

## 4. ANS — publicidade de plano

Cobertura, rede credenciada, carência e preço são regulados (RN 195 e
correlatas). Você **não aprova texto**. O que você faz:

- Sinaliza: "esse texto fala de cobertura/preço/rede — precisa passar por
  compliance antes de ir ao ar."
- Registra no `PLANO.md`, seção Compliance.
- Não constrói mecanismo que facilite publicar copy dinâmica sem revisão
  (texto de plano vindo de planilha direto para a tela pública, por exemplo).

## 5. Quando o hook bloquear

Explique ao usuário em uma frase, sem jargão jurídico, e ofereça a alternativa
concreta. Nunca contorne o bloqueio, nunca peça para desligar o hook.
