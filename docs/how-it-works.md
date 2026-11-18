# How It Works

[Overview](../README.md) · **How it works** · [Evaluation](evaluation.md) · [Running guide](running.md) · [Upstream results](upstream-results.md) · [24h results](../results/README.md)

<p align="center">
  <img src="../assets/how-it-works.svg" width="100%" alt="Harnessed RSI architecture: Harbor 1.4 task package, RSI-Harness outer loop with coding agent and isolated clean-image Judge, and verified score frontier">
</p>

OpenRSI-AI-Infra-Bench pairs self-contained [Harbor 1.4](../tasks/) serving benchmarks with [RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness) to run autonomous, verifier-checked single-GPU hill-climbing loops.

## 1. Two Nested Loops

1. **Inner loop — Coding Agent (`Work` container):**
   - Runs inside a persistent offline container (`/workspace/sglang-omni`, `allow_internet = false`) with **1 exclusive GPU**, frozen model weights, and fixed SeedTTS datasets.
   - Profiles CPU thread scheduling, inter-stage serialization, and GPU kernel traces; edits runtime code inside the permitted `sglang_omni/` scope; runs local micro-benchmarks; and submits a candidate snapshot whenever ready.
2. **Outer loop — Isolated Verifier (`Clean-Image Judge` container):**
   - After ensuring the Work container leaves `0 MiB` of residual GPU memory, `RSI-Harness` mounts the submitted workspace **read-only** into a fresh Judge container built from the unmodified task image.
   - The Judge pins **16 distinct non-SMT physical CPU cores** on the GPU's NUMA node, executes **3 fresh repetitions per mode** (and per language for ASR), checks every quality, tail-latency, streaming-continuity, and integrity guard against the fixed initial baseline **B₀**, and returns structured telemetry (`report.json` + logs) to guide the next round.

> [!IMPORTANT]
> **Hill-climbing without baseline drift:** Every submission in a run is scored against the **same initial baseline B₀**, while the agent builds on its best verified runtime modifications across rounds. A faster candidate that violates any quality, latency, or streaming guard receives `score = 0`.

## 2. Harbor 1.4 Task Anatomy

Every directory under [`tasks/`](../tasks/) is a standalone Harbor 1.4 package runnable directly with `rsi-harness run`:

```text
tasks/<task-slug>/
├── task.toml           # Harbor 1.4 resources, 24h default budget, clean-image Judge config
├── instruction.md      # Self-contained agent prompt, permitted scope & scoring contract
├── README.md           # Task overview, reference B0 metrics & GPU recalibration notes
├── environment/        # Pinned Dockerfile, uv/pip lockfiles & trimmed source.tar.gz
├── solution/solve.sh   # Restores pristine baseline source (--agent oracle -> reward 1.0)
└── tests/              # Isolated Judge harness, baseline.json, calibrate.py & guards
```

| Component | Agent visibility | Role in the loop |
| :--- | :---: | :--- |
| `/workspace/sglang-omni` | Read / Write | Unpacked `SGLang-Omni` runtime edited by the agent (sampling semantics & model weights remain locked) |
| `/workspace/research` | Read / Write | Unscored scratchpad for profiling scripts, FlameGraphs, traces, and round-by-round ablation notes |
| `environment/` | Build-time only | Rebuilds deterministic container layers and verifies SHA-256 hashes of model weights & SeedTTS splits |
| `tests/` | Judge-only (`ro`) | Runs outside the agent workspace in a clean container; enforces `baseline.json` gates and writes `reward.txt` |
| `solution/solve.sh` | Oracle-only | Restores unmodified `SGLang-Omni` source so `rsi-harness run <task> --agent oracle` validates the full evaluation path (`reward = 1.0`) |

## 3. Trajectory Artifacts & 24-Hour Cutoff

During a run, `RSI-Harness` records every round under `logs/runs/<run-id>/`:

- `started_at` and `evolve_state.json` — wall-clock timestamps (`at - started_at`), submission sequence, and running best verified score.
- `submissions/agent-N/report.json` and `test_output.txt` — exact per-repetition QPS, RTF, P95 latency / TTFA / TTFT, corpus WER / CER, streaming chunk / SSE delta statistics, and guard margins.
- Agent session transcripts and workspace diffs for full post-hoc auditability.

The [main leaderboard](../README.md#leaderboard) and [24-hour audit](../results/README.md) select the highest verified score achieved within `0 <= at - started_at <= 86400` seconds on a single H100 80GB HBM3 GPU across all 16 paired runs.
