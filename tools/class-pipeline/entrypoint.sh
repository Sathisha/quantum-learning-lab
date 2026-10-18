#!/bin/sh
# Point the CUDA loader at the pip-installed cuBLAS/cuDNN libraries (site-packages/nvidia/*/lib), then run the pipeline.
LIBS=$(python - <<'EOF'
import glob, os, site
dirs = []
for sp in site.getsitepackages():
    dirs += sorted(d for d in glob.glob(os.path.join(sp, "nvidia", "*", "lib")) if os.path.isdir(d))
print(":".join(dirs))
EOF
)
[ -n "$LIBS" ] && export LD_LIBRARY_PATH="$LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec python /app/class_pipeline.py "$@"
