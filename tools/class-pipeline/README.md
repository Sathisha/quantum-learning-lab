# Class recording pipeline (Docker)

One command turns a class recording into text that's quick to read and to hand to Claude. Everything runs on your PC: the recordings never leave it.

```powershell
tools\class-pipeline\transcribe.cmd "C:\workspace\quantum-learning-lab\class material\week-02\lecture.mp4"
```

```
lecture.mp4
   │  1. Whisper speech-to-text (NVIDIA GPU, or CPU)
   │  2. Slide snapshots: one frame a minute, 12 per sheet
   │  3. Optional (-Notes): LM Studio writes lecture notes from the transcript
   ▼
lecture.processed\
   transcript.txt    [00:12:41] So the inner product conjugates the first slot ...
   transcript.srt    subtitles: open in VLC next to the video
   slides-01.jpg …   contact sheets, each frame labelled with its time
   notes.md          (with -Notes) topics with times, definitions, examples, announcements
   done.json         settings used; delete it to re-transcribe
```

LM Studio runs text models only and can't turn speech into text, so step 1 uses Whisper (`large-v3-turbo` via faster-whisper) inside the container. LM Studio is used for step 3.

## One-time setup

**1. Docker Desktop.** Skip this if `docker --version` works in a terminal.

```powershell
winget install Docker.DockerDesktop
```

Restart the PC, open Docker Desktop once, and keep the default **WSL 2** backend.

**2. Check that Docker can see the GPU.** You need a current NVIDIA driver.

```powershell
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

If this prints a GPU table, you're set. If it errors, update the NVIDIA driver (NVIDIA app → Drivers) and try again. You can still run everything on the CPU with `-Cpu`, just slower.

**3. First run** builds the image (about 3 GB, a few minutes) and downloads the Whisper model once (about 1.6 GB, kept in the `whisper-models` Docker volume):

```powershell
cd C:\workspace\quantum-learning-lab
tools\class-pipeline\transcribe.cmd "class material\1071830_ssgv.mp4"
```

Rough time for a 2-hour class: 6–15 minutes on an RTX laptop GPU, 40–90 minutes on CPU.

**4. LM Studio, for `-Notes` (optional).**

1. Download an instruction model that fits your GPU. A 7–8B model such as **Qwen2.5 7B Instruct** or **Llama 3.1 8B Instruct** (Q4_K_M) suits 6–8 GB of VRAM.
2. Load it with **context length 16384** or more. The pipeline sends about 3,000 words at a time.
3. In the **Developer** tab, turn on **Start server** (port 1234). If the pipeline then says LM Studio is "not reachable", also turn on **Serve on Local Network** in the server settings, so the container can reach it at `host.docker.internal`.

The pipeline finishes transcribing before it calls LM Studio, so Whisper and the LLM don't overlap. On a GPU with 8 GB or less, it's still safest to unload the LM Studio model while transcribing and load it for `-Notes`. Notes for a recording that's already transcribed:

```powershell
tools\class-pipeline\transcribe.cmd "class material\week-02\lecture.mp4" -- --only notes
```

## Every week

1. Put the recordings and slide PDFs in a new folder, for example `class material\week-02\`.
2. Run one command on the folder. It processes every recording in it that isn't done yet:
   ```powershell
   tools\class-pipeline\transcribe.cmd "C:\workspace\quantum-learning-lab\class material\week-02" -Notes
   ```
3. Tell Claude **"process week 02 class material"**. Claude reads the transcripts, slide sheets, notes and PDFs from your linked computer and updates the study pages.

## Options

| Option | What it does |
| --- | --- |
| `-Notes` | Also write `notes.md` with LM Studio |
| `-Cpu` | Run without the GPU |
| `-Rebuild` | Rebuild the image after the pipeline code changes (for example after `git pull`) |
| `-- --model large-v3` | Most accurate Whisper model, slower. `medium.en` or `small.en` are faster on a CPU. |
| `-- --frame-every 30` | Slide snapshot every 30 s instead of 60 s |
| `-- --only transcript` / `slides` / `notes` | Run one step only |
| `-- --lmstudio-model <id>` | Pick a specific model when LM Studio has several loaded |

Everything after `--` is passed to `class_pipeline.py`; `--help` lists all options. On macOS or Linux, use `./transcribe.sh <path> [--notes] [--cpu] [--rebuild] [-- options]`.

## Without Docker

`class_pipeline.py` also runs directly: `pip install -r requirements.txt`, then `python class_pipeline.py <video or folder>`. On Windows that also needs the cuBLAS/cuDNN lines in `requirements.txt` for the GPU.

## Files

| File | Role |
| --- | --- |
| `transcribe.cmd` | The one command on Windows; calls `transcribe.ps1` without needing a PowerShell policy change |
| `transcribe.ps1` / `transcribe.sh` | Mount the recording's folder into the container and run the right service |
| `docker-compose.yml` | Services `transcribe` (GPU) and `transcribe-cpu`, plus the model-cache volume |
| `Dockerfile`, `entrypoint.sh` | Python 3.12 image with faster-whisper and the CUDA libraries |
| `class_pipeline.py` | The pipeline itself |

## Privacy and the public repo

`class material/` is in `.gitignore`, so recordings, slides, transcripts and notes stay on your PC and never reach GitHub or the public site. Only this tool is committed.
