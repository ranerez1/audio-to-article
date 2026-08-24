---
name: transcribe-audio
description: >-
  Turn an audio recording into the plain-text transcript the audio-to-article
  pipeline reads. Wraps tools/transcribe/transcribe.py (OpenAI transcription API by
  default) and writes input/<slug>/transcript.txt. Use when the user has an audio
  file to turn into an article, or says "transcribe this", before running
  audio-to-article. If a transcript already exists, skip this and drop it at
  input/<slug>/transcript.txt.
---

# Transcribe audio (skill)

Prereq step for [audio-to-article](../audio-to-article/SKILL.md). Produces the
transcript that pipeline consumes.

## When to use

- The user has an audio file (interview, talk, working session, voice memo) they
  want turned into an article.
- Run this first, then hand the resulting slug to `audio-to-article`.

## Skip it when

- A transcript already exists. Save it as `input/<slug>/transcript.txt` (plain text
  or markdown) and go straight to `audio-to-article`. No transcription needed.

## Steps

1. **Check for a key.** `tools/transcribe/transcribe.py` needs `OPENAI_API_KEY`
   (default backend). If it's absent and no transcript exists yet, tell the user to
   either export a key or drop their own transcript at `input/<slug>/transcript.txt`.
2. **Run the tool:**

   ```bash
   python3 tools/transcribe/transcribe.py --audio <path-to-audio> [--slug <slug>] [--language en]
   ```

   For **Hebrew audio**, use the local ivrit.ai model instead of the API (`pip install faster-whisper`):

   ```bash
   python3 tools/transcribe/transcribe.py --audio <path-to-audio> --provider ivrit
   ```

   Either way it writes `input/<slug>/transcript.txt` and prints the path.
3. **Report** the transcript path and hand off: "ready for `audio-to-article` on slug
   `<slug>`." Do not read or summarize the audio itself — the tool handles it.

## Notes

- The API caps uploads at ~25 MB. For longer audio, compress (mono 16 kHz) or split;
  see [tools/transcribe/README.md](../../../tools/transcribe/README.md).
- Backend is swappable (local Whisper, another API) — one function in the tool.
