#!/usr/bin/env bash
set -euo pipefail

MOSHI_HF_REPO="${MOSHI_HF_REPO:-kyutai/moshiko-pytorch-bf16}"
MOSHI_HOST="${MOSHI_HOST:-0.0.0.0}"
MOSHI_PORT="${MOSHI_PORT:-8000}"
MOSHI_EXTRA_ARGS="${MOSHI_EXTRA_ARGS:-}"

if [[ -n "${HF_TOKEN:-}" ]]; then
  echo "Logging into Hugging Face CLI"
  huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential
fi

echo "Starting Moshi server"
echo "repo=${MOSHI_HF_REPO} host=${MOSHI_HOST} port=${MOSHI_PORT}"

exec python3 -m moshi.server \
  --hf-repo "${MOSHI_HF_REPO}" \
  --host "${MOSHI_HOST}" \
  --port "${MOSHI_PORT}" \
  ${MOSHI_EXTRA_ARGS}
