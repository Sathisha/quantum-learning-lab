"""Turn class recordings into text Claude can read: transcript, slide snapshots, and (optionally) LM Studio notes.

For every .mp4/.mkv/.m4a/.mp3 under the class-material folder that hasn't been processed yet, writes a folder
next to it called "<video name>.processed/" containing:

  transcript.txt     timestamped transcript, one line per segment: [01:02:03] text
  transcript.srt     the same as subtitles (open it in VLC alongside the video)
  slides-NN.jpg      contact sheets: one frame every --frame-every seconds, 12 per sheet, numbered
  notes.md           (only with --notes) lecture notes written by the model loaded in LM Studio
  done.json          settings used; delete this file to re-process the recording

Runs fully on this PC. Speech-to-text uses faster-whisper (OpenAI Whisper, re-implemented to run fast);
the NVIDIA GPU is used if available, otherwise the CPU.

Usage (normally via Docker: transcribe.ps1 / transcribe.sh; see README.md):
  python class_pipeline.py "lecture.mp4"                 # one recording: transcript + slide sheets
  python class_pipeline.py "class material/week-02"      # every new recording in a folder
  python class_pipeline.py lecture.mp4 --notes           # ...and LM Studio notes
  python class_pipeline.py lecture.mp4 --only notes      # notes for a recording already transcribed
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

def default_path() -> Path:
    """PIPELINE_DEFAULT_PATH (set to /data in Docker), else the repo's "class material" folder."""
    if os.environ.get("PIPELINE_DEFAULT_PATH"):
        return Path(os.environ["PIPELINE_DEFAULT_PATH"])
    here = Path(__file__).resolve()
    return (here.parents[2] if len(here.parents) > 2 else here.parent) / "class material"

MEDIA = {".mp4", ".mkv", ".mov", ".webm", ".m4a", ".mp3", ".wav"}
VIDEO = {".mp4", ".mkv", ".mov", ".webm"}

# Words Whisper might otherwise mishear; it uses this as context, not as a script.
COURSE_PROMPT = (
    "IIT Delhi lecture on quantum computing and linear algebra. Terms: qubit, ket, bra, Dirac notation, "
    "Hadamard, Hermitian, unitary, eigenvalue, eigenvector, orthonormal basis, inner product, norm, "
    "Cauchy-Schwarz, Parseval, tensor product, Kronecker, Bloch sphere, superposition, entanglement, "
    "CNOT, Pauli X Y Z, Qiskit, Grover, Shor, Deutsch-Jozsa, quantum Fourier transform, QAOA, VQE, NISQ."
)


def hms(t: float) -> str:
    t = int(t)
    return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"


def add_cuda_dlls() -> None:
    """On Windows, make the pip-installed NVIDIA cuBLAS/cuDNN DLLs findable."""
    if os.name != "nt":
        return
    import site
    for sp in site.getsitepackages() + [site.getusersitepackages()]:
        for d in glob.glob(os.path.join(sp, "nvidia", "*", "bin")):
            os.add_dll_directory(d)
            os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]


def load_whisper(model_name: str, device: str):
    from faster_whisper import WhisperModel
    if device in ("auto", "cuda"):
        try:
            add_cuda_dlls()
            m = WhisperModel(model_name, device="cuda", compute_type="float16")
            print(f"  speech model: {model_name} on GPU")
            return m
        except Exception as e:  # no NVIDIA GPU, or CUDA libraries missing
            if device == "cuda":
                raise
            print(f"  GPU not usable ({str(e)[:120]}); using CPU (slower)")
    m = WhisperModel(model_name, device="cpu", compute_type="int8")
    print(f"  speech model: {model_name} on CPU")
    return m


def transcribe(model, media: Path, out: Path, language: str) -> float:
    segments, info = model.transcribe(
        str(media), language=language, vad_filter=True, beam_size=5,
        initial_prompt=COURSE_PROMPT, condition_on_previous_text=False,
    )
    total = info.duration or 1
    start = time.time()
    with open(out / "transcript.txt", "w", encoding="utf-8") as txt, \
         open(out / "transcript.srt", "w", encoding="utf-8") as srt:
        txt.write(f"# Transcript of {media.name} (duration {hms(total)})\n")
        for i, s in enumerate(segments, 1):
            text = s.text.strip()
            txt.write(f"[{hms(s.start)}] {text}\n")
            srt.write(f"{i}\n{srt_time(s.start)} --> {srt_time(s.end)}\n{text}\n\n")
            if i % 50 == 0:
                done = s.end / total
                eta = (time.time() - start) / max(done, 1e-3) * (1 - done)
                print(f"    {done:5.1%} transcribed, about {eta / 60:.0f} min left", flush=True)
    return total


def slide_sheets(video: Path, out: Path, every: int) -> int:
    """Grab one frame every `every` seconds and tile 12 per sheet (4 x 3), each labelled with its time."""
    import av
    from PIL import Image, ImageDraw

    frames, w = [], 640
    with av.open(str(video)) as c:
        stream = c.streams.video[0]
        dur = float(c.duration / 1_000_000) if c.duration else 0
        t = 0.0
        while t < dur:
            c.seek(int(t / stream.time_base), stream=stream, any_frame=False, backward=True)
            for f in c.decode(stream):
                if f.time is None or f.time >= t - 0.5:
                    img = f.to_image()
                    img = img.resize((w, int(img.height * w / img.width)))
                    frames.append((t, img))
                    break
            t += every
    if not frames:
        return 0
    h = frames[0][1].height
    try:
        from PIL import ImageFont
        font = ImageFont.load_default(size=20)
    except TypeError:  # Pillow older than 10.1
        font = None
    n_sheets = 0
    for k in range(0, len(frames), 12):
        sheet = Image.new("RGB", (4 * w + 12, 3 * h + 8), "black")
        for j, (t, img) in enumerate(frames[k:k + 12]):
            x, y = (j % 4) * (w + 4), (j // 4) * (h + 4)
            sheet.paste(img, (x, y))
            d = ImageDraw.Draw(sheet)
            d.rectangle([x, y, x + 100, y + 28], fill="black")
            d.text((x + 6, y + 3), hms(t), fill="yellow", font=font)
        n_sheets += 1
        sheet.save(out / f"slides-{n_sheets:02d}.jpg", quality=80)
    return n_sheets


def lmstudio(prompt: str, url: str, model: str | None, max_tokens: int = 2500) -> str:
    body = {"messages": [{"role": "user", "content": prompt}], "temperature": 0.2, "max_tokens": max_tokens}
    if model:
        body["model"] = model
    req = urllib.request.Request(url.rstrip("/") + "/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)["choices"][0]["message"]["content"].strip()


def notes(out: Path, url: str, model: str | None, chunk_chars: int) -> None:
    lines = (out / "transcript.txt").read_text(encoding="utf-8").splitlines()[1:]
    chunks, cur = [], ""
    for ln in lines:
        if len(cur) + len(ln) > chunk_chars and cur:
            chunks.append(cur)
            cur = ""
        cur += ln + "\n"
    if cur:
        chunks.append(cur)
    parts = []
    for i, ch in enumerate(chunks, 1):
        print(f"    notes: part {i}/{len(chunks)}", flush=True)
        parts.append(lmstudio(
            "You are taking study notes from part of a recorded university lecture (IIT Delhi, quantum computing "
            "and linear algebra). Speech-to-text errors are likely; fix obvious ones. From the transcript below, write:\n"
            "1. Topics covered, in order, with the timestamp where each starts.\n"
            "2. Every definition, formula and worked example the lecturer gave, with each step.\n"
            "3. Anything the lecturer stressed (\"important\", \"common mistake\", \"exam\", \"you will need this\").\n"
            "4. Questions students asked and the answers.\n"
            "5. Announcements: homework, deadlines, readings, what comes next.\n"
            "Use plain-text maths (Unicode, no LaTeX). Leave out a section if nothing fits it.\n\n"
            f"TRANSCRIPT PART {i} of {len(chunks)}:\n{ch}", url, model))
    merged = "\n\n".join(f"## Part {i}\n\n{p}" for i, p in enumerate(parts, 1))
    summary = lmstudio(
        "Below are notes from consecutive parts of one lecture. Write a one-page overview: the topics in order with "
        "start times, the 5 most important ideas, and every announcement (homework, readings, deadlines). Plain text "
        "maths, no LaTeX.\n\n" + merged[:60000], url, model, max_tokens=1500)
    (out / "notes.md").write_text(f"# Lecture notes (LM Studio, from the transcript)\n\n## Overview\n\n{summary}\n\n"
                                  f"{merged}\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path, nargs="?", default=None,
                    help="a recording, or a folder searched recursively for recordings")
    ap.add_argument("--model", default="large-v3-turbo", help="Whisper model: large-v3-turbo (default), large-v3, medium.en, small.en")
    ap.add_argument("--device", default=os.environ.get("PIPELINE_DEVICE", "auto"), choices=["auto", "cuda", "cpu"])
    ap.add_argument("--language", default="en")
    ap.add_argument("--frame-every", type=int, default=60, help="seconds between slide snapshots")
    ap.add_argument("--only", choices=["transcript", "slides", "notes"], help="run just one step")
    ap.add_argument("--notes", action="store_true", help="also write notes.md with LM Studio")
    ap.add_argument("--lmstudio-url", default=os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1"))
    ap.add_argument("--lmstudio-model", default=None, help="model id in LM Studio (default: the loaded one)")
    ap.add_argument("--chunk-chars", type=int, default=12000, help="transcript characters per LM Studio request")
    a = ap.parse_args()
    a.path = a.path or default_path()

    if a.path.is_file():
        if a.path.suffix.lower() not in MEDIA:
            sys.exit(f"Not a recording I can read: {a.path.name} (expected one of {', '.join(sorted(MEDIA))})")
        media, base = [a.path], a.path.parent
    elif a.path.is_dir():
        media = sorted(p for p in a.path.rglob("*") if p.suffix.lower() in MEDIA and ".processed" not in str(p))
        base = a.path
    else:
        sys.exit(f"Path not found: {a.path}")
    if not media:
        sys.exit(f"No recordings found in {a.path}")
    want = {a.only} if a.only else {"transcript", "slides"} | ({"notes"} if a.notes else set())
    outs = {m: m.with_name(m.stem + ".processed") for m in media}
    for out in outs.values():
        out.mkdir(exist_ok=True)

    # Step 1: transcripts for every recording (the speech model is loaded once, then freed before LM Studio runs)
    if "transcript" in want:
        model = None
        for m, out in outs.items():
            print(f"\n== {m.relative_to(base)}")
            if (out / "transcript.txt").exists() and (out / "done.json").exists():
                print("  transcript: already done")
                continue
            model = model or load_whisper(a.model, a.device)
            t0 = time.time()
            dur = transcribe(model, m, out, a.language)
            (out / "done.json").write_text(json.dumps({"model": a.model, "duration_s": dur,
                                                       "took_min": round((time.time() - t0) / 60, 1)}))
            print(f"  transcript done in {(time.time() - t0) / 60:.0f} min")
        del model

    # Step 2: slide snapshot sheets
    if "slides" in want:
        for m, out in outs.items():
            if m.suffix.lower() in VIDEO and not list(out.glob("slides-*.jpg")):
                print(f"\n== {m.relative_to(base)}\n  slide sheets: {slide_sheets(m, out, a.frame_every)} written")

    # Step 3: notes with the model loaded in LM Studio
    if "notes" in want:
        for m, out in outs.items():
            print(f"\n== {m.relative_to(base)}")
            if not (out / "transcript.txt").exists():
                print("  notes: skipped, no transcript yet")
            elif (out / "notes.md").exists() and a.only != "notes":
                print("  notes: already done")
            else:
                try:
                    notes(out, a.lmstudio_url, a.lmstudio_model, a.chunk_chars)
                    print("  notes.md written")
                except OSError as e:
                    print(f"  notes: LM Studio not reachable at {a.lmstudio_url} ({e}). Start its server and rerun with --only notes")
    print(f"\nAll done. Results are in the .processed folder next to each recording ({len(media)} checked).")


if __name__ == "__main__":
    main()
