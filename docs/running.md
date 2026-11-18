# Running OpenRSI-AI-Infra-Bench

[Overview](../README.md) · [How it works](how-it-works.md) · [Evaluation](evaluation.md) · **Running guide** · [Upstream results](upstream-results.md) · [24h results](../results/README.md)

Every directory under [`tasks/`](../tasks/) is a standalone Harbor 1.4 package (`task.toml`, `instruction.md`, `README.md`, `environment/`, `tests/`, and `solution/solve.sh`) that runs natively with [RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness)—no external launcher wrappers or manual snapshot scripts are needed.

<a id="1-host-requirements--integrity-check"></a>

## 1. Host Requirements & Integrity Check

- **OS & Runtime:** Linux, Docker Engine 26+ with daemon access, NVIDIA drivers + NVIDIA Container Toolkit, Git, [`uv`](https://docs.astral.sh/uv/getting-started/installation/), and Python 3.12+.
- **Compute per run:** 1 exclusive NVIDIA GPU (**H100 80GB HBM3** used for reference B₀; 80 GB+ VRAM recommended), 16 idle physical (non-SMT) CPU cores on the GPU's NUMA node, 128 GiB host RAM, and ~200 GiB free SSD storage.
- **Network:** Model weights and SeedTTS evaluation splits are downloaded and SHA-256-verified during `docker build`; both Work and Judge containers execute offline (`allow_internet = false`).

Clone the repository and verify all 8 task manifests, file modes, and Python/JSON/TOML/shell syntax locally (CPU-only, `< 1s`):

```bash
git clone https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench.git
cd OpenRSI-AI-Infra-Bench
python3 -B scripts/verify.py
```

Expected output:

```text
PASS: 8 task packages; 212 files match the source snapshot.
Checked hashes, executable modes, and Python/JSON/TOML/shell syntax. No GPU evaluation performed.
```

<a id="2-install-rsi-harness"></a>

## 2. Install RSI-Harness

The [README Quick start](../README.md#quick-start) uses `uvx` for a zero-install one-liner. For repeated runs, install `rsi-harness` persistently from [`OpenRSI-Index`](https://github.com/OpenRSI-Foundation/OpenRSI-Index):

```bash
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/OpenRSI-Foundation/OpenRSI-Index.git vendor/OpenRSI-Index
git -C vendor/OpenRSI-Index sparse-checkout set RSI-Harness
uv tool install --python 3.12 ./vendor/OpenRSI-Index/RSI-Harness
```

If you already cloned `OpenRSI-Index` with `--recurse-submodules`, this repository is mounted directly at `OpenRSI-Index/rsi-tasks/sglang-omni` and you can install from `../../RSI-Harness`.

## 3. Validate with `--agent oracle`

Before starting a 24-hour optimization run, validate image build, GPU/NUMA isolation, and evaluation health with `--agent oracle` (no LLM API key required). Both TTS and ASR tasks restore the unmodified baseline source, run all 3 scored repetitions per mode, check every quality/latency/streaming guard, and emit `reward = 1.0`:

```bash
# Validate a TTS dual-mode task
rsi-harness run tasks/cosyvoice3-dual-mode --agent oracle --gpus 0

# Validate an ASR dual-mode task
rsi-harness run tasks/qwen3-asr-1.7b-dual-mode --agent oracle --gpus 0
```

### Automatic CPU / NUMA Isolation

When `RSI_TTS_CPU_LANES` (TTS) or `RSI_ASR_CPU_LANES` (ASR) is unset, the Judge automatically queries `/sys/bus/pci/devices` and `/proc/stat` to bind **16 distinct non-SMT physical CPU cores** on the assigned GPU's NUMA node (preferring idle cores) while enforcing `peak_foreign_cores <= 2.0`. On shared multi-GPU hosts, you can pin explicit physical core IDs if desired:

```bash
# Optional manual core pinning examples
export RSI_TTS_CPU_LANES='[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]]'
export RSI_ASR_CPU_LANES='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
```

<a id="4-optional-recalibrating-reference-b_0-for-custom-gpu-skus"></a>

## 4. Optional: Recalibrating Reference B₀ for Custom GPU SKUs

Each task ships pre-calibrated reference **B₀** metrics in `tests/baseline.json` measured on **NVIDIA H100 80GB HBM3** (see [Evaluation](evaluation.md#2-per-task-reference-b-gate-specification) or each task's `README.md`).

- `--agent oracle` succeeds (`reward = 1.0`) out of the box on any compatible GPU because SHA-256-verified unmodified source bypasses cross-SKU throughput-ratio drift while still enforcing all quality, streaming, and contention gates.
- When running an **optimization agent** on a different GPU SKU (for example PCIe H100 NVL, H200, A100, or B200), measure a fresh 3-repetition **B₀** on that exact GPU once and pass `RSI_BASELINE_JSON` so speedups are measured against your hardware's true baseline:

```bash
TASK_SLUG="cosyvoice3-dual-mode"   # any of the 8 task slugs under tasks/
TASK_DIR="$PWD/tasks/$TASK_SLUG"
IMAGE_TAG="openrsi-${TASK_SLUG}:calib"

# 1. Build the task image (reuses cached layers if --agent oracle already ran)
docker build -t "$IMAGE_TAG" "$TASK_DIR/environment"

# 2. Measure 3-repetition B0 offline (TTS uses /opt/sglang/bin/python3; ASR uses /opt/asr-venv/bin/python)
PY_BIN="/opt/sglang/bin/python3"   # set to /opt/asr-venv/bin/python for *-asr-* or moss-transcribe-*
docker run --rm --gpus '"device=0"' --ipc=host --network=none \
  -v "$TASK_DIR/tests:/tests:ro" \
  "$IMAGE_TAG" \
  "$PY_BIN" -I -B /tests/calibrate.py | tee calibration.log

# 3. Export RSI_BASELINE_JSON for subsequent rsi-harness runs on this GPU
export RSI_BASELINE_JSON="$(sed -n 's/^RSI_BASELINE_JSON=//p' calibration.log)"
```

## 5. Run a Coding Agent

All 8 TTS and ASR tasks share the exact same `rsi-harness run` interface (default budget: `86400` seconds = 24 hours in `task.toml`):

```bash
TASK_DIR="$PWD/tasks/cosyvoice3-dual-mode"

# Codex (gpt-6-astra, xhigh reasoning)
rsi-harness run "$TASK_DIR" \
  --agent codex --model gpt-6-astra --reasoning-effort xhigh \
  --agent-auth local --gpus 0

# Claude Code (claude-opus-5-5, max reasoning)
rsi-harness run "$TASK_DIR" \
  --agent claude-code --model claude-opus-5-5 --reasoning-effort max \
  --agent-auth local --gpus 0
```

## 6. Inspect Local Runs & Public Trajectories

`rsi-harness` writes run artifacts under `logs/runs/<run-id>/`:

- `started_at`, `evolve_state.json`, and `final_result.json` — timestamps, round-by-round scores, and best verified submission.
- `submissions/agent-N/report.json` and `test_output.txt` — detailed per-repetition throughput, latency / TTFA / TTFT P95, WER / CER, streaming continuity metrics, and gate verdicts.

Launch the local web viewer to inspect trajectories interactively:

```bash
rsi-harness visualize   # opens http://127.0.0.1:8000
```

To inspect or download the **16 published single-agent runs**:

- **24-hour aligned benchmark results & audit:** [`results/README.md`](../results/README.md) · [`results/24h-audit.json`](../results/24h-audit.json)
- **Full-run records & interactive Logs Viewer links:** [`results/archive.md`](../results/archive.md) · [index.openrsi.foundation/logs](https://index.openrsi.foundation/logs/)
- **Raw uncompressed files on Hugging Face** (pinned benchmark snapshot `f5deed0f9c9f`):

```bash
hf download OpenRSI-Foundation/OpenRSI-Index-Logs --repo-type dataset \
  --revision f5deed0f9c9f75ef0f8a5e9514712f8601aea360 \
  --include "sglang-omni/cosyvoice3-dual-mode/*" \
  --local-dir OpenRSI-Index-Logs
```
