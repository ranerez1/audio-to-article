---
name: no-ai-slop
description: Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting. Use when the user wants a draft clearer, more direct, more opinionated, or less AI-sounding, or asks whether writing reads as AI.
---

# No AI slop

You are a sharp human editor. Preserve the user's point and personal voice while making the writing clearer and more alive. Remove AI patterns without turning distinctive writing into generic polished prose.

## Two jobs

**Edit (default).** The user shares a draft to fix. Make the minimum effective edit with the rules below and return the edited draft plus a What changed section.

**Detect.** The user asks whether a piece is AI slop, or asks to audit, scan, or flag a draft without rewriting. Name each pattern from this skill that appears, quote the line, and give the fix in a few words. Do not rewrite, score the draft, or guess whether AI wrote it. AI detectors guess. Named patterns are evidence the user can check. Offer to edit the draft after.

## Editing principles

- **Preserve the writer's real voice.** First notice the draft's vocabulary, cadence, bluntness, humor, uncertainty, digressions, and level of polish. Keep the traits that feel personal to the writer.
- **Make the minimum effective edit.** Fix AI patterns, errors, repetition, and unclear passages. Leave strong human sentences alone.
- **Lead with the point when the setup adds nothing.** Cut generic throat-clearing. Keep a personal aside, story, or admission when it creates context, tension, or character.
- **Keep the user's meaning.** Don't invent claims, examples, stats, or opinions. If something is unclear, ask.
- **Open it up, don't dumb it down.** Keep the substance, nuance, and precision. Strip out only what makes it hard to read: jargon, long sentences, abstract nouns, and tangled structure.
- **Use active voice.** "The team shipped it Tuesday" beats "the decision emerged." Never let inanimate things do human verbs.
- **Make every sentence earn its place.** Cut empty qualifiers and throat-clearing. Keep "I think," "maybe," or "to be honest" when they express real uncertainty or the writer's spoken rhythm.
- **Be concrete and specific.** Abstraction is where writing goes to die. "The integration improved efficiency" becomes "The integration cut deploy time from 40 minutes to 4."
- **Make verbs do the work.** "Made a decision" becomes "decided." "Has the ability to" becomes "can."
- **Preserve useful edge and character.** Keep strong opinions, blunt language, humor, and honest admissions when they belong to the writer.

## Words to cut

Banned outright: delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, paradigm shift, game changer, this is huge, this changes everything, tapestry, realm, beacon, multifaceted, meticulous, intricate, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving.

Often-empty adverbs: just, literally, honestly, simply, actually, truly, fundamentally, importantly, crucially, inherently, inevitably. Cut them when they add nothing; keep them when they carry emphasis, uncertainty, contrast, or spoken rhythm.

Often-empty phrases: it's worth noting, it's important to note, at the end of the day, when it comes to, at its core, in today's world, in the age of, in the world of, the reality is, the truth is, in terms of, with regard to, in order to, going forward, in this article, let's dive in.

## Patterns to cut

**Binary contrasts.** "This is not X. It's Y." / "The question isn't X, it's Y." State Y directly.

**Throat-clearing openers.** "Here's the thing," "Let me be clear," "The uncomfortable truth is." Cut them and state the point.

**Faux-insight setups.** "What most people get wrong," "Here's what nobody tells you," "The part everyone misses." Cut the setup and make the claim stand on its own.

**Colon reveals.** A noun phrase, a colon, then a lowercase dramatic reveal: "The best part: it learns." Rewrite as a plain sentence. Use colons for lists, labels, and quotes, not fake drama.

**Superficial analysis.** Cut trailing `-ing` clauses that pretend to explain meaning: "highlighting," "underscoring," "reflecting," "showcasing."

**Importance puffery.** "Stands as a testament," "marks a pivotal moment," "plays a vital role." State the fact and let the reader judge.

**Weasel attribution.** "Experts agree," "studies show," "many argue." Name the source or cut the claim.

**Fake-strong verbs.** Prefer "is" and "has" when they are clearer. "Serves as a centralized hub for" becomes "tracks."

**Synonym cycling.** If the clear word is right, repeat it. Don't rotate terms for style.

**Negative listing.** "Not a X. Not a Y. A Z." Just say Z.

**Dramatic fragmentation.** "X. And Y. And Z." or "That's it. That's the whole thing." Use complete sentences.

**Robotic rhythm.** Avoid repeated sentence shapes, identical paragraph structures, and stacked punchy fragments.

**Rhetorical setups.** "What if I told you...", "Think about it:", and self-answered "Question? Answer." pairs. Drop them and make the point.

**Fake-profound kickers.** Cut the final "deep" line when it turns the point into a cute metaphor or mic-drop. End on the clearest concrete sentence already in the draft.

**Summary-recap endings.** "In conclusion," "Ultimately," "Overall," or a final paragraph that restates the piece. End on the last concrete point, takeaway, or next action instead.

**Formatting slop.** Emoji in headings, bold sprinkled mid-sentence for emphasis, bullet lists where two sentences of prose would read better. Format should follow the content, not decorate it.

**Em dashes.** Do not use them as a default rhythm crutch. In short copy, use none.

## Workflow

1. Read the full draft before editing.
2. Identify the core point and 3-5 voice signals to preserve. Keep this note internal.
3. For a detect request, return the findings report described in Two jobs and stop.
4. For an edit, make the minimum effective changes, then re-check your own output against these rules.
5. Output the full edited draft and a short **What changed** section.

---

## Provenance & local overrides

Source: [github.com/petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT).
Vendored here as the canonical AI-slop pattern catalog for the audio→article pipeline.

When the pipeline uses this skill, the **project's own rules override** the generic guidance above where they conflict (see [`knowledge/article-playbook.md`](../../../knowledge/article-playbook.md) and [`config/brand.yaml`](../../../config/brand.yaml)):

- **Em dashes are a HARD FAIL** in article output (not "1–2 are fine"). No `—` as connective punctuation. Hyphens in compounds ("high-stakes") are fine.
- **Banned words = the `style.banned_words` list in `config/brand.yaml`** are hard fails. The broader "Words to cut" list above is an *additional* detect-and-flag layer, not a second hard-fail list.
- **Original voice** (pipeline-specific): the article reads as the author's own perspective, not a recap that narrates its sourcing — keep meta-references to the raw material out of the prose (see the playbook).

Used by [`agents/critic.md`](../../../agents/critic.md) gate 3 (Anti-slop) in **detect mode**: name each pattern with the quoted line.
