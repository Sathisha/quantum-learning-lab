# Quantum Learning Lab

My workspace for learning quantum computing: course material, notebooks and experiments.

**Read on a phone:** https://sathisha.github.io/quantum-learning-lab/ (the HTML pages rendered, via GitHub Pages)

## Projects

| Folder | What it is | Status |
| --- | --- | --- |
| [iitd-cep-applied-quantum-ai](iitd-cep-applied-quantum-ai/) | IIT Delhi CEP Certification in Applied Quantum Computing & AI (Oct 2026 – Apr 2027), organised by concept | In progress: Week 1 done |

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
