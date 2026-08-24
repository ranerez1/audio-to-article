# Audio → article playbook (SEO + GEO)

The durable spec for turning one audio recording into a publishable **thought-leadership
article**. Read every run. Identity, voice, links, and style come from
[`config/brand.yaml`](../config/brand.yaml); this file is the source-agnostic recipe.

---

## What we're making

A **standalone article that stands on its own ideas** — the author's field-tested take,
grounded in the source's tactics and outcomes. **Not** a recap or transcript write-up. The
source is raw material, not the subject.

- The article targets **buyer intent** for the author's audience (defined by `config/brand.yaml`).
  It lives at `<site.blog_path>/<slug>`.

**Sources are generalized:** no direct quotes, no full names. Reference the insight ("a VP of
Product I spoke with described…"), not the person. Real numbers only if attributable; otherwise
`[NEED: verify]`. This also keeps the source anonymous.

**Currency.** Name every business/monetary value in `style.target_currency` (config; default USD).
Convert non-target source amounts to an approximate, clearly-round figure and use it consistently
on every mention. Don't stack "≈"/"about" clutter on an illustrative figure; a round amount reads
as the approximation.

**Original voice, no meta-references.** The article reads as the author's own field experience,
framed directly or as a conversation they had: "I sat down with…", "a VP of Product I spoke
with…". Keep meta-references to the raw material out of the prose: don't narrate where the ideas
came from or how the piece was produced ("in the transcript", "as my interviewee put it", a link
back to the source), and don't add a source-pointing frontmatter field. The source is **internal
raw material only** — it may appear in the digest and brief, never in the article body or its
visible framing. A reader should get the ideas as the author's thinking, not a play-by-play of the
sourcing.

**Timeless framing (no recency words).** Articles may publish weeks-to-months after they're
written, so nothing in the prose may claim freshness it won't have. **Banned in the body:**
*recently, today, currently, this week / month / year / quarter, lately, right now, nowadays,
latest, newest, "the new wave of"* (and any bare year used as "now"). Any genuinely time-bound
claim takes an **absolute** anchor ("as of early 2026"), never a relative one. The piece must
read identically whether it ships next week or next year.

---

## SEO recipe

The article must hit all of these:

- **One clear H1** containing the primary keyword.
- **Primary keyword** in: title tag, H1, first 100 words, and ≥1 H2.
- **Meta description:** 140–160 chars, specific, benefit-led.
- **Slug:** short, hyphenated, keyword-bearing, under `site.blog_path`.
- **≥3 extractable, question-shaped H2/H3** (e.g. "How do you know a feature is worth killing?").
  Each answered in its **first 1–2 sentences** underneath (GEO passage).
- **Internal links:** ≥1 to the conversion target (`conversion.cta_url`) + ≥1 secondary
  (`conversion.secondary_link` or a related guide). Anchor text descriptive, not "click here."
- **Length:** within `style.word_count` (default 900–1500). Depth over padding.
- **Schema:** `Article` (+ `BreadcrumbList`) JSON-LD, with `inLanguage` (template below).
- **No meta-reference or source link in the body or schema.** The article doesn't narrate or link
  its raw material — no back-link to the source, no source-pointing frontmatter field.

## GEO recipe (AI Overviews / ChatGPT / Perplexity)

The article's job is to be **citable**:

- **≥1 specific, attributed, citable stat** — a concrete number tied to a real outcome or a named
  public source. Never fabricate; flag gaps with `[NEED: verify]`.
- **Every cited study/research finding carries an inline link** (hard requirement) — any stat,
  experiment, or named effect attributed to research or a public source must link to that source
  in the body. Record the URL in `source-digest.md` when you pick the stat and verify it resolves.
- **Citable stat sentences:** every key stat lives in **one self-contained sentence** that carries
  subject + context + attribution (source still generalized), liftable without the surrounding
  paragraph. "In one eight-week zero-to-one at a sales-intelligence SaaS, the team reported 93%
  accuracy" lifts; "They hit 93%" doesn't.
- **Extractable answers:** every H2/H3 states its answer up front, in a self-contained sentence an
  LLM can lift.
- **A "Key takeaways" or short FAQ block** (3–5 bullets/Q&As) near the top or bottom, **mirrored
  into `FAQPage` JSON-LD** (template below).
- **Named concept (when the source supports one):** if the source genuinely coins a rule or
  framing, give it a name once and reuse it — LLMs cite named ideas. **Never fabricate** a concept
  the source doesn't support; skip rather than force.
- **≥1 structured element** — numbered steps or a small table — where the content is naturally
  list- or comparison-shaped. Don't bolt one on.
- **Entity clarity:** name the author and publisher (from `config/brand.yaml`) where natural; tie
  claims to real experience (`author.credibility`) — this is the E-E-A-T competitors can't fake.
  The `author` schema carries the machine-readable version (`jobTitle`, `knowsAbout`, `sameAs`).

## Engagement & conversion recipe

SEO gets the reader to the page; this keeps them on it and gives them somewhere to go:

- **Hook:** the first two sentences name the reader's situation and stakes, or make a sharp claim.
  No throat-clearing, no "in this article we'll…".
- **So-what per section:** every H2 states the implication for the reader — what to do or stop
  doing — not just case narration.
- **Actionable payoff:** the reader leaves with ≥1 thing they could run next week.
- **Skim path:** headers + bolded lines + the takeaways block alone must tell the whole argument.
- **One primary conversion goal** per article (`conversion.primary_offer`), chosen in the brief.
- **One contextual mid-article CTA:** a natural sentence tied to the pain just described, linking
  the conversion target. Not banner-speak, not "click here."
- **One closing CTA with a concrete next step:** the last paragraph tells the reader what to do
  next (via `conversion.cta_url`). A secondary link may accompany it.
- **Max 2 CTAs total.** More reads as selling, which kills the thought-leadership frame.

---

## Anti-AI-slop checklist

Zero tolerance. Fail the gate if any cluster appears. **Canonical pattern catalog:** the
[`no-ai-slop`](../.claude/skills/no-ai-slop/SKILL.md) skill — the Critic runs it in **detect mode**
(name each pattern, quote the offending line). The bullets below are the local layer on top of it.

- **Banned words (hard fail):** the `style.banned_words` list in `config/brand.yaml`. (The skill's
  broader words-to-cut list is an **additional flag layer**, not a second hard-fail set.)
- **Em-dashes (hard fail):** no `—` as connective punctuation. It's the single most recognizable AI
  tell. Rewrite with a period, comma, colon, or parentheses. (Hyphens in compounds are fine.)
- **Named patterns to scan (from the skill), each hit = quoted line + fix:** binary contrasts,
  throat-clearing openers, faux-insight setups, colon reveals, superficial `-ing` analysis,
  importance puffery, weasel attribution, fake-strong verbs, synonym cycling, negative listing,
  dramatic fragmentation, robotic rhythm, rhetorical setups, fake-profound kickers, summary-recap
  endings, formatting slop.
- **Rhythm:** vary sentence and paragraph length. No wall of same-length paragraphs.
- **Concreteness:** at most **one** sentence in the whole piece could apply to any company unedited.
  Every other sentence needs a specific anchor: a number, a named method, a real scenario.
- **Voice:** per `voice.summary` in config — direct, evidence-based, active voice, lead with the
  recommendation. Sounds like the author talking, not a content mill.

---

## Frontmatter + schema template

`article.en.md` opens with YAML frontmatter, then the body. Fill every field; leave gaps as
`[NEED: ...]`. Values in ALL-CAPS come from `config/brand.yaml`.

```yaml
---
title: "<title tag, keyword-bearing, ~60 chars>"
description: "<meta description, 140–160 chars>"
slug: "<SITE.BLOG_PATH>/<slug>"
lang: en
primary_keyword: "<keyword>"
date: YYYY-MM-DD
---
```

JSON-LD to embed at the end of the body (inside `<script type="application/ld+json">` tags, not
markdown fences) — `Article`, `BreadcrumbList`, and `FAQPage`:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "<H1>",
  "inLanguage": "en",
  "author": {
    "@type": "Person",
    "name": "<AUTHOR.NAME>",
    "url": "<AUTHOR.URL>",
    "jobTitle": "<AUTHOR.JOB_TITLE>",
    "knowsAbout": ["<AUTHOR.KNOWS_ABOUT ...>"],
    "sameAs": ["<AUTHOR.SAME_AS ...>"]
  },
  "publisher": { "@type": "Organization", "name": "<PUBLISHER.NAME>", "url": "<PUBLISHER.URL>" },
  "datePublished": "YYYY-MM-DD",
  "mainEntityOfPage": "<SITE.BASE_URL><SITE.BLOG_PATH>/<slug>"
}
```

`FAQPage` mirrors the article's FAQ/takeaways block (3–5 Q&As, answers ≤2 sentences each). Each
`Question.name` must match its on-page H2 verbatim.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "<question, ideally one of the H2s>",
      "acceptedAnswer": { "@type": "Answer", "text": "<the answer's first 1–2 sentences>" }
    }
  ]
}
```

---

## Coherence & storytelling gate

An article can pass SEO and anti-slop and still be bad: examples that only make sense to someone who saw
the source, ideas that don't connect, a narrative that doesn't hold. Every version must pass:

- **Self-contained examples.** A reader who never saw the source understands every example
  without extra context. If a story needs the source to make sense, give it a one-line
  standalone setup or cut it.
- **One spine.** The piece follows a single through-line; each H2 advances it. No orphaned tangents.
- **Earned transitions.** Each section connects to the last; a reader follows top to bottom without
  backtracking.
- **The lead pays off.** Whatever tension the intro sets up, the body resolves.
- **Setup before payoff.** Every dramatic turn (a failure, reversal, "but it still…", or surprising
  number) needs the stakes established in the 1–2 sentences before it, or the payoff isn't earned.
  Also: one job per paragraph, and any "N levers/things/steps" promise must signpost where each is
  delivered.
- **Sentence-level integrity.** Read each sentence on its own, aloud. Every one must be complete,
  grammatical, and keep the contrast it implies. Compressions of the source are the usual culprit:
  when you squeeze a digest line into a shorter parallel, don't drop the half that carries the
  meaning. If a sentence can't be read aloud cleanly, rewrite it.

---

## The rubric (Critic): six gates

The article is **done** only when it passes all six gates. Per-role detail in
[`agents/critic.md`](../agents/critic.md).

1. **SEO gate** — the SEO recipe above, all items.
2. **GEO gate** — the GEO recipe above, all items (incl. `FAQPage` JSON-LD, rich author entity,
   citable stat sentences, structured element, and an inline link on every cited research finding).
3. **Anti-slop gate** — the anti-slop checklist (incl. em-dash + banned-word hard fails).
4. **Coherence & storytelling gate** — self-contained examples, one spine, earned transitions,
   setup before payoff, sentence-level integrity.
5. **Voice/fact gate** — the author's voice; no fabricated metrics/quotes/client names; sources
   generalized; **original voice with no meta-references** to the raw material in the body or
   frontmatter (present ideas directly or as a conversation; no "in the transcript", "my
   interviewee", or a link back to the source); currency in the target currency; timeless framing.
6. **Engagement & conversion gate** — the Engagement & conversion recipe above, all items.

Loop Writer ⇄ Critic until the article passes, or 4 iterations (then finalize the best draft and
list failing gates at the top of `review-log.md`).

The Critic runs **fresh-eyes**: a clean-context subagent that reads only the on-disk artifacts,
never the Writer's conversation. Before any PASS verdict it must name the 3 strongest candidate
weaknesses it considered and why each doesn't fail.

## Self-improving evaluation (the learnings loop)

The rubric is not static. Every run feeds it:

- **[`eval-learnings.md`](eval-learnings.seed.md)** is the accumulating failure-pattern base: dated
  entries with the pattern, the failing text, a detection rule, and a status (`active` |
  `promoted-to-playbook`). The **Critic reads it every run** and explicitly checks each `active`
  pattern. (On first run, copy `eval-learnings.seed.md` to `eval-learnings.md` and append there.)
- **Retro step (end of every run):** append every gate failure, near-miss, and user correction from
  the session. Record a "Retro" block in `review-log.md`.
- **Promotion rule:** a pattern seen in **≥2 runs** gets proposed (in the run summary) as a permanent
  playbook/gate edit. Promoted entries stay in the learnings file with status `promoted-to-playbook`
  so the history is auditable.
