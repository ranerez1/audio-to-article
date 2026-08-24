#!/usr/bin/env python3
"""
transcribe.py — turn an audio file into a plain-text transcript.

The article engine works from a transcript at input/<slug>/transcript.txt.
This tool produces that file from an audio recording. If you already have a
transcript, skip this entirely: drop your .txt/.md at input/<slug>/transcript.txt.

Two backends ship, each isolated in one function so adding another is a small edit:
    - openai (default): the OpenAI transcription API (whisper-1 / gpt-4o-transcribe).
      Standard library only, no install.
    - ivrit: the ivrit.ai Hebrew-tuned Whisper model (faster-whisper / CTranslate2),
      run locally on CPU with no API key — best for Hebrew audio. See github.com/ivrit-ai.
      Needs `pip install faster-whisper`.

Usage:
    # OpenAI API (default):
    export OPENAI_API_KEY=sk-...
    python3 tools/transcribe/transcribe.py --audio path/to/recording.mp3
    python3 tools/transcribe/transcribe.py --audio talk.m4a --slug my-article-slug

    # Hebrew audio via the local ivrit.ai model:
    pip install faster-whisper
    python3 tools/transcribe/transcribe.py --audio talk.m4a --provider ivrit

Notes:
    - The OpenAI endpoint caps uploads at ~25 MB. For longer audio, compress to
      a mono 16 kHz mp3/m4a first, split into chunks, or bring your own transcript.
    - Output: input/<slug>/transcript.txt  (printed on success).
"""

import argparse
import os
import re
import sys
import uuid
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = REPO_ROOT / "input"
OPENAI_URL = "https://api.openai.com/v1/audio/transcriptions"

# ivrit.ai Hebrew-tuned Whisper (CTranslate2). Override with the IVRIT_MODEL env var.
IVRIT_MODEL_DEFAULT = os.environ.get("IVRIT_MODEL", "ivrit-ai/whisper-large-v3-turbo-ct2")

# Common audio types → MIME, for the multipart part header.
MIME = {
    ".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".mp4": "audio/mp4",
    ".wav": "audio/wav", ".webm": "audio/webm", ".ogg": "audio/ogg",
    ".flac": "audio/flac", ".mpeg": "audio/mpeg", ".mpga": "audio/mpeg",
}


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", text) or "untitled"


def _multipart(fields: dict, file_field: str, file_path: Path) -> tuple[bytes, str]:
    """Encode a multipart/form-data body with stdlib only. Returns (body, content_type)."""
    boundary = f"----audio2article{uuid.uuid4().hex}"
    crlf = b"\r\n"
    parts = []
    for name, value in fields.items():
        parts += [
            f"--{boundary}".encode(),
            f'Content-Disposition: form-data; name="{name}"'.encode(),
            b"",
            str(value).encode(),
        ]
    mime = MIME.get(file_path.suffix.lower(), "application/octet-stream")
    parts += [
        f"--{boundary}".encode(),
        f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"'.encode(),
        f"Content-Type: {mime}".encode(),
        b"",
        file_path.read_bytes(),
    ]
    parts += [f"--{boundary}--".encode(), b""]
    return crlf.join(parts), f"multipart/form-data; boundary={boundary}"


def transcribe_openai(audio_path: Path, model: str, language: str | None) -> str:
    """POST the audio to the OpenAI transcription API and return the text."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit("error: OPENAI_API_KEY is not set. export it, or bring your own transcript "
                 "(drop a .txt at input/<slug>/transcript.txt and skip this tool).")

    size_mb = audio_path.stat().st_size / 1_000_000
    if size_mb > 25:
        print(f"warning: {audio_path.name} is {size_mb:.0f} MB; the API caps at ~25 MB. "
              f"Compress (mono 16 kHz) or split if the request fails.", file=sys.stderr)

    fields = {"model": model, "response_format": "text"}
    if language:
        fields["language"] = language
    body, content_type = _multipart(fields, "file", audio_path)

    req = urllib.request.Request(
        OPENAI_URL, data=body, method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": content_type},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return resp.read().decode("utf-8").strip()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit(f"error: transcription API returned {e.code}\n{detail}")
    except urllib.error.URLError as e:
        sys.exit(f"error: could not reach the transcription API: {e.reason}")


def transcribe_ivrit(audio_path: Path, model_repo: str, language: str | None) -> str:
    """Transcribe locally with the ivrit.ai Hebrew Whisper model (faster-whisper / CTranslate2).

    Runs on CPU, no API key. Needs `pip install faster-whisper`; the model downloads from
    Hugging Face on first use (set HF_HUB_OFFLINE=1 to force the local cache, no network).
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("error: the ivrit backend needs faster-whisper. Install it with:\n"
                 "    pip install faster-whisper\n"
                 "or use --provider openai (the default).")

    model_path = model_repo
    try:
        from huggingface_hub import snapshot_download
        offline = bool(os.environ.get("HF_HUB_OFFLINE"))
        model_path = snapshot_download(model_repo, local_files_only=offline)
    except Exception as e:
        print(f"[transcribe] model cache resolve fallback: {e}", file=sys.stderr)

    model = WhisperModel(model_path, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(str(audio_path), language=language, beam_size=5, vad_filter=True)
    return " ".join(seg.text.strip() for seg in segments).strip()


def main() -> None:
    ap = argparse.ArgumentParser(description="Audio file → input/<slug>/transcript.txt")
    ap.add_argument("--audio", required=True, help="path to the audio file")
    ap.add_argument("--slug", help="output slug (default: derived from the filename)")
    ap.add_argument("--model", default=None,
                    help="model override. openai default: whisper-1 (e.g. gpt-4o-transcribe); "
                         "ivrit default: the ivrit.ai CT2 repo (or set IVRIT_MODEL)")
    ap.add_argument("--language", help="ISO-639-1 hint, e.g. 'en' or 'he' (ivrit defaults to 'he')")
    ap.add_argument("--provider", default="openai", choices=["openai", "ivrit"],
                    help="transcription backend: 'openai' (API) or 'ivrit' (local ivrit.ai Hebrew model)")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="override output dir (default: input/<slug>/)")
    args = ap.parse_args()

    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.is_file():
        sys.exit(f"error: audio file not found: {audio_path}")

    slug = slugify(args.slug or audio_path.stem)
    out_dir = args.out_dir or (DEFAULT_INPUT_DIR / slug)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "transcript.txt"

    if args.provider == "ivrit":
        model = args.model or IVRIT_MODEL_DEFAULT
        lang = args.language or os.environ.get("TRANSCRIBE_LANG", "he")
        lang = None if lang in ("", "auto") else lang
        print(f"transcribing {audio_path.name} via ivrit:{model} (local) ...", file=sys.stderr)
        text = transcribe_ivrit(audio_path, model, lang)
    else:
        model = args.model or "whisper-1"
        print(f"transcribing {audio_path.name} via openai:{model} ...", file=sys.stderr)
        text = transcribe_openai(audio_path, model, args.language)
    if not text:
        sys.exit("error: transcription returned empty text.")

    out_path.write_text(text + "\n", encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
