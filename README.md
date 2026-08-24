# audio-to-article

Turn one audio recording into a publish-ready, SEO- and GEO-optimized thought-leadership
article — original, in your voice, grounded in your experience, not a transcript recap.

It's an agent pipeline you run in [Claude Code](https://claude.com/claude-code) (or any
Claude-Code-compatible harness): a **Curator** distills the transcript, an **SEO brief** plans
the piece, a **Writer** drafts it in your voice, and a fresh-eyes **Critic** scores it against a
six-gate rubric and loops with the Writer until it passes. Everything that makes the article
*yours* — name, voice, links, style — lives in one config file.

## What you get

- **Audio in, article out.** Transcribe a recording (or bring your own transcript), get an
  `article.en.md` with frontmatter and `Article` + `BreadcrumbList` + `FAQPage` JSON-LD.
- **SEO + GEO built in.** One keyword-bearing H1, extractable question-shaped H2s, one citable
  attributed stat with a source link, a Key-takeaways/FAQ block mirrored into `FAQPage` schema.
- **Anti-AI-slop.** A vendored [no-ai-slop](https://github.com/petergyang/no-ai-slop) catalog plus
  hard fails on em-dashes and your banned words. The Critic runs it in detect mode and quotes every hit.
- **Original voice, not a recap.** A dedicated gate keeps meta-references to the raw material out
  of the prose, so the piece reads as your own perspective — presented directly or as a
  conversation you had — rather than a transcript write-up.
- **Self-improving.** Each run's failures append to a learnings file the Critic checks next time.

## Quickstart

1. **Configure yourself.** Copy the example config and edit it:

   ```bash
   cp config/brand.example.yaml config/brand.yaml
   ```

   Fill in your author identity, publisher, site, voice, conversion links, and banned words. The
   shipped example is a working product-consultancy config, so you can also just run it as a demo.

2. **Get a transcript.** Either transcribe an audio file:

   ```bash
   export OPENAI_API_KEY=sk-...
   python3 tools/transcribe/transcribe.py --audio path/to/recording.mp3 --slug my-topic
   # → input/my-topic/transcript.txt
   ```

   …or drop your own transcript at `input/<slug>/transcript.txt` and skip transcription.

3. **Write the article.** In Claude Code, run the skill:

   ```
   /audio-to-article
   ```

   It runs Curator → SEO brief → (you confirm the angle) → Writer ⇄ Critic → Retro, and writes
   `output/<date_slug>/` with `source-digest.md`, `brief.md`, `article.en.md`, and `review-log.md`.

## Layout

```
config/brand.yaml            # your identity, voice, links, style (copy from brand.example.yaml)
.claude/skills/
  audio-to-article/          # the orchestration entrypoint
  transcribe-audio/          # audio → transcript
  no-ai-slop/                # vendored AI-slop catalog (MIT)
agents/                      # the role prompts: curator, seo-brief, writer, critic
knowledge/
  article-playbook.md        # the durable SEO/GEO/anti-slop spec + the rubric
  eval-learnings.seed.md     # seed failure-pattern base (copy to eval-learnings.md on first run)
tools/transcribe/            # the transcription tool (stdlib only, backend swappable)
input/  output/              # your transcripts in, your article runs out (gitignored)
```

## Requirements

- Claude Code (or a compatible agent harness that reads `.claude/skills` + agent files).
- Python 3.10+ for the transcription tool (standard library only for the default backend).
- A transcription API key (default: `OPENAI_API_KEY`). Not needed if you bring your own transcript.
- For **Hebrew audio**, an optional local backend using the [ivrit.ai](https://github.com/ivrit-ai)
  model (`--provider ivrit`, needs `pip install faster-whisper`, no API key).

## Notes

- **Cursor:** the same skill files work under `.cursor/skills/` — copy the `.claude/skills` tree there.
- **Not affiliated** with any transcription provider. The transcription backend is a single swappable
  function in `tools/transcribe/transcribe.py` (use a local Whisper model if you prefer).

## Who built this

This pipeline was built by **[Ran Erez](https://re-focus.io/about)**, founder of
**[RE.FOCUS](https://re-focus.io)** — a product consultancy that helps product teams refocus on
**impact over busywork**. Ran has led product at high-scale product companies (monday, Elementor,
Taboola, Cloudinary) and now works with product orgs and leaders through three tracks:

- **Advanced team workshops** — hands-on discovery and prioritization on your real cases, with
  implementation hours so the learning embeds in day-to-day work (not another one-off slide deck).
- **Product leadership advisory** — strategy, operating model, and measurable impact for VPs and
  Heads of Product.
- **Founder & startup mentoring** — product strategy, path to PMF, and building a product org that lasts.

If your team ships features but struggles to tie them to business outcomes, that's the gap RE.FOCUS
closes.

**[Learn more →](https://re-focus.io)**  ·  **[About Ran →](https://re-focus.io/about)**  ·  **[Book a call →](https://re-focus.io/contact)**

## License

MIT — see [LICENSE](LICENSE). The `no-ai-slop` catalog is MIT, from
[petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop).
