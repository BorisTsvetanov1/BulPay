# BulPay - A Digital Wallet for Tech-Shy Adults in Bulgaria

> A product management case study covering problem definition, market discovery, user 
> research, experiment design, prototyping, and usability testing.  
> **Status:** Usability testing in progress.

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

I interviewed **5 people** matching my target profile using the 
**Mom Test** framework - focusing on real behaviours and pain point, not 
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

📁 *See:* `02_design/` - `04_prototype/prototype-link.md`

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

> ⚠️ *Testing in progress — results will be added here upon completion.*

📄 *See:* `05_user-testing/hypotheses.md` and `05_user-testing/insights.md`

---

## What I Would Do Next

- Iterate the prototype based on usability test findings
- Test whether a visible **fee comparison** ("You saved X vs. your 
  local bank") meaningfully increases trust - directly targeting 
  the primary pain point from interviews.
- Define the activation metric that would justify moving from 
  prototype to build

---

## Reflections

This project taught me that the best product insights rarely come from 
a whiteboard. They come from paying attention to the people around you 
and being empathetic for their struggles.

The structured process of working through the experiment canvas, interviews, user persona, wireframes, 
prototype, usability testing - taught me how to take a raw observation and turn 
it into a testable and defensible MVP. It also challenged my original assumptions and my prototype hypotheses: I thought speed was a top priority... I also thought my original home screen was easy to use... but based on user feedback I quickly adapted and adjusted my work to deliver a more polished product.

---
