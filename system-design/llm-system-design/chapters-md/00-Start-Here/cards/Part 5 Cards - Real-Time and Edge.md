---
title: "Part 5 Cards — Real-Time and Edge (Ch 14, 18, 31)"
tags: [cards, realtime, voice, edge]
---

# Part 5 Cards — Real-Time and Edge

Every card here is **P9 (latency budget per stage + stream + degrade)**. Write the millisecond budget on the whiteboard first; everything else follows from it.

---

### Ch 14 — Design a Real-Time Meeting Summarizer
**One line:** Live transcript, rolling notes and final action items for meetings.
**Shape:** Audio stream → VAD → Streaming ASR → Diarization → **Incremental summarizer** (window + running summary) → Live notes → Final summary + action items
**Patterns:** P9

**3 ideas**
1. **Streaming audio pipeline:** chunked audio, streaming ASR with partial/final hypotheses, only finals go to the LLM.
2. **Incremental summarization:** summarize each window, merge into a running summary. Don't re-summarize the whole meeting every minute.
3. **Speaker attribution:** diarization + calendar/voice enrollment to map speakers to names. Let users correct, and propagate corrections.

**2 trade-offs**
- Update frequency (freshness) vs cost and flicker.
- On-device ASR (privacy, cost) vs cloud (accuracy).

**Numbers:** Summary update every ~30–60s is enough; ASR lag a second or two.
**Soundbite:** *"I keep a running summary and only feed new finalized transcript, so cost grows linearly with meeting length, not quadratically."*

> [!question]- Why not re-summarize the whole transcript each time?
> Cost and latency grow quadratically with meeting length. Incremental window + running summary keeps it linear.

> [!question]- How do you handle "who said what" errors?
> Diarization + enrollment mapping, confidence flags, user correction that rewrites attribution in the notes.

**Go deep:** [[Chapter 14 - Design a Real-Time Meeting Summarizer]] → "Incremental Summarization".

---

### Ch 18 — Design a Voice-First Real-Time Agent
**One line:** A voice assistant that responds within half a second and handles interruptions naturally.
**Shape:** Mic → VAD/endpointing → Streaming ASR → LLM (streamed) → Streaming TTS → Speaker; barge-in detection cancels everything
**Patterns:** P1, P4, P9

**3 ideas**
1. **Latency budget:** endpointing + ASR + LLM TTFT + TTS first-audio must fit in ~500ms. Stream every stage and start TTS on the first sentence.
2. **Turn-taking:** smart endpointing (semantic, not just silence), barge-in cancels TTS and LLM generation, keep what was actually spoken in history.
3. **Pipeline vs native speech-to-speech:** cascade (ASR→LLM→TTS: controllable, debuggable, tool-friendly) vs native audio models (lower latency, more natural prosody, harder to guard).

**2 trade-offs**
- Aggressive endpointing (snappy, cuts people off) vs conservative (natural, laggy).
- Filler words/acknowledgements to mask latency vs feeling scripted.

**Numbers:** Voice **< 500ms** to first audio.
**Soundbite:** *"Users judge voice by time-to-first-audio, so I stream every stage and start speaking at the first sentence boundary."*

> [!question]- Write the voice latency budget.
> e.g. endpointing ~150ms + ASR final ~100ms + LLM TTFT ~200ms + TTS first audio ~100ms ≈ 550ms. Shave with streaming, smaller models, colocation.

> [!question]- What happens on barge-in?
> Stop TTS playback, cancel LLM generation, truncate the assistant turn in history to what was actually spoken, then process the new utterance.

> [!question]- When would you choose native speech-to-speech?
> When naturalness and latency dominate and tool use / compliance needs are light. Otherwise the cascade is easier to control and audit.

**Go deep:** [[Chapter 18 - Design a Voice-First Real-Time Agent]] → "End-to-End Voice Latency Pipeline" and "Interruption Handling and Turn-Taking".

---

### Ch 31 — Edge and On-Device LLM Deployment
**One line:** Run models on phones/laptops for privacy, offline use and cost, and fall back to the cloud when needed.
**Shape:** On-device small model (quantized) + runtime → Router (task, confidence, battery, connectivity) → Cloud for hard tasks; OTA model updates
**Patterns:** P1, P6, P9

**3 ideas**
1. **Quantization for edge:** 4-bit (and lower) weights; RAM, not compute, is usually the limit. A 3B model at 4-bit ≈ 1.5–2 GB.
2. **Runtime choice:** llama.cpp/GGUF, MLC, ExecuTorch, Core ML, ONNX Runtime, matched to the hardware accelerator (NPU/GPU).
3. **Hybrid edge-cloud routing:** default on-device; escalate on complexity or low confidence, with consent if private data leaves the device.

**2 trade-offs**
- Model quality vs RAM/battery/thermal.
- Ship model in app (big download) vs download on demand (delta updates, versioning).

**Numbers:** INT4 ≈ **0.5 GB per 1B params**.
**Soundbite:** *"On-device, the binding constraints are RAM and thermals, so I size the model to memory first and treat the cloud as the fallback tier."*

> [!question]- How much RAM does a 7B INT4 model need?
> ~3.5 GB for weights plus KV cache and runtime. Too much for many phones, which is why 1–3B is typical.

> [!question]- What triggers cloud fallback?
> Task complexity, low on-device confidence, long context, low battery/thermal throttling, user tier. Respect privacy policy before sending data.

> [!question]- How do you update on-device models safely?
> Versioned OTA, staged rollout, delta downloads on Wi-Fi/charging, compatibility check with app version, rollback.

**Go deep:** [[Chapter 31 - Edge and On-Device LLM Deployment]] → "Quantization for Edge" and "Hybrid Edge-Cloud Architecture and Routing".
