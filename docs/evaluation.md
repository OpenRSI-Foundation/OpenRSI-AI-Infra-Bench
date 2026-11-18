# Evaluation Protocol & Gates

[Overview](../README.md) · [How it works](how-it-works.md) · **Evaluation** · [Running guide](running.md) · [Upstream results](upstream-results.md) · [24h results](../results/README.md)

The optimization objective is **sustained serving throughput** under realistic concurrency, guarded by speech intelligibility, tail-latency, streaming-continuity, hardware-isolation, and code-integrity checks. **Any guard violation rejects the submission (`score = 0`).**

## 1. Scoring Formula

Every task in the suite evaluates **both streaming and non-streaming serving** across **3 scored repetitions per mode** (after untimed warmup requests). Let **Rₛ** and **Rₙ** denote the candidate's mean throughput divided by the run's initial 3-repetition baseline **B₀** in streaming and non-streaming modes:

$$
\mathrm{score} = R_s^{2/3} \, R_n^{1/3}
$$

- **Bilingual ASR tasks:** Each mode's ratio is the geometric mean across English and Mandarin workloads:

$$
R_m = \sqrt{\frac{Q_{m,\mathrm{en}}(C)}{Q_{m,\mathrm{en}}(B_0)} \cdot \frac{Q_{m,\mathrm{zh}}(C)}{Q_{m,\mathrm{zh}}(B_0)}}, \quad m \in \{\mathrm{stream}, \mathrm{nonstream}\}
$$

- **Strict dual-mode improvement:** Modified candidates must achieve **`R_s > 1.0` and `R_n > 1.0`** simultaneously (and improve every scored language/mode pair), preventing a speedup in one path from masking a regression in the other.
- **Oracle verification (`reward = 1.0`):** When SHA-256 checks confirm unmodified baseline source (`--agent oracle`), the Judge still executes all 3 repetitions per mode and enforces quality, streaming, and contention gates, emitting `1.0` if healthy.

## 2. Per-Task Reference B₀ & Gate Specification

Reference **B₀** throughputs below are the 3-repetition means baked into `tests/baseline.json`, measured on one **NVIDIA H100 80GB HBM3** GPU (`NS` = non-streaming, `S` = streaming):

| Task package | Track | Workload & Concurrency | Reference B₀ (`req/s`) | Quality, Tail-Latency & Streaming Gates |
| :--- | :---: | :--- | :--- | :--- |
| [`cosyvoice3-dual-mode`](../tasks/cosyvoice3-dual-mode/) | TTS | 1,088 EN · `c = 16` | `9.06` NS · `7.52` S | WER ≤ 2.0%; Latency/RTF/TTFA P95 ≤ 1.03× B₀; ≥ 95% multi-chunk; `c50` ≥ 95% |
| [`moss-tts-v1.5-dual-mode`](../tasks/moss-tts-v1.5-dual-mode/) | TTS | 1,088 EN · `c = 16` | `7.86` NS · `6.56` S | WER ≤ 2.0%; Latency/RTF/TTFA P95 ≤ 1.03× B₀; ≥ 95% multi-chunk; `c50` ≥ 95% |
| [`fish-s2-pro-dual-mode`](../tasks/fish-s2-pro-dual-mode/) | TTS | 1,088 EN · `c = 16` | `1.25` NS · `1.24` S | WER ≤ 2.0%; Latency/RTF/TTFA P95 ≤ 1.03× B₀; ≥ 95% multi-chunk; `c50` ≥ 95% |
| [`qwen3-tts-0.6b-dual-mode`](../tasks/qwen3-tts-0.6b-dual-mode/) | TTS | 1,088 EN · `c = 16` | `17.58` NS · `19.38` S | WER ≤ 2.0%; Latency/RTF/TTFA P95 ≤ 1.03× B₀; ≥ 95% multi-chunk; `c50` ≥ 95% |
| [`qwen3-tts-1.7b-dual-mode`](../tasks/qwen3-tts-1.7b-dual-mode/) | TTS | 1,088 EN · `c = 16` | `18.79` NS · `19.97` S | WER ≤ 2.0%; Latency/RTF/TTFA P95 ≤ 1.03× B₀; ≥ 95% multi-chunk; `c50` ≥ 95% |
| [`qwen3-asr-1.7b-dual-mode`](../tasks/qwen3-asr-1.7b-dual-mode/) | ASR | 1,088 EN + 2,020 ZH · `c = 32` | EN `168.92` NS / `160.60` S<br>ZH `179.78` NS / `172.06` S | EN WER & ZH CER ≤ 2.0%; Latency/RTF/TTFT P95 ≤ 1.03× B₀; `single_delta` ≤ 5% |
| [`whisper-large-v3-dual-mode`](../tasks/whisper-large-v3-dual-mode/) | ASR | 1,088 EN + 2,020 ZH · `c = 32` | EN `53.21` NS / `52.43` S<br>ZH `48.62` NS / `48.57` S | EN WER & ZH CER ≤ 1.03× B₀; Latency/RTF/TTFT P95 ≤ 1.03× B₀; `single_delta` ≤ 5% |
| [`moss-transcribe-diarize-dual-mode`](../tasks/moss-transcribe-diarize-dual-mode/) | ASR | 1,088 EN + 2,020 ZH · `c = 32` | EN `106.81` NS / `102.15` S<br>ZH `109.60` NS / `105.50` S | EN WER & ZH CER ≤ 1.03× B₀; Latency/RTF/TTFT P95 ≤ 1.03× B₀; `single_delta` ≤ 5%; ≥ 80% speaker tags |

> [!NOTE]
> **What streaming gates verify:**
> - **TTS (`cosy_stream`, `moss_stream`, `fish_stream`, `qwen*_stream`):** HTTP responses must stream incremental PCM audio chunks (`chunk_count >= 2` on ≥ 95% of requests and 50th-percentile chunk cadence `c50 >= 95%`), preventing buffered whole-utterance responses disguised as streaming. Every synthesized waveform is independently transcribed by a frozen `Qwen/Qwen3-ASR-1.7B` model in the Judge to verify corpus WER.
> - **ASR (`stream/en`, `stream/zh`):** Server-Sent Events (SSE) after audio upload must emit genuinely incremental text deltas (`single_delta_fraction <= 5%`) within first-token (`TTFT P95`) and inter-chunk latency budgets. On `moss-transcribe-diarize-dual-mode`, ≥ 80% of diarized utterances must preserve valid speaker-turn markers.

## 3. System Isolation & Anti-Cheat Guards

To ensure speedups reflect genuine runtime improvements rather than measurement artifacts or reward hacking, every Judge run enforces five system-level guards:

1. **NUMA-local physical CPU pinning:** Automatically selects and binds **16 distinct non-SMT physical cores** on the target GPU's NUMA node via `/sys/bus/pci/devices` and `/proc/stat`.
2. **Host contention ceiling:** Samples host-wide CPU activity throughout benchmark repetitions and invalidates runs where external processes consume `peak_foreign_cores > 2.0`.
3. **Frozen weights, precision & sampling:** Model checkpoints, tokenizers, SeedTTS audio/text splits, repetition seeds (`42, 43, 44`), and `sglang_omni/sampling/` semantics are verified against SHA-256 manifests and protected paths.
4. **AST & runtime call-site liveness:** Static AST inspection and runtime provenance checks reject request caching across utterances, stubbed model layers, skipped decoding steps, or bypassed HTTP/SSE handlers.
5. **Clean GPU handoff (`0 MiB`):** Before launching the Judge server, the evaluator verifies that no lingering Work-container processes hold memory or compute contexts on the assigned GPU.
