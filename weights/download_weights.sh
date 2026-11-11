#!/bin/bash
# Download v5.0 models from https://github.com/ultralytics/yolov5/releases/tag/v5.0
# Usage:
#    $ bash weights/download_weights.sh

python - <<EOF
from utils.google_utils import attempt_download

for x in ['s', 'm', 'l', 'x']:
    attempt_download(f'yolov5{x}.pt')

EOF
