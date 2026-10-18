#!/bin/sh
# Point the CUDA loader at the pip-installed cuBLAS/cuDNN libraries, then run the pipeline with the given arguments.
LIBS=$(python -c "import os, nvidia.cublas.lib, nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ':' + os.path.dirname(nvidia.cudnn.lib.__file__))" 2>/dev/null)
[ -n "$LIBS" ] && export LD_LIBRARY_PATH="$LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec python /app/class_pipeline.py "$@"
