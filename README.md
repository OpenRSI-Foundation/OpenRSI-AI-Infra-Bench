<a id="readme-top"></a>

<p align="center">
  <img src="assets/banner.jpg" width="100%" alt="OpenRSI AI-Infra-Bench: hand-drawn notes on RadixAttention, GPUs, SGLang-Omni pipelines, rooflines, CUDA graphs and the RSI loop around the OpenRSI AI-Infra-Bench title">
</p>

<h3 align="center">Can coding agents make real AI infrastructure faster?</h3>

<p align="center">
  <a href="https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/"><img src="https://img.shields.io/badge/Blog-OpenRSI_×_SGLang--Omni-C96442?style=for-the-badge&logo=gitbook&logoColor=white" alt="Blog"></a>&nbsp;
  <a href="https://index.openrsi.foundation"><img src="https://img.shields.io/badge/Website-OpenRSI_Index-4F86D8?style=for-the-badge&logo=googleearth&logoColor=white" alt="Website"></a>&nbsp;
  <a href="https://index.openrsi.foundation/logs/"><img src="https://img.shields.io/badge/RSI_Logs-21_Trajectories-14967F?style=for-the-badge&logo=googlesheets&logoColor=white" alt="RSI Logs Viewer"></a>&nbsp;
  <a href="https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni"><img src="https://img.shields.io/badge/Hugging_Face-Logs_Archive-E08A3C?style=for-the-badge&logo=huggingface&logoColor=white" alt="Hugging Face Dataset"></a>&nbsp;
  <a href="#upstream"><img src="https://img.shields.io/badge/Upstream-14_PRs_Merged-2F8F4E?style=for-the-badge&logo=github&logoColor=white" alt="14 PRs Merged"></a>&nbsp;
  <a href="https://x.com/OpenRSI/status/2102831770458890626"><img src="https://img.shields.io/badge/Twitter-35434D?style=for-the-badge&logo=x&logoColor=white" alt="X / Twitter"></a>&nbsp;
  <a href="https://discord.gg/3EG8Qhmfsa"><img src="https://img.shields.io/badge/Discord-6674D8?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
</p>

<p align="center">
  <a href="#leaderboard"><b>🏆&nbsp;Leaderboard</b></a> &nbsp;·&nbsp;
  <a href="#highlights"><b>✨&nbsp;Highlights</b></a> &nbsp;·&nbsp;
  <a href="#how-it-works"><b>⚙️&nbsp;How&nbsp;It&nbsp;Works</b></a> &nbsp;·&nbsp;
  <a href="#tasks"><b>📦&nbsp;12&nbsp;Tasks</b></a> &nbsp;·&nbsp;
  <a href="#upstream"><b>🔁&nbsp;Upstream&nbsp;PRs</b></a> &nbsp;·&nbsp;
  <a href="#quick-start"><b>🚀&nbsp;Quick&nbsp;Start</b></a> &nbsp;·&nbsp;
  <a href="#evaluation"><b>⚖️&nbsp;Evaluation</b></a> &nbsp;·&nbsp;
  <a href="#citation"><b>📖&nbsp;Citation</b></a>
</p>

---

**OpenRSI-AI-Infra-bench** benchmarks **recursive self-improvement (RSI) in real AI serving systems**. Agents iteratively optimize a serving stack with fixed model weights and GPU resources. An independent evaluator verifies speedups under **quality and latency constraints**; each accepted improvement becomes the next baseline.

Developed [jointly by OpenRSI and the SGLang-Omni team](https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/), the benchmark includes **10 carefully reviewed tasks for omni models**. Each task provides a production serving stack with pinned source code, assets, dependencies and evaluation protocols. The collection is part of the [OpenRSI Index](https://index.openrsi.foundation/).

<details>
<summary><strong>📑 Table of Contents</strong></summary>

- [🏆 Leaderboard](#leaderboard)
- [📰 News](#news)
- [✨ Highlights](#highlights)
- [⚙️ How it works](#how-it-works)
- [📦 Tasks (12 Harbor 1.4 Packages)](#tasks)
- [🔁 From benchmark to upstream (5 Optimization Patterns & 14 Merged PRs)](#upstream)
- [🚀 Quick start](#quick-start)
  - [1. Clone and verify task integrity](#1-clone-and-verify-task-integrity)
  - [2. Install RSI-Harness and validate with `--agent oracle`](#2-install-rsi-harness-and-validate-with---agent-oracle)
  - [3. Run a coding agent](#3-run-a-coding-agent)
  - [4. Inspect local runs or download the 21 baseline trajectories](#4-inspect-local-runs-or-download-the-21-baseline-trajectories)
- [⚖️ Evaluation](#evaluation)
- [🔗 Resources](#resources)
- [🤝 Contributors & acknowledgements](#contributors)
- [📜 Provenance & license](#provenance)
- [📖 Citation](#citation)

</details>

<a id="leaderboard"></a>

## 🏆 Leaderboard

Best verified scores from **21 unguided single-agent runs** with [RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness). **Higher is better; 1.0× is the starting baseline B₀.**

**Codex:** `gpt-6-astra` (xhigh) · **Claude Code:** `claude-opus-5-5` (max).

Click a score to explore the run's progress and agent transcript; `HF ↗` opens the raw logs.

| Task | Track | Mode | Codex | Claude Code | Raw Archive |
| :--- | :---: | :--- | ---: | ---: | :--- |
| **[CosyVoice3 (0.5B)](tasks/cosyvoice3-dual-mode/)** · [Sample ↗](https://index.openrsi.foundation/tasks/cosyvoice3-dual-mode.html) | 🗣️ TTS | Dual mode | [1.172×](https://index.openrsi.foundation/logs/#run=5e67e03919819ebb) | [**1.297×**](https://index.openrsi.foundation/logs/#run=9de597863ceaafa7) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/cosyvoice3-dual-mode) |
| **[MOSS-TTS v1.5](tasks/moss-tts-v1.5-dual-mode/)** | 🗣️ TTS | Dual mode | [1.339×](https://index.openrsi.foundation/logs/#run=770379d74c291ea5) | [**1.935×**](https://index.openrsi.foundation/logs/#run=cd131351fd998975) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/moss-tts-v1.5-dual-mode) |
| **[Fish Audio S2-Pro](tasks/fish-s2-pro-dual-mode/)** | 🗣️ TTS | Dual mode | [1.803×](https://index.openrsi.foundation/logs/#run=3a65be48b77269bd) | [**6.288×**](https://index.openrsi.foundation/logs/#run=a2067dc23a561358) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/fish-s2-pro-dual-mode) |
| **[Qwen3-TTS Base 0.6B](tasks/qwen3-tts-0.6b-dual-mode/)** | 🗣️ TTS | Dual mode | [1.141×](https://index.openrsi.foundation/logs/#run=c8f89a668fcb7e92) | [**1.252×**](https://index.openrsi.foundation/logs/#run=4bdc101cfe415ada) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/qwen3-tts-0.6b-dual-mode) |
| **[Qwen3-TTS Base 1.7B](tasks/qwen3-tts-1.7b-dual-mode/)** | 🗣️ TTS | Dual mode | [1.096×](https://index.openrsi.foundation/logs/#run=bb3980b8f4ef5741) | [**1.283×**](https://index.openrsi.foundation/logs/#run=6ee3ceb2d4cacae3) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/qwen3-tts-1.7b-dual-mode) |
| **[Ming3-TTS 0.5B](tasks/ming3-tts-0.5b-nonstream/)** | 🗣️ TTS | Non-streaming | — | [**4.298×**†](https://index.openrsi.foundation/logs/#run=e7daa9d0dcc71af4) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/ming3-tts-0.5b-nonstream) |
| **[Ming3-TTS 0.5B](tasks/ming3-tts-0.5b-streaming/)** | 🗣️ TTS | Streaming | [**2.038×**](https://index.openrsi.foundation/logs/#run=a9073807b4975864) | — | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/ming3-tts-0.5b-streaming) |
| **[Ming3-TTS Tiny](tasks/ming3-tts-tiny-nonstream/)** | 🗣️ TTS | Non-streaming | [1.899×¹](https://index.openrsi.foundation/logs/#run=5da5fe181e667430) | [**3.634×**](https://index.openrsi.foundation/logs/#run=283899e5e2403399) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/ming3-tts-tiny-nonstream) |
| **[Ming3-TTS Tiny](tasks/ming3-tts-tiny-streaming/)** | 🗣️ TTS | Streaming | [**1.722×**](https://index.openrsi.foundation/logs/#run=4dc68c591bbcb7cf) | — | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/ming3-tts-tiny-streaming) |
| **[Qwen3-ASR 1.7B](tasks/qwen3-asr-1.7b-dual-mode/)** | 👂 ASR | Dual mode | [1.117×](https://index.openrsi.foundation/logs/#run=536fb8d8084974b9) | [**1.317×**†](https://index.openrsi.foundation/logs/#run=f19f174bf5532f64) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/qwen3-asr-1.7b-dual-mode) |
| **[Whisper large-v3](tasks/whisper-large-v3-dual-mode/)** | 👂 ASR | Dual mode | [1.126×](https://index.openrsi.foundation/logs/#run=62020e82a96ad29a) | [**1.979×**†](https://index.openrsi.foundation/logs/#run=fb0a3a20e9dc5775) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/whisper-large-v3-dual-mode) |
| **[MOSS-Transcribe-Diarize](tasks/moss-transcribe-diarize-dual-mode/)** | 👂 ASR | Dual mode | [1.134×](https://index.openrsi.foundation/logs/#run=5cd12dacf82da288) | [**1.490×**](https://index.openrsi.foundation/logs/#run=85955c2d14726320) | [HF ↗](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni/moss-transcribe-diarize-dual-mode) |

<sub>— No published score. † Best verified score from a cancelled run. ¹ Resumed run, totaling 23.68 h.</sub>

<details>
<summary><strong>Hardware and run notes</strong></summary>

- **Comparability.** Hardware and run durations vary; scores are reported per task without an aggregate ranking. The eight dual-mode tasks used H100 80GB HBM3 GPUs; Ming3 runs used H100 NVL or H200 GPUs. Ming3 streaming runs lasted 8 h; all current task packages default to 24 h.
- **Task version.** CosyVoice3 is pinned to SGLang-Omni `1523543056bf`, matching both published baselines.
- **Cancelled runs (†).** Ming3-TTS 0.5B non-streaming stopped after ~12.2 h; Qwen3-ASR and Whisper stopped after ~24.0–24.4 h. Each score is the best result verified before cancellation.
- **Resumed run (¹).** Ming3-TTS Tiny non-streaming (Codex) resumed after a 4-minute gap: 8.77 h + 14.91 h = 23.68 h within the 24 h budget. The first segment reached 1.358× over 13 submissions; the resumed segment reached 1.899× over 32 submissions.
- **Selection.** Calibration runs, guided-prompt ablations and multi-agent runs are excluded.

</details>

[Run records & methodology](results/README.md) · [JSON](results/main.json) · [CSV](results/runs.csv) · [Logs viewer](https://index.openrsi.foundation/logs/)

<a id="news"></a>

## 📰 News

- **[2026-11]** 🚀 **Refined Harbor 1.4 benchmark & 21 trajectories released** — All 12 SGLang-Omni tasks now run natively via `rsi-harness run` out of the box (`-89.6%` repository footprint, hardened clean-image Judge gates) alongside **21 uncompressed single-agent trajectories** on [Hugging Face](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni) and the [RSI Logs Viewer](https://index.openrsi.foundation/logs/).
- **[2026-11]** 🎤 Presented **Scaling RSI for AI Infra** at [SGLang Summit 2026](https://www.sglang.io/summit) · [[Slides]](https://docs.google.com/presentation/d/1ODcBjqT9sl0NRa7SdtV4rwULmMZI71xx/edit).
- **[2026-11]** 📝 Blog: **[OpenRSI × SGLang-Omni: Scaling RSI for AI Infra](https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/)** — Agent-discovered optimizations raised H100 throughput by **+7.6% to +326.5%** across eight omni model families, with **14 PRs** reviewed and merged upstream.

<a id="highlights"></a>

## ✨ Highlights

<table>
  <tr>
    <td align="center" width="20%"><h3>12</h3></td>
    <td align="center" width="20%"><h3>10</h3></td>
    <td align="center" width="20%"><h3>21</h3></td>
    <td align="center" width="20%"><h3>6.29×</h3></td>
    <td align="center" width="20%"><h3>14</h3></td>
  </tr>
  <tr>
    <td align="center">Harbor 1.4 tasks</td>
    <td align="center">Model checkpoints<br/><sub>(8 families)</sub></td>
    <td align="center">Public single-agent<br/>trajectories</td>
    <td align="center">Peak verified<br/>speedup</td>
    <td align="center">Upstream PRs<br/>merged</td>
  </tr>
</table>

- **100% native `rsi-harness run` across TTS & ASR.** One uniform CLI entrypoint for every task—no external `launch.py` wrappers or stateful rolling-baseline adapters. `--agent oracle` validates any task end-to-end on 1 GPU (`reward = 1.0`).
- **Isolated clean-image Judge & automatic NUMA pinning.** Every submission runs 3 fresh repetitions per mode in a clean Judge container, automatically binding **16 idle non-SMT physical CPU cores** on the GPU's NUMA node and enforcing `peak_foreign_cores <= 2.0`. Non-reference GPUs can recalibrate B₀ once via `/tests/calibrate.py` (`RSI_BASELINE_JSON`).
- **Hardened streaming, quality & anti-cheat gates.** Verifies true incremental delivery (`>= 95%` multi-chunk audio & `c50 >= 95%` on TTS; `single_delta_fraction <= 5%` on ASR; `>= 80%` diarization speaker markers on MOSS-TD), `Qwen3-ASR-1.7B` / bilingual SeedTTS intelligibility ceilings, frozen weights/sampling configs, and AST + call-site liveness.
- **Every iteration open & inspectable.** Full agent prompts, reasoning traces, code diffs, and round-by-round Judge reports for all 21 runs are open in [OpenRSI-Index-Logs](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni).

<a id="how-it-works"></a>

## ⚙️ How it works

<p align="center">
  <img src="assets/how-it-works.svg" width="100%" alt="Harnessed RSI architecture: Harbor 1.4 task package, RSI-Harness outer loop with coding agent and isolated clean-image Judge, and verified reward frontier">
</p>

[RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness) orchestrates the outer loop: the coding agent iterates inside an offline container (`/workspace/sglang-omni`) with 1 GPU and submits candidates whenever ready; each candidate is mounted read-only into a fresh Judge container that benchmarks serving throughput from scratch against the fixed reference baseline B₀ and returns structured telemetry.

Each standalone package under [`tasks/`](tasks/) follows the Harbor 1.4 layout:

```text
tasks/<task-slug>/
├── task.toml           # Harbor 1.4 resources, 24h budget, clean-image Judge config
├── instruction.md      # Self-contained agent prompt, allowed scope & evaluation contract
├── README.md           # Reference B0 table, logged baselines & GPU recalibration guide
├── environment/        # Pinned Dockerfile, lockfiles & trimmed SGLang-Omni source.tar.gz
├── solution/solve.sh   # Restores pristine baseline source (--agent oracle -> reward 1.0)
└── tests/              # Clean-image evaluator, baseline.json, calibrate.py & gates
```

<a id="tasks"></a>

## 📦 Tasks

Technical specification across all **12 benchmark packages** (best verified single-agent speedup vs. B₀, paired with detailed 3-repetition mean B₀ throughput from `tests/baseline.json`; `NS` = non-streaming, `S` = streaming):

| Package | Model Checkpoint | `sglang-omni` Base | Best Speedup | Reference B₀ Throughput (`req/s`) |
| :--- | :--- | :---: | ---: | :--- |
| [`cosyvoice3-dual-mode`](tasks/cosyvoice3-dual-mode/) | [`Fun-CosyVoice3-0.5B-2512`](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) | [**1.297×**](https://index.openrsi.foundation/logs/#run=9de597863ceaafa7) | Non-streaming `9.06` · Streaming `7.52` <sub>(H100 80GB HBM3)</sub> |
| [`moss-tts-v1.5-dual-mode`](tasks/moss-tts-v1.5-dual-mode/) | [`MOSS-TTS-v1.5`](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | [`cb75ab40`](https://github.com/sgl-project/sglang-omni/tree/cb75ab409669a6ab672fa42421b41b11af2fe263) | [**1.935×**](https://index.openrsi.foundation/logs/#run=cd131351fd998975) | Non-streaming `7.86` · Streaming `6.56` <sub>(H100 80GB HBM3)</sub> |
| [`fish-s2-pro-dual-mode`](tasks/fish-s2-pro-dual-mode/) | [`fishaudio/s2-pro`](https://huggingface.co/fishaudio/s2-pro) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) | [**6.288×**](https://index.openrsi.foundation/logs/#run=a2067dc23a561358) | Non-streaming `1.25` · Streaming `1.24` <sub>(H100 80GB HBM3)</sub> |
| [`qwen3-tts-0.6b-dual-mode`](tasks/qwen3-tts-0.6b-dual-mode/) | [`Qwen3-TTS-12Hz-0.6B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) | [**1.252×**](https://index.openrsi.foundation/logs/#run=4bdc101cfe415ada) | Non-streaming `17.58` · Streaming `19.38` <sub>(H100 80GB HBM3)</sub> |
| [`qwen3-tts-1.7b-dual-mode`](tasks/qwen3-tts-1.7b-dual-mode/) | [`Qwen3-TTS-12Hz-1.7B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) | [**1.283×**](https://index.openrsi.foundation/logs/#run=6ee3ceb2d4cacae3) | Non-streaming `18.79` · Streaming `19.97` <sub>(H100 80GB HBM3)</sub> |
| [`ming3-tts-0.5b-nonstream`](tasks/ming3-tts-0.5b-nonstream/) | [`Ming-3.0-tts-0.5B`](https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5B) | [`ca9e8789`](https://github.com/sgl-project/sglang-omni/tree/ca9e8789fcd84ed6f7272276cb99447eec751787) | [**4.298×**](https://index.openrsi.foundation/logs/#run=e7daa9d0dcc71af4) | Non-streaming `8.77` <sub>(H100 NVL)</sub> |
| [`ming3-tts-0.5b-streaming`](tasks/ming3-tts-0.5b-streaming/) | [`Ming-3.0-tts-0.5B`](https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5B) | [`0c663861`](https://github.com/sgl-project/sglang-omni/tree/0c663861d7d4a558e4f53258c4d48cfce577b47e) | [**2.038×**](https://index.openrsi.foundation/logs/#run=a9073807b4975864) | Streaming `14.99` <sub>(H200)</sub> |
| [`ming3-tts-tiny-nonstream`](tasks/ming3-tts-tiny-nonstream/) | [`Ming-3.0-tts-tiny`](https://huggingface.co/inclusionAI/Ming-3.0-tts-tiny) | [`ca9e8789`](https://github.com/sgl-project/sglang-omni/tree/ca9e8789fcd84ed6f7272276cb99447eec751787) | [**3.634×**](https://index.openrsi.foundation/logs/#run=283899e5e2403399) | Non-streaming `5.91` <sub>(H100 NVL)</sub> |
| [`ming3-tts-tiny-streaming`](tasks/ming3-tts-tiny-streaming/) | [`Ming-3.0-tts-tiny`](https://huggingface.co/inclusionAI/Ming-3.0-tts-tiny) | [`0c663861`](https://github.com/sgl-project/sglang-omni/tree/0c663861d7d4a558e4f53258c4d48cfce577b47e) | [**1.722×**](https://index.openrsi.foundation/logs/#run=4dc68c591bbcb7cf) | Streaming `5.31` <sub>(H200)</sub> |
| [`qwen3-asr-1.7b-dual-mode`](tasks/qwen3-asr-1.7b-dual-mode/) | [`Qwen3-ASR-1.7B`](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | [`eb7e97ed`](https://github.com/sgl-project/sglang-omni/tree/eb7e97ed9438ef4e4352656aec6170aeeb90966f) | [**1.317×**](https://index.openrsi.foundation/logs/#run=f19f174bf5532f64) | EN `168.92` NS / `160.60` S · ZH `179.78` NS / `172.06` S <sub>(H100 80GB HBM3)</sub> |
| [`whisper-large-v3-dual-mode`](tasks/whisper-large-v3-dual-mode/) | [`openai/whisper-large-v3`](https://huggingface.co/openai/whisper-large-v3) | [`eb7e97ed`](https://github.com/sgl-project/sglang-omni/tree/eb7e97ed9438ef4e4352656aec6170aeeb90966f) | [**1.979×**](https://index.openrsi.foundation/logs/#run=fb0a3a20e9dc5775) | EN `53.21` NS / `52.43` S · ZH `48.62` NS / `48.57` S <sub>(H100 80GB HBM3)</sub> |
| [`moss-transcribe-diarize-dual-mode`](tasks/moss-transcribe-diarize-dual-mode/) | [`MOSS-Transcribe-Diarize`](https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-Diarize) | [`8220d220`](https://github.com/sgl-project/sglang-omni/tree/8220d220703cf8d8f5c5d9a2cde00b5ed13717b8) | [**1.490×**](https://index.openrsi.foundation/logs/#run=85955c2d14726320) | EN `106.81` NS / `102.15` S · ZH `109.60` NS / `105.50` S <sub>(H100 80GB HBM3)</sub> |

> [!NOTE]
> For TTS, *streaming* means incremental multi-chunk PCM audio delivery over HTTP (`chunk_count >= 2` on ≥ 95% of requests and `c50 >= 95%`). For ASR, it means incremental SSE text deltas (`single_delta_fraction <= 5%`) after audio upload, evaluated across 1,088 English and 2,020 Mandarin SeedTTS utterances per repetition.

<a id="upstream"></a>

## 🔁 From benchmark to upstream

The same harnessed loop was used to land real optimizations in [`sgl-project/sglang-omni`](https://github.com/sgl-project/sglang-omni). Agents ran the profiling and optimization experiments; people defined the problems and reviewed the pull requests. Across 14 merged PRs, agent-found changes fall into **five recurring systems patterns**:

<p align="center">
  <img src="assets/five-patterns.svg" width="100%" alt="Five recurring serving optimization patterns across 14 merged SGLang-Omni PRs: idle-thread spinning, per-hop data conversion, redundant work, fragmented small GPU launches, and unpipelined stages">
</p>

Throughput gains on **H100** (non-streaming / streaming), measured on `sglang-omni` `main` before the first and after the last OpenRSI PR:

| Model | Merged PRs | Non-streaming | Streaming |
| :--- | :--- | ---: | ---: |
| CosyVoice3 | [#2524](https://github.com/sgl-project/sglang-omni/pull/2524) [#2555](https://github.com/sgl-project/sglang-omni/pull/2555) | +44.4% | +46.2% |
| MOSS-TTS | [#2525](https://github.com/sgl-project/sglang-omni/pull/2525) [#2859](https://github.com/sgl-project/sglang-omni/pull/2859) | +48.5% | +76.3% |
| Fish S2-Pro | [#2778](https://github.com/sgl-project/sglang-omni/pull/2778) | +9.6% | +0.3% |
| Qwen3-TTS | [#2779](https://github.com/sgl-project/sglang-omni/pull/2779) | +25.2% | +4.7% |
| Qwen3-ASR | [#2880](https://github.com/sgl-project/sglang-omni/pull/2880) [#2881](https://github.com/sgl-project/sglang-omni/pull/2881) [#2882](https://github.com/sgl-project/sglang-omni/pull/2882) | +14.2% | +5.0% |
| Whisper large-v3 | [#2901](https://github.com/sgl-project/sglang-omni/pull/2901) | +7.6% | +12.2% |
| MOSS-Transcribe-Diarize | [#3071](https://github.com/sgl-project/sglang-omni/pull/3071) | +18.8% | +30.0% |
| Ming3-TTS 0.5B | [#3136](https://github.com/sgl-project/sglang-omni/pull/3136) [#3189](https://github.com/sgl-project/sglang-omni/pull/3189) [#3190](https://github.com/sgl-project/sglang-omni/pull/3190) | **+326.5%** | **+93.9%** |

<sub>These upstream numbers come from a separate measurement protocol (`128` requests/round on `sglang-omni` `main`) than the benchmark rewards above, and some commit ranges include concurrent upstream changes (#3189 and #3190 also add people-designed opt-in streaming for Ming3-TTS). See the <a href="https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/">blog post</a> for H200 numbers and per-PR caveats.</sub>

<a id="quick-start"></a>

## 🚀 Quick start

### 1. Clone and verify task integrity

Clone this repository directly—or pull it via the `rsi-tasks/sglang-omni` submodule inside `OpenRSI-Index`:

```bash
# Option A: standalone repository
git clone https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench.git
cd OpenRSI-AI-Infra-Bench

# Option B: via OpenRSI-Index
git clone --recurse-submodules https://github.com/OpenRSI-Foundation/OpenRSI-Index.git
cd OpenRSI-Index/rsi-tasks/sglang-omni

# Verify all 12 task manifests, SHA-256 hashes, and Python/JSON/TOML/shell syntax (CPU-only)
python3 -B scripts/verify.py
```

Expected output:

```text
PASS: 12 task packages; 320 files match the source snapshot.
Checked hashes, executable modes, and Python/JSON/TOML/shell syntax. No GPU evaluation performed.
```

### 2. Install RSI-Harness and validate with `--agent oracle`

**Requirements:** Linux, Docker Engine 26+, NVIDIA Container Toolkit, Python 3.12, 1 GPU (80 GB+ VRAM recommended), 16 idle physical CPU cores, 128 GiB RAM, and ~200 GiB free SSD storage.

Install [RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness), then run `--agent oracle` on any TTS or ASR task to verify Docker image build, NUMA core pinning, and full 3-repetition Judge evaluation (`reward = 1.0`):

```bash
rsi-harness run tasks/cosyvoice3-dual-mode --agent oracle --gpus 0
rsi-harness run tasks/qwen3-asr-1.7b-dual-mode --agent oracle --gpus 0
```

<details>
<summary><strong>Expected clean-image Judge verification output (<code>reward = 1.0</code>)</strong></summary>

```text
[judge] Pinned 16 idle physical CPU cores on GPU 0 NUMA node 0 (peak_foreign_cores <= 2.0)
[judge] Unmodified baseline source detected -> running 3x verification repeats per mode
[judge] Non-streaming mean throughput : R_n = 1.000x  (WER <= 2.0%, P95 <= 1.03x B0)
[judge] Streaming mean throughput     : R_s = 1.000x  (multi-chunk >= 95%, c50 >= 95%)
[judge] All quality, latency, streaming, and cleanup gates PASSED -> /logs/verifier/reward.txt = 1.0
```

</details>

### 3. Run a coding agent

All 12 TTS and ASR tasks share the exact same `rsi-harness run` interface:

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

> [!TIP]
> **Custom GPU SKUs (`RSI_BASELINE_JSON`):** Each task bakes reference B₀ metrics into `tests/baseline.json`. When running optimization loops on a different GPU SKU (e.g., PCIe H100 NVL vs. SXM5 H100, or A100/B200), measure a fresh 3-repetition B₀ once with `/opt/sglang/bin/python3 -I -B /tests/calibrate.py` and export `RSI_BASELINE_JSON`—see [docs/running.md](docs/running.md#4-optional-recalibrating-reference-b_0-for-custom-gpu-skus).

### 4. Inspect local runs or download the 21 baseline trajectories

```bash
# Visualize local RSI-Harness runs at http://127.0.0.1:8000
rsi-harness visualize

# Download one task's published trajectories (or omit --include for all 21 runs)
hf download OpenRSI-Foundation/OpenRSI-Index-Logs --repo-type dataset \
  --include "sglang-omni/cosyvoice3-dual-mode/*" --local-dir OpenRSI-Index-Logs
```

📖 **[Full setup, GPU calibration and execution guide →](docs/running.md)**

<a id="evaluation"></a>

## ⚖️ Evaluation

The target is **serving throughput**, subject to each task's quality, tail-latency, streaming-continuity, resource, and integrity gates. A faster implementation is rejected (`reward = 0`) if it violates any guard.

For all eight dual-mode tasks (TTS and ASR), let **Rₛ** and **Rₙ** be the streaming and non-streaming throughput ratios against the reference baseline **B₀** (for ASR, each mode ratio is the geometric mean across English and Mandarin):

$$
\mathrm{reward} = R_s^{2/3} \, R_n^{1/3}
$$

**Both modes must strictly improve** over B₀ (`> 1.0`) for modified candidates, preventing a gain in one mode from masking a regression in the other. Ming3's four single-mode tasks score the target mode's throughput ratio against B₀.

| Gate Layer | Workload and checks |
| :--- | :--- |
| **TTS (9 tasks)** | 1,088 English SeedTTS requests per repetition; concurrency 16; 3 repetitions per mode; independent `Qwen3-ASR-1.7B` WER verification (≤ 2.0%), 3% latency/RTF/TTFA P95 budgets, and ≥ 95% multi-chunk streaming (`c50` ≥ 95%) |
| **ASR (3 tasks)** | 1,088 English + 2,020 Mandarin SeedTTS requests per repetition; non-streaming HTTP and post-upload SSE; 3 repetitions per language and mode; strict WER/CER ceilings, `single_delta_fraction` ≤ 5%, and ≥ 80% speaker-turn tags on MOSS-TD |
| **System guards** | Automatic NUMA-local 16-physical-core pinning, host contention gate (`peak_foreign_cores <= 2.0`), frozen weights & sampling semantics, AST & call-site liveness checks, and `0 MiB` GPU process cleanup |

<a id="resources"></a>

## 🔗 Resources

| Resource | Link |
| :--- | :--- |
| Blog post | [OpenRSI × SGLang-Omni: Scaling RSI for AI Infra](https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/) |
| Interactive Logs Viewer | [index.openrsi.foundation/logs](https://index.openrsi.foundation/logs/) (all 21 single-agent runs) |
| Trajectory dataset | [OpenRSI-Foundation/OpenRSI-Index-Logs (`sglang-omni/`)](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni) |
| Featured Task Sample | [CosyVoice3 Dual-Mode (`cosyvoice3-dual-mode`)](https://index.openrsi.foundation/tasks/cosyvoice3-dual-mode.html) |
| OpenRSI Index | [index.openrsi.foundation](https://index.openrsi.foundation) · [GitHub](https://github.com/OpenRSI-Foundation/OpenRSI-Index) (`rsi-tasks/sglang-omni`) |
| Runner & Pipeline | [RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness) · [RSI-Anything (`CONTRIBUTING.md`)](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/CONTRIBUTING.md) |
| Serving framework | [SGLang-Omni](https://github.com/sgl-project/sglang-omni) |
| Task collection | [Browse `tasks/`](tasks/) · [Running guide](docs/running.md) · [Baseline records](results/README.md) |
| Contribute a task | [Call for contributors](https://github.com/OpenRSI-Foundation/OpenRSI-Index#-call-for-contributors) |

<a id="contributors"></a>

## 🤝 Contributors & acknowledgements

Led by **[Zhuofeng Li](https://zhuofeng-li.github.io/)**, **[Aaron Tian](https://github.com/db-ol)**, and **[Chenyang Zhao](https://github.com/zhaochenyang20)**, with **[Yichen Feng](https://yichenfeng.me/)**, **[Wenhao Chai](https://wenhaochai.com/)**, **[Xinyang Han](https://davidhanx.github.io/)**, **[Cara Li](https://caralinotes.com/)**, **[Shujia Liang](https://vincentcaptain.github.io/)**, and **[Yuetai Li](https://yuetl9.github.io/)**.

We thank the **[SGLang-Omni](https://github.com/sgl-project/sglang-omni)** maintainers and contributors for many rounds of code review, design guidance, and independent benchmark reproductions. Interested in building new AI infrastructure RSI benchmarks? See the **[OpenRSI Call for Contributors](https://github.com/OpenRSI-Foundation/OpenRSI-Index#-call-for-contributors)**.

<a id="provenance"></a>

## 📜 Provenance & license

The benchmark tasks originate from OpenRSI Index discussions [#154](https://github.com/OpenRSI-Foundation/OpenRSI-Index/discussions/154) (TTS) and [#257](https://github.com/OpenRSI-Foundation/OpenRSI-Index/discussions/257) (ASR). All 21 single-agent baseline trajectories are archived uncompressed in [OpenRSI-Index-Logs](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/main/sglang-omni).

This repository carries the [Apache-2.0 license](LICENSE). Bundled source, model weights, and datasets retain their own upstream licenses and attribution requirements.

<a id="citation"></a>

## 📖 Citation

If you find OpenRSI-AI-Infra-Bench useful in your research or engineering, please cite:

```bibtex
@misc{li2026openrsisglangomni,
  title  = {{OpenRSI} $\times$ {SGLang-Omni}: Scaling {RSI} for {AI} Infra},
  author = {Li, Zhuofeng and Tian, Aaron and Feng, Yichen and Chai, Wenhao and
            Han, Xinyang and Li, Cara and Liang, Shujia and Li, Yuetai and
            Zhao, Chenyang},
  year   = {2026},
  month  = nov,
  url    = {https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/}
}
```

<p align="right"><a href="#readme-top">↑ Back to top</a></p>

---

<p align="center">
  Built by the <a href="https://github.com/OpenRSI-Foundation"><b>OpenRSI Foundation</b></a>
  with the <a href="https://github.com/sgl-project/sglang-omni"><b>SGLang-Omni</b></a> community.
</p>
