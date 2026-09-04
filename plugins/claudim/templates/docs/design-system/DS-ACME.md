# DS Acme V2 — Design System

> Este arquivo explica **como usar**. Os valores — hex, px, sombra, família —
> vivem só em [`DESIGN.md`](./DESIGN.md), e de lá o
> [`gerar-tema.py`](./gerar-tema.py) escreve o `@theme` do Tailwind e o
> `showcase.html`. Aqui os tokens aparecem por **nome**, nunca por valor:
> valor repetido em dois arquivos é valor que vai divergir.

> **Stack:** Next.js (App Router) + TypeScript + Tailwind v4 + shadcn/ui. O tema
> é o `@theme` de `app/globals.css`, **gerado** do `DESIGN.md`; cada token vira
> utilitária (`bg-primary`, `text-foreground`, `shadow-sm`, `rounded-lg`,
> `px-container-md`). Primitivas do shadcn ficam em `components/ui/`, entram
> por `npx shadcn@latest add <nome>` e depois o código é seu.

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
   - 7.21 [DatePicker](#721-datepicker)
   - 7.22 [CurrencyInput](#722-currencyinput)
8. [Acessibilidade](#8-acessibilidade)
9. [Diretrizes de uso](#9-diretrizes-de-uso)
10. [Referência rápida — utilitários Tailwind](#10-referência-rápida--utilitários-tailwind)
11. [Como estender o design system](#11-como-estender-o-design-system)
12. [Onde está cada coisa](#onde-está-cada-coisa)

---

## 1. Princípios

- **Acolhimento e confiança** — comunicação humanizada (ilustrações com poucos elementos, traçado próximo, sempre com retas/curvas seguindo a forma do símbolo da marca).
- **Acessibilidade primeiro** — contraste mínimo WCAG AA (4.5:1). Cor nunca é o único indicador de estado.
- **Mobile-first responsivo** — quatro breakpoints fixos (320 / 720 / 1400 / 1920 px) com grids, margens e gutters dedicados.
- **Sistema baseado em tokens** — todo valor visual passa por uma CSS variable em `:root`; não use literais hex em componentes.
- **Composição shadcn + Tailwind** — primitiva entra por `npx shadcn@latest add` em `components/ui/` e a partir daí é sua. Composições de tela ficam em `components/`. Estenda com classes de token, não com CSS à parte.

---

## 2. Foundations

### 2.1 Breakpoints

| Token         | Min width | Faixa               | Uso            |
| ------------- | --------- | ------------------- | -------------- |
| `Small`       | 320 px    | até 599 px          | Mobile         |
| `Medium`      | 720 px    | 600 – 1023 px       | Tablet         |
| `Default`     | 1400 px   | 1024 – 1440 px      | Desktop padrão |
| `Extra Large` | 1920 px   | a partir de 1440 px | Desktop amplo  |

Os variants do Tailwind (`sm:` 640, `md:` 768, `lg:` 1024, `2xl:` 1536) **não**
coincidem com essas faixas — o template não declara `--breakpoint-*`. Use os
variants que existem para aplicar os tokens de espaçamento; as quatro larguras
acima são alvo de design, não breakpoint de código.

### 2.2 Margens (container)

| Faixa de viewport      | Margem horizontal |
| ---------------------- | ----------------- |
| Até 599 px (Small)     | **15 px**         |
| 600 – 1023 px (Medium) | **30 px**         |
| 1024 – 1440 px         | **40 px**         |
| ≥ 1440 px (XL)         | **80 px**         |

Implementação: `px-container-sm md:px-container-md lg:px-container-default 2xl:px-container-xl` — tokens `--spacing-container-*`.

### 2.3 Gutter (grid)

| Faixa          | Gutter fixo |
| -------------- | ----------- |
| Até 599 px     | **15 px**   |
| 600 – 1023 px  | **20 px**   |
| 1024 – 1440 px | **30 px**   |
| ≥ 1440 px      | **40 px**   |

Implementação: `gap-gutter-sm md:gap-gutter-md lg:gap-gutter-default 2xl:gap-gutter-xl` — tokens `--spacing-gutter-*`.

### 2.4 Overlay

- Token: `--color-overlay` (preto a 80%; o valor está no `DESIGN.md`)
- Uso: modais, drawers, lightbox.

### 2.5 Sombras

Toda sombra deriva de `--primary` a 20% de opacidade, não de preto — é isso que dá sensação de marca:

| Token CSS | Uso |
| ---------------- | ---------------------------- |
| `--shadow-sm` | Cards comuns e menores |
| `--shadow-lg` | Componentes maiores / hover |
| `--shadow-focus` | Foco de inputs/CTA acessível |

### 2.6 Raio (border radius)

| Token | Uso |
| --- | --- |
| `--radius-sm` | badges pequenos, pílulas |
| `--radius-md` | elementos médios |
| `--radius-lg` | padrão: botão, input, card |
| `--radius-xl` | cantos de modal |

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

Duas famílias, expostas como `--font-sans` e `--font-display` no `@theme` gerado. Carregue-as no `app/layout.tsx` com `next/font` e passe a `className` da fonte no `<body>`.

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

Três famílias de token, todas em `--spacing-*` no `DESIGN.md`, todas viram
utilitária de espaçamento (`p-`, `px-`, `gap-`, `m-`):

- **Container** (`container-sm/md/default/xl`): margem lateral da página por
  faixa. `mx-auto max-w-[1400px] px-container-sm md:px-container-md lg:px-container-default 2xl:px-container-xl`.
- **Gutter** (`gutter-sm/md/default/xl`): espaço entre colunas de grid.
  `grid gap-gutter-sm md:gap-gutter-md lg:gap-gutter-default`.
- **Card padding** (`card-padding-mobile/tablet/desktop`): respiro interno de
  card. `p-card-padding-mobile md:p-card-padding-tablet lg:p-card-padding-desktop`.

```html
<section class="mx-auto max-w-[1400px] px-container-sm md:px-container-md lg:px-container-default">
  <div class="grid grid-cols-1 gap-gutter-sm sm:grid-cols-2 md:gap-gutter-md lg:grid-cols-3 lg:gap-gutter-default">
    <article class="rounded-lg border border-primary bg-card p-card-padding-mobile shadow-sm md:p-card-padding-tablet lg:p-card-padding-desktop">…</article>
  </div>
</section>
```

Não existe classe `.ds-*` neste projeto. Tudo é composição de utilitária de
token — se precisar repetir a mesma combinação três vezes, vire componente em
`components/`, não classe em CSS à parte.

---

## 6. Iconografia

- **Biblioteca de referência atual:** [Google Material Icons](https://fonts.google.com/icons).
- **Implementação no projeto:** `lucide-react` (alinhado ao shadcn).
- **Tamanhos:** 16 (inline em texto small), **20** (botões/inputs), **24** (default), **32+** (decorativo).
- **Cor:** herda do texto (`text-primary`, `text-muted-foreground`). Para ícones decorativos use `aria-hidden="true"`.
- **Ilustrações:** somente nas cores **`--primary` ou `--background`**; traçado próximo, humanizado, com retas/curvas seguindo a forma do símbolo da marca.

---

## 7. Componentes

> Primitiva (botão, input, dialog, accordion) vem do shadcn: `npx shadcn@latest
> add <nome>` grava em `components/ui/` e o código passa a ser seu. Composição
> de tela (header, card de serviço, banner) é sua e mora em `components/`.
> **Não reescreva uma primitiva que o shadcn já tem.** Cada seção abaixo diz o
> que o componente **é** e como se comporta; os valores estão no `DESIGN.md`.

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
- **Arrow button**: `size-10 rounded-lg border border-primary bg-background text-primary shadow-sm`.
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
  - **Botão Enviar** primário, alinhado à direita em desktop e full width em mobile (`sticky bottom-0 bg-card border-t border-border-muted`).
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

### 7.21 DatePicker

Seleção de data composta sobre `<input type="date">` nativo — **sem dependência
nova**. Herda o calendário da plataforma, navegação por teclado e formato
localizado.

```tsx
<DatePicker value={dataInicio} onChange={setDataInicio} aria-invalid={temErro} />
```

- `value`/`onChange` trafegam em ISO `YYYY-MM-DD`, a forma que o `zod` valida
  na server action — sem conversão de fuso no caminho.
- Reaproveita o `Input` do shadcn: `border-input`, altura, `focus-visible:ring`,
  `aria-invalid`. Glifo de calendário à esquerda.
- Estados: idle · foco · inválido (`aria-invalid`) · desabilitado (`disabled:opacity-50`).

### 7.22 CurrencyInput

Campo monetário composto sobre `<input type="text">` com máscara pt-BR —
**sem dependência nova**. Cada tecla vira dígito em centavos; o texto exibido é
sempre `1.234,56`.

```tsx
<CurrencyInput value={valor} onChange={setValor} aria-invalid={temErro} />
```

- `value`/`onChange` trafegam como número JS (`1234.56`), a forma que
  `z.number()` espera — sem parsing de locale, sem `NaN`. Dinheiro no banco é
  `Int` em centavos; a conversão é na fronteira.
- Reaproveita o `Input` do shadcn + glifo `R$` à esquerda + `tabular-nums`
  alinhado à direita.
- Estados: idle · foco · inválido · somente-leitura (`read-only:opacity-70`) ·
  desabilitado.

---

## 8. Acessibilidade

- **Contraste:** mínimo WCAG **4.5:1** entre texto e fundo (ver alerta no PDF). Em combinações limítrofes, use **negrito** ou outro reforço.
- **Foco visível:** sempre via `--shadow-focus`. Nunca `outline: none`.
- **Cor não é o único indicador de estado** — combine com ícone, label ou padrão.
- **Tipografia mínima:** 14 px corpo, 12 px metadados. Nunca abaixo de 12 px.
- **Tap target:** mínimo 44×44 px em touch (`h-11`).
- **Daltonismo:** evite combinar as duas cores de destaque da marca (`--highlight` + `--accent`) em alta área. Prefira contraste preto/branco quando precisar.
- **Reduced motion:** respeite `prefers-reduced-motion: reduce` (já declarado em `global.css`).

---

## 9. Diretrizes de uso

### Faça

- **Token, sempre.** `bg-primary`, `text-muted-foreground`, `shadow-sm`,
  `rounded-lg`, `px-container-md`. O valor vive no `DESIGN.md`; o componente
  só conhece o nome.
- **Container e grid por token de espaçamento** (§5). Repetiu a combinação
  três vezes? Vire componente em `components/`, não classe em CSS à parte.
- **Card**: `rounded-lg border border-primary bg-card shadow-sm` + padding por
  breakpoint (§5). Hover: `hover:shadow-lg transition-shadow`. Selecionado:
  `ring-2 ring-primary`. Alternativo sem destaque: `border-border-muted bg-secondary`.
- **Input**: o `Input` do shadcn em `components/ui/`, envolvido no padrão de
  float label (§7.7) quando a tela pede.
- **Animação só em `transform` e `opacity`** — o resto força layout e trava em
  máquina fraca. Respeite `prefers-reduced-motion`.
- **Ícone decorativo leva `aria-hidden="true"`.** Ícone que carrega
  informação leva rótulo.
- **Ilustração**: só `--primary` e `--background`, traçado humanizado (§1).

### Não faça

- ❌ Hex na classe (`bg-[#0055ff]`) ou em `style={{}}` — o hook bloqueia, e
  com razão: a cor fica órfã quando a marca mudar.
- ❌ Cor da paleta genérica do Tailwind (`bg-blue-600`, `text-gray-500`) —
  é uma segunda identidade visual entrando pela porta dos fundos.
- ❌ Classe de tema que não é token (`bg-azul`) — não gera estilo nenhum.
- ❌ `box-shadow` escrito à mão ou sombra preta — toda sombra deriva de
  `--primary` (§2.5). Use `shadow-sm` / `shadow-lg`.
- ❌ Editar `app/globals.css` — é gerado; some na próxima execução.
- ❌ Animar `width`, `height`, `top`, `left`.
- ❌ Brand Display em corpo de texto longo (§4).
- ❌ `--warning` em fundo cheio — só a 10%, e só em Atalhos / Passo a Passo.
- ❌ Banner vertical em mobile (§7.5).
- ❌ Reescrever primitiva que o shadcn já entrega. Adicione, depois estenda.
- ❌ Estado sinalizado só por cor. Combine com ícone ou rótulo (§8).

---

## 10. Referência rápida — utilitários Tailwind

Tudo abaixo é utilitária gerada de token do `DESIGN.md` ou nativa do Tailwind.
Nada aqui exige CSS à parte.

| Necessidade | Classe |
| --- | --- |
| Container da página | `mx-auto max-w-[1400px] px-container-sm md:px-container-md lg:px-container-default 2xl:px-container-xl` |
| Grid com gutter do DS | `grid gap-gutter-sm md:gap-gutter-md lg:gap-gutter-default` |
| Card padrão | `rounded-lg border border-primary bg-card shadow-sm p-card-padding-mobile md:p-card-padding-tablet lg:p-card-padding-desktop` |
| Card com hover | card padrão + `hover:shadow-lg transition-shadow` |
| Card selecionado | card padrão + `ring-2 ring-primary` |
| Card alternativo (sem destaque) | `rounded-lg border border-border-muted bg-secondary` + padding |
| Botão primário (ação) | `bg-accent text-accent-foreground rounded-lg px-6 py-3 font-bold shadow-sm hover:shadow-lg transition` |
| Botão secundário | `border border-primary text-primary rounded-lg px-6 py-3 font-bold hover:bg-primary hover:text-primary-foreground transition` |
| Link | `text-primary underline-offset-4 hover:underline focus-visible:underline` |
| Título display | `font-display text-4xl tracking-tight` |
| Corpo | `font-sans text-base leading-7 text-foreground` |
| Texto auxiliar | `text-sm text-muted-foreground` |
| Alerta de atenção | `flex items-start gap-2` + ícone `text-warning` + `<b>Atenção:</b>` |
| Alerta informativo | `flex items-start gap-2 bg-soft border-l-4 border-primary p-4 rounded-lg` |
| Foco visível | já é global (`:focus-visible` em `globals.css`); não precisa de classe |
| Rodapé fixo de wizard | `sticky bottom-0 bg-card border-t border-border-muted` |
| Números alinhados | `tabular-nums` |

---

## 11. Como estender o design system

Uma tela pediu algo que o DS não cobre — um estado a mais no badge, uma cor de
gráfico, um componente novo. A ordem é esta, e ela existe para o DS continuar
sendo um só:

1. **Já existe?** Procure em §7 e no `DESIGN.md › components`. A maior parte do
   que parece novo é variante do que já está lá.
2. **É valor novo** (cor, raio, espaçamento)? Entra no front matter do
   `DESIGN.md`, roda `python3 docs/design-system/gerar-tema.py`, e só então
   vira classe. Nunca o contrário. Tema é decisão de design — confirme com quem
   pediu antes de inventar o valor.
3. **É componente novo?** Componha em `components/` com as utilitárias de
   token, e registre a anatomia aqui em §7, com o mesmo formato das outras.
4. **É regra nova** (quando usar, quando não)? Vai em §9.

O que **não** se faz: criar a classe primeiro e documentar depois. É assim que
o guia passa a citar token que não existe — e foi exatamente o que aconteceu
antes deste arranjo.

---

## Onde está cada coisa

| O quê | Onde |
| --- | --- |
| Valores de tema (a fonte) | `docs/design-system/DESIGN.md`, front matter |
| Gerador dos derivados | `docs/design-system/gerar-tema.py` |
| `@theme` do Tailwind — **gerado** | `app/globals.css` |
| Tokens renderizados — **gerado** | `docs/design-system/showcase.html` |
| Primitivas shadcn | `components/ui/` — `npx shadcn@latest add <nome>` |
| Suas composições | `components/` |
| Fontes | `app/layout.tsx`, via `next/font` |

Divergência entre este guia e o `DESIGN.md`: o `DESIGN.md` prevalece para
valor, este guia prevalece para uso. Divergência entre qualquer um dos dois e
o `app/globals.css`: é bug — o CSS é gerado, rode o gerador e a checagem.
