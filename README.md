# Quantum Learning Lab

My workspace for learning quantum computing: study notes, notebooks and experiments.

**Read on a phone:** https://sathisha.github.io/quantum-learning-lab/ (the HTML pages rendered, via GitHub Pages)

## Projects

| Folder | What it is | Status |
| --- | --- | --- |
| [quantum-foundations](quantum-foundations/) | Maths and quantum computing foundations, organised by concept | In progress |

New projects get their own top-level folder.

## Tools

| Folder | What it is |
| --- | --- |
| [tools/class-pipeline](tools/class-pipeline/) | One-command Docker pipeline: class recording → Whisper transcript, slide snapshots, optional LM Studio notes. Runs locally. |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```
