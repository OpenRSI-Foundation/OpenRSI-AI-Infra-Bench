# Results at 24 Hours

[Back to the benchmark](../README.md)

**16 runs across 8 tasks**, with Codex and Claude Code evaluated over the same first **24 hours**. [Structured JSON](main.json) · [CSV](runs.csv) · [Cutoff audit](24h-audit.json) · [Full trajectories for these 16 runs](archive.md)

## Selection and cutoff

- Start the clock at the Unix timestamp in each trajectory's `started_at` file. Include completed, finite scores whose `evolve_state.json` record satisfies `0 <= at - started_at <= 86400`; take the maximum without rounding.
- Apply this cutoff to both agents, including runs configured for 48 h or whose final evaluation overran a 24 h timeout. Later results never replace the selected score.
- Require coverage of the full 24-hour window and a corresponding result for both agents on the task. Shorter and incomplete trajectories do not qualify; they are not extrapolated to 24 h.
- Match task instructions, base image, environment, GPU SKU and reported evaluation-protocol hash within each pair. Each run keeps its own three-repetition initial B₀ calibration; numerical baselines can differ.

## Paired results

| Task | Codex @ 24h | Claude Code @ 24h | GPU |
| :--- | ---: | ---: | :--- |
| [CosyVoice3 (0.5B)](../tasks/cosyvoice3-dual-mode/) | [1.172×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/cosyvoice3-dual-mode/codex-gpt-6-astra/submissions/agent-11/report.json) | [1.297×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/cosyvoice3-dual-mode/claude-code-claude-opus-5-5/submissions/agent-3/report.json) | H100 80GB HBM3 |
| [MOSS-TTS v1.5](../tasks/moss-tts-v1.5-dual-mode/) | [1.339×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/moss-tts-v1.5-dual-mode/codex-gpt-6-astra/submissions/agent-8/report.json) | [1.935×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/moss-tts-v1.5-dual-mode/claude-code-claude-opus-5-5/submissions/agent-4/report.json) | H100 80GB HBM3 |
| [Fish Audio S2-Pro](../tasks/fish-s2-pro-dual-mode/) | [1.739×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/fish-s2-pro-dual-mode/codex-gpt-6-astra/submissions/agent-9/report.json) | [6.288×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/fish-s2-pro-dual-mode/claude-code-claude-opus-5-5/submissions/agent-5/report.json) | H100 80GB HBM3 |
| [Qwen3-TTS Base 0.6B](../tasks/qwen3-tts-0.6b-dual-mode/) | [1.141×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/qwen3-tts-0.6b-dual-mode/codex-gpt-6-astra/submissions/agent-3/report.json) | [1.252×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/qwen3-tts-0.6b-dual-mode/claude-code-claude-opus-5-5/submissions/agent-5/report.json) | H100 80GB HBM3 |
| [Qwen3-TTS Base 1.7B](../tasks/qwen3-tts-1.7b-dual-mode/) | [1.096×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/qwen3-tts-1.7b-dual-mode/codex-gpt-6-astra/submissions/agent-10/report.json) | [1.283×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/qwen3-tts-1.7b-dual-mode/claude-code-claude-opus-5-5/submissions/agent-3/report.json) | H100 80GB HBM3 |
| [Qwen3-ASR 1.7B](../tasks/qwen3-asr-1.7b-dual-mode/) | [1.117×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/qwen3-asr-1.7b-dual-mode/codex-gpt-6-astra/submissions/agent-47/report.json) | [1.278×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/qwen3-asr-1.7b-dual-mode/claude-code-claude-opus-5-5/submissions/agent-11/report.json) | H100 80GB HBM3 |
| [Whisper large-v3](../tasks/whisper-large-v3-dual-mode/) | [1.126×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/whisper-large-v3-dual-mode/codex-gpt-6-astra/submissions/agent-8/report.json) | [1.979×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/whisper-large-v3-dual-mode/claude-code-claude-opus-5-5/submissions/agent-12/report.json) | H100 80GB HBM3 |
| [MOSS-Transcribe-Diarize](../tasks/moss-transcribe-diarize-dual-mode/) | [1.134×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/moss-transcribe-diarize-dual-mode/codex-gpt-6-astra/submissions/agent-19/report.json) | [1.490×](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/blob/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni/moss-transcribe-diarize-dual-mode/claude-code-claude-opus-5-5/submissions/agent-6/report.json) | H100 80GB HBM3 |

Scores link to the exact selected report. The RSI Logs Viewer and raw archive still show full trajectories, which can contain later scores.

## Changes from full-run maxima

| Task / agent | Full-run best | Best within 24h | Selected round | Recorded at |
| :--- | ---: | ---: | :--- | ---: |
| fish-s2-pro-dual-mode / codex | 1.803× | 1.739× | agent-9 | 23.00 h |
| qwen3-asr-1.7b-dual-mode / claude-code | 1.317× | 1.278× | agent-11 | 18.36 h |

## Evidence and limits

The audit uses the immutable [Hugging Face snapshot `f5deed0f9c9f`](https://huggingface.co/datasets/OpenRSI-Foundation/OpenRSI-Index-Logs/tree/f5deed0f9c9f75ef0f8a5e9514712f8601aea360/sglang-omni). For the 16 runs in this suite, it retains original timeouts, durations, maxima, all submission timestamps, selected-report hashes and comparison checks. [Original JSON](archive.json) and [original CSV](archive-runs.csv) preserve the full-run records.

For the three ASR pairs, the run-plan source/test-directory digests differ even though task instructions, base image, environment and the reported evaluation-protocol hashes match. The audit records this distinction; matching protocol hashes do not establish byte-identical test directories. GPU UUIDs are redacted in the public archive, so hardware alignment is checked at the GPU-model level.

Each score remains relative to its own run's initial calibration. No baseline replacement, score averaging, new GPU evaluation or extrapolation was performed.
