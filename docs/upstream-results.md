# From Benchmark to Upstream

[Overview](../README.md) · [How it works](how-it-works.md) · [Evaluation](evaluation.md) · [Running guide](running.md) · **Upstream results** · [24h results](../results/README.md)

Agent-discovered optimizations for the models in this suite contributed to **11 pull requests merged into [`sgl-project/sglang-omni`](https://github.com/sgl-project/sglang-omni)** after multi-round maintainer review. Agents ran the profiling, hypothesis testing, and runtime optimization loops; people defined the tasks and owned architectural review and merge decisions.

<p align="center">
  <img src="../assets/five-patterns.svg" width="100%" alt="Five serving optimization patterns across 11 merged SGLang-Omni PRs: CPU contention, data conversion, redundant computation, GPU launch overhead, and pipeline scheduling">
</p>

## 1. Five Recurring Runtime Patterns

Almost all 11 PRs eliminate runtime overhead *around* the model while keeping model weights and sampling settings fixed:

1. **Idle threads competing for CPU cores ([#2524](https://github.com/sgl-project/sglang-omni/pull/2524)):** Busy-spinning wait loops held physical CPU cores needed by audio/tokenizer workers; putting idle threads to sleep freed cores immediately (+32.5% streaming throughput on its own).
2. **Per-hop tensor-to-list conversion ([#2555](https://github.com/sgl-project/sglang-omni/pull/2555), [#2778](https://github.com/sgl-project/sglang-omni/pull/2778)):** Stage boundaries serialized tensors into Python lists and rebuilt them on the receiver; passing native tensors and deferring byte packing to the final response removed IPC stalls.
3. **Redundant & discarded computation ([#2525](https://github.com/sgl-project/sglang-omni/pull/2525), [#2778](https://github.com/sgl-project/sglang-omni/pull/2778), [#2882](https://github.com/sgl-project/sglang-omni/pull/2882), [#3071](https://github.com/sgl-project/sglang-omni/pull/3071)):** Eliminated unused quantizer reconstructions, per-channel tensor reallocations, duplicate fallback frontends, and audio feature extraction past utterance boundaries.
4. **Fragmented small GPU kernel launches ([#2779](https://github.com/sgl-project/sglang-omni/pull/2779), [#2859](https://github.com/sgl-project/sglang-omni/pull/2859), [#2880](https://github.com/sgl-project/sglang-omni/pull/2880), [#2901](https://github.com/sgl-project/sglang-omni/pull/2901), [#3071](https://github.com/sgl-project/sglang-omni/pull/3071)):** Captured prefill, decode, and vocoder steps into replayable CUDA Graphs, fused embedding arithmetic, and moved Whisper encoder attention to FlashAttention-4.
5. **Unpipelined prefill & decode stages ([#2779](https://github.com/sgl-project/sglang-omni/pull/2779), [#2859](https://github.com/sgl-project/sglang-omni/pull/2859), [#2881](https://github.com/sgl-project/sglang-omni/pull/2881), [#3071](https://github.com/sgl-project/sglang-omni/pull/3071)):** Replaced alternating prefill/decode turn-taking with asynchronous prefill so request `k+1` prefills while request `k` decodes.

## 2. Merged Pull Requests & Measured Upstream Gains

Throughput gains below compare `sglang-omni` `main` before each model's first OpenRSI PR against `main` after its last (`128` requests per round, reported as **non-streaming / streaming**):

| Model | `sglang-omni` range | Merged PRs | What changed upstream | H100 gain (NS / S) | H200 gain (NS / S) |
| :--- | :---: | :--- | :--- | ---: | ---: |
| **CosyVoice3** | [`f29a119 → fe4b23f`](https://github.com/sgl-project/sglang-omni/compare/f29a1195d12826bcedfda78f4e58429745eda5b8...fe4b23f06b27f7b2492703891c8036a919d2041e) | [#2524](https://github.com/sgl-project/sglang-omni/pull/2524) [#2555](https://github.com/sgl-project/sglang-omni/pull/2555) | Sleeping idle encoder threads; native tensor transport across stages | +44.4% / +46.2% | +48.1% / +56.3% |
| **MOSS-TTS**¹ | [`a65abc0 → 53ea267`](https://github.com/sgl-project/sglang-omni/compare/a65abc07e535a57589aebc7ebbf92498e2170761...53ea2678733ac7b4c4744895e8cf2632117c2dcd) | [#2525](https://github.com/sgl-project/sglang-omni/pull/2525) [#2859](https://github.com/sgl-project/sglang-omni/pull/2859) | In-place embedding sums, fused channel embeddings & overlapped graphed decode | +48.5% / +76.3% | +65.2% / +149.5% |
| **Fish S2-Pro** | [`08182f2 → 28c3e35`](https://github.com/sgl-project/sglang-omni/compare/08182f2bc44dbf951e086927d6eb657f3a419171...28c3e35a33bef2f45b3315431f4a512d6ed463cf) | [#2778](https://github.com/sgl-project/sglang-omni/pull/2778) | Skipped unused quantizer reconstruction and packed waveforms | +9.6% / +0.3% | +13.4% / +2.1% |
| **Qwen3-TTS** | [`8220d22 → 08182f2`](https://github.com/sgl-project/sglang-omni/compare/8220d220703cf8d8f5c5d9a2cde00b5ed13717b8...08182f2bc44dbf951e086927d6eb657f3a419171) | [#2779](https://github.com/sgl-project/sglang-omni/pull/2779) | Reused prefill and vocoder CUDA graphs for Base checkpoints (`0.6B` & `1.7B`) | +25.2% / +4.7% | +44.1% / +12.0% |
| **Qwen3-ASR**² | [`e43663e → cca9cf5`](https://github.com/sgl-project/sglang-omni/compare/e43663e908bf1c3aee15abfd3a19d44373459108...cca9cf580b87b0c039e8da001c415e5c4046bfb2) | [#2880](https://github.com/sgl-project/sglang-omni/pull/2880) [#2881](https://github.com/sgl-project/sglang-omni/pull/2881) [#2882](https://github.com/sgl-project/sglang-omni/pull/2882) | Async prefill/decode overlap, prefill & decode CUDA graphs, planned encoder chunks | +14.2% / +5.0% | +15.4% / +8.4% |
| **Whisper large-v3** | [`4809648 → ff302a0`](https://github.com/sgl-project/sglang-omni/compare/4809648d486bdff88dee5199b3e448af3c250f00...ff302a0c1ee9c28bce8604c14e374a02d3ec5ade) | [#2901](https://github.com/sgl-project/sglang-omni/pull/2901) | Incremental text streaming, FlashAttention-4 encoder attention & reachable prefill graphs | +7.6% / +12.2% | +14.0% / +17.6% |
| **MOSS-TD** | [`6e1a217 → 39113da`](https://github.com/sgl-project/sglang-omni/compare/6e1a217974743f7f858537169d835c42f9f0d5b9...39113da3ec2ed39d4bfa370e35b06ea3edd96757) | [#3071](https://github.com/sgl-project/sglang-omni/pull/3071) | Full prefill graphs, packed encoder attention, trimmed fbank extraction & async prefill | +18.8% / +30.0% | +19.9% / +32.1% |

## 3. Measurement Protocol & Caveats

- **Separate from the 24-hour benchmark leaderboard:** Upstream table numbers measure `sglang-omni` `main` before vs. after merged PRs at `128` requests per round, after maintainer review and multi-commit refinement (median review cycle ~3.5 days). They are not directly comparable to the single-agent 24-hour [benchmark leaderboard](../README.md#leaderboard).
- **Concurrent upstream commits:**
  - ¹ **MOSS-TTS:** The `a65abc0 → 53ea267` range also includes non-OpenRSI upstream changes (streaming codec rewrite `#2805`, `#2662`, `#2770`, `#2772`, and SGLang 0.5.22 upgrade `#2964`). `#2859` adds ~41 s of startup graph capture and ~3.7 GiB peak VRAM.
  - ² **Qwen3-ASR:** The `e43663e → cca9cf5` range also includes the SGLang 0.5.22 upgrade (`#2964`).
- Full per-PR breakdowns, absolute `req/s` numbers, and additional exploratory models outside this 8-task benchmark are documented in **[OpenRSI × SGLang-Omni: Scaling RSI for AI Infra](https://index.openrsi.foundation/blog/2026/openrsi-sglang-omni/)**.
