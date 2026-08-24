---
name: audio-to-article
description: >-
  Turns one audio recording (interview, talk, working session) into a publish-ready
  English thought-leadership article, following SEO + GEO + engagement/conversion best
  practices (FAQPage schema, citable stats, CTAs), then self-refines the draft via a
  clean-context Critic subagent until it passes a six-gate quality rubric (no AI slop).
  The article reads as original thought-leadership in the author's voice, grounded in their
  experience, not a transcript recap. Ends with a Retro that feeds failure
  patterns back into the rubric. Reads a transcript from input/<slug>/transcript.txt
  (produce one with the transcribe-audio skill, or bring your own). Author identity,
  voice, links, and style come from config/brand.yaml. Agent definitions live in
  agents/*.md; this skill is the workflow entrypoint.
---

# Audio → article (skill)

This file is the **skill**: **when** to use it, **what** to read globally, and **in
what order** to apply roles. Full role prompts live in **[agents/](../../../agents/)**.

The engine takes a transcript and produces a standalone article that stands on its own
ideas. The source is **raw material, never the subject**. The finished piece reads as
original thought-leadership in the author's voice, presented directly or as a conversation
they had, not a recap of what was said.

| Step | Agent definition |
|------|-------------------|
| 0 (prereq) | a transcript at `input/<slug>/transcript.txt` — via [transcribe-audio](../transcribe-audio/SKILL.md) or your own |
| 1 | [agents/curator.md](../../../agents/curator.md) |
| 2 | [agents/seo-brief.md](../../../agents/seo-brief.md) |
| 3 | [agents/writer.md](../../../agents/writer.md) |
| 4 (loop) | [agents/critic.md](../../../agents/critic.md) |

## When to use

- The user wants an **English thought-leadership article** built from a recording they
  have (or a transcript of one).

## Must read first (all steps)

1. [config/brand.yaml](../../../config/brand.yaml) — author/publisher identity, voice,
   links, style, currency, banned words. (If only `brand.example.yaml` exists, tell the
   user to copy it to `brand.yaml` and edit; you may run on the example to demo.)
2. [knowledge/article-playbook.md](../../../knowledge/article-playbook.md) — the SEO/GEO
   recipe, engagement & conversion recipe, anti-slop rules, frontmatter + schema, the rubric.
3. [knowledge/eval-learnings.seed.md](../../../knowledge/eval-learnings.seed.md) — accumulated
   failure patterns; the Writer avoids them, the Critic checks every `active` one, the Retro
   appends new ones. (On first run, copy the seed to `knowledge/eval-learnings.md` and append there.)

## Pipeline (order)

Fully autonomous **after** the transcript is in place — one human checkpoint on the
angle, then run to completion.

0. **Prereq:** confirm `input/<slug>/transcript.txt` exists. If not, run
   [transcribe-audio](../transcribe-audio/SKILL.md) or ask the user for a transcript.
1. **Curator** — read `input/<slug>/transcript.txt` → `source-digest.md`. Never read media.
2. **SEO brief** — buyer-intent English brief → `brief.md`. **Confirm the angle with the
   user** before writing (the one checkpoint).
3. **Writer** — `article.en.md`.
4. **Critic loop (fresh eyes)** — spawn the Critic as a **clean-context subagent** (Agent
   tool, [critic.md](../../../agents/critic.md) as its prompt) that reads only the on-disk
   artifacts (`article.en.md`, `brief.md`, `source-digest.md`, playbook, learnings file) —
   never the Writer's conversation. It scores the six gates, checks every `active` pattern in
   the learnings file, applies the forced-find rule before any all-PASS → `review-log.md`;
   the Writer revises; repeat until **it passes or 4 iterations**.
5. **Retro** — after finalize: append every gate failure, near-miss, and user correction from
   the run to `knowledge/eval-learnings.md` (increment `Occurrences` on repeats); add a
   **"Retro"** block to `review-log.md`. Any pattern at **≥2 occurrences**: propose a playbook
   edit in the run summary. Then present the article.

## Scope

- **Thought-leadership**, not a recap. **Sources generalized** (no direct quotes / full
  names — refer to role + company-type). **No fabricated** metrics/quotes/client names
  (`[NEED: ...]` for gaps).
- **Delivers markdown files in `output/`** — no writing to a live site.
- **Original voice.** The article presents ideas as the author's own perspective or a
  conversation they had, with no meta-references to the raw material in the body or
  frontmatter (see the Writer's framing rules and Critic gate 5).

## Output (files on disk)

Write to **`output/<YYYY-MM-DD_slug>/`**:

`source-digest.md` → `brief.md` → `article.en.md` + `review-log.md`.

## Optional QA

If you have the `claude-seo` plugin (or similar), point its content/GEO check at
`article.en.md` for an independent compliance read.
