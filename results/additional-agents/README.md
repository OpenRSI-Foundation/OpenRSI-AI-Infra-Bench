# Additional agent runs at 24 hours

This snapshot covers eight completed H100 runs for Kimi Code (`kimi-k3.1-pro-m17`) and DeepSeek Harness (`deepseek-v4.1-flash-m17`) as of November 25, 2026. The Codex and Claude Code columns reproduce the [published 24-hour results](../README.md). The [round trajectories](runs.json) include elapsed time, submission status, failed gates, and every eligible reward. An em dash indicates that this snapshot has no completed run for the pair.

| Task | Codex | Claude Code | Kimi Code | DeepSeek Harness |
| :--- | ---: | ---: | ---: | ---: |
| [CosyVoice3 (0.5B)](../../tasks/cosyvoice3-dual-mode/) | 1.1723× | 1.2970× | No eligible score | No eligible score |
| [MOSS-TTS v1.5](../../tasks/moss-tts-v1.5-dual-mode/) | 1.3385× | 1.9353× | In progress | — |
| [Fish Audio S2-Pro](../../tasks/fish-s2-pro-dual-mode/) | 1.7392× | 6.2883× | 1.0140× | 7.4578× |
| [Qwen3-TTS Base 0.6B](../../tasks/qwen3-tts-0.6b-dual-mode/) | 1.1406× | 1.2519× | 1.1062× | No eligible score |
| [Qwen3-TTS Base 1.7B](../../tasks/qwen3-tts-1.7b-dual-mode/) | 1.0964× | 1.2827× | No eligible score | 1.0626× |
| [Qwen3-ASR 1.7B](../../tasks/qwen3-asr-1.7b-dual-mode/) | 1.1168× | 1.2779× | In progress | — |
| [Whisper large-v3](../../tasks/whisper-large-v3-dual-mode/) | 1.1256× | 1.9790× | — | — |
| [MOSS-Transcribe-Diarize](../../tasks/moss-transcribe-diarize-dual-mode/) | 1.1338× | 1.4895× | — | — |

## Evaluation and coverage

- Each additional run had its own 86,400-second window. Only eligible Judge results completed within that window contribute to the maximum. Campaigns that produced no eligible candidate are recorded explicitly.
- The additional runs used NVIDIA H100 80GB HBM3 GPUs on Modal. The Judge used guest CPU telemetry and did not verify physical-host NUMA locality or host contention. Each candidate was evaluated offline against a fresh same-device reference. The published Codex and Claude Code runs used fixed per-run calibrations. The comparison is descriptive because those settings can affect scores.
- The trajectory export contains round outcomes and Judge metrics. It omits raw session content, infrastructure identifiers, and credentials. Active campaigns and unverified legacy attempts are excluded from the completed-run data.

## Fish-S2 Pro and Kimi Work audit

DeepSeek reached 7.458× relative to its round-six calibration. That round's baseline measured 1.031 and 1.040 requests per second in non-streaming and streaming mode. Its accepted candidate measured 7.992 and 7.606 requests per second. In round seven, a candidate with similar absolute throughput scored 3.363× against a faster baseline of 2.191 and 2.254 requests per second.

The selected DeepSeek round measured 7.733 weighted requests per second. The published Claude score and baseline imply 7.980 weighted requests per second under the same mode-weighting formula. The runs used different host setups. The higher normalized DeepSeek score does not establish higher absolute throughput on matched hardware.

The Kimi campaigns used a Work launcher that let the ACP driver exit after a single turn and supplied no explicit reasoning effort. On Fish-S2 Pro, 260 Work rounds ended without a source change, including 242 with zero tool calls. The two eligible Kimi Fish submissions remain in the trajectory. The launcher settings and low submission count limit what can be inferred about Kimi from this run.
