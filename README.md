<a id="readme-top"></a>

<p align="center">
  <img src="assets/banner.jpg" width="100%" alt="OpenRSI AI-Infra-Bench: coding agents optimize SGLang-Omni serving">
</p>

<h3 align="center">Can coding agents make real AI infrastructure faster?</h3>

<p align="center">
  <a href="https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/"><img src="https://img.shields.io/badge/Blog-OpenRSI_×_SGLang--Omni-C85A35?style=for-the-badge&logo=gitbook&logoColor=white&labelColor=2B2927" alt="Blog"></a>&nbsp;
  <a href="results/archive.md"><img src="https://img.shields.io/badge/RSI_Logs-16_Runs-C9862E?style=for-the-badge&logo=googlesheets&logoColor=white&labelColor=2B2927" alt="16 benchmark runs"></a>&nbsp;
  <a href="docs/upstream-results.md"><img src="https://img.shields.io/badge/Upstream-11_PRs_Merged-4D6B5D?style=for-the-badge&logo=github&logoColor=white&labelColor=2B2927" alt="11 PRs Merged"></a>&nbsp;
  <a href="https://x.com/OpenRSI/status/2119869682929066288"><img src="https://img.shields.io/badge/X-@OpenRSI-4A4742?style=for-the-badge&logo=x&logoColor=white&labelColor=2B2927" alt="X / Twitter"></a>
</p>

---

**OpenRSI-AI-Infra-bench** benchmarks **recursive self-improvement (RSI) in real AI serving systems**. Agents iteratively optimize a serving stack with fixed model weights and GPU resources. An independent evaluator verifies speedups under quality and latency constraints; each accepted improvement becomes the next baseline.

Developed jointly by [OpenRSI and the SGLang-Omni team](https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/), the benchmark includes **8 carefully reviewed tasks for omni models**. Each task provides a production serving stack with pinned source code, assets, dependencies and evaluation protocols. The collection is part of the [OpenRSI Index](https://index.openrsi.foundation/).

<a id="highlights"></a>

## ✨ Highlights

- **Built with SGLang maintainers.** OpenRSI collaborated with SGLang-Omni maintainers to design tasks grounded in real-world production serving workloads. Agent-discovered optimizations have already resulted in [14 PRs merged upstream](https://github.com/sgl-project/sglang-omni/pulls?q=is%3Apr+state%3Aclosed+author%3AZhuofeng-Li).

- **Lightweight, single-GPU RSI.** Each task runs on just 1 × GPU, making iterative RSI experiments accessible without requiring large GPU clusters. Agents progressively improve serving throughput by building on their best results from previous rounds.

- **Fully open-source and reproducible.** We fully open-source the tasks, RSI harness, agent trajectories, and execution logs, enabling anyone to reproduce experiments, benchmark their agents on the leaderboard, and contribute new optimization strategies.

<a id="leaderboard"></a>

## 🏆 Leaderboard

Best verified score within the **first 24 hours** of each unguided single-agent run. **1.0× is the initial baseline; higher is better.** All runs use one H100 80GB HBM3 GPU.

**Codex:** `gpt-6-astra` · `xhigh` reasoning. **Claude Code:** `claude-opus-5-5` · `max` reasoning.

| Task | Track | Codex | Claude Code | Trajectories |
| :--- | :---: | ---: | ---: | :--- |
| [**CosyVoice3 (0.5B)**](https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench/tree/main/tasks/cosyvoice3-dual-mode) | 🗣️ TTS | [1.172×](https://index.openrsi.foundation/logs/#run=5e67e03919819ebb&tab=submissions) | [**1.297×**](https://index.openrsi.foundation/logs/#run=9de597863ceaafa7&tab=submissions) | [View logs ↗](https://index.openrsi.foundation/logs/#run=5e67e03919819ebb) |
| [**MOSS-TTS v1.5**](https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench/tree/main/tasks/moss-tts-v1.5-dual-mode) | 🗣️ TTS | [1.339×](https://index.openrsi.foundation/logs/#run=770379d74c291ea5&tab=submissions) | [**1.935×**](https://index.openrsi.foundation/logs/#run=cd131351fd998975&tab=submissions) | [View logs ↗](https://index.openrsi.foundation/logs/#run=770379d74c291ea5) |
| [**Fish Audio S2-Pro**](https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench/tree/main/tasks/fish-s2-pro-dual-mode) | 🗣️ TTS | [1.739×](https://index.openrsi.foundation/logs/#run=3a65be48b77269bd&tab=submissions) | [**6.288×**](https://index.openrsi.foundation/logs/#run=a2067dc23a561358&tab=submissions) | [View logs ↗](https://index.openrsi.foundation/logs/#run=3a65be48b77269bd) |
| [**Qwen3-TTS Base 0.6B**](https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench/tree/main/tasks/qwen3-tts-0.6b-dual-mode) | 🗣️ TTS | [1.141×](https://index.openrsi.foundation/logs/#run=c8f89a668fcb7e92&tab=submissions) | [**1.252×**](https://index.openrsi.foundation/logs/#run=4bdc101cfe415ada&tab=submissions) | [View logs ↗](https://index.openrsi.foundation/logs/#run=c8f89a668fcb7e92) |
| [**Qwen3-TTS Base 1.7B**](https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench/tree/main/tasks/qwen3-tts-1.7b-dual-mode) | 🗣️ TTS | [1.096×](https://index.openrsi.foundation/logs/#run=bb3980b8f4ef5741&tab=submissions) | [**1.283×**](https://index.openrsi.foundation/logs/#run=6ee3ceb2d4cacae3&tab=submissions) | [View logs ↗](https://index.openrsi.foundation/logs/#run=bb3980b8f4ef5741) |
| [**Qwen3-ASR 1.7B**](https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench/tree/main/tasks/qwen3-asr-1.7b-dual-mode) | 👂 ASR | [1.117×](https://index.openrsi.foundation/logs/#run=536fb8d8084974b9&tab=submissions) | [**1.278×**](https://index.openrsi.foundation/logs/#run=f19f174bf5532f64&tab=submissions) | [View logs ↗](https://index.openrsi.foundation/logs/#run=536fb8d8084974b9) |
| [**Whisper large-v3**](https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench/tree/main/tasks/whisper-large-v3-dual-mode) | 👂 ASR | [1.126×](https://index.openrsi.foundation/logs/#run=62020e82a96ad29a&tab=submissions) | [**1.979×**](https://index.openrsi.foundation/logs/#run=fb0a3a20e9dc5775&tab=submissions) | [View logs ↗](https://index.openrsi.foundation/logs/#run=62020e82a96ad29a) |
| [**MOSS-Transcribe-Diarize**](https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench/tree/main/tasks/moss-transcribe-diarize-dual-mode) | 👂 ASR | [1.134×](https://index.openrsi.foundation/logs/#run=5cd12dacf82da288&tab=submissions) | [**1.490×**](https://index.openrsi.foundation/logs/#run=85955c2d14726320&tab=submissions) | [View logs ↗](https://index.openrsi.foundation/logs/#run=5cd12dacf82da288) |
<details>
<summary><strong>Scoring and comparison protocol</strong></summary>

Each mode's ratio is candidate mean throughput / initial B₀ mean throughput, with three repetitions per mean. Combine streaming (Rₛ) and non-streaming (Rₙ) as:

```math
\mathrm{score} = R_s^{2/3} \, R_n^{1/3}
```

ASR uses the geometric mean of English and Mandarin ratios within each mode. Modified candidates must improve both modes and pass all [quality, latency, streaming, and integrity gates](docs/evaluation.md).

Both agents are ranked by their best valid score within each run's first 24 hours, using that run's fixed B₀. See the [cutoff audit](results/README.md#evidence-and-limits) for hardware, protocol, and source-snapshot comparisons.

</details>

<a id="tasks"></a>

## 📦 Tasks

OpenRSI-AI-Infra-Bench targets omni model serving optimization in **SGLang-Omni**: improve both streaming and non-streaming throughput without degrading quality, latency, or streaming continuity. Its **8 tasks across 7 model families** cover core speech models for text-to-speech, recognition, and diarization. Each task is **self-contained and ready to run**, with pinned code, dependencies, model assets, and evaluators, plus reference throughput and GPU calibration instructions.

After [installing RSI-Harness](docs/running.md#2-install-rsi-harness) and configuring local credentials for your chosen agent, copy a command below and run it from the repository root. Each command starts an optimization run with a default **24-hour budget** on **GPU 0**, using `--agent-auth local`.

| Task package | Model checkpoint | SGLang-Omni base commit | Run with Codex | Run with Claude Code |
| :--- | :--- | :--- | :--- | :--- |
| [`cosyvoice3-dual-mode`](tasks/cosyvoice3-dual-mode/) | [`Fun-CosyVoice3-0.5B-2512`](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) | `rsi-harness run tasks/cosyvoice3-dual-mode --agent codex --model gpt-6-astra --reasoning-effort xhigh --agent-auth local --gpus 0` | `rsi-harness run tasks/cosyvoice3-dual-mode --agent claude-code --model claude-opus-5-5 --reasoning-effort max --agent-auth local --gpus 0` |
| [`moss-tts-v1.5-dual-mode`](tasks/moss-tts-v1.5-dual-mode/) | [`MOSS-TTS-v1.5`](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | [`cb75ab40`](https://github.com/sgl-project/sglang-omni/tree/cb75ab409669a6ab672fa42421b41b11af2fe263) | `rsi-harness run tasks/moss-tts-v1.5-dual-mode --agent codex --model gpt-6-astra --reasoning-effort xhigh --agent-auth local --gpus 0` | `rsi-harness run tasks/moss-tts-v1.5-dual-mode --agent claude-code --model claude-opus-5-5 --reasoning-effort max --agent-auth local --gpus 0` |
| [`fish-s2-pro-dual-mode`](tasks/fish-s2-pro-dual-mode/) | [`fishaudio/s2-pro`](https://huggingface.co/fishaudio/s2-pro) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) | `rsi-harness run tasks/fish-s2-pro-dual-mode --agent codex --model gpt-6-astra --reasoning-effort xhigh --agent-auth local --gpus 0` | `rsi-harness run tasks/fish-s2-pro-dual-mode --agent claude-code --model claude-opus-5-5 --reasoning-effort max --agent-auth local --gpus 0` |
| [`qwen3-tts-0.6b-dual-mode`](tasks/qwen3-tts-0.6b-dual-mode/) | [`Qwen3-TTS-12Hz-0.6B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) | `rsi-harness run tasks/qwen3-tts-0.6b-dual-mode --agent codex --model gpt-6-astra --reasoning-effort xhigh --agent-auth local --gpus 0` | `rsi-harness run tasks/qwen3-tts-0.6b-dual-mode --agent claude-code --model claude-opus-5-5 --reasoning-effort max --agent-auth local --gpus 0` |
| [`qwen3-tts-1.7b-dual-mode`](tasks/qwen3-tts-1.7b-dual-mode/) | [`Qwen3-TTS-12Hz-1.7B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) | `rsi-harness run tasks/qwen3-tts-1.7b-dual-mode --agent codex --model gpt-6-astra --reasoning-effort xhigh --agent-auth local --gpus 0` | `rsi-harness run tasks/qwen3-tts-1.7b-dual-mode --agent claude-code --model claude-opus-5-5 --reasoning-effort max --agent-auth local --gpus 0` |
| [`qwen3-asr-1.7b-dual-mode`](tasks/qwen3-asr-1.7b-dual-mode/) | [`Qwen3-ASR-1.7B`](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | [`eb7e97ed`](https://github.com/sgl-project/sglang-omni/tree/eb7e97ed9438ef4e4352656aec6170aeeb90966f) | `rsi-harness run tasks/qwen3-asr-1.7b-dual-mode --agent codex --model gpt-6-astra --reasoning-effort xhigh --agent-auth local --gpus 0` | `rsi-harness run tasks/qwen3-asr-1.7b-dual-mode --agent claude-code --model claude-opus-5-5 --reasoning-effort max --agent-auth local --gpus 0` |
| [`whisper-large-v3-dual-mode`](tasks/whisper-large-v3-dual-mode/) | [`openai/whisper-large-v3`](https://huggingface.co/openai/whisper-large-v3) | [`eb7e97ed`](https://github.com/sgl-project/sglang-omni/tree/eb7e97ed9438ef4e4352656aec6170aeeb90966f) | `rsi-harness run tasks/whisper-large-v3-dual-mode --agent codex --model gpt-6-astra --reasoning-effort xhigh --agent-auth local --gpus 0` | `rsi-harness run tasks/whisper-large-v3-dual-mode --agent claude-code --model claude-opus-5-5 --reasoning-effort max --agent-auth local --gpus 0` |
| [`moss-transcribe-diarize-dual-mode`](tasks/moss-transcribe-diarize-dual-mode/) | [`MOSS-Transcribe-Diarize`](https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-Diarize) | [`8220d220`](https://github.com/sgl-project/sglang-omni/tree/8220d220703cf8d8f5c5d9a2cde00b5ed13717b8) | `rsi-harness run tasks/moss-transcribe-diarize-dual-mode --agent codex --model gpt-6-astra --reasoning-effort xhigh --agent-auth local --gpus 0` | `rsi-harness run tasks/moss-transcribe-diarize-dual-mode --agent claude-code --model claude-opus-5-5 --reasoning-effort max --agent-auth local --gpus 0` |

**Agent settings:** Codex uses `gpt-6-astra` with `xhigh` reasoning; Claude Code uses `claude-opus-5-5` with `max` reasoning. Change `--gpus 0` to select another GPU; each concurrent run needs an exclusive GPU. For GPU types other than the reference H100 80GB HBM3, [calibrate the initial baseline and set `RSI_BASELINE_JSON`](docs/running.md#4-optional-recalibrating-reference-b_0-for-custom-gpu-skus) before launching.

<p align="center">
  <img src="assets/tasks.svg" width="100%" alt="Serving pipelines for eight SGLang-Omni tasks: five TTS and three ASR or diarization tasks, all in streaming and non-streaming modes">
</p>


<a id="quick-start"></a>

## 🚀 Quick start

**Requires:** Linux, Docker Engine 26+ with daemon access, NVIDIA drivers + Container Toolkit, Git, and [uv](https://docs.astral.sh/uv/getting-started/installation/). Use one NVIDIA GPU (80 GB+ VRAM recommended); see [full hardware requirements](docs/running.md#1-host-requirements--integrity-check).

Copy and run to set up RSI-Harness and validate CosyVoice3 on GPU 0. No model API key is needed:

```bash
git clone --depth 1 https://github.com/OpenRSI-Foundation/OpenRSI-AI-Infra-Bench.git &&
cd OpenRSI-AI-Infra-Bench &&
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/OpenRSI-Foundation/OpenRSI-Index.git vendor/OpenRSI-Index &&
git -C vendor/OpenRSI-Index sparse-checkout set RSI-Harness &&
uvx --python 3.12 --from ./vendor/OpenRSI-Index/RSI-Harness \
  rsi-harness run tasks/cosyvoice3-dual-mode --agent oracle --gpus 0
```

The first run installs the Harness, builds the task image, and downloads model weights. Expected result: **`reward = 1.0`**, with artifacts under `logs/runs/<run-id>/`.

To run another benchmark, replace `cosyvoice3-dual-mode` with any [task slug](#tasks). See the [full guide](docs/running.md) for Codex / Claude Code runs, GPU calibration, and result inspection, or [browse the 16 benchmark runs](results/archive.md).

<a id="how-it-works"></a>

<details>
<summary><strong>⚙️ How it works</strong></summary>

1. **Optimize.** A coding agent profiles and edits the serving runtime in a persistent container, with fixed model weights and one GPU.
2. **Evaluate.** Each submitted candidate is tested in a fresh Judge container against the fixed initial B₀, using three repetitions per mode.
3. **Iterate.** The agent uses the evaluator's feedback to improve its next submission. The leaderboard reports the highest valid score within 24 hours.

[RSI-Harness architecture](docs/how-it-works.md) · [Quality and latency gates](docs/evaluation.md) · [Run your own agent](docs/running.md)

</details>

<a id="contributors"></a>

## 🤝 Core Contributors

<table>
  <tr>
    <td align="center" width="20%"><a href="https://zhuofeng-li.github.io/"><strong>Zhuofeng Li</strong></a></td>
    <td align="center" width="20%"><a href="https://github.com/db-ol"><strong>Aaron Tian</strong></a></td>
    <td align="center" width="20%"><a href="https://yichenfeng.me/"><strong>Yichen Feng</strong></a></td>
    <td align="center" width="20%"><a href="https://wenhaochai.com/"><strong>Wenhao Chai</strong></a></td>
    <td align="center" width="20%"><a href="https://weikangda.github.io/kangda.github.io/"><strong>Kangda Wei</strong></a></td>
  </tr>
  <tr>
    <td align="center" width="20%"><a href="https://davidhanx.github.io/"><strong>Xinyang Han</strong></a></td>
    <td align="center" width="20%"><a href="https://caralinotes.com/"><strong>Cara Li</strong></a></td>
    <td align="center" width="20%"><a href="https://vincentcaptain.github.io/"><strong>Shujia Liang</strong></a></td>
    <td align="center" width="20%"><a href="https://yuetl9.github.io/"><strong>Yuetai Li</strong></a></td>
    <td align="center" width="20%"><a href="https://github.com/zhaochenyang20"><strong>Chenyang Zhao</strong></a></td>
  </tr>
</table>

We thank the [SGLang-Omni](https://github.com/sgl-project/sglang-omni) maintainers and contributors for task design, code review, and independent reproductions. To contribute a benchmark, see the [OpenRSI call for contributors](https://github.com/OpenRSI-Foundation/OpenRSI-Index#-call-for-contributors). Join the community on [Discord](https://discord.gg/3EG8Qhmfsa) or follow [OpenRSI on X](https://x.com/OpenRSI/status/2119869682929066288).

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
