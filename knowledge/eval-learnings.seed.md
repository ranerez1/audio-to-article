# Article eval learnings (self-improving rubric) — seed

The accumulating failure-pattern base for the audio→article pipeline. The **Critic reads this
file every run** and explicitly checks each `active` pattern against the draft. The **Retro step**
(end of every run) appends new entries. A pattern seen in **≥2 runs** is proposed for promotion
into [`article-playbook.md`](article-playbook.md); promoted entries keep status
`promoted-to-playbook` for the audit trail.

> This is a **seed**. On first run, copy it to `eval-learnings.md` and append your own runs
> there. The entries below are generalized detection rules distilled from real runs — no names,
> no private content. They are the patterns that most often slip past a first read.

**Entry format** — copy this template:

```markdown
## YYYY-MM-DD — <pattern-name> · status: active
- **Run:** <output/ folder>
- **Pattern:** <one sentence: what went wrong>
- **Failing text:** "<the exact offending text>"
- **Detection rule:** <what the Critic should do to catch it next time>
- **Occurrences:** 1
```

On a repeat occurrence, increment **Occurrences** and add the new run + failing text to the same
entry (don't duplicate patterns).

---

## seed — meta-reference to the raw material · status: active
- **Pattern:** The article narrated its own sourcing instead of presenting the idea directly,
  positioning the piece as a recap rather than original thought-leadership. Also seen: a
  source-pointing frontmatter field, and the bare word "guest" (a conversation has no "guest").
- **Failing text:** e.g. "as my interviewee put it…"; "in the transcript I…"; a frontmatter field
  linking back to the raw source; "The guest's own summary of the lesson has stayed with me."
- **Detection rule:** the article should read as the author's own perspective or a conversation
  ("I sat down with…"). Grep the draft (body + frontmatter, case-insensitive) for meta-references
  to the raw material: `transcript|recording|my guest|guest|interviewee|as I (said|mentioned) (earlier|above)|in our (chat|conversation)`
  and any source-pointing frontmatter field. Any hit that narrates the sourcing is a Voice/Fact
  FAIL. Watch for the standalone word "guest" specifically.
- **Occurrences:** 1

## seed — compression drops the load-bearing half · status: active
- **Pattern:** Compressing a source line into a shorter parallel construction dropped the half that
  carried the meaning, leaving a sentence that doesn't parse. Same-context review tends to miss it;
  a fresh-eyes read catches it — which is why the Critic runs as a clean-context subagent.
- **Failing text:** "Too few and you recreate silos. The whole company and the room stops being
  productive." (source: "not the whole company — that kills productivity — not a tiny siloed group").
- **Detection rule:** read every sentence in isolation, aloud; any parallel/compressed construction
  must keep the contrast it implies and have a working subject-verb. Quote and FAIL anything that
  doesn't parse.
- **Occurrences:** 1

## seed — stat-unit drift (right number, wrong denominator) · status: active
- **Pattern:** A source stat kept its number but swapped its unit/denominator, so the claim was no
  longer traceable to the fact base. A matching number with a different unit reads as fine but is
  fabricated.
- **Failing text:** "people averaged 11.7 messages per session" when the source says 11.7 messages
  **per user**.
- **Detection rule:** when cross-checking numbers against `source-digest.md`, verify the
  **unit/denominator and timeframe**, not just the number. A matching number with a different unit
  is a Voice/Fact FAIL.
- **Occurrences:** 1

## seed — schema block format drift (fences / missing BreadcrumbList) · status: active
- **Pattern:** JSON-LD emitted inside markdown ```json fences instead of
  `<script type="application/ld+json">` tags, and/or `BreadcrumbList` dropped. Fenced JSON renders
  as visible code on the page and is not parsed as structured data.
- **Failing text:** the article ended with a single fenced `Article` object; no `BreadcrumbList`,
  no script tags.
- **Detection rule:** grep for `application/ld+json` (must appear per schema block) and for
  ```` ```json ```` near the file end (must not); confirm `Article`, `BreadcrumbList`, and `FAQPage`
  all present and parseable.
- **Occurrences:** 1

## seed — primary keyword absent from every H2 · status: active
- **Pattern:** The primary keyword was in title + H1 + first 100 words but in **no H2**, failing the
  SEO gate's "keyword in ≥1 H2." Also exposes a sub-check: the on-page H2 and its FAQPage-mirror
  question drifted to different wordings.
- **Failing text:** primary_keyword present everywhere except the five H2s, none containing it.
- **Detection rule:** grep every H2/H3 for the `primary_keyword` (or a clear morphological form);
  ≥1 must contain it. Then confirm each FAQPage `name` matches its on-page H2 verbatim.
- **Occurrences:** 1

## seed — cold dramatic turn (payoff with no setup) · status: active
- **Pattern:** A reversal or surprising number landed without its stakes established in the prior
  1–2 sentences, so the passage reads as "missing context."
- **Failing text:** "Their agent was roughly twice as accurate as the market leader. A month into a
  large pilot, the customer aggressively switched it off." — the reversal landed cold.
- **Detection rule:** for every dramatic turn (failure/reversal/"but it still…"/surprising number),
  confirm the 1–2 sentences before it set up the stakes. If not, FAIL Coherence and quote the cold
  turn.
- **Occurrences:** 1

## seed — templated opener across consecutive articles · status: active
- **Pattern:** Nearly every article opened with the same "I sat down with a [role] at a [company]"
  construction — a detectable template even though each instance is fine on its own.
- **Failing text:** three consecutive drafts all opening "I sat down with a [role] at a [company]…".
- **Detection rule:** check the opener against recent runs; rotate the framing (see the Writer's
  opener menu) so no two consecutive articles match.
- **Occurrences:** 1
