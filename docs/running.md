# Running the benchmark

[Back to the overview](../README.md)

Each task is a complete Harbor-format package: `instruction.md`, `task.toml`,
`environment/`, `tests/`, and a restoration-only `solution/solve.sh`.
RSI-Harness runs the coding agent, snapshots its workspace, and evaluates
submissions in a separate Judge phase. The task's evaluator owns the score.

## 1. Choose a task and reserve resources

Use the [task index](../README.md#tasks) to select the **inner directory containing
`task.toml`**. All packages declare one GPU for Work and one for Judge; these phases
reuse the same exclusive physical GPU. Reserve 16 physical CPU cores and 128 GiB
RAM, and record CPU/NUMA affinity. A different GPU or allocation requires a fresh
calibration. H100/H200 were used in the archived runs.

The host needs Linux, NVIDIA drivers and Container Toolkit, Docker, Git, `uv`, and
Python 3.12. Allow space for model downloads, images, generated audio and snapshots:
the task declarations plan 1 TiB for TTS or 200 GiB for ASR. Downloads happen during
the build; Work and Judge use the task's offline policy.

Default agent budgets are 24 hours, except Ming3 streaming at 8 hours. TTS Judges
allow 4 hours per evaluation; ASR Judges allow 3. These are limits, not measured
completion times. The historical baseline table contains some different budgets.

```bash
git clone https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra.git
cd OpenRSI-AI-Infra
uv run --python 3.12 python -B scripts/verify.py
```

This verification is CPU-only. It does not build containers or validate GPU
performance.

## 2. Install RSI-Harness

The public Harness is distributed inside OpenRSI-Index. Keep the runner outside
the task package. This reference checkout pins the public source used when this
repository was assembled:

```bash
git clone --filter=blob:none --sparse \
  https://github.com/OpenRSI-Foundation/OpenRSI-Index.git vendor/OpenRSI-Index
git -C vendor/OpenRSI-Index sparse-checkout set RSI-Harness
git -C vendor/OpenRSI-Index checkout 21e552f396fa1c3f4d418ada4b4ac7e73dde5b2f
uv tool install --python 3.12 ./vendor/OpenRSI-Index/RSI-Harness
```

Use the [pinned Harness documentation](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/21e552f396fa1c3f4d418ada4b4ac7e73dde5b2f/RSI-Harness/README.md)
for authentication, Docker setup, clusters and recovery. The ASR tasks require an
older, separately pinned Harness interface; use section 4 for those packages.

## 3. TTS: calibrate, then run either agent

Select a TTS package, for example Qwen3-TTS Base 0.6B:

```bash
TASK_DIR="$PWD/tasks/qwen3-tts-0.6b/sglang-omni-qwen3-tts-base-0.6b-dual-mode-runtime"
```

Before starting an agent, follow that package's **Validation and operation**
section. Build its Docker image and validate pristine startup, device mapping,
assets and dependencies. In a prepared container with the task's tests at
`/tests`, the evaluator provides these entrypoints:

```bash
# Inside the prepared calibration container, with the reserved GPU/CPU lane.
/opt/sglang/bin/python3 -I /tests/calibrate.py
/opt/sglang/bin/python3 -I /tests/pool_calibrations.py /operator/calibration-record.json
```

`calibrate.py` emits `RSI_TTS_CALIBRATION=<JSON>`; save the JSON payload as the
record file. `pool_calibrations.py` emits `RSI_TTS_NOISE_CALIBRATION=<JSON>`; save
that JSON payload as the frozen baseline. Preserve the complete records.

The allocation must provide `RSI_HARNESS_EXPECTED_GPU_UUIDS` for the assigned GPU,
`RSI_TTS_CPU_LANES` as a JSON array containing one array of 16 reserved physical
CPU IDs, and `RSI_TTS_NUMA_LANES` for the corresponding NUMA nodes. These values
describe a real exclusive reservation. They are not arbitrary example settings.

Run the required held-out pristine A/A evaluation through the full Judge path.
Keep its actual outcome even if strict improvement makes it ineligible. The
operator retains B0 and manages the last accepted baseline Bk with the task's
`noise.freeze_accepted` procedure. Calibration is specific to the source,
protocol, assets, software, GPU and CPU allocation; old run scores cannot replace it.

After validation, set the Judge inputs on the host and run one agent:

```bash
# Set these paths/allocations to the ones validated above.
export RSI_TTS_BASELINE_JSON="$(cat /absolute/operator-state/baseline.json)"
export RSI_TTS_CPU_LANES="$(cat /absolute/operator-state/cpu-lanes.json)"
export RSI_TTS_NUMA_LANES="$(cat /absolute/operator-state/numa-lanes.json)"
GPU_UUID='GPU-REPLACE-WITH-YOUR-RESERVED-UUID'

# Codex + GPT-6 Astra, xhigh
sudo -E "$(command -v rsi-harness)" run "$TASK_DIR" \
  --agent codex --model gpt-6-astra --reasoning-effort xhigh \
  --agent-auth local --gpus "$GPU_UUID"

# Claude Code + Opus 5.5, max (a separate run with independent baseline state)
sudo -E "$(command -v rsi-harness)" run "$TASK_DIR" \
  --agent claude-code --model claude-opus-5-5 --reasoning-effort max \
  --agent-auth local --gpus "$GPU_UUID"
```

`--agent-auth local` uses an existing login. For API authentication, omit that
flag and supply `RSI_AGENT_API_KEY` through the operator environment; a compatible
proxy may also need `RSI_AGENT_API_BASE_URL`. Use credentials for the selected
provider. Keep calibration state on the operator/Judge side, outside Work.

These are post-calibration launch commands. The copied TTS packages expose the
calibration and promotion primitives, rather than a single automatic setup
command. Preserve their state-management requirements when automating repeated
submissions. `solution/solve.sh` restores the starting source; it is not an optimized
agent solution and does not establish a valid improved score.

## 4. ASR: use the host state adapter

Qwen3-ASR, Whisper and MOSS-Transcribe-Diarize require their own `tools/launch.py`.
It manages B0, held-out A/A, build inventory and atomic Bk transitions. Calling
the plain `rsi-harness run` command bypasses that required adapter.

The original launcher verifies seven Harness source hashes. All three manifests
match the public OpenRSI-Index revision below; current Harness `main` does not.
Install this runner in a separate environment:

```bash
git -C vendor/OpenRSI-Index fetch origin b753b9ab6c7e2f5c3e24169463bb25338b726355
git -C vendor/OpenRSI-Index worktree add --detach \
  "$PWD/vendor/OpenRSI-Index-ASR" b753b9ab6c7e2f5c3e24169463bb25338b726355
git -C vendor/OpenRSI-Index-ASR sparse-checkout set RSI-Harness
uv venv --python 3.12 .venv-asr
uv pip install --python .venv-asr/bin/python ./vendor/OpenRSI-Index-ASR/RSI-Harness
export HARNESS_PYTHON="$PWD/.venv-asr/bin/python"
```

The publication appended provenance to each README and added metadata. Those
additions predate neither the original package manifest nor the launcher's strict
file inventory. Materialize a separate execution copy that restores the exact
original README bytes and omits publication-only files:

```bash
uv run --python 3.12 python -B scripts/prepare_asr.py \
  tasks/qwen3-asr-1.7b/qwen3-asr-streaming-throughput \
  work/qwen3-asr-streaming-throughput
TASK_DIR="$PWD/work/qwen3-asr-streaming-throughput"
"$HARNESS_PYTHON" -B "$TASK_DIR/tools/check_package.py"
```

The helper verifies every original manifest hash and leaves the published package
unchanged. Use the corresponding task paths for Whisper or MOSS-Transcribe-Diarize.

Set `RSI_GPU_POOL` to one reserved GPU, `RSI_CPU_SET` to 16 reserved physical CPU
IDs separated by commas, and `RSI_STATE_DIR` to a **new, absolute host directory**.
The launcher creates the state directory itself. Configure the runner's API
credentials/base URL as described in its pinned README. Then:

```bash
export RSI_MODEL=gpt-6-astra
export RSI_REASONING_EFFORT=xhigh

# Prepare B0 and A/A using real Work/Judge execution, without a model agent.
sudo -E "$HARNESS_PYTHON" "$TASK_DIR/tools/launch.py" \
  --prepare --state-dir "$RSI_STATE_DIR" \
  --gpus "$RSI_GPU_POOL" --cpu-set "$RSI_CPU_SET" \
  --model "$RSI_MODEL" --reasoning-effort "$RSI_REASONING_EFFORT"

# Start research only after the adapter admits the prepared environment.
sudo -E "$HARNESS_PYTHON" "$TASK_DIR/tools/launch.py" \
  --state-dir "$RSI_STATE_DIR" \
  --gpus "$RSI_GPU_POOL" --cpu-set "$RSI_CPU_SET" \
  --model "$RSI_MODEL" --reasoning-effort "$RSI_REASONING_EFFORT" \
  --primary-reward reward --score-direction maximize \
  --max-submissions 64 --hours 24
```

The archived ASR launcher defaults to **Codex** and has no `--agent` option.
Changing `--model` to a Claude model does not change its agent adapter. The Claude
Code historical runs used a separate configured runner; reproducing those runs
requires that runner or an explicitly adapted host launcher with the same state
callbacks. The two generic TTS commands above are not ASR replacements.

## 5. Inspect and report results

Standard Harness runs write `logs/runs/RUN_ID/…/final_result.json` and per-round
`submissions/agent-N/report.json`. ASR stores its logs beneath the chosen host
state directory. Check the best round's completed report as well as the run's
terminal status: a failed or cancelled run can retain an earlier scored submission.

```bash
rsi-harness visualize
# Open http://127.0.0.1:8000 for the standard local logs.
```

Report the task and Harness commits, agent/model/effort, actual GPU and CPU
allocation, B0 identity, time limit and elapsed time, submission count, terminal
status, best completed round, per-mode throughput ratios and quality/latency
guards. Distinguish a missing score from zero and from the normalized B0 value of
1.0. See the [baseline evidence](../results/README.md) for this release's records.
