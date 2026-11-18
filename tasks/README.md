# Task catalog

[Overview](../README.md) · [Quick start](../README.md#quick-start) · [Running guide](../docs/running.md) · [24-hour results](../results/README.md)

The suite contains **8 Harbor 1.4 tasks: 5 TTS and 3 ASR / diarization tasks**, covering 8 model checkpoints across 7 families. Every task evaluates streaming and non-streaming serving. Reference B₀ measurements use one NVIDIA H100 80GB HBM3 GPU.

| Task package | Model checkpoint | SGLang-Omni base commit |
| :--- | :--- | :--- |
| [`cosyvoice3-dual-mode`](./cosyvoice3-dual-mode/) | [`Fun-CosyVoice3-0.5B-2512`](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) |
| [`moss-tts-v1.5-dual-mode`](./moss-tts-v1.5-dual-mode/) | [`MOSS-TTS-v1.5`](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | [`cb75ab40`](https://github.com/sgl-project/sglang-omni/tree/cb75ab409669a6ab672fa42421b41b11af2fe263) |
| [`fish-s2-pro-dual-mode`](./fish-s2-pro-dual-mode/) | [`fishaudio/s2-pro`](https://huggingface.co/fishaudio/s2-pro) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) |
| [`qwen3-tts-0.6b-dual-mode`](./qwen3-tts-0.6b-dual-mode/) | [`Qwen3-TTS-12Hz-0.6B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) |
| [`qwen3-tts-1.7b-dual-mode`](./qwen3-tts-1.7b-dual-mode/) | [`Qwen3-TTS-12Hz-1.7B-Base`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | [`15235430`](https://github.com/sgl-project/sglang-omni/tree/1523543056bf334bc2f4d69db23aad0a002cedf2) |
| [`qwen3-asr-1.7b-dual-mode`](./qwen3-asr-1.7b-dual-mode/) | [`Qwen3-ASR-1.7B`](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | [`eb7e97ed`](https://github.com/sgl-project/sglang-omni/tree/eb7e97ed9438ef4e4352656aec6170aeeb90966f) |
| [`whisper-large-v3-dual-mode`](./whisper-large-v3-dual-mode/) | [`openai/whisper-large-v3`](https://huggingface.co/openai/whisper-large-v3) | [`eb7e97ed`](https://github.com/sgl-project/sglang-omni/tree/eb7e97ed9438ef4e4352656aec6170aeeb90966f) |
| [`moss-transcribe-diarize-dual-mode`](./moss-transcribe-diarize-dual-mode/) | [`MOSS-Transcribe-Diarize`](https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-Diarize) | [`8220d220`](https://github.com/sgl-project/sglang-omni/tree/8220d220703cf8d8f5c5d9a2cde00b5ed13717b8) |

Each package includes pinned source, model assets and dependencies, the agent's instructions, and an isolated evaluator. See its README for workload details and reference throughput.

From the repository root, after [installing RSI-Harness](../docs/running.md#2-install-rsi-harness):

```bash
rsi-harness run tasks/cosyvoice3-dual-mode --agent oracle --gpus 0
```

The oracle restores the pristine source and verifies the task's full evaluation path, with an expected reward of `1.0`. For agent runs on another GPU SKU, [recalibrate B₀](../docs/running.md#4-optional-recalibrating-reference-b_0-for-custom-gpu-skus) first.
