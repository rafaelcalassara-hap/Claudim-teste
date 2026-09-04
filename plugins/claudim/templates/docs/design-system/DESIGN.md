---
version: 1.0.0
name: Acme Design System V2
description: >
  Machine-readable theme tokens. Single source of every theme value.
  Consumed by gerar-tema.py, which writes app/globals.css (Tailwind @theme)
  and showcase.html. Usage guidance lives in DS-ACME.md.
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

> **This file answers one question: what is the value.** The YAML front matter
> at the top is the single source of every theme value; the tables below name
> the tokens and what each one is for. `gerar-tema.py` reads the front matter
> and writes `app/globals.css` and `showcase.html` — never edit those by hand.
>
> **It does not answer how to use them.** Component anatomy, variants, states,
> do/don't and accessibility live in [`DS-ACME.md`](./DS-ACME.md). Building a
> screen? Read that one.

> **Human-readable reference**: see [`DS-ACME.md`](./DS-ACME.md) for full prose, illustrations, and usage rationale.
> **Generated theme**: `app/globals.css` — run `python3 docs/design-system/gerar-tema.py`
> **Rendered tokens**: `showcase.html`, same folder

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

Two official families, exposed as `--font-sans` and `--font-display` in the generated `@theme`.

| Family      | CSS Variable                        | Tailwind              | When to use                                                     |
| ----------- | ----------------------------------- | --------------------- | --------------------------------------------------------------- |
| **Brand Display** | `--font-display` | `font-display`        | Creative headings, banners, highlights. **Never** in body text. |
| **Inter**  | `--font-sans`     | `font-sans` (default) | All other text: headings, body, labels, buttons.                |

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

> ⚠️ **The Tailwind column is a reference, not a binding**: this template does
> not declare `--breakpoint-*` tokens, so `sm:`/`md:`/`lg:` fire at Tailwind v4
> defaults (640/768/1024). The four DS widths are design targets. How to apply
> them with the variants that exist is in `DS-ACME.md` §2.

### Container

| Breakpoint  | Padding Inline | Max Width |
| ----------- | -------------- | --------- |
| Small       | 15 px          | —         |
| Medium      | 30 px          | 800 px    |
| Default     | 40 px          | 1400 px   |
| Extra Large | 80 px          | 1920 px   |

### Grid gutter

| Breakpoint  | Gap   |
| ----------- | ----- |
| Small       | 15 px |
| Medium      | 20 px |
| Default     | 30 px |
| Extra Large | 40 px |

### Card padding

| Breakpoint | Padding |
| ---------- | ------- |
| Mobile     | 20 px   |
| Tablet     | 24 px   |
| Desktop    | 32 px   |


---

## Elevation & Depth

Every shadow is derived from `--primary` at 20% opacity — never pure black.

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
| `--radius-sm` | Small badges |
| `--radius-md` | Medium elements |
| `--radius-lg` | Standard |
| `--radius-xl` | Modal corners |

---

## Reference

| What | Where |
| --- | --- |
| How to use each token, component anatomy, do/don't, accessibility | [`DS-ACME.md`](./DS-ACME.md) |
| Generator: reads this file, writes the derived artifacts | [`gerar-tema.py`](./gerar-tema.py) |
| Tailwind `@theme` — **generated**, do not edit | `app/globals.css` |
| Rendered tokens — **generated** | [`showcase.html`](./showcase.html) |
| shadcn primitives (`npx shadcn@latest add <name>`) | `components/ui/` |
| Your own components | `components/` |

This file answers *what is the value*. For *how do I use it*, read `DS-ACME.md`.
