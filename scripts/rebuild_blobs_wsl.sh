#!/bin/bash
set -euxo pipefail
export PATH="/opt/toolchain/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
cd /mnt/c/Antigravity/HEADRUSH
bash scripts/build_blobs_native.sh

