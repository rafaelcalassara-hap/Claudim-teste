# DS Acme V2 — Design System

> Este arquivo explica **como usar**. Os valores — hex, px, sombra, família —
> vivem só em [`DESIGN.md`](./DESIGN.md), e de lá o
> [`gerar-tema.py`](./gerar-tema.py) escreve o `@theme` do Tailwind e o
> `showcase.html`. Aqui os tokens aparecem por **nome**, nunca por valor:
> valor repetido em dois arquivos é valor que vai divergir.

Documento de referência consolidado a partir do documento de design de origem e dos tokens já implementados em `apps/site/src/app/global.css`.

> **Stack alvo:** Next.js 16 (App Router) + TypeScript estrito + Tailwind CSS + shadcn/ui + Radix. Tokens são expostos como CSS Custom Properties em `:root` e mapeados via `@theme inline` para uso direto em utilitários Tailwind (`bg-primary`, `text-foreground`, `shadow-sm`, etc.).

---

## Sumário

1. [Princípios](#1-princípios)
2. [Foundations](#2-foundations)
   - 2.1 [Breakpoints](#21-breakpoints)
   - 2.2 [Margens (container)](#22-margens-container)
   - 2.3 [Gutter (grid)](#23-gutter-grid)
   - 2.4 [Overlay](#24-overlay)
   - 2.5 [Sombras](#25-sombras)
   - 2.6 [Raio (border radius)](#26-raio-border-radius)
3. [Tokens — Cores](#3-tokens--cores)
4. [Tokens — Tipografia](#4-tokens--tipografia)
5. [Tokens — Espaçamento e Layout](#5-tokens--espaçamento-e-layout)
6. [Iconografia](#6-iconografia)
7. [Componentes](#7-componentes)
   - 7.1 [Header](#71-header)
   - 7.2 [Footer](#72-footer)
   - 7.3 [Banner principal](#73-banner-principal)
   - 7.4 [Banner intermediário](#74-banner-intermediário)
   - 7.5 [Banner vertical](#75-banner-vertical)
   - 7.6 [Buttons](#76-buttons)
   - 7.7 [Links](#77-links)
   - 7.8 [Slider e arrows](#78-slider-e-arrows)
   - 7.9 [Cards textuais](#79-cards-textuais)
   - 7.10 [Cards de Serviços](#710-cards-de-serviços)
   - 7.11 [Cards de Atalhos](#711-cards-de-atalhos)
   - 7.12 [Cards de Unidades](#712-cards-de-unidades)
   - 7.13 [Cards Passo a Passo](#713-cards-passo-a-passo)
   - 7.14 [Prova social / Detalhamento](#714-prova-social--detalhamento)
   - 7.15 [Cards de Planos](#715-cards-de-planos)
   - 7.16 [FAQ (Accordion)](#716-faq-accordion)
   - 7.17 [Form](#717-form)
   - 7.18 [File Upload](#718-file-upload)
   - 7.19 [Alerts e mensagens](#719-alerts-e-mensagens)
   - 7.20 [Float label input](#720-float-label-input)
8. [Acessibilidade](#8-acessibilidade)
9. [Diretrizes de uso](#9-diretrizes-de-uso)
10. [Referência rápida — utilitários Tailwind](#10-referência-rápida--utilitários-tailwind)

---

## 1. Princípios

- **Acolhimento e confiança** — comunicação humanizada (ilustrações com poucos elementos, traçado próximo, sempre com retas/curvas seguindo a forma do símbolo da marca).
- **Acessibilidade primeiro** — contraste mínimo WCAG AA (4.5:1). Cor nunca é o único indicador de estado.
- **Mobile-first responsivo** — quatro breakpoints fixos (320 / 720 / 1400 / 1920 px) com grids, margens e gutters dedicados.
- **Sistema baseado em tokens** — todo valor visual passa por uma CSS variable em `:root`; não use literais hex em componentes.
- **Composição shadcn + Tailwind** — não modifique primitivas em `packages/ui/` inline; estenda via `cn()` e composição em `packages/layout/` ou em features.

---

## 2. Foundations

### 2.1 Breakpoints

| Token         | Min width | Faixa               | Uso            |
| ------------- | --------- | ------------------- | -------------- |
| `Small`       | 320 px    | até 599 px          | Mobile         |
| `Medium`      | 720 px    | 600 – 1023 px       | Tablet         |
| `Default`     | 1400 px   | 1024 – 1440 px      | Desktop padrão |
| `Extra Large` | 1920 px   | a partir de 1440 px | Desktop amplo  |

Mapeamento no Tailwind v4 (já default em `@theme`): `sm` ≈ 720, `lg` ≈ 1400, `2xl` ≈ 1920. Para fidelidade com o DS, use as utilidades semânticas `.ds-container` e `.ds-grid` declaradas em `global.css`.

### 2.2 Margens (container)

| Faixa de viewport      | Margem horizontal |
| ---------------------- | ----------------- |
| Até 599 px (Small)     | **15 px**         |
| 600 – 1023 px (Medium) | **30 px**         |
| 1024 – 1440 px         | **40 px**         |
| ≥ 1440 px (XL)         | **80 px**         |

Implementação: classe utilitária `.ds-container` aplica `padding-inline` automático por faixa.

### 2.3 Gutter (grid)

| Faixa          | Gutter fixo |
| -------------- | ----------- |
| Até 599 px     | **15 px**   |
| 600 – 1023 px  | **20 px**   |
| 1024 – 1440 px | **30 px**   |
| ≥ 1440 px      | **40 px**   |

Implementação: classe `.ds-grid` aplica `gap` correspondente.

### 2.4 Overlay

- Token: `--color-overlay` (preto a 80%; o valor está no `DESIGN.md`)
- Uso: modais, drawers, lightbox.

### 2.5 Sombras

A paleta oficial usa **navy 20%** (não preto puro) — define a sensação de marca:

| Token CSS | Uso |
| ---------------- | ---------------------------- |
| `--shadow-sm` | Cards comuns e menores |
| `--shadow-lg` | Componentes maiores / hover |
| `--shadow-focus` | Foco de inputs/CTA acessível |

### 2.6 Raio (border radius)

| Token         | Valor                       |
| ------------- | --------------------------- |
| `--radius-sm` | `calc(var(--radius) - 4px)` |
| `--radius-md` | `calc(var(--radius) - 2px)` |
| `--radius-lg` | `var(--radius)`             |
| `--radius-xl` | `calc(var(--radius) + 4px)` |

---

## 3. Tokens — Cores

Todos os tokens vivem em `:root` e são consumidos pelo Tailwind via `@theme inline`. **Nunca** use hex literal em componentes — sempre referencie pelo token.

### Brand

| Token CSS | Tailwind | Uso |
| ---------------------- | ------------------------- | ----------------------------------- |
| `--primary` | `bg-primary` | Marca principal (cor primária) |
| `--primary-darker` | n/a (manual) | Hover/estado pressionado em primary |
| `--primary-foreground` | `text-primary-foreground` | Texto sobre primary |
| `--accent` | `bg-accent` | CTA secundário, destaques de apoio |
| `--accent-foreground` | `text-accent-foreground` | Texto sobre accent |
| `--highlight` | n/a | Realces curtos (badges, pílulas) |
| `--soft` | n/a | Fundo suave de seções com accent |

### Surfaces

| Token CSS | Tailwind | Uso |
| -------------------- | ----------------------- | -------------------------- |
| `--background` | `bg-background` | Fundo padrão |
| `--foreground` | `text-foreground` | Texto padrão |
| `--card` | `bg-card` | Fundo de cards |
| `--card-foreground` | `text-card-foreground` | Texto em cards |
| `--popover` | `bg-popover` | Fundo de popover/dropdown |
| `--secondary` | `bg-secondary` | Fundo alternativo de seção |
| `--muted` | `bg-muted` | Estado desabilitado, fundo |
| `--muted-foreground` | `text-muted-foreground` | Texto secundário, helper |

### Linhas, foco e inputs

| Token CSS | Uso |
| ---------------- | ----------------------------------- |
| `--border` | Borda padrão (alinhada a `primary`) |
| `--border-muted` | Bordas de campos desabilitados |
| `--input` | Borda padrão de inputs |
| `--ring` | Halo de foco acessível |

### Status

| Token CSS | Tailwind | Uso |
| -------------------------- | ----------------------------- | ------------------------------------------------------- |
| `--success` | n/a (`bg-[var(--success)]`) | Sucesso, upload concluído |
| `--destructive` | `bg-destructive` | Erros, ações destrutivas |
| `--destructive-foreground` | `text-destructive-foreground` | Texto sobre destructive |
| `--warning` | n/a | Atenção / cards de “Atalhos” a 10% de opacidade |

### Cores reservadas (PDF)

- `--warning` — exclusivo para **Cards de Atalhos** (sempre a 10% de opacidade) e **Cards de Passo a Passo**.
- `--background` e `--secondary` — únicas opções para fundo de **banners intermediários, cards textuais, cards de serviços, cards de unidades e formulários**.

> **Aviso de contraste:** o contraste entre as duas cores de destaque da marca (`--highlight` e `--accent`) é alto, mas evite combiná-los — perde legibilidade para daltônicos. Mínimo WCAG = **4.5 : 1**. Se não for possível, use **negrito** ou outro reforço visual.

---

## 4. Tokens — Tipografia

Duas famílias oficiais, ambas injetadas via `next/font/local` em `packages/fonts/`.

| Família     | Variável                            | Tailwind                        | Quando usar                                                               |
| ----------- | ----------------------------------- | ------------------------------- | ------------------------------------------------------------------------- |
| **Brand Display** | `--font-display` | `font-display`, `.font-display` | Títulos criativos, banners, destaques. **Nunca** em corpo de texto longo. |
| **Inter**  | `--font-sans` | `font-sans` (default)           | Títulos comuns, corpo de texto, subtítulos de banners, formulários.       |

`.font-display` aplica `font-weight: 700` e `letter-spacing: -0.01em`.

### Heading scale (recomendado)

A escala segue o padrão da marca (Brand Display em H1/H2 de banner, Inter no restante). Use as utilitárias Tailwind de tamanho com line-height ajustado:

| Tag   | Mobile (320)        | Tablet (720)          | Desktop (1400+)       | Família          |
| ----- | ------------------- | --------------------- | --------------------- | ---------------- |
| H1    | `text-3xl/tight`    | `text-4xl/tight`      | `text-5xl/tight`      | Brand Display          |
| H2    | `text-2xl/snug`     | `text-3xl/snug`       | `text-4xl/snug`       | Brand Display / Inter |
| H3    | `text-xl/snug`      | `text-2xl/snug`       | `text-3xl/snug`       | Inter           |
| H4    | `text-lg/snug`      | `text-xl/snug`        | `text-2xl/snug`       | Inter           |
| H5    | `text-base`         | `text-lg`             | `text-xl`             | Inter           |
| H6    | `text-sm`           | `text-base`           | `text-lg`             | Inter Bold      |
| Body  | `text-sm leading-6` | `text-base leading-7` | `text-base leading-7` | Inter           |
| Small | `text-xs`           | `text-xs`             | `text-sm`             | Inter           |

Regras complementares:

- **Títulos criativos**: `font-display` + Brand Display + tracking ligeiramente negativo.
- **Botões**: sempre Inter, peso 700.
- **Form labels**: Inter 14px (16px mobile) — flutuam para 11px / 700 quando o campo está preenchido (ver `.float-field`).

---

## 5. Tokens — Espaçamento e Layout

- **Container responsivo:** `.ds-container` controla `max-width` e `padding-inline` automáticos (15 → 30 → 40 → 80 px) com `max-width: 1400px` no Default e `1920px` no XL.
- **Grid responsivo:** `.ds-grid` aplica `gap` (15 → 20 → 30 → 40 px). Combine com `grid-cols-{n}` Tailwind por breakpoint.
- **Padding interno padrão de cards:** `20px` (mobile) → `24px` (tablet) → `32px` (desktop), via `.ds-card`.

```html
<section class="ds-container">
  <div class="ds-grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
    <article class="ds-card">…</article>
    <article class="ds-card ds-card--hover">…</article>
    <article class="ds-card ds-card--selected">…</article>
  </div>
</section>
```

---

## 6. Iconografia

- **Biblioteca de referência atual:** [Google Material Icons](https://fonts.google.com/icons).
- **Implementação no projeto:** `lucide-react` (alinhado ao shadcn).
- **Tamanhos:** 16 (inline em texto small), **20** (botões/inputs), **24** (default), **32+** (decorativo).
- **Cor:** herda do texto (`text-primary`, `text-muted-foreground`). Para ícones decorativos use `aria-hidden="true"`.
- **Ilustrações:** somente nas cores **`--primary` ou `--background`**; traçado próximo, humanizado, com retas/curvas seguindo a forma do símbolo da marca.

---

## 7. Componentes

> Cada componente abaixo já tem (ou deve ter) implementação em `packages/ui` (primitivos shadcn) ou `packages/layout` (composições com regras Acme). **Nunca duplique primitivas** — adicione-as via skill a skill de scaffold do projeto.

### 7.1 Header

Estrutura comum às três variantes (desktop / tablet / mobile):

- Top bar: `Portal Parceiro`, `Imprensa`, `Outros sites`, controles `A+ A-` (ajuste de tipografia).
- Nav primário: **Sobre a Empresa**, **Produtos**, **Locais**, **Serviços**, CTA `Seja cliente`, link `Acesse sua área`.
- **Mega menu** (desktop) com colunas por seção; em **tablet/mobile** vira drawer com botão `Fechar`.
- Submenu de “Acesse sua área”: Cliente, Empresa, Fornecedor, Revenda.

Diretrizes:

- Header sticky no topo; sombra `--shadow-sm` ao rolar.
- Foco visível em todos os links (`--shadow-focus`).
- Em mobile, ícone hamburger abre drawer full-screen com botão `Fechar` no canto direito.

### 7.2 Footer

Conteúdo obrigatório (desktop / tablet / mobile):

- Endereço institucional, identificador fiscal, canal de atendimento, contato responsável, registros regulatórios.
- Quatro colunas: **Serviços**, **Atalhos**, **Atendimento**, **Baixe o App**.
- Bloco **Redes sociais**.
- Copyright: `© 2025 Acme Inc. Todos os direitos reservados.`

Mobile colapsa em accordion (Serviços, Atalhos, Atendimento) com endereço + copyright ao final.

### 7.3 Banner principal

- Aceita breadcrumbs (`Home > Fornecedor`).
- Título em **Brand Display**, subtítulo Inter.
- CTA opcional (`Seja cliente`).
- Em mobile, conteúdo empilhado e tipografia reduzida.

### 7.4 Banner intermediário

- Backgrounds permitidos: `--background` ou `--secondary`.
- Layout 2 colunas em desktop / tablet (imagem + texto), empilhado em mobile.
- Botão primário centralizado abaixo do texto.

### 7.5 Banner vertical

- Backgrounds permitidos: `--background` ou `--secondary`.
- Disponível apenas em **Desktop** e **Tablet** — mobile **NÃO** utiliza banner vertical.

### 7.6 Buttons

| Variante              | Estado | Estilo                                                         |
| --------------------- | ------ | -------------------------------------------------------------- |
| **Primary (default)** | rest   | `bg-accent text-accent-foreground` (`--accent`) |
| Primary               | hover  | escurecer 10% (`brightness-95`) + `shadow-lg`                  |
| **Secondary**         | rest   | `border border-primary text-primary bg-transparent`            |
| Secondary             | hover  | `bg-primary text-primary-foreground`                           |
| **Tertiary (link)**   | rest   | `text-primary underline underline-offset-4`                    |
| Tertiary disabled     |        | `text-border-muted cursor-not-allowed`                         |
| Outline disabled      |        | `border-border-muted text-border-muted bg-transparent`         |
| Ícone à esquerda      |        | gap 8 px entre ícone (16 px) e label                           |

Anatomia (PDF): padding interno `24 / 16 / 24 / 16` (T/R/B/L), borda `3 px` opcional para foco. Use `border-radius: var(--radius)` (6 px).

> Tamanho do botão é proporcional ao texto, mas botões adjacentes devem ter **a mesma largura**.

### 7.7 Links

- **Default:** `text-primary` + sublinhado em hover/focus.
- **Com ícone:** chevron à direita (`>`) com gap 4 px.
- **Disabled:** `text-border-muted`, sem sublinhado, `cursor-not-allowed`.

### 7.8 Slider e arrows

- **Indicador de slide ativo:** ponto cheio `--primary`, inativo `--border-muted`. Diâmetros: 6 px inativo / 10 px ativo.
- **Arrow button** (`.ds-arrow`): 40×40 px, `border-radius: var(--radius)`, fundo branco, sombra `--shadow-sm`.
  - Hover: borda e ícone passam para `--primary`.
  - Disabled: borda e ícone `--border-muted`.
- Em desktop o slider é clicável; em mobile/tablet, swipe.

**Quiosque — slider de cartões selecionáveis** (`UserCardSlider`):
quando uma lista de cards-de-cartão precisa ser percorrida por toque em quiosque,
use scroll horizontal nativo (`snap-x snap-mandatory`) em vez de pilha vertical.
Cada card ocupa ~85% da largura (`basis-[85%]`, reduz em telas maiores) para que
o vizinho "espie" e sinalize que há mais itens. Abaixo do trilho: a fileira de
dots (7.8) + setas opcionais + contador textual `"{atual} de {total}"`
(`aria-live="polite"`) — o número é indicador redundante à cor para
acessibilidade. O índice ativo é derivado do card mais visível
(`IntersectionObserver`), não do item selecionado: seleção e foco visual são
estados independentes da posição no slider.

### 7.9 Cards textuais

- Backgrounds: `--background` ou `--secondary`.
- Estrutura: título (Inter 700) + parágrafo + CTA (botão ou link).
- Apresentação:
  - Desktop: até **3 cards por linha**.
  - Tablet: 2 colunas.
  - Mobile: 1 coluna empilhada.

### 7.10 Cards de Serviços

- Backgrounds: `--background` ou `--secondary`.
- **Desktop 1400’**: até **3 cards por página** (apresentados ao lado do banner vertical).
- **Tablet 720’**: até **3 cards por página** com chevron link `Clique aqui >`.
- **Mobile 320’**: cards empilháveis, máximo **4 cards**.

### 7.11 Cards de Atalhos

- Background: `--warning` a **10% de opacidade** (`bg-warning/10`).
- Mesma regra de quantidade dos cards de serviços (3 por página em desktop/tablet, empilhados em mobile).
- CTA padrão: `Consulte a rede >`.

### 7.12 Cards de Unidades

- Background: `--background`.
- Estrutura: badge de distância (“{distância} km de você”), nome da unidade, endereço, telefone, link `Ver unidade`.
- Apresentação: **9 cards/página** (desktop), **4 cards/página** (tablet), empilhado em mobile.

### 7.13 Cards Passo a Passo

Variante padrão (com banner intermediário “Saiba como enviar o formulário”):

- Backgrounds permitidos: `--background`, `--secondary` ou `--warning` a 10% (apenas variante de formulários).
- Estrutura por etapa: título + descrição + ícone numerado.
- Em mobile vira lista vertical com etapas separadas por divisor.

Variante “Quero ser fornecedor”: 4 etapas (`Preencha o formulário → Cotação → Cadastro → Pedido`).

### 7.14 Prova social / Detalhamento

- Usado para números (“120 unidades”, “45 pontos de atendimento”) e reviews (“4,8/5 - 1.240 avaliações”).
- Desktop: até **5 cards/página**. Tablet: 3. Mobile: 1 e meio (visível parcial — sliderable).
- Tipografia em destaque: número grande Brand Display + descrição Inter.

### 7.15 Cards de Planos

- Variantes: **Essencial**, **Avançado**, **Empresarial**.
- Atenção: **a cor do card varia por variante** (verificar paleta no arquivo de design — não há literal na fonte além de `Atenção a cor dos cards!`).

### 7.16 FAQ (Accordion)

- Backgrounds permitidos: `--background` ou `--secondary`.
- Padrão: lista de perguntas com `chevron` que expande conteúdo.
- Estrutura recomendada (shadcn `Accordion`):

```tsx
<Accordion type="single" collapsible>
  <AccordionItem value="q1">
    <AccordionTrigger>
      Quais tipos de benefícios e ofertas estão disponíveis no programa?
    </AccordionTrigger>
    <AccordionContent>
      No nosso Programa de Benefícios você encontra…
    </AccordionContent>
  </AccordionItem>
</Accordion>
```

- Em mobile, o accordion ocupa 100% da largura e o chevron fica alinhado à direita com `text-primary`.

### 7.17 Form

- Background: `--secondary` (desktop / tablet) ou `--background` (mobile).
- Layout: 2 colunas em desktop, 1 coluna em tablet/mobile.
- Componentes:
  - **Float label input** (`.float-field` + `.float-input`).
  - **Select** com placeholder “Selecione”.
  - **Radio group** horizontal (“Manhã / Tarde / Ambos”).
  - **Textarea** sempre full width.
  - **reCAPTCHA** “Não sou um robô”.
  - **Botão Enviar** primário, alinhado à direita em desktop e full width em mobile (`sticky-cta`).
- Mensagens:
  - Asterisco `*` antes de labels obrigatórios + nota `*Estes campos são obrigatórios`.
  - Erro: borda `--destructive`, label `--destructive`, `data-invalid="true"`.
- Validação: **Zod via `@hookform/resolvers/zod`** em todo formulário (regra do projeto — ver `AGENTS.md`).

Sucesso (post-submit):

```
Seu cadastro foi enviado com sucesso!
Obrigada por enviar seu cadastro, por favor aguarde nosso contato.
```

### 7.18 File Upload

Estados visuais:

| Estado       | Visual                                                    |
| ------------ | --------------------------------------------------------- |
| Em andamento | Barra de progresso na cor primária (`--primary`) com `%`             |
| Sucesso      | Ícone check verde `--success` + label “Sucesso!”          |
| Erro         | Ícone X vermelho `--destructive` + label “Erro no upload” |

Diretrizes:

- Drop zone: `Clique aqui para selecionar o arquivo ou o arraste para essa área`.
- Restrição padrão: `.jpg, .jpeg, .png, .pdf` — **máximo de 2 MB por arquivo**.
- Linha por arquivo: `nome.ext` + `tamanho • timestamp`.

### 7.19 Alerts e mensagens

#### Alert box (com ilustração)

- Ilustração: somente `--primary` ou `--background`; traçado humanizado.
- Largura segue o grid do maior componente em tela.
  - Telas **≤ 612 px**: largura = `viewport - 2 × margem` (ex.: 390 – 60 = **330 px**).
  - Telas **> 612 px**: largura igual ao campo de texto associado.
- Conteúdo: **Título** + **Subtítulo**. Em mobile, dois alerts podem ficar lado a lado.

#### Atenção (inline)

```
Atenção: Envie os documentos referente à sua solicitação.
```

- Ícone âmbar (`--warning`) à esquerda, texto Inter 700 no início (“Atenção:”).

#### Informação (inline)

- Ícone na cor primária (`--primary`) à esquerda, texto explicativo. Usado para avisos não-bloqueantes (ex.: “Para consultar serviços anteriores à data de corte da migração…”).

### 7.20 Float label input

Já implementado em `global.css` via classes utilitárias. Marcação mínima:

```html
<div class="float-field" data-filled="true">
  <input id="email" type="email" class="float-input" placeholder=" " />
  <label for="email">*E-mail</label>
</div>
```

Estados:

- `:focus-within` ou `[data-filled="true"]` → label sobe para 11 px e fica em `--primary`.
- `[data-invalid="true"]` → borda + label em `--destructive`.
- `:disabled` → fundo `--muted`, opacidade 0.7, cursor not-allowed.

### 7.21 DatePicker (DS-EXT-1)

Primitiva de seleção de data adicionada para os campos de vigência das telas
SCREEN-A / SCREEN-B (`dtInicio`/`dtFim`/`dtVigenciaIni`/`dtVigenciaFim`).
Componente: `packages/ui/src/lib/date-picker.tsx` (`DatePicker`).

```tsx
<DatePicker value={dtInicio} onChange={setDtInicio} aria-invalid={hasError} />
```

- Composto sobre `<input type="date">` nativo — **sem nova dependência de
  runtime** (react-day-picker/calendar não estão instalados). Herda o calendário
  nativo da plataforma, navegação por teclado e exibição localizada.
- `value`/`onChange` trafegam sempre em ISO `YYYY-MM-DD` (a forma esperada no
  boundary Zod `isoDate`), evitando conversões de fuso.
- Reaproveita os tokens do `Input` (`border-input`, `h-9`, `focus-visible:ring`,
  `aria-invalid`) + glifo de calendário à esquerda.
- **Dark mode:** `dark:[color-scheme:dark]` mantém o controle nativo legível.
- Estados: idle / foco (`focus-visible:ring`) / inválido (`aria-invalid`) /
  desabilitado (`disabled:opacity-50`).

### 7.22 CurrencyInput (DS-EXT-2)

Primitiva monetária adicionada para os campos de valor das telas SCREEN-A /
SCREEN-B (`vlItem`, `vlLimite`). Componente:
`packages/ui/src/lib/currency-input.tsx` (`CurrencyInput`).

```tsx
<CurrencyInput
  value={vlItem}
  onChange={setVlItem}
  aria-invalid={hasError}
/>
```

- Composto sobre `<input type="text">` como máscara de valor — **sem nova
  dependência de runtime**. Cada tecla é reduzida a dígitos interpretados como
  centavos, então o texto exibido é sempre um valor pt-BR válido (`1.234,56`).
- `value`/`onChange` trafegam sempre como número canônico JS (`1234.56`), a forma
  esperada no boundary Zod `z.number()` — sem ambiguidade de parsing de locale,
  sem `NaN`.
- Reaproveita os tokens do `Input` (`border-input`, `h-9`, `focus-visible:ring`,
  `aria-invalid`) + glifo `R$` à esquerda e alinhamento à direita com
  `tabular-nums`.
- **Dark mode:** herda `dark:bg-input/30` do padrão de input; símbolo em
  `text-muted-foreground`.
- Estados: idle / foco / inválido (`aria-invalid`) / somente-leitura
  (`read-only:opacity-70`) / desabilitado (`disabled:opacity-50`).

---

## 8. Acessibilidade

- **Contraste:** mínimo WCAG **4.5:1** entre texto e fundo (ver alerta no PDF). Em combinações limítrofes, use **negrito** ou outro reforço.
- **Foco visível:** sempre via `--shadow-focus`. Nunca `outline: none`.
- **Cor não é o único indicador de estado** — combine com ícone, label ou padrão.
- **Tipografia mínima:** 14 px corpo, 12 px metadados. Nunca abaixo de 12 px.
- **Tap target:** mínimo 44×44 px em touch (`h-11`).
- **Daltonismo:** evite combinar as duas cores de destaque da marca (`--highlight` + `--accent`) em alta área. Prefira contraste preto/branco quando precisar.
- **Reduced motion:** respeite `prefers-reduced-motion: reduce` (já declarado em `global.css`).
- **Dark mode:** todo componente DEVE incluir variantes `dark:` (regra do projeto). Use os mesmos tokens — apenas redeclare em `:root.dark { … }` quando necessário.

---

## 9. Diretrizes de uso

### Faça

- Use sempre os tokens (`--primary`, `--accent`, `bg-secondary`, `shadow-sm`, etc.) — nunca hex literal.
- Combine `.ds-container` + `.ds-grid` para garantir margens e gutters do DS.
- Para cards, use `.ds-card` como base e estenda com classes Tailwind. Estado
  de hover e de selecionado saem de `--color-soft` e `--color-secondary`.
- Para inputs, use `.float-field` + `.float-input` ou o componente `Input` de `@acme/ui` envolvido no padrão.
- Animações com Framer Motion: somente `transform` e `opacity` (regra do projeto — GPU-safe).
- Ilustrações: paleta restrita (primária + branco) com traçado humanizado.

### Não faça

- ❌ Hex literal em componente (`bg-[#0055ff]`) — use o token: `bg-primary`.
- ❌ Sombras pretas (`rgba(0, 0, 0,0.x)`) — todas as sombras usam **navy 20%**.
- ❌ Animar `width`, `height`, `top`, `left` — viola regra de performance.
- ❌ Combinar Brand Display em corpo de texto longo.
- ❌ Usar `--warning` em fundo cheio — apenas a **10% de opacidade** e **somente em Atalhos / Passo a Passo**.
- ❌ Banner vertical em mobile.
- ❌ Acessar arquivos de primitivas em `packages/ui` para editar inline — sempre estender por composição.

---

## 10. Referência rápida — utilitários Tailwind

| Necessidade                  | Classe                                                                                                                            |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Container DS responsivo      | `ds-container`                                                                                                                    |
| Grid DS responsiva           | `ds-grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`                                                                               |
| Card padrão                  | `ds-card`                                                                                                                         |
| Card hoverable               | `ds-card ds-card--hover`                                                                                                          |
| Card selecionado             | `ds-card ds-card--selected`                                                                                                       |
| Card alternativo (sem borda) | `ds-card ds-card--muted`                                                                                                          |
| Botão primário (CTA)         | `bg-accent text-accent-foreground rounded-md px-6 py-3 font-semibold shadow-sm hover:shadow-lg transition`                        |
| Botão secundário             | `border border-primary text-primary rounded-md px-6 py-3 font-semibold hover:bg-primary hover:text-primary-foreground transition` |
| Link DS                      | `text-primary underline-offset-4 hover:underline focus-visible:underline`                                                         |
| Texto título display         | `font-display text-4xl tracking-tight`                                                                                            |
| Texto corpo padrão           | `font-sans text-base leading-7 text-foreground`                                                                                   |
| Texto auxiliar               | `text-sm text-muted-foreground`                                                                                                   |
| Alerta de atenção (inline)   | `flex items-start gap-2 text-foreground` + ícone `text-[var(--warning)]`                                                          |
| Foco acessível custom        | `focus-visible:shadow-[var(--shadow-focus)] outline-none`                                                                         |
| Sticky CTA mobile            | `sticky-cta`                                                                                                                      |
| Tabular nums                 | `tabular-nums`                                                                                                                    |
| Shake (erro de form)         | `shake`                                                                                                                           |

"
".---

## 11. Extensões por tela

Extensões pontuais do DS, justificadas por dados/domínio e registradas no Storybook. Promover a primitiva de primeira-classe quando o uso se generalizar.

### 11.1 APP-EXT — `TicketStatusBadge` (conjunto de 10 estados FL_STATUS)

A primitiva compartilhada `Badge` oferece 6 variantes; o domínio de senha/ticket do APP-EXT tem **10 estados** (`FL_STATUS` 0–9). Em vez de mutar a primitiva, cada estado **compõe tokens registrados no DS** sobre `variant="outline"` via `cn()` — uma mistura de tokens semânticos e da paleta de dados `chart-*` (ver DESIGN.md › Colors › Data Visualization), pois 10 estados excedem os 6 tokens semânticos disponíveis.

Mapeamento exato (código ↔ token):

| FL_STATUS | Rótulo         | Token de cor                                   |
| --------- | -------------- | ---------------------------------------------- |
| 0         | Pendente       | `muted`                                        |
| 1         | Aguardando     | `primary`                                      |
| 2         | Chamado        | `chart-3` (laranja — atenção)                  |
| 3         | Em atendimento | `primary`                                      |
| 4         | Atendido       | `chart-2` (verde — sucesso)                    |
| 5         | Ausente        | `chart-5` (vermelho-laranja — negativo brando) |
| 6         | Cancelado      | `destructive`                                  |
| 7         | Pausado        | `muted`                                        |
| 8         | Transferido    | `chart-4` (violeta — transição especial)       |
| 9         | Encerrado      | `chart-2` (verde — sucesso)                    |

- A cor **nunca** é o único indicador: cada estado combina ícone + rótulo de texto.
- Todos os tokens acima estão registrados em `DESIGN.md` (semânticos em Colors › Status/Surfaces; `chart-1..5` em Colors › Data Visualization) e expostos como `--color-chart-N` no `@theme` consumido (console `globals.css` e Storybook `preview.css`, ambos via `tokens-internal.css`, com redefinição `.dark`).
- Render-only — sem lógica de transição no cliente (estado é derivado do servidor).
- Storybook: `APP-EXT / DS Extensions / TicketStatusBadge` (história `AllStates` cobre os 10 estados em fundo claro e escuro).
- Implementação: `packages/feature-directory/src/lib/components/TicketStatusBadge.tsx`.

### 11.2 APP-EXT — `ColorPickerDialog` / swatch de cor definida pelo usuário (off-palette por dado)

O fundo do swatch é um valor arbitrário armazenado pelo usuário (`TB_USER_COLOR.CD_COLOR`), **não** um token do DS. É o único ponto em que `style` inline dinâmico é permitido — apenas no quadrado de cor.

- Cada swatch expõe o nome da cor via `aria-label`/`title`, então a cor não é o único indicador.
- Storybook: `APP-EXT / DS Extensions / ColorPickerDialog (swatch)`.
- Implementação: `ColorPickerDialog.tsx` e o preview em `UserColorForm.tsx` / `UserColorsPage.tsx`.

### 11.3 APP-EXT — `FormDialog` cap de scroll (`max-h-[85dvh]`)

O `FormDialog.tsx` aplica `max-h-[85dvh]` no contêiner do diálogo para impedir que formulários longos ultrapassem a viewport, habilitando scroll interno. O DS **não** define token de altura relativa à viewport (`dvh`), então este é um **valor arbitrário documentado** — exceção pontual, restrita ao cap de scroll do diálogo.

- Escopo: apenas o contêiner do `FormDialog`; nenhum outro componente usa `dvh`.
- `85dvh` deixa margem para a barra de endereços móvel (dynamic viewport height) e respeita o padding do overlay.
- Promoção futura: se mais diálogos precisarem do mesmo cap, registrar o
  token no `DESIGN.md` e migrar. Enquanto for um caso só, fica na classe.
- Implementação: `packages/feature-directory/src/lib/components/forms/FormDialog.tsx`.

### 11.4 Novo Cadastro — faixa de cabeçalho de wizard + rodapé persistente (DS-EXT-3)

Anatomia canônica do card de passo de wizard (`WizardShell` em
`packages/feature-signup/src/lib/components/wizard/`):

- **Faixa única de contexto** no topo do card: trilha de progresso em linha
  única (bolhas de 28px com rótulo ao lado, alvo de toque de 44px restaurado
  via pseudo-elemento `after:-inset-2`) + hairline `var(--border-muted)` +
  título `font-display text-xl sm:text-2xl` com subtítulo como aposto na
  mesma baseline.
- **Um único indicador de passo por tela.** O card expõe o contexto por
  `aria-label="Passo X de 4: {título}"` na região; a trilha visível é o
  indicador. **Don't:** repetir "Passo X de 4" em eyebrow/texto quando a
  trilha está visível; usar sub-headers de seção **puramente decorativos**
  dentro do corpo (custam mais altura do que o agrupamento que entregam —
  rótulos semanticamente necessários, como os de grupos de checkboxes,
  continuam válidos).
- **Rodapé `.sticky-cta--persist`** (modificador aditivo sobre
  `.sticky-cta`): CTA sempre visível também em ≥720px. Fundo `var(--card)`,
  hairline superior, cantos inferiores `var(--radius)`, padding vertical
  12px @720 / 16px @1400; sangria lateral/inferior via `--spacing-card-padding-mobile`
  (definida pelo `.ds-card`: 20/24/32px), `z-index: 10`. Acompanha
  `scroll-padding-bottom` no `html` para o foco por teclado nunca ficar
  sob a faixa (WCAG 2.4.11). A legenda "Campos com asterisco (\*) são
  obrigatórios" vive no rodapé (custo de altura zero), oculta em mobile.
- **Ritmo vertical em dois níveis**: 16px (`space-y-4`) entre blocos de
  campo; 12px (`gap-3`) dentro de um agrupamento. A altura de 56px do
  `.float-input` permanece intocada.
- **Grids de formulário**: pares de campos em `sm:` (640px); linhas
  assimétricas de 3+ colunas (ex.: Documento ⅓ + Nome ⅔; Registro Profissional ½ + UF-Registro ¼ +
  Código da Unidade ¼) em `md:` (768px), para não espremer campos mascarados na faixa
  640–743px, onde o `.ds-card` ainda usa padding de 20px.
- Storybook: `Public / SignupWizard / Wizard / WizardShell`
  (`ComFaixaDeProgresso`, `RodapePersistente`) e `.../WizardProgress`.

> **Dessincronia de breakpoints (registro):** o `@theme` dos portais não
> declara `--breakpoint-*`, então as variantes Tailwind v4 usam os defaults
> (sm=640, md=768, lg=1024) e NÃO os breakpoints do DS (720/1400/1920), que
> valem apenas nas media queries manuais de `tokens.css`. Alinhar as
> duas escalas é follow-up de blast radius alto — não misturar as escalas
> silenciosamente em código novo.

---

## Implementação de referência

- **Tokens vivos:** `apps/site/src/app/global.css`
- **Fontes:** `packages/fonts/` (Inter + Brand Display via `next/font/local`)
- **Primitivas shadcn:** `packages/ui/src/lib`
- **Composições de layout (AppShell, TitleBar, Sidebar, etc.):** `packages/layout/src/lib`
- **Adicionar nova primitiva shadcn:** sempre via skill a skill de scaffold do projeto — nunca copiar arquivos manualmente.

---

## Histórico

- **DS V2** — versão atual (documento de design de origem). Tokens sincronizados com o `global.css` em vigor.

> Para qualquer divergência entre este documento e o PDF original, **o PDF prevalece** para foundations e o `global.css` prevalece para implementação. Atualize este arquivo via PR sempre que houver evolução do DS.
