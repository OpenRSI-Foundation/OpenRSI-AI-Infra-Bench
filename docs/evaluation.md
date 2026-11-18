# Evaluation

[Back to the overview](../README.md) · [Running guide](running.md)

The target is **serving throughput**, subject to each task's quality, tail-latency, streaming-continuity, resource, and integrity gates. A faster implementation is rejected (`reward = 0`) if it violates any guard.

For all eight dual-mode tasks (TTS and ASR), let **Rₛ** and **Rₙ** be the streaming and non-streaming throughput ratios against the reference baseline **B₀** (for ASR, each mode ratio is the geometric mean across English and Mandarin):

$$
\mathrm{reward} = R_s^{2/3} \, R_n^{1/3}
$$

**Both modes must strictly improve** over B₀ (`> 1.0`) for modified candidates, preventing a gain in one mode from masking a regression in the other.

| Gate Layer | Workload and checks |
| :--- | :--- |
| **TTS (5 tasks)** | 1,088 English SeedTTS requests per repetition; concurrency 16; 3 repetitions per mode; independent `Qwen3-ASR-1.7B` WER verification (≤ 2.0%), 3% latency/RTF/TTFA P95 budgets, and ≥ 95% multi-chunk streaming (`c50` ≥ 95%) |
| **ASR (3 tasks)** | 1,088 English + 2,020 Mandarin SeedTTS requests per repetition; non-streaming HTTP and post-upload SSE; 3 repetitions per language and mode; strict WER/CER ceilings, `single_delta_fraction` ≤ 5%, and ≥ 80% speaker-turn tags on MOSS-TD |
| **System guards** | Automatic NUMA-local 16-physical-core pinning, host contention gate (`peak_foreign_cores <= 2.0`), frozen weights & sampling semantics, AST & call-site liveness checks, and `0 MiB` GPU process cleanup |
