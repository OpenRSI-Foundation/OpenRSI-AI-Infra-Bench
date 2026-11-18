<p align="center">
  <img src="assets/banner.svg" width="100%" alt="OpenRSI AI Infra — a benchmark for agents that optimize AI serving systems">
</p>

<h3 align="center">A benchmark for coding agents that improve real AI infrastructure.</h3>

<p align="center">
  <a href="#tasks">Tasks</a> ·
  <a href="#baselines">Baselines</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#evaluation">Evaluation</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Models-10-5b59db" alt="10 models">
  <img src="https://img.shields.io/badge/Task_packages-12-30928a" alt="12 task packages">
  <img src="https://img.shields.io/badge/Agents-Codex_%7C_Claude_Code-435063" alt="Codex and Claude Code">
  <img src="https://img.shields.io/badge/License-Apache_2.0-667181" alt="Apache 2.0">
</p>

**OpenRSI AI Infra** evaluates whether coding agents can make AI serving systems
faster while preserving their quality and latency requirements. Agents profile
the runtime, propose changes, run experiments and submit code for evaluation.
Model weights stay fixed; improvements must pass the task's evaluator.

The initial collection focuses on **SGLang-Omni speech serving**: 10 models across
text-to-speech (TTS) and automatic speech recognition (ASR), packaged as 12
reproducible tasks with pinned source, assets, dependencies and evaluation rules.

> **At a glance:** real serving workloads · streaming and non-streaming objectives ·
> single-GPU evaluation · Codex and Claude Code baselines.

<!-- TODO: Add the project website, paper and public results dashboard when available. -->

## Tasks

**Eight dual-mode tasks** evaluate streaming and non-streaming together.
**Four Ming3 tasks** evaluate the two modes separately, for 0.5B and Tiny.

| Model | Track | Evaluation modes | Default agent budget | Package |
| :--- | :--- | :--- | :--- | :--- |
| **CosyVoice3** | TTS | Dual mode | 24 h | [Task](tasks/cosyvoice3/sglang-omni-cosyvoice3-dual-mode-runtime/) |
| **MOSS-TTS v1.5** | TTS | Dual mode | 24 h | [Task](tasks/moss-tts-v1.5/sglang-omni-moss-v1.5-dual-mode-runtime/) |
| **Fish S2-Pro** | TTS | Dual mode | 24 h | [Task](tasks/fish-s2-pro/sglang-omni-fish-s2-pro-dual-mode-runtime/) |
| **Qwen3-TTS Base 0.6B** | TTS | Dual mode | 24 h | [Task](tasks/qwen3-tts-0.6b/sglang-omni-qwen3-tts-base-0.6b-dual-mode-runtime/) |
| **Qwen3-TTS Base 1.7B** | TTS | Dual mode | 24 h | [Task](tasks/qwen3-tts-1.7b/sglang-omni-qwen3-tts-base-1.7b-dual-mode-runtime/) |
| **Ming3-TTS 0.5B** | TTS | Separate NS / S | 24 h / 8 h | [Non-streaming](tasks/ming3-0.5b/sglang-omni-ming3-0.5b-nonstream/) · [Streaming](tasks/ming3-0.5b/sglang-omni-ming3-0.5b-streaming/) |
| **Ming3-TTS Tiny** | TTS | Separate NS / S | 24 h / 8 h | [Non-streaming](tasks/ming3-tiny/sglang-omni-ming3-tiny-nonstream/) · [Streaming](tasks/ming3-tiny/sglang-omni-ming3-tiny-streaming/) |
| **Qwen3-ASR 1.7B** | ASR | Dual mode | 24 h | [Task](tasks/qwen3-asr-1.7b/qwen3-asr-streaming-throughput/) |
| **Whisper large-v3** | ASR | Dual mode | 24 h | [Task](tasks/whisper-large-v3/whisper-asr-streaming-throughput/) |
| **MOSS-Transcribe-Diarize** | ASR | Dual mode | 24 h | [Task](tasks/moss-transcribe-diarize/moss-transcribe-diarize-streaming-throughput/) |

For TTS, streaming means incremental audio delivery. For ASR, it means text
delivered over SSE after the audio upload; it is not live microphone streaming.
The Ming3 streaming packages use a different source baseline and compatibility
port from their non-streaming counterparts.

Each task includes:

| File or directory | What it provides |
| :--- | :--- |
| `instruction.md` | The objective, allowed changes and constraints |
| `task.toml` | Resources, time limits and runtime configuration |
| `environment/` | Container build, pinned runtime and model asset specifications |
| `tests/` | Evaluator, fixed assets, quality checks and scoring rules |
| `solution/solve.sh` | Restoration of the starting implementation |
| `publication.json` | Original source revision and file hashes |

## Baselines

We report the **Main experiments** for two coding agents running under RSI-Harness:

| Agent | Model | Reasoning effort |
| :--- | :--- | :--- |
| **Codex** | `gpt-6-astra` | `xhigh` |
| **Claude Code** | `claude-opus-5-5` | `max` |

The table shows the **best recorded reward per task and agent** among archived
research runs in the Main repositories. Each selected score was checked against
its best submission's completed evaluator report. Higher is better; 1.0× is the
normalized starting performance. These are historical results, not new evaluations
of this repository snapshot.

| Task | Scored modes | Codex | Claude Code | Archived runs¹ |
| :--- | :--- | ---: | ---: | :---: |
| CosyVoice3 | Dual | 1.172× | 1.297× | 1 / 1 |
| MOSS-TTS v1.5 | Dual | 1.440× | 2.195× | 2 / 2 |
| Fish S2-Pro | Dual | 1.803× | 6.288× | 2 / 1 |
| Qwen3-TTS Base 0.6B | Dual | 1.141× | 1.252× | 1 / 2 |
| Qwen3-TTS Base 1.7B | Dual | 1.096× | 1.283× | 2 / 1 |
| Ming3-TTS 0.5B | Non-streaming | Not archived‡ | 4.298×† | — / 2 |
| Ming3-TTS Tiny | Non-streaming | 1.899×† | 3.634× | 2 / 1 |
| Qwen3-ASR 1.7B | Dual | 1.139× | 1.317×† | 2 / 1 |
| Whisper large-v3 | Dual | 1.126× | 1.979×† | 1 / 1 |
| MOSS-Transcribe-Diarize | Dual | 1.134× | 1.490× | 1 / 1 |

¹ Run counts are **Codex / Claude Code**, including interrupted and unscored
research runs. Preparation runs, model-scaling experiments and other agent
frameworks are excluded. The table is a best-observed summary, not a mean over seeds.

† The overall run ended as `failed` or `cancelled`, but retained the shown score
from an earlier completed submission. ‡ The Main tracking sheet marks the
Ming3-0.5B Codex run as done; its numerical result was not found in the inspected
archive, so no score is assigned.

<details>
<summary><strong>Hardware, budgets and version notes</strong></summary>

- Most selected runs used one **H100 80GB HBM3** and a **24-hour** budget.
- Ming3 Tiny used **H200 / 24 h** for Codex and **H100 NVL / 12 h** for Claude Code.
  Its Codex run failed after about 14.9 h. Ming3-0.5B Claude Code used H100 NVL with
  a 24 h budget and was cancelled after about 12.2 h.
- Qwen3-ASR and Whisper Claude Code runs had 48 h configured budgets and were
  cancelled after about 24.4 h and 24.0 h, respectively. Runtime can include
  evaluator overhead beyond an agent's configured limit.
- **CosyVoice3 differs by version:** Main baselines use SGLang-Omni
  `1523543056bf` (0.1.7); the task copied from SGNOMI is the later guided version at
  `fa90213e1674` (0.1.9). Its Main scores do not measure that later task.
- Ming3 scores above are **non-streaming only**. The two streaming task packages
  are included in the benchmark but have no scores in this Main selection.
- Hardware, time budgets and the number of attempts vary. We therefore do not
  report an aggregate ranking or a controlled agent-to-agent win rate.

</details>

**Results:** [Run records and methodology](results/README.md) ·
[Machine-readable snapshot](results/main.json) ·
Public dashboard: **coming soon**.

<!-- TODO: Replace the dashboard placeholder with the public Main-results URL. -->

## Quick start

### 1. Get the tasks

```bash
git clone https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra.git
cd OpenRSI-AI-Infra

# Verify task contents and syntax without a GPU.
uv run --python 3.12 python -B scripts/verify.py
```

### 2. Prepare the environment

Use **Linux, Docker, NVIDIA Container Toolkit and Python 3.12**, with one compatible
GPU, 16 reserved physical CPU cores and 128 GiB RAM. Install
[RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness),
then build and validate the selected task's environment.

Before research, measure a fresh **B0 calibration** and run the required held-out
**A/A check** on the same hardware, runtime and allocation. Keep the operator-owned
baseline state outside the agent workspace. The task README defines the exact
preparation procedure; historical scores are not calibration inputs.

### 3. Run a coding agent

For a **prepared TTS task**, launch either agent with the task's calibrated Judge
inputs configured:

```bash
TASK_DIR="$PWD/tasks/qwen3-tts-0.6b/sglang-omni-qwen3-tts-base-0.6b-dual-mode-runtime"

# Codex
sudo -E "$(command -v rsi-harness)" run "$TASK_DIR" \
  --agent codex --model gpt-6-astra --reasoning-effort xhigh \
  --agent-auth local --gpus 0

# Claude Code — launch as a separate experiment with independent baseline state
sudo -E "$(command -v rsi-harness)" run "$TASK_DIR" \
  --agent claude-code --model claude-opus-5-5 --reasoning-effort max \
  --agent-auth local --gpus 0
```

`--agent-auth local` reuses an existing login. API-key authentication is also
supported by the Harness. Replace GPU `0` with your reserved GPU selector.

> **ASR uses a different entrypoint.** Qwen3-ASR, Whisper and MOSS-Transcribe-Diarize
> require their task-local `tools/launch.py` host state adapter and a matching
> Harness revision. Follow the [full running guide](docs/running.md#4-asr-use-the-host-state-adapter)
> for preparation and launch commands.

### 4. Inspect the results

```bash
rsi-harness visualize
# Open http://127.0.0.1:8000
```

Inspect `final_result.json` for run status and best reward, then check the selected
round's `submissions/agent-N/report.json` for evaluator status. Preserve task and
runner commits, hardware, calibration identity, budgets and per-mode metrics.

→ **[Full setup, calibration and execution guide](docs/running.md)**

## Evaluation

The optimization target is serving throughput subject to the task's quality,
latency, resource and integrity checks. A faster implementation can still be
ineligible if it fails a guard.

For dual-mode tasks, let $R_s$ and $R_n$ be streaming and non-streaming throughput
ratios against the initial baseline $B_0$:

$$
\mathrm{reward} = R_s^{2/3} \, R_n^{1/3}.
$$

**Both modes must improve** over the last accepted baseline $B_k$ before a
candidate is eligible. A higher combined score cannot offset a regression in one
mode. Ming3's separate tasks score the selected mode's throughput ratio against
$B_0$. The task evaluator defines the exact aggregation and acceptance rules.

| Track | Workload and evaluation |
| :--- | :--- |
| TTS | 1,088 English requests per repetition; concurrency 16; three repetitions per evaluated mode; independent ASR-based quality checks |
| ASR | English and Chinese workloads; non-streaming and post-upload SSE; three repetitions per language and mode |
| Guards | Task-specific WER/error ceilings, latency and other performance tolerances, complete coverage, source integrity and cleanup |

Model weights, sampling semantics and fixed evaluation assets are protected.
WER checks transcription accuracy; they do not establish perceptual audio quality.

## Project links

| Resource | Link |
| :--- | :--- |
| Project website | Coming soon |
| Paper / technical report | Coming soon |
| Public Main-results dashboard | Coming soon |
| Task collection | [Browse tasks](tasks/) |
| Runner | [RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness) |
| Serving framework | [SGLang-Omni](https://github.com/sgl-project/sglang-omni) |

## Provenance and license

The initial task collection comes from
[OpenRSI-Index / SGNOMI](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/21e552f396fa1c3f4d418ada4b4ac7e73dde5b2f/rsi-tasks/SGNOMI).
Original task directory names, evaluators, pinned assets and publication metadata
are retained. Main baseline results were collected separately from the run
repositories identified by the project tracking sheet; their task versions are
recorded with the results.

The repository carries the upstream [Apache-2.0 license](LICENSE). Bundled source,
model weights and datasets retain their own licenses and attribution requirements.

Built by **OpenRSI Foundation**, with the **SGLang-Omni** community.
