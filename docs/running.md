# Running OpenRSI-AI-Infra-Bench

[Back to the overview](../README.md)

Every directory under [`tasks/`](../tasks/) is a standalone Harbor 1.4 package (`task.toml`, `instruction.md`, `README.md`, `environment/`, `tests/`, and `solution/solve.sh`) that runs natively with current [RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness)—no external launcher wrappers or manual snapshot scripts are needed.

## 1. Host Requirements & Integrity Check

- **OS & Runtime:** Linux, Docker Engine 26+, NVIDIA drivers + NVIDIA Container Toolkit, Git, `uv`, and Python 3.12+.
- **Compute per run:** 1 exclusive GPU (80 GB+ VRAM recommended: H100 / H200), 16 idle physical (non-SMT) CPU cores on the GPU's NUMA node, 128 GiB host RAM, and ~200 GiB free SSD storage.
- **Network:** Model weights and SeedTTS evaluation splits are downloaded and SHA-256-verified during `docker build`; Work and Judge phases execute offline (`allow_internet = false`).

Verify all 12 task manifests and file hashes locally (CPU-only):

```bash
git clone https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench.git
cd OpenRSI-AI-Infra-Bench
python3 -B scripts/verify.py
```

## 2. Install RSI-Harness

The [Quick start](../README.md#quick-start) uses `uvx` for a one-off run. To make `rsi-harness` available for the commands below, install it from [`OpenRSI-Index`](https://github.com/OpenRSI-Foundation/OpenRSI-Index):

```bash
git clone --filter=blob:none --sparse \
  https://github.com/OpenRSI-Foundation/OpenRSI-Index.git vendor/OpenRSI-Index
git -C vendor/OpenRSI-Index sparse-checkout set RSI-Harness
uv tool install --python 3.12 ./vendor/OpenRSI-Index/RSI-Harness
```

## 3. Validate with `--agent oracle`

Before launching a 24-hour optimization run, validate your Docker build, GPU/NUMA isolation, and pristine serving stack with `--agent oracle`. Both TTS and ASR tasks restore the unmodified baseline source, run all 3-repetition scored workloads, verify quality/latency gates, and emit `reward.json = {"reward": 1.0}`:

```bash
# Validate a TTS dual-mode task
rsi-harness run tasks/cosyvoice3-dual-mode --agent oracle --gpus 0

# Validate an ASR dual-mode task
rsi-harness run tasks/qwen3-asr-1.7b-dual-mode --agent oracle --gpus 0
```

### Automatic CPU/NUMA Isolation

When `RSI_TTS_CPU_LANES` (TTS) or `RSI_ASR_CPU_LANES` (ASR) is unset, the Judge automatically queries `/sys/bus/pci/devices` and `/proc/stat` to select and pin **16 distinct non-SMT physical CPU cores** on the assigned GPU's NUMA node (preferring idle cores), while monitoring host CPU contention (`peak_foreign_cores <= 2.0`). You may also pin explicit core IDs via `RSI_TTS_CPU_LANES='[[0,1,...]]'` or `RSI_ASR_CPU_LANES='0,1,...'`.

## 4. Optional: Recalibrating Reference $B_0$ for Custom GPU SKUs

Each task ships pre-calibrated reference $B_0$ metrics in `tests/baseline.json` (measured on H100 80GB HBM3, H100 NVL, or H200; see each task's `README.md`).

- `--agent oracle` succeeds (`reward = 1.0`) out of the box on any compatible GPU because SHA-256-verified unmodified source bypasses cross-SKU throughput-ratio drift while still enforcing quality, streaming, and contention checks.
- When running an **optimization agent** on a different GPU SKU (for example PCIe H100 NVL vs. SXM5 H100, or A100/B200), measure a fresh 3-repetition $B_0$ on that exact GPU before starting the agent so candidate throughput ratios are compared against your hardware's true baseline:

```bash
TASK_DIR="$PWD/tasks/cosyvoice3-dual-mode"

# Build the task image once (or reuse the image built by --agent oracle), then run calibrate.py:
docker run --rm --gpus '"device=0"' --ipc=host --network=none \
  -v "$TASK_DIR/tests:/tests:ro" \
  <built-task-image> \
  /opt/sglang/bin/python3 -I -B /tests/calibrate.py | tee calibration.log

# Extract the emitted RSI_BASELINE_JSON line and pass it to rsi-harness run:
export RSI_BASELINE_JSON="$(sed -n 's/^RSI_BASELINE_JSON=//p' calibration.log)"
```

## 5. Run a Coding Agent (TTS or ASR)

Launch any coding agent supported by `rsi-harness` using the exact same command pattern across all 12 tasks:

```bash
TASK_DIR="$PWD/tasks/cosyvoice3-dual-mode"

# Codex
rsi-harness run "$TASK_DIR" \
  --agent codex --model gpt-6-astra --reasoning-effort xhigh \
  --agent-auth local --gpus 0

# Claude Code
rsi-harness run "$TASK_DIR" \
  --agent claude-code --model claude-opus-5-5 --reasoning-effort max \
  --agent-auth local --gpus 0
```

## 6. Inspect Results

`rsi-harness` writes run artifacts under `logs/runs/<run-id>/`:
- `final_result.json` and `evolve_state.json` (best round, best score, submission history)
- `submissions/agent-N/report.json` and `test_output.txt` (per-repetition throughput, latency/TTFA/TTFT P95, WER/CER, streaming chunk/delta metrics, and gate verdicts)

```bash
rsi-harness visualize   # open http://127.0.0.1:8000
```

Browse the 21 published baseline trajectories in the [RSI Logs Viewer](https://index.openrsi.foundation/logs/), or download one task's raw files with the [Hugging Face CLI](https://huggingface.co/docs/huggingface_hub/guides/cli):

```bash
hf download OpenRSI-Foundation/OpenRSI-Index-Logs --repo-type dataset \
  --include "sglang-omni/cosyvoice3-dual-mode/*" --local-dir OpenRSI-Index-Logs
```

Omit `--include` to download the entire dataset, including runs from other benchmark tracks.
