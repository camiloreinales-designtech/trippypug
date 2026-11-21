---
name: ideacleaner
description: Turn a messy brain dump of an idea into a clear, technical project brief. Reads the dump, asks as many rounds of targeted questions as needed to fill in the technical gaps, then writes a structured spec. Use when the user types /ideacleaner or asks to clean up, flesh out, or spec out a rough idea.
---

# Idea Cleaner

Take a rough brain dump and turn it into a brief someone could start building from.
The value is in the questions: find what is missing or vague, and ask until it is pinned down.

## 1. Get the brain dump

- If the user passed text with the command, that is the brain dump.
- If not, ask them to paste or type it: "Dump the idea, however messy it is." Wait for it.
- Read all of it. Don't correct or judge yet.

## 2. Play it back

In 3–5 short lines, say what you think the idea is:
- **What it is**, in one sentence
- **Who it's for**
- **The main thing it does**
- **What's still unclear** (a short list)

Use the user's own words where you can. If you got the core idea wrong, the questions will be wrong too, so let them correct you here.

## 3. Find the gaps

Check the dump against these areas. Mark each one **known**, **vague**, or **missing**:

| Area | What you need to know |
|---|---|
| Problem & goal | What pain it solves, why now, what "done" looks like |
| Users | Who uses it, how many, how technical they are, single vs. multi-user |
| Core features | The 3–5 must-haves vs. nice-to-haves |
| Platform | Web, mobile, desktop, CLI, hardware, physical product, service |
| Tech stack | Languages, frameworks, hosting, existing code or tools to reuse |
| Data | What gets stored, where it comes from, how sensitive it is, rough volume |
| Integrations | APIs, payment, auth, third-party services, devices |
| Constraints | Budget, deadline, team size and skills, legal or compliance |
| Scale & performance | Expected load, latency needs, offline needs |
| Monetization | Free, paid, subscription, internal tool, none |
| Success metrics | How you'll know it works |
| Risks | The hardest or least certain part |

Not every area applies. A painting series doesn't need a tech stack, and a weekend script doesn't need monetization. Skip the areas that don't fit.

## 4. Ask questions in rounds

Use the **AskUserQuestion** tool so the user can click answers.

- **Up to 4 questions per round.** Ask the ones with the biggest effect on the design first, like platform, users, and core features, before details.
- **Give 2–4 concrete options per question,** based on what the dump suggests. Put the option you'd pick first and mark it "(Recommended)" when you have a real reason. The user can always type "Other."
- **Write each question so it stands on its own,** naming the feature or part it's about.
- **Don't ask what the dump already answers.**
- **After each round, reassess.** Answers often raise new questions. For example, "multi-user" leads to auth, roles, and sync. Follow those threads.
- **Keep going as long as it's needed.** Stop only when every relevant area is known, or the user has said "don't know" or "you decide" for it. Before each new round, add one line in chat about what you're digging into next.
- If the user says "enough," "just write it," or similar, stop asking and go to step 5. List whatever is still open under Open questions.
- When the user says "you decide," make a sensible call and label it **Assumption** in the brief.

## 5. Write the cleaned brief

Write it in chat as markdown, using this structure. Leave out sections that don't apply.

```
# <Project name>  (suggest one if the user didn't give one)

**One-liner:** <what it is, for whom, in one sentence>

## Problem
## Users
## Goals & success metrics
## Scope
### MVP (must-have)
### Later (nice-to-have)
### Out of scope
## Technical approach
- Platform:
- Stack:
- Hosting / infra:
- Data model (key entities and fields):
- Integrations:
- Architecture sketch (components and how they talk; short text or ASCII diagram)
## Constraints
## Risks & unknowns
## Assumptions  (things you decided on the user's behalf)
## Open questions
## Suggested next steps  (3–5 concrete first actions, in order)
```

Keep it tight. Use bullets, not paragraphs, and use the user's terms.

## 6. Offer follow-ups

End with one line offering to:
- save the brief as a file (for example `ideas/<slug>.md` in the current repo), or
- start building the first next step.

Don't start building or create files unless the user asks.
