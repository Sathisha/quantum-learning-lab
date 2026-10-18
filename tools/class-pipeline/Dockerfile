# Class recording pipeline: Whisper speech-to-text (GPU or CPU), slide snapshots, optional LM Studio notes.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/models \
    PIPELINE_DEFAULT_PATH=/data

WORKDIR /app
COPY requirements.txt .
# The NVIDIA cuBLAS/cuDNN wheels let the same image use an NVIDIA GPU; on a CPU-only machine they sit unused.
RUN pip install -r requirements.txt \
 && python -c "import glob, sys; libs = [n for p in ('libcublas.so.12', 'libcudnn.so.9') for n in glob.glob('/usr/local/lib/python3.*/site-packages/nvidia/*/lib/' + p)]; print('CUDA libraries:', *libs, sep='\n  '); sys.exit(0 if len(libs) == 2 else 'cuBLAS 12 / cuDNN 9 libraries missing')"

COPY class_pipeline.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

VOLUME ["/data", "/models"]
ENTRYPOINT ["/app/entrypoint.sh"]
