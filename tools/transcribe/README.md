# tools/transcribe

Turns an audio recording into the plain-text transcript the article engine reads
(`input/<slug>/transcript.txt`).

## Backends

- **`openai`** (default) — the OpenAI transcription API. Python 3.10+, standard library only,
  no `pip install`. Needs a key:

  ```bash
  export OPENAI_API_KEY=sk-...
  ```

- **`ivrit`** — the [ivrit.ai](https://github.com/ivrit-ai) Hebrew-tuned Whisper model
  (`ivrit-ai/whisper-large-v3-turbo-ct2`), run locally on CPU via faster-whisper. No API key,
  best for Hebrew audio. Needs one dependency and downloads the model on first use:

  ```bash
  pip install faster-whisper
  python3 tools/transcribe/transcribe.py --audio talk.m4a --provider ivrit
  ```

  Language defaults to Hebrew (`he`); override with `--language` or the `TRANSCRIBE_LANG` env
  var (`auto` to detect). Point at a different model with `IVRIT_MODEL`. Set `HF_HUB_OFFLINE=1`
  to force the local cache with no network.

## Usage

```bash
python3 tools/transcribe/transcribe.py --audio path/to/recording.mp3
# → input/recording/transcript.txt

python3 tools/transcribe/transcribe.py --audio talk.m4a --slug feature-prioritization
# → input/feature-prioritization/transcript.txt
```

Options: `--model` (default `whisper-1`; also `gpt-4o-transcribe`), `--language`
(ISO-639-1 hint like `en`), `--slug`, `--out-dir`.

## Bring your own transcript (skip this tool)

If you already have a transcript, you don't need to transcribe anything. Just save
it as `input/<slug>/transcript.txt` and run the `audio-to-article` skill on that slug.

## Adding another backend

Each backend is one function (`transcribe_openai`, `transcribe_ivrit`). To add a different
service or model, write a function with the same signature and dispatch to it in `main()`. The
rest of the pipeline never knows or cares which backend produced the transcript.

## Limits

The OpenAI endpoint caps uploads at ~25 MB. For longer recordings, export mono 16 kHz
audio, split into chunks and concatenate the transcripts, or bring your own transcript.
