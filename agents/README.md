# Agent definitions

These files define **each role** (inputs, outputs, must-read knowledge, handoffs) for turning
one audio recording into an English thought-leadership article. Author identity, voice, links,
and style all come from [`config/brand.yaml`](../config/brand.yaml) — the roles read it, they
don't hardcode a brand.

**Orchestration** (when to run, global must-reads, step order) lives in the **skill**, not here:

- **Transcribe audio:** [.claude/skills/transcribe-audio/SKILL.md](../.claude/skills/transcribe-audio/SKILL.md)
- **Produce an article:** [.claude/skills/audio-to-article/SKILL.md](../.claude/skills/audio-to-article/SKILL.md)

Use the skill when you want a single request to flow transcript → Curator → SEO brief → Writer ⇄
Critic. Use an **individual agent file** when you only need that role.

| Agent | Definition |
|-------|------------|
| [curator.md](curator.md) | Transcript → token-efficient English digest (source generalized) |
| [seo-brief.md](seo-brief.md) | Digest → SEO/GEO brief (keyword, outline, schema plan) |
| [writer.md](writer.md) | Brief → English draft, in the author's voice, source hidden |
| [critic.md](critic.md) | Draft → six-gate score + fixes; runs as a **clean-context subagent** with a forced-find rule; drives the refine loop |

Supporting corpus: [knowledge/article-playbook.md](../knowledge/article-playbook.md) + the
self-improving failure-pattern base [knowledge/eval-learnings.md](../knowledge/eval-learnings.seed.md)
(the Critic checks every `active` pattern; the skill's Retro step appends new ones each run).

**File output:** each run uses a folder under `output/` (`source-digest.md` → `brief.md` →
`article.en.md` + `review-log.md`). Transcripts live under `input/<slug>/transcript.txt`.
