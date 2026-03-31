# BulPay Analytics Dashboard — Build Plan

## Overview
Build a portfolio-grade analytics dashboard for BulPay.
Generate two synthetic CSV files with a Jan→Feb→Mar growth curve (Jan 1 – Mar 31, 2026),
then build a single-page HTML/CSS/JS dashboard in `05_Success_Metrics_Dashboard/`
that loads and computes all 19 metrics dynamically.

---

## To-Do List

### Phase 1 — Data Generation
- [x] **CSV-USERS** — Generate `bulpay_users.csv`: 50 rows with `user_id`, `registered_at`, `num_linked_cards`, `default_payment_source`, `balance_jan_eur`, `balance_feb_eur`, `balance_mar_eur` (NULL where user hadn't registered yet; Jan < Feb < Mar progression per user) ✅
- [x] **CSV-SESSIONS** — Generate `bulpay_sessions.csv`: 466 rows with `session_id`, `user_id`, `started_at`, `hour_of_day`, `day_of_week`, `is_first_session`, `core_action_performed`, `funnel_step_reached`, `amount_eur`, `payment_duration_seconds`, `pin_attempts`, `payment_source`, `switched_source`, `technical_success` ✅ *(revised: row count increased from 400 to 466 to hit growth-curve targets)*

### Phase 2 — HTML Scaffold & Engine
- [x] **HTML-SCAFFOLD** — Create `index.html` scaffold: sticky header, CSS variables, grid layout, CDN imports for Chart.js + PapaParse ✅
- [x] **DATA-ENGINE** — Build JS data engine: CSV loading, parsing, join, and all 19 metric computation functions with time-filter support ✅
- [x] **FILTER-LOGIC** — Wire global time filter: recompute all metrics and re-render all charts on 7d / 30d / 90d switch ✅ *(Zone 1 Health Pulse cards — NSM, MAU, D30 — are deliberately filter-independent; they always display their canonical full-period values regardless of the active filter, and carry a "filter-independent" sub-label to make this explicit to readers)*

### Phase 3 — Dashboard Zones
- [x] **ZONE-1** — Build Zone 1: NSM SVG bullet chart, MAU card, D30 doughnut gauge card with dual display logic ✅ 
- [x] **ZONE-2** — Build Zone 2: 5 financial KPI cards with GMV/ATV sparklines and delta arrows for short periods ✅ 
- [x] **ZONE-3** — Build Zone 3: transaction heatmap canvas, payment frequency distribution bar (completed payments per user, bucketed), time-to-first-payment histogram ✅
- [x] **ZONE-4** — Build Zone 4: SVG trapezoid funnel, time-to-complete histogram, PIN attempts KPI bar, technical success gauge ✅
- [x] **ZONE-5** — Build Zone 5: cards-per-user horizontal bar, card switch rate KPI card ✅

---

## Status Key
- ✅ = Completed
- 🔲 = Pending
- 🔄 = In Progress
---

# BulPay Analytics Dashboard — Build Plan

> Date range: **January 1 – March 31, 2026** (90 full days). Data is synthetic and the Mar 31 future date is intentional for portfolio narrative purposes.

## Deliverables

3 files inside `05_Success_Metrics_Dashboard/`:

- `bulpay_users.csv`
- `bulpay_sessions.csv`
- `index.html`

---

## Phase 1 — CSV Data Design

### `bulpay_users.csv` (50 rows)

Columns:

- `user_id` — u001 to u050
- `registered_at` — ISO datetime; 28 in Jan, 12 in Feb, 10 in Mar
- `num_linked_cards` — integer 1–4; distribution: 1→40%, 2→35%, 3→15%, 4→10%
- `default_payment_source` — `bulpay_balance`, `card_1`, `card_2`, etc.
- `balance_jan_eur` — BulPay wallet balance snapshot end-of-January; small test amounts (€5–€40); NULL for users who registered after Jan
- `balance_feb_eur` — end-of-February snapshot; growing trust (€15–€120); NULL for users who registered after Feb
- `balance_mar_eur` — end-of-March snapshot; established balance (€30–€300); reflects full 90-day arc

### `bulpay_sessions.csv` (466 rows)

Columns:

- `session_id` — s001 to s400
- `user_id` — FK to users
- `started_at` — ISO datetime; distribution: Jan ~90, Feb ~144, Mar 1–31 ~232
- `hour_of_day` — integer 0–23; pre-parsed from `started_at` for heatmap computation 
- `day_of_week` — string Mon/Tue/Wed/Thu/Fri/Sat/Sun; pre-parsed for heatmap 
- `is_first_session` — boolean; true if this is the user's first-ever session 
- `core_action_performed` — enum: `send` / `add_card` / `view_balance` / `freeze_card`; ~80% `send`, ~10% `add_card`, ~7% `view_balance`, ~3% `freeze_card`
- `funnel_step_reached` — integer 1–6 (1=Initiated, 2=Recipient Selected, 3=Amount Entered, 4=Confirmation Reached, 5=PIN Attempted, 6=Payment Completed); **only populated when `core_action_performed = 'send'`**, NULL for all other session types
- `amount_eur` — float; populated for step ≥ 3; avg €35–45, growing Jan→Mar
- `payment_duration_seconds` — integer; populated for step = 6; bins: 0–10, 10–30, 30–60, 60–120, 120+
- `pin_attempts` — integer 1–4; populated for step ≥ 5; trending down Jan→Mar (avg 1.5→1.2→1.05)
- `payment_source` — actual source used at time of payment
- `switched_source` — boolean; ~14% of transactions switch away from default (flat Jan/Feb/Mar — persistent adoption challenge)
- `technical_success` — boolean; `true` for step=6 + ~2% of step=5 failures

**Session type distribution (466 total):**


| Type           | %     | Count |
| -------------- | ----- | ----- |
| `send`         | ~83%  | 385   |
| `add_card`     | ~9%   | 40    |
| `view_balance` | ~7%   | 29    |
| `freeze_card`  | ~3%   | 12    |


**Growth curve targets** (send sessions only; non-send sessions excluded from payment metrics):


| Month      | Total sessions | Send sessions | Completed txns | MAU | NSM (txns/MAU) | Avg Amount |
| ---------- | -------------- | ------------- | -------------- | --- | -------------- | ---------- |
| Jan        | 90             | 73            | 48             | 26  | 1.85           | ~€34       |
| Feb        | 144            | 118           | 94             | 34  | 2.76           | ~€39       |
| Mar (1–31) | 232            | 194           | 161            | 38  | 4.24           | ~€45       |


**Funnel shape** (applies only to `core_action_performed = 'send'` sessions; base = 385):


| Step                     | Count | Step-over-step rate |
| ------------------------ | ----- | ------------------- |
| 1 — Initiated            | 385   | 100% (base)         |
| 2 — Recipient Selected   | ~365  | ~95%                |
| 3 — Amount Entered       | ~345  | ~90%                |
| 4 — Confirmation Reached | ~325  | ~84%                |
| 5 — PIN Attempted        | ~310  | ~81%                |
| 6 — Payment Completed    | 303   | 78.7%               |


D30 Retention (true D30, not calendar-month approximation):

- Jan cohort (28 users, registered Jan 1–31): ~61% retained (17/28) — meaning any session ≥ registered_at + 30 days; D30 window falls Feb 1 – Mar 2, fully within dataset
- Feb cohort (12 users, registered Feb 1–28): ~58% retained (7/12) — D30 window falls Mar 3 – Mar 30, fully within dataset
- Mar cohort (10 users, registered Mar 1–31): N/A — D30 window would fall Apr 1–Apr 30, entirely outside the dataset
- **Blended D30 (Jan + Feb evaluable cohorts): (17+7)/(28+12) = 24/40 = 60%**

---

## Phase 2 — Dashboard Architecture

**Single file:** `index.html` with embedded `<style>` and `<script>`

**Dependencies (CDN only):**

- Chart.js 4.x
- PapaParse (CSV parsing)

**Data loading flow:**

```
Promise.all([fetch(users.csv), fetch(sessions.csv)])
  → PapaParse both
  → join on user_id
  → build derived dataset
  → render all zones
  → attach filter event listeners
```

**State management:** One global `state.filter = '90d' | '30d' | '7d'` that triggers full re-render on change.

**Date windows:**

- 90d: Jan 1 – Mar 31, 2026 (full dataset)
- 30d: Mar 2 – Mar 31 (current) vs. Jan 31 – Mar 1 (prior)
- 7d: Mar 25 – Mar 31 (current) vs. Mar 18 – Mar 24 (prior)

---

## Phase 3 — Zone-by-Zone Implementation

### Zone 0 — Sticky Header

- Text logo + subtitle hardcoded
- Three `<button>` segments; active state styled with border/bg
- Click → `setFilter(period)` → recompute all zones

### Zone 1 — Health Pulse

> **Design decision — all three cards are filter-independent.** The 7D / 30D / 90D filter exists to let readers slice financial flow metrics (Zone 2). The Zone 1 health-pulse cards represent structural, cohort-level truths that should not be misread as short-window snapshots. Each card carries a muted "filter-independent" sub-label directly below its title (matching the same visual treatment across all three cards).

- **NSM bullet chart**: SVG-based, 3 colored bands (red 0–2, amber 2–3, green 3–4+), target line at 4.0; sub-label reads "90-day blended average · filter-independent"; big number = **90-day blended NSM** = total completed `send` txns ÷ sum of monthly MAU values = 303 ÷ (26+34+38) = **3.09 txns/user/month** (preserves the monthly rate unit; dividing by average MAU would give a 90-day count, not a monthly rate); needle lands in **green "Good" zone**; Jan/Feb/Mar plaintext footer shows monthly values (1.85 · 2.76 · 4.24); no delta badge — filter-independent
- **MAU card**: sub-label reads "March · most recent full month · filter-independent"; big number = **38** (March MAU — most recent full month; MAU is a point-in-time metric, summing months would double-count users); "of 50 registered" sub-label beneath the hero; monthly trend shown as a **Chart.js horizontal bar chart** (not plaintext) — 3 rows (Jan / Feb / Mar), bars extend left-to-right, full card width = 50 registered users, bar lengths proportional to 26 / 34 / 38; progressive blue opacity (Jan lightest → Mar full `#2563EB`); inline `afterDraw` plugin writes the raw count to the right of each bar's end; no delta badge — filter-independent
- **D30 card**: sub-label reads "Jan & Feb cohorts · filter-independent"; big number = **blended D30 rate across Jan + Feb evaluable cohorts only** (weighted by cohort size: (17+7)/(28+12) = 60%); Chart.js Doughnut (2 arcs: retention % + remainder); cohort list shows Jan: 61% (17/28) · Feb: 58% (7/12) · Mar: N/A; amber footnote explains Mar cohort excluded because D30 window falls outside the dataset

### Zone 2 — Financial Performance

- 5 KPI cards in 3+2 grid layout (Row A: GMV · ATV · Cost per Transaction; Row B: Total BulPay Balance · Avg BulPay Balance per Active User)
- GMV + ATV each have a small Chart.js Line sparkline (weekly, ~12 data points Jan–Mar)
- **GMV big number (90d)**: **SUM** of all completed transaction amounts across the full 90 days — additive flow metric; Jan/Feb/Mar plaintext shows monthly sums
- **ATV big number (90d)**: **90-day blended average** = total transaction value ÷ total completed txns — ratio metric; Jan/Feb/Mar shows monthly averages (~€35 · ~€39 · ~€46)
- **Cost per Transaction big number (90d)**: flat rate of **€0.15 per completed transaction** — constant, no trend; Jan/Feb/Mar plaintext all show €0.15 (the rate is unchanged); the growth story in Zone 2 is carried by GMV and ATV, not by cost efficiency
- **Total BulPay Balance big number (90d)**: **March snapshot** (`SUM(balance_mar_eur)`) — point-in-time metric, not additive across months; Jan/Feb/Mar shows `SUM(balance_jan_eur)` · `SUM(balance_feb_eur)` · `SUM(balance_mar_eur)` (NULLs excluded per month)
- **Avg BulPay Balance per Active User big number (90d)**: **March snapshot** (`SUM(balance_mar_eur) / March MAU`) — point-in-time; Jan/Feb/Mar shows monthly averages
- On 30d/7d: all 5 cards switch to delta = `((current - prior) / prior * 100)`, colored ▲/▼ arrow

### Zone 3 — User Behaviour

- **Heatmap**: Chart.js Matrix plugin (or custom `<canvas>` drawn with `fillRect`), 7 rows × 24 cols, sequential blue scale
- **Payment Frequency Distribution**: Chart.js Bar, buckets 1 / 2–3 / 4–6 / 7–10 / 10+ — measures how many **completed payments** (`core_action_performed = 'send'` + `funnel_step_reached = 6`) users make within the selected period, bucketed by payment count per user; subtitle reads "Completed payments per user · within selected period"
- **Time to First Payment**: Chart.js Bar histogram, 6 buckets

### Zone 4 — Payment Flow & Quality

- **SVG Funnel**: hand-drawn trapezoid polygons in inline SVG; each step computed from `funnel_step_reached` column **filtered to `core_action_performed = 'send'` rows only**; labels overlay absolute count + step-over-step %
- **Time to Complete**: Chart.js Bar, 5 bins
- **PIN Attempts KPI**: big number = **90-day blended average** across all completed send sessions (ratio metric); Jan/Feb/Mar plaintext shows monthly averages trending down; benchmark bar at 1.0
- **Technical Success Rate**: big number = **90-day blended %** across all send sessions (ratio metric); Chart.js Doughnut gauge + green/amber/red color coding; Jan/Feb/Mar shows monthly rates

### Zone 5 — Card Ecosystem

- **Cards per User**: Chart.js horizontal Bar, 4 rows (1/2/3/4 cards)
- **Card Switch Rate**: big number = **90-day blended %** of send sessions where user switched from default source (ratio metric); Jan/Feb/Mar plaintext shows monthly rates (~15% · ~14% · ~13% — flat, amber signal, persistent adoption friction)

---

## Phase 4 — Styling

### Color Palette — matched to the BulPay prototype

The dashboard uses the **exact same color tokens** as the prototype (`v3/index.html`). A hiring manager reviewing both the prototype and the dashboard will see one cohesive product, not two separate tools. This is a deliberate portfolio signal.

**Core palette (direct extractions from `v3/index.html`):**

- `--color-bg`: `#EEF2F8` — page background; identical to `pageBg` in the app
- `--color-surface`: `#FFFFFF` — card backgrounds; identical to `headerBg`
- `--color-primary`: `#2563EB` — brand blue; the app's `btnPrimary`, pin dots, active nav
- `--color-primary-light`: `rgba(37,99,235,0.10)` — tinted highlights, hover states
- `--color-border`: `#E5E7EB` — card borders; same as `C.border` in the app
- `--color-border-subtle`: `#F3F4F6` — inner dividers; same as `C.rowBorder`
- `--color-txt-primary`: `#111827` — headings and KPI numbers; same as `C.txtPrimary`
- `--color-txt-secondary`: `#374151` — body text
- `--color-txt-muted`: `#4B5563` — axis labels, footnotes; same as `C.txtMuted`

**Semantic status colors (all present in the prototype):**

- `--color-good`: `#16A34A` — positive delta arrows, retention green, high NSM band; same green used for income amounts in the app's transaction list
- `--color-warn`: `#D97706` — amber mid-band, satisfactory NSM zone, churn footnote
- `--color-bad`: `#EF4444` — negative delta arrows, churn spike, PIN error; same as `C.pin-dot.err`

**Chart accent colors (pulled from the three card gradients in the prototype):**

- Primary series: `#2563EB` (brand blue — card3 start / btnPrimary)
- Secondary series: `#6878F5` (indigo — card2 start)
- Tertiary series: `#9B6BF8` (violet — card2 end)
- Quaternary series: `#06B6D4` (cyan — card3 end)
- Quinary series: `#93ADFD` (periwinkle — card1 start)

These five colors are used in order for multi-series charts and as the discrete bucket fills in bar charts.

**Heatmap sequential scale:**
Single-hue blue progression in 6 steps anchored to the brand primary:
`rgba(37,99,235,0.07)` → `rgba(37,99,235,0.20)` → `rgba(37,99,235,0.38)` → `rgba(37,99,235,0.55)` → `rgba(37,99,235,0.75)` → `#1d4ed8`

Zero-count cells render as `#F8FAFC` (near-white, distinct from the page background).

**NSM bullet chart bands:**

- Poor (0–2.0): `rgba(239,68,68,0.12)` fill, label `#EF4444`
- Satisfactory (2.0–3.0): `rgba(217,119,6,0.12)` fill, label `#D97706`
- Good (3.0–4.0+): `rgba(22,163,74,0.12)` fill, label `#16A34A`
- Target line at 4.0: `#2563EB` dashed stroke
- **Needle lands in the green "Good" zone at 3.09**

**Typography:**

Font: **Roboto** (loaded from Google Fonts) — the prototype's font. Not Inter. Using the same typeface reinforces the single-product feel.

Weights in use: 300 (muted footnotes), 400 (body), 500 (card labels), 700 (KPI hero numbers)

**Card styling:**

- `border-radius: 10px`
- `box-shadow: 0 2px 10px rgba(0,0,0,0.08)` — matches `C.cardShadow` spirit
- `padding: 20px 24px`
- Background: `--color-surface` (`#FFFFFF`)

**Chart defaults:**

- Grid lines: `rgba(0,0,0,0.05)` — near-invisible
- Tick labels: `--color-txt-muted` (`#4B5563`), `font-size: 11px`
- No chart borders; tension on line charts: `0.35`

---

## Key Technical Constraints

- All metric values computed programmatically from CSV rows — **no hardcoded values**
- Funnel uses `<polygon>` SVG elements, not Chart.js bars
- Bullet chart uses SVG `<rect>` zones + `<line>` marker — not a `<progress>` element
- NSM (90d view) = `completedSendTxns.length / sumOfMonthlyMAU` — divides total transactions by total user-months of exposure; do NOT divide by average MAU (that strips the "per month" unit and inflates the result by 3×); computed value = 303 / 98 = **3.09**
- D30 retention uses true D30 logic: `retainedUsers.filter(u => sessions.some(s => s.user_id === u.user_id && date(s.started_at) >= addDays(date(u.registered_at), 30)))` — a user who registers Jan 31 and returns Feb 2 does NOT count as D30 retained; blended result = **24/40 = 60%**
- Only Jan and Feb cohorts are evaluated; Mar cohort is excluded (D30 window falls outside dataset)
- Churn = users active in prior month but absent in current month / users active in prior month
- Card switch rate ≈ **14% flat** across Jan/Feb/Mar — deliberate amber signal, framed as persistent adoption friction not a regression
- Time to First Payment: **27% of users take > 14 days** to make first payment after registration — reflects real friction for elderly Bulgarian target audience; 13 of 48 paying users fall in the >14-day bucket

