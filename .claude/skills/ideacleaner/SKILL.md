---
name: ideacleaner
description: Turn a messy brain dump of an idea into a clean, buildable spec. Reads the dump, asks as many rounds of targeted technical questions as needed to fill the gaps, then writes a structured idea brief. Use when the user types /ideacleaner or pastes a rough idea and wants it cleaned up and made concrete.
---

# /ideacleaner: brain dump to clean spec

Goal: take whatever the user dumped (rambling, half sentences, voice-note style) and end with a
clear, technical brief someone could start building from. The questions are what makes this
work. Keep asking until the important unknowns are settled, not just a fixed handful.

## 1. Get the brain dump
- If the user passed text with the command (`/ideacleaner <text>`) or pasted it, use that.
- If they pointed at a file, read it.
- If there is nothing yet, ask them to dump the idea in one message, as messy as they like, and stop
  until they reply. Do not start asking structured questions on an empty dump.

## 2. Read it back in one tight paragraph
Before asking anything, play back what you understood in 3 to 5 sentences:
- What it is, who it is for, the core problem it solves.
- Then a short list: **Clear** (what the dump already settles) and **Unknown** (gaps you spotted).

Do not ask the user to confirm this. Go straight to questions; they can correct you in their answers.

## 3. Ask questions in rounds
Use the `AskUserQuestion` tool (up to 4 questions per call). If it is not available, ask in chat
as a numbered list of at most 4 and wait.

Rules:
- Every question must be specific to *this* idea. No generic filler. Offer 2 to 4 concrete options
  drawn from what is realistic for the idea, with a one-line tradeoff each. Put your recommended
  option first and mark it "(Recommended)" when you have a real reason to.
- Use `multiSelect: true` when choices are not exclusive (features, platforms, integrations).
- Do not ask what the dump already answered. Do not ask what has a safe default; state the default
  in the brief instead.
- After each round, update your picture of the idea, then decide what is still unknown. Later rounds
  should go deeper based on earlier answers (e.g. "mobile app" leads to offline, push, app store
  questions; "takes payments" leads to provider, pricing model, refunds).
- Stop when every item below is either answered, safely defaulted, or explicitly marked out of scope.
  Typically 2 to 5 rounds. If the user says "enough", "skip" or "just write it", stop immediately and
  list remaining assumptions in the brief.

### Coverage checklist (pick what applies, skip what does not)
**Product**
- Target user and the one main job they hire it for
- Core features for v1 vs later
- Success metric: how they will know it works

**Platform and UX**
- Surface: web, mobile (iOS / Android / both), desktop, CLI, API, browser extension, hardware
- Rough UX: key screens or flows, single user vs multi user, auth needed or not

**Data**
- What data is stored, where it comes from, how much, how sensitive (PII, payments, health)
- Real time needs, offline needs, imports and exports

**Tech stack and integrations**
- Preferred languages and frameworks, or "no preference"
- Hosting: static, serverless, managed platform, self hosted
- Third party services: payments, email, maps, AI / LLM, analytics, auth providers
- Existing systems it must plug into

**Constraints**
- Budget (build and monthly running), timeline, team size and skill level
- Scale expectations (users, requests, storage) at launch and in a year
- Legal or compliance (GDPR, HIPAA, age limits, licensing of content)

**Business (only if relevant)**
- Free, paid, freemium, one time, subscription, ads, internal tool
- Competitors or references the user likes

## 4. Write the clean brief
When questions are done, write a markdown file at `ideas/<short-kebab-slug>.md` in the working
directory (create `ideas/` if needed), then show the user the one-line pitch and the path.

Use this structure, and keep it tight. Bullets over paragraphs.

```markdown
# <Idea name>

**One-liner:** <what it is, for whom, why>

## Problem
## Target users
## Core features (v1)
## Later / nice to have
## Out of scope
## User flow
<numbered steps of the main path>

## Technical shape
- Platform:
- Frontend:
- Backend:
- Data and storage:
- Auth:
- Integrations:
- Hosting:

## Data model (sketch)
<main entities and key fields>

## Constraints
- Budget:
- Timeline:
- Scale:
- Compliance:

## Success metrics
## Risks and open questions
## Assumptions made
<every default you chose without asking, so the user can override>

## Suggested first steps
<3 to 6 concrete next actions, smallest buildable slice first>
```

Rules for the brief:
- Only write what the user said or chose, or what you mark under **Assumptions made**. No invented facts.
- Keep the user's own language for the idea name and features where it is clear.
- Recommend a stack only when they said "no preference", and say why in one line.

## 5. Wrap up
Reply with: the one-liner, the file path, and the 2 or 3 biggest open questions or risks.
Offer to commit it, refine a section, or go deeper on one area. Do not commit unless asked.
