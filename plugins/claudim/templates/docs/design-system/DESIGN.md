---
version: 1.0.0
name: Acme Design System V2
description: >
  Machine-readable tokens and component guidelines for the Acme React monorepo.
  Consumed by apps/console (internal panel) and apps/site (public sites).
  Canonical token source: apps/site/src/app/global.css
colors:
  brand:
    primary: '#8D0000'
    primary-darker: '#4D1D00'
    primary-foreground: '#FFFFFF'
    accent: '#009E90'
    accent-foreground: '#FFFFFF'
    highlight: '#4EE0FF'
    soft: '#E3F6F6'
  surface:
    background: '#FFFFFF'
    foreground: '#2D2D2D'
    card: '#FFFFFF'
    card-foreground: '#2D2D2D'
    popover: '#FFFFFF'
    popover-foreground: '#2D2D2D'
    secondary: '#F5F5F5'
    secondary-foreground: '#2D2D2D'
    muted: '#F5F5F5'
    muted-foreground: 'rgba(45, 45, 45,0.6)'
  status:
    success: '#16A34A'
    destructive: '#DC2626'
    destructive-foreground: '#FFFFFF'
    warning: '#F59E0B'
  chart:
    chart-1: 'oklch(0.45 0.18 250)'
    chart-2: 'oklch(0.58 0.16 165)'
    chart-3: 'oklch(0.65 0.2 45)'
    chart-4: 'oklch(0.55 0.22 300)'
    chart-5: 'oklch(0.65 0.2 16)'
  line:
    border: '#8D0000'
    border-muted: '#ACACAC'
    input: '#ACACAC'
    ring: '#F1D0C5'
typography:
  display:
    fontFamily: 'Brand Display'
    fontWeight: 700
    letterSpacing: '-0.01em'
  sans:
    fontFamily: 'Inter'
    fontWeight: 400
rounded:
  sm: '2px'
  md: '4px'
  lg: '6px'
  xl: '10px'
spacing:
  container-sm: '15px'
  container-md: '30px'
  container-default: '40px'
  container-xl: '80px'
  gutter-sm: '15px'
  gutter-md: '20px'
  gutter-default: '30px'
  gutter-xl: '40px'
  card-padding-mobile: '20px'
  card-padding-tablet: '24px'
  card-padding-desktop: '32px'
elevation:
  sm: '0 3px 6px rgba(141, 0, 0,0.20)'
  lg: '0 6px 12px rgba(141, 0, 0,0.20)'
  focus: '0 0 0 3px #F1D0C5'
  overlay: 'rgba(0, 0, 0,0.80)'
components:
  button-primary:
    background: '{colors.brand.accent}'
    foreground: '{colors.brand.accent-foreground}'
    border-radius: '{rounded.lg}'
    shadow: '{elevation.sm}'
    padding: '12px 24px'
    font-weight: 700
    font-family: 'Inter'
  button-secondary:
    background: 'transparent'
    border: '1px solid {colors.brand.primary}'
    foreground: '{colors.brand.primary}'
    border-radius: '{rounded.lg}'
    hover-background: '{colors.brand.primary}'
    hover-foreground: '{colors.brand.primary-foreground}'
  link:
    foreground: '{colors.brand.primary}'
    decoration: 'underline on hover/focus'
    disabled-foreground: '{colors.line.border-muted}'
  float-input:
    height: '56px'
    border: '1px solid {colors.line.input}'
    border-radius: '{rounded.lg}'
    focus-ring: '{elevation.focus}'
    focus-border: '{colors.brand.primary}'
    invalid-border: '{colors.status.destructive}'
    label-float-size: '11px'
    label-float-weight: 700
    label-float-color: '{colors.brand.primary}'
  card:
    background: '{colors.surface.card}'
    border: '1px solid {colors.brand.primary}'
    border-radius: '{rounded.lg}'
    shadow: '{elevation.sm}'
    padding-mobile: '{spacing.card-padding-mobile}'
    padding-tablet: '{spacing.card-padding-tablet}'
    padding-desktop: '{spacing.card-padding-desktop}'
  card-quick-access:
    background: 'rgba(245, 158, 11,0.10)'
    note: 'Exclusive to Quick Access cards and Step-by-Step cards. Never use #F59E0B at full opacity.'
  accordion:
    background: '{colors.surface.background}'
    chevron-color: '{colors.brand.primary}'
  ds-arrow:
    size: '40px'
    border-radius: '{rounded.lg}'
    background: '{colors.surface.background}'
    border: '1px solid {colors.brand.primary}'
    shadow: '{elevation.sm}'
    hover-color: '{colors.brand.primary}'
    disabled-color: '{colors.line.border-muted}'
---

# Acme Design System V2 — DESIGN.md

> O **front matter YAML no topo deste arquivo é a única fonte dos valores** de
> tema. O corpo abaixo documenta uso e cita token por nome. `gerar-tema.py` lê
> o front matter e escreve `app/globals.css` e `showcase.html` — não edite os
> derivados à mão.

> **Human-readable reference**: see [`DS-ACME.md`](./DS-ACME.md) for full prose, illustrations, and usage rationale.
> **Live tokens**: `apps/site/src/app/global.css`
> **Storybook**: `npm run storybook` → `http://localhost:6006`

---

## Overview

Acme React is an enterprise SPA. The DS is built on four core principles:

- **Acolhimento e confiança** — humanized communication; illustration style: `--primary` or `--background`, rounded strokes following the brand symbol shape.
- **Accessibility first** — minimum WCAG AA contrast (4.5:1). Color is never the sole state indicator.
- **Mobile-first** — four fixed breakpoints: 320 / 720 / 1400 / 1920 px.
- **Token-based** — every visual value flows through a CSS custom property in `:root`. Never use hex literals in components.
- **Composition-only** — extend primitives in `packages/ui` via `cn()` and `packages/layout`. Never edit shadcn source files.

---

## Colors

### Brand

| CSS Token | Tailwind | Usage |
| ------------------ | ------------ | ----------------------------------- |
| `--primary` | `bg-primary` | Core brand (primary) |
| `--primary-darker` | — | Hover/pressed state on primary |
| `--accent` | `bg-accent` | Primary CTA, accent highlight |
| `--highlight` | — | Short highlights (badges, pills) |
| `--soft` | — | Soft background for accent sections |

### Surfaces

| CSS Token | Tailwind | Usage |
| -------------------- | ----------------------- | -------------------------------- |
| `--background` | `bg-background` | Default page background |
| `--foreground` | `text-foreground` | Default text |
| `--card` | `bg-card` | Card background |
| `--secondary` | `bg-secondary` | Alternate section background |
| `--muted` | `bg-muted` | Disabled state, muted background |
| `--muted-foreground` | `text-muted-foreground` | Helper text, secondary labels |

### Status

| CSS Token | Usage |
| --------------- | --------------------------------------------------------------- |
| `--success` | Success states, completed upload |
| `--destructive` | Errors, destructive actions |
| `--warning` | Attention inline alerts; Quick Access cards at 10% opacity only |

### Lines / Focus

| CSS Token | Usage |
| ---------------- | ------------------------------------- |
| `--border` | Default border (aligned with primary) |
| `--border-muted` | Disabled field borders |
| `--input` | Default input border |
| `--ring` | Accessible focus halo |

### Data Visualization (data palette)

Five-hue categorical palette for charts, multi-state badges and any data viz
where the six semantic Status/Surface tokens are insufficient. Defined as
`oklch()`, declared in the `DESIGN.md` front matter and emitted to the `@theme`
and exposed in each portal `@theme` as `--color-chart-N` → `bg-chart-N` /
`text-chart-N` / `border-chart-N`. Pair with a non-color cue (icon + label)
whenever used as a state indicator — color is never the sole signal.

| CSS Token | Tailwind | Hue family |
| ----------- | ------------ | --------------------------- |
| `--chart-1` | `bg-chart-1` | Blue (brand-adjacent) |
| `--chart-2` | `bg-chart-2` | Green (success family) |
| `--chart-3` | `bg-chart-3` | Orange (attention family) |
| `--chart-4` | `bg-chart-4` | Violet (special transition) |
| `--chart-5` | `bg-chart-5` | Red-orange (soft-negative) |

---

## Typography

Two official families, both injected via `next/font/local` from `packages/fonts`.

| Family      | CSS Variable                        | Tailwind              | When to use                                                     |
| ----------- | ----------------------------------- | --------------------- | --------------------------------------------------------------- |
| **Brand Display** | `--font-brand-display` (`--font-display`) | `font-display`        | Creative headings, banners, highlights. **Never** in body text. |
| **Inter**  | `--font-inter` (`--font-sans`)     | `font-sans` (default) | All other text: headings, body, labels, buttons.                |

`.font-display` applies `font-weight: 700` and `letter-spacing: -0.01em`.

### Heading Scale

| Tag   | Mobile              | Tablet                | Desktop               | Family           |
| ----- | ------------------- | --------------------- | --------------------- | ---------------- |
| H1    | `text-3xl/tight`    | `text-4xl/tight`      | `text-5xl/tight`      | Brand Display          |
| H2    | `text-2xl/snug`     | `text-3xl/snug`       | `text-4xl/snug`       | Brand Display / Inter |
| H3    | `text-xl/snug`      | `text-2xl/snug`       | `text-3xl/snug`       | Inter           |
| H4    | `text-lg/snug`      | `text-xl/snug`        | `text-2xl/snug`       | Inter           |
| H5    | `text-base`         | `text-lg`             | `text-xl`             | Inter           |
| H6    | `text-sm`           | `text-base`           | `text-lg`             | Inter Bold      |
| Body  | `text-sm leading-6` | `text-base leading-7` | `text-base leading-7` | Inter           |
| Small | `text-xs`           | `text-xs`             | `text-sm`             | Inter           |

Minimum body size: 14 px. Minimum metadata size: 12 px. Never below 12 px. Tap targets: 44×44 px minimum.

---

## Layout

### Breakpoints

| Name        | Min Width | Tailwind |
| ----------- | --------- | -------- |
| Small       | 320 px    | default  |
| Medium      | 720 px    | `sm:`    |
| Default     | 1400 px   | `lg:`    |
| Extra Large | 1920 px   | `2xl:`   |

> ⚠️ **The Tailwind column above is aspirational, not implemented**: no
> `--breakpoint-*` tokens are declared in any `@theme`, so `sm:`/`md:`/`lg:`
> actually fire at Tailwind v4 defaults (640/768/1024). Only the manual
> media queries in `tokens.css` (`.ds-container`, `.ds-card`,
> `.sticky-cta`) use 720/1400/1920. See the desync note under DS-EXT-3.

### Responsive Container — `.ds-container`

| Breakpoint  | Padding Inline | Max Width |
| ----------- | -------------- | --------- |
| Small       | 15 px          | —         |
| Medium      | 30 px          | 800 px    |
| Default     | 40 px          | 1400 px   |
| Extra Large | 80 px          | 1920 px   |

### Responsive Grid — `.ds-grid`

| Breakpoint  | Gap   |
| ----------- | ----- |
| Small       | 15 px |
| Medium      | 20 px |
| Default     | 30 px |
| Extra Large | 40 px |

### Card Padding — `.ds-card`

| Breakpoint | Padding |
| ---------- | ------- |
| Mobile     | 20 px   |
| Tablet     | 24 px   |
| Desktop    | 32 px   |

```html
<section class="ds-container">
  <div class="ds-grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
    <article class="ds-card ds-card--hover">…</article>
  </div>
</section>
```

---

## Elevation & Depth

All shadows use **navy at 20% opacity** — never pure black shadows.

| Token | Usage |
| ---------------- | ----------------------------------- |
| `--shadow-sm` | Cards, smaller components |
| `--shadow-lg` | Larger components, hover state |
| `--shadow-focus` | Accessible focus ring on inputs/CTA |
| `--color-overlay` | Modals, drawers, lightbox |

---

## Shapes

| Token | Usage |
| ----------------- | ---------------------- |
| `--radius` (base) | Buttons, inputs, cards |
| `--radius-sm` | Small badges |
| `--radius-md` | Medium elements |
| `--radius-lg` | Standard |
| `--radius-xl` | Modal corners |

---

## Components

### Button

```tsx
// Primary (CTA) — bg-accent text-accent-foreground
<Button className="bg-accent text-accent-foreground rounded-md px-6 py-3 font-semibold shadow-sm hover:shadow-lg transition">
  Seja cliente
</Button>

// Secondary — border outline
<Button variant="outline" className="border-primary text-primary hover:bg-primary hover:text-primary-foreground">
  Saiba mais
</Button>

// Tertiary (link)
<Button variant="link" className="text-primary underline-offset-4">
  Ver detalhes
</Button>
```

Primitiva: `packages/ui/src/lib/button.tsx`

### Float Label Input

```html
<div class="float-field" data-filled="true">
  <input id="email" type="email" class="float-input" placeholder=" " />
  <label for="email">*E-mail</label>
</div>
```

States: `:focus-within` / `[data-filled="true"]` → label floats to 11 px + primary color.
`[data-invalid="true"]` → border + label in destructive color.

Primitiva: `.float-field` / `.float-input` utilities in `apps/site/src/app/global.css`.
React wrapper: `packages/feature-signup/src/lib/fields/FloatInput.tsx`

### DatePicker (DS-EXT-1)

```tsx
<DatePicker
  value={vigenciaIni}
  onChange={setVigenciaIni}
  aria-invalid={hasError}
/>
```

Date selection primitive introduced for SCREEN-A vigência fields (reused by
SCREEN-B). Composed from a native `<input type="date">` (zero extra runtime
dependency) so it ships a platform calendar popover + keyboard support, while
its `value`/`onChange` stay canonical ISO `YYYY-MM-DD` strings (the
transport-boundary shape). Reuses the `Input` tokens (border/height
`h-9`/focus-ring/`aria-invalid`) plus a leading calendar glyph;
`dark:[color-scheme:dark]` keeps the native control legible in dark mode.

Primitiva: `packages/ui/src/lib/date-picker.tsx` (`DatePicker`).

### CurrencyInput (DS-EXT-2)

```tsx
<CurrencyInput
  value={vlItem}
  onChange={setVlItem}
  aria-invalid={hasError}
/>
```

Money primitive introduced for SCREEN-A value fields (`vlItem`,
`vlLimite`; reused by SCREEN-B). Composed from a plain text input driven as a
pt-BR amount mask (**zero extra runtime dependency**): keystrokes are reduced to
digits read as centavos, so the display is always a valid `1.234,56` amount
while `value`/`onChange` stay a canonical JS number (`1234.56`) — the
transport-boundary shape (`z.number()`). Reuses the `Input` tokens
(border/height `h-9`/focus-ring/`aria-invalid`) plus a leading `R$` glyph and
`tabular-nums` right alignment; `read-only`/`disabled` states mirror the DS.

Primitiva: `packages/ui/src/lib/currency-input.tsx` (`CurrencyInput`).

### Wizard header band + persistent footer (DS-EXT-3)

Introduced for the Novo Cadastro wizard (apps/site). One context band
per step card — never two step indicators on the same screen:

- **Band anatomy**: single-line progress trail (28px bubbles, label beside
  the bubble) + hairline `var(--border-muted)` + `font-display text-xl
sm:text-2xl` title with the subtitle as an inline apposition. The
  "Passo X de 4" eyebrow is forbidden when a progress trail is visible;
  the step context is exposed via `aria-label` on the card region.
- **`.sticky-cta--persist`** (additive modifier over `.sticky-cta`,
  declared in `packages/tokens/src/tokens.css`): keeps the
  wizard footer sticky at ≥720px. Background `var(--card)` (not
  `--background` — no color step inside the card), top hairline
  `var(--border-muted)`, bottom corners `var(--radius)`, own padding
  12px @720 / 16px @1400 (vertical). Side bleed and bottom inset derive
  from `--ds-card-pad` (custom property set by `.ds-card`: 20/24/32px),
  so the band always reaches the card edge. Compound selector
  (`.sticky-cta.sticky-cta--persist`) wins by specificity — source-order
  independent. Pairs with `html:has(.sticky-cta--persist)
{ scroll-padding-bottom: 96px }` so keyboard focus is never hidden
  under the band (WCAG 2.4.11).
- **Form rhythm (two levels)**: 16px (`space-y-4`) between field blocks,
  12px (`gap-3`) inside a field group. `.float-input` height (56px) is
  untouched.
- **Form grid breakpoints**: field pairs use `sm:` (640px); asymmetric
  rows of 3+ columns use `md:` (768px). See the breakpoint note below.

> **Breakpoint desync note**: no `--breakpoint-*` tokens are declared in
> the `@theme` blocks, so Tailwind v4 variants use its defaults
> (`sm`=640, `md`=768, `lg`=1024, `2xl`=1536) while the DS media queries
> (`.ds-container`, `.ds-card`, `.sticky-cta`) fire at 720/1400/1920.
> Aligning them (declaring `--breakpoint-*`) is a high-blast-radius
> follow-up — do not mix the two scales silently in new code.

### Card

```tsx
<div className="ds-card ds-card--hover">
  <h3 className="text-xl font-semibold text-foreground">Title</h3>
  <p className="text-muted-foreground text-sm mt-2">Description</p>
</div>
```

Primitiva: `.ds-card` + modifier classes. shadcn wrapper: `packages/ui/src/lib/card.tsx`

### Alert (inline)

```tsx
// Attention (amber icon)
<div className="flex items-start gap-2">
  <TriangleAlert className="text-[var(--warning)] mt-0.5 shrink-0" size={20} />
  <p><strong>Atenção:</strong> Envie os documentos referente à sua solicitação.</p>
</div>

// Info (primary icon)
<div className="flex items-start gap-2">
  <Info className="text-primary mt-0.5 shrink-0" size={20} />
  <p>Para consultar serviços anteriores à data de corte da migração…</p>
</div>
```

Primitiva: `packages/ui/src/lib/alert.tsx`

### FAQ / Accordion

```tsx
<Accordion type="single" collapsible>
  <AccordionItem value="q1">
    <AccordionTrigger>Quais benefícios estão disponíveis?</AccordionTrigger>
    <AccordionContent>
      No nosso Programa de Benefícios você encontra…
    </AccordionContent>
  </AccordionItem>
</Accordion>
```

---

## Do's and Don'ts

### Do

- Use tokens (`--primary`, `bg-accent`, `shadow-sm`) — never hex literals.
- Combine `.ds-container` + `.ds-grid` for DS margins and gutters.
- Use `.ds-card` + modifiers (`--hover`, `--selected`, `--muted`) as base; extend with Tailwind.
- Animate only `transform` and `opacity` (GPU-safe).
- Provide `dark:` variants on all new components.
- Add `aria-hidden="true"` on decorative icons.
- Respect `prefers-reduced-motion` (declared in `global.css`).

### Don't

- ❌ `bg-[#0055ff]` — use the token: `bg-primary`.
- ❌ A hand-written `box-shadow` — use `shadow-sm` / `shadow-lg`; every shadow
  in the system is derived from `--primary`.
- ❌ Animate `width`, `height`, `top`, `left` — layout thrashing.
- ❌ Combine Brand Display in long body text.
- ❌ Use `--warning` at full opacity — only at 10% for Quick Access / Step-by-Step cards.
- ❌ Banner vertical on mobile.
- ❌ Edit files in `packages/ui` inline — extend via composition in `packages/layout` or features.
- ❌ `any` type — use `unknown` + type guards.
- ❌ Default exports — always named exports.

---

## Reference

| Resource                                     | Path                                                                                 |
| -------------------------------------------- | ------------------------------------------------------------------------------------ |
| Full prose guidelines                        | [`DS-ACME.md`](./DS-ACME.md)                                                   |
| Design source document (authoritative for foundations) | `design-source.pdf`                                                          |
| Live CSS tokens                              | `apps/site/src/app/global.css` |
| shadcn primitives                            | `packages/ui/src/lib/`                               |
| Layout composites                            | `packages/layout/src/lib/`                       |
| Fonts (Brand Display + Inter)                     | `packages/fonts/src/lib/`                         |
| Storybook host                               | `apps/storybook/`                                       |
