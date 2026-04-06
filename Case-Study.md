# BulPay - A Digital Wallet for Tech-Shy Adults in Bulgaria

> A product management case study covering problem definition, market discovery, user  
> research, experiment design, prototyping, usability testing, iteration and success metrics dashboard  
> **Status:** Custom-made BulPay dashboard in progress.

---

## The Problem

Older, low-income Bulgarian adults are stuck between two bad options. 
Local bank apps are confusing, crash-prone, and charge fees that eat 
into tight budgets. Neobanks like Revolut are cheaper - but they feel 
foreign, offer no Bulgarian-language support, and were never designed 
for someone who learned to bank at a physical branch.

The result: people avoid digital payments entirely, pay utility bills 
in cash to dodge fees, and check their balance every other day out 
of anxiety - not habit.

**BulPay** is a digital wallet built to close that gap.
📄 *See:* [01_Experimentation/Competitor_Analysis](01_Experimentation)

---

## Finding the Opportunity

The idea came to me from a real moment: helping my uncle and aunt (both ~50 years old, 
not particularly tech-savvy) set up a Revolut account. I watched them 
struggle with steps I considered obvious - KYC, first transfer, basic 
navigation. They were confused and frustrated, close to giving up until I helped.

That observation became a question: are they an exception, or a pattern?

I spent several weeks reviewing both local bank apps and foreign 
alternatives (e.g. Revolut, Wise, etc.). I paid close attention to the user behavior in this demographic 
and I came to the conclusion that this was a pattern. No payment services app was meaningfully designed 
for this segment.

To pressure-test this before building anything, I used the **MVP 
Experiment Canvas by Bram Kanstein** to sharpen my customer segment, 
value proposition, and riskiest assumption. I went through several 
feedback iterations with my mentor before I had answers I could defend.

📄 *See:* [01_Experimentation/MVP_Experiment_Canvas](01_Experimentation)

---

## Talking to Users Before Building

I interviewed **10 people** matching my target profile using the  
**Mom Test** framework - focusing on real behaviours and pain points, not 
opinions about my idea.

**What I assumed going in:** this segment would prioritize simple UI, 
fast payments, and the psychological safety of a Bulgarian-branded app 
with easy to reach local support.

**What the interviews revealed:** my assumptions held except for one. Speed 
was not among the core frustrations of my targeted audience. **But Fees and Anxiety were.** 
Users  feel stressed and confused when dealing with digital payments, and they highly dislike local bank's high fees. Speed matters for them, but it's not the biggest priority.

This shifted BulPay's core promise from *"simple fast payments"* to 
**"simple, stress-free payments."**

Once I completed the interviews I gathered all my insights to define the patterns and similarities among my target audience.
This led me to create my User Persona: George, a 53-years old cashier 
from Sofia - who grounds every design decision that followed.

📄 *See:* `01_experimentation/user-persona.pdf`

---

## Designing and Prototyping the MVP

With a validated direction, I narrowed the MVP to one core flow: 
**sending money.** Not budgeting, not investing - just the most 
fundamental wallet action, done simply and with enough signals of confirmation 
to make George feel safe.

I moved through two design phases:

- **Lo-fi wireframes in Balsamiq** — mapped the core flow and logic at first, then added a few extra screens such as login and "add new card" functionality to give the prototype a more complete look.
- **Hi-fi wireframes in Figma** — here I focused on design mentality, thinking about the font size (bigger is better)
clear button labels with no jargon, clear confirmation screens, and a choice of colors that feel trustworthy rather than flashy.

I then used **Cursor AI** to turn the designs into a clickable 
prototype. It does not process real transactions but replicates the 
full send-money experience with enough fidelity to generate genuine user reactions.

📁 *See:* [02_Design](02_Design/) · [03_Prototype](03_Prototype/)

---

## Hypotheses I Am Testing

I defined four hypotheses before running moderated usability tests 
with 6 participants from my target segment:

**H1 - Core Flow Simplicity:** At least 5/6 participants will complete 
"Send €15 to a saved recipient" beginning from login screen and ending at “Successful transfer” screen 
without moderator assistance in ≤ 3 minutes.

**H2 - Home Screen Clarity:** At least 5/6 participants will tap the correct entry point to start 
a transfer from the Home screen within 15 seconds, without exploring more 
than 1 unrelated feature (e.g. tapping on “Add card,” or “Help/Settings”)

**H3 - Trustworthiness:** After finishing the transfer, at least 5/6 participants will rate confidence 
that the money was sent at ≥ 5/7 and can identify at least two confirmation cues from the UI 
(e.g., “Successful transfer” message, green tick, receipt details, transaction reference).

**H4 - Security:** At least 5/6 participants will rate their feeling of safety at ≥ 5/7,  
and fewer than 2 participants will question or resist the additional PIN confirmation step.

📄 *See:* [04_Usability_Research](04_Usability_Research/) · [Usability_Research.md](04_Usability_Research/Usability_Research.md)

---

## Building a Success Metrics Dashboard

With the usability research complete, I shifted focus to answering a harder question: **if this product were live, how would I know it was working?**

I started by identifying the **North Star Metric (NSM)**: the single number that best captures whether BulPay is delivering real value to its users. For BulPay, that is **transactions completed per active user per month** — because a user who keeps sending money is a user who trusts the product. All other metrics were evaluated in relation to how well they predict or explain movement in the NSM.

From there I synthesised a longlist of candidate metrics across acquisition, engagement, retention, payment quality, and financial performance — then cut it down to a **prioritised top-20 list**, grouping them into five measurement zones:

- **Zone 1 — Health Pulse:** NSM, Monthly Active Users (MAU), and D30 retention — the three metrics that tell you whether the product is fundamentally working.
- **Zone 2 — Financial Performance:** Gross Merchandise Volume (GMV), Average Transaction Value (ATV), cost per transaction, and wallet balance trends.
- **Zone 3 — User Behaviour:** session heatmap by day and hour, payment frequency distribution, and time-to-first-payment histogram.
- **Zone 4 — Payment Flow & Quality:** a step-by-step conversion funnel, time-to-complete distribution, PIN attempt trends, and technical success rate.
- **Zone 5 — Card Ecosystem:** cards linked per user and payment source switch rate — a proxy for how deeply users embed BulPay into their financial habits.

I then built a **single-page interactive HTML dashboard** using Chart.js and PapaParse, backed by two synthetic CSV files (50 users, 466 sessions across Jan–Mar 2026) that simulate a realistic early-growth curve. The dashboard computes every metric programmatically from the raw data — no hardcoded values. A global 7D / 30D / 90D filter re-slices all financial metrics dynamically, while cohort-level health metrics (NSM, MAU, D30) remain pinned to their full-period values to avoid misleading short-window reads.

The visual design uses the **exact same color tokens and typography as the BulPay prototype** — a deliberate signal that the dashboard and the product are one coherent system, not two separate artefacts.

📁 *See:* [05_Success_Metrics_Dashboard](05_Success_Metrics_Dashboard/)

---

## Reflections (project is still in progress so this section is only partially-complete)

This project taught me that the best product insights rarely come from 
a whiteboard. They come from paying attention to the people around you 
and being empathetic for their struggles.

The structured process of working through the experiment canvas, interviews, user persona, wireframes, 
prototype, usability testing - taught me how to take a raw observation and turn 
it into a testable and defensible MVP. It also challenged my original assumptions and my prototype hypotheses: I thought speed was a top priority... I also thought my original home screen was easy to use... but based on user feedback I quickly adapted and adjusted my work to deliver a more polished product.

---

