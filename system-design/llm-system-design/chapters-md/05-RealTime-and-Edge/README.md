# 05 — Real-Time and Edge

This folder covers LLM system designs where the dominant constraint is **hard real-time latency** or **resource-constrained compute** rather than raw scale or output quality. It includes low-latency streaming pipelines (transcription + summarization), full-duplex voice pipelines (speech-to-speech agents), and on-device/edge deployment (quantized models on phones/laptops with cloud fallback). The common thread across all three chapters:

- Latency budgets are decomposed per-stage in milliseconds, with each stage's budget independently engineered (chunk sizes, model sizes, quantization) to hit a total end-to-end target.
- Streaming/incremental processing replaces batch processing everywhere on the critical path — partial results are emitted before the full input is available.
- Every design includes an explicit fallback/degradation path (cloud overflow, degraded local response, provider failover) for when the primary low-latency path fails or is unavailable.
- Small/quantized models are preferred over large ones on the hot path, with larger models reserved for non-real-time or cloud-side work.

---

## Chapter 14 — Design a Real-Time Meeting Summarizer

**Problem:** Ingest live audio from concurrent meetings, produce real-time speaker-attributed transcription, and generate streaming incremental summaries with action items, all within seconds of utterance.

**Core pattern:** Streaming STT + speaker diarization + hierarchical incremental summarization.

- **Audio Ingestion Gateway** — WebRTC/SFU (mediasoup/Janus) extracts per-participant RTP streams (avoids cross-talk from mixed audio), buffers 200ms chunks into Kafka partitioned by `meeting_id:speaker_id`.
- **VAD front-end** — cascaded energy threshold (<1ms, -40dBFS cutoff) → Silero VAD (1.8M-param LSTM, ~2ms/200ms chunk, 96%+ accuracy) filters ~60% of frames before neural STT, cutting STT GPU load ~40% (~1,000 GPUs saved at scale).
- **Streaming STT Service** — Conformer-Transducer (RNN-T), 200ms chunks, 200ms lookahead (400ms algorithmic latency), stateful workers pin RNN-T hidden state (~50MB/stream) in GPU VRAM via consistent hashing (`hash(meeting_id:speaker_id) % N`) — saves 20-50ms/chunk vs stateless workers that reload state from Redis. Endpointer fires on 600ms silence.
- **Speaker Diarization Service** — ECAPA-TDNN 192-dim embeddings from 1.5s windows of mixed audio, every 1.5s, run in parallel with STT (non-blocking). Hybrid strategy: enrollment-based cosine-similarity matching (3-second voice sample per participant, threshold 0.65, 5-8% DER) falls back to online agglomerative clustering (distance threshold 0.45, 12-18% DER) for unenrolled guests.
- **Transcript Assembler** — joins STT segments with diarization labels on timestamp overlap; overlap regions resolved by dominant energy.
- **Incremental Summarizer** — every 30s, snapshots last 5 min raw transcript (~1,500 tokens) + condensed prior summary (~300 tokens) → 7B INT8-quantized model (~2,000 token prompt, ~2s inference), streamed to client over WebSocket.
- **Final Summary Generator** — triggered on meeting-end, concatenates all section summaries (~3-4K tokens) → 13B model, structured output (exec summary, decisions, action items, next steps), must complete in <10s.
- Storage: Cassandra (time-series transcript), Elasticsearch (full-text search), Redis (session-scoped voiceprint cache).

**Pros:**
- Independently scalable/deployable services — a summarization outage doesn't interrupt live transcript delivery.
- Hybrid diarization degrades gracefully (5-8% DER enrolled → 12-18% DER anonymous) rather than failing outright for unenrolled guests.
- Hierarchical summarization (rolling window + compressed prior summary) avoids both context-window overflow and total loss of early-meeting detail.
- Self-hosted streaming Conformer STT is ~6-10x cheaper than managed APIs at scale ($0.15/hr vs $0.90-1.44/hr) and meets the same latency budget.

**Cons / failure modes:**
- Stateful STT workers are harder to scale horizontally (hash-range rebalancing migrates stream state) and a worker failure causes a 5-10s transcript gap even with 5s Redis checkpointing.
- Diarization label flip-flopping during quiet transitions requires hysteresis (minimum 500ms segment duration, 3 consecutive frames above threshold).
- Cross-talk (simultaneous speech) degrades DER to 20%+ and can misattribute action items — flagged but not fully solved (`[attribution uncertain]` tagging).
- Summary hallucination during silence gaps (system fabricates content) requires explicit `[No discussion for N minutes]` markers.
- Full-transcript-in-context approach doesn't scale past ~25-30 minutes (quadratic attention cost); hierarchical summary+window is required, at the cost of nuance/verbatim loss.
- Poor network codecs (Opus at 8kbps) spike WER to 25%+.

**When to use:** High-concurrency, multi-speaker live audio where both a real-time UI (rolling summary) and a durable accurate archive are needed. Not suited to single-speaker or short-form audio, where a simple post-hoc (batch) summarization is cheaper and higher quality (see the Strategy table: post-hoc for <15 min meetings).

---

## Chapter 18 — Design a Voice-First Real-Time Agent (AI Drive-Thru / Phone Agent)

**Problem:** Conduct natural spoken conversations (phone/drive-thru) with sub-500ms voice-to-voice latency, handle mid-sentence interruptions, and maintain task state across turns at 50K concurrent sessions.

**Core pattern:** Fully-streaming cascade pipeline (STT → LLM → TTS) with barge-in handling, budgeted in milliseconds per stage — "zero slack, every stage must hit budget."

Latency budget (500ms total, p95):

| Stage | Budget |
|---|---|
| VAD (end-of-speech detection) | 50ms |
| STT finalization | 100ms |
| Network (STT→LLM) | 20ms |
| LLM prefill + first token | 150ms |
| LLM→TTS handoff | 30ms |
| TTS first audio chunk | 100ms |
| Network (TTS→user) | 50ms |

- **VAD** — Silero VAD (10-30ms, 95%+ accuracy, CPU-only) is production default over WebRTC VAD (faster but 2x false positives) or energy-only (unusable in noisy environments). End-of-speech: 300ms silence threshold (adaptive to 500ms for deliberate speakers).
- **Streaming STT** — Deepgram Nova-2 (100ms finalization after end-of-speech, 3.2% WER clean / 8.5% noisy) chosen over self-hosted Whisper (requires 500ms chunking, adds 200ms). Hot-word boosting for domain vocab (menu items) gives +15% accuracy at zero latency cost.
- **LLM Engine** — self-hosted Llama 3 8B INT4 via vLLM (80ms TTFT, 8ms TPOT, 88% task completion) beats API models (GPT-4o-mini: 200-400ms TTFT including network). Speculative decoding variant cuts TPOT to 3ms. Prompts enforce short, speakable responses (1-2 sentences, ≤50 output tokens ≈15s of speech).
- **Streaming TTS** — self-hosted XTTS v2 (80ms first-chunk, MOS 4.2) is production default over ElevenLabs (200-400ms, MOS 4.5 but $0.18/1K chars vs ~$0.001/min self-hosted). Sentence-boundary buffering (min 5 words, max 500ms wait) feeds TTS incrementally.
- **Barge-In Controller** — AEC (acoustic echo cancellation) strips the agent's own played-back audio from the mic input before VAD runs, so the agent's own TTS doesn't self-trigger. On real barge-in: stop TTS (10ms), cancel LLM generation (10ms), reroute audio to STT (10ms) — full sequence in ~70ms, within the 200ms budget. Two-stage detection (50% volume reduction for 500ms, then full stop if speech continues) avoids jarring cuts from backchannel ("uh-huh") or noise: 3% false-barge-in rate vs 25% for naive immediate-stop.
- **Session State Store** — Redis, with optimistic locking (version numbers) to prevent concurrent-interruption state corruption.

**Pros:**
- Streaming (vs batch) cuts voice-to-voice latency from 2-3s to 400-500ms, which is the difference between "matches human operators" and "30% mid-order abandonment" (800ms) per the chapter's real-world example.
- Self-hosted stack is ~23x cheaper than managed APIs ($33K/day vs $760K/day at 50K concurrent sessions; $0.0019/min vs $0.044/min).
- Two-stage barge-in detection produces the most natural interruption UX (3% false-positive rate) without the 100% missed-interruption rate of a no-barge-in design.
- Contextual pre-loading (menu/account data into KV cache before the caller finishes speaking) shaves 30-40ms off per-turn LLM latency.

**Cons / failure modes:**
- Full streaming pipeline raises task-completion failure rate 2-4% vs batch because partial-transcript errors reach the LLM.
- Speculative execution (starting LLM generation on partial STT) is wrong ~30% of the time, wasting ~25-30% of GPU compute on discarded generations.
- STT provider latency spikes under peak load (Deepgram p95 jumping 100ms→500ms during lunch rush) can blow the whole budget to 900ms; requires multi-provider failover circuit-breaker plus a standing Whisper GPU pool as last resort.
- Background noise (kitchen exhaust, intercom feedback) without location-specific VAD fine-tuning causes false barge-in every 2-5s.
- Native multimodal (audio-to-audio, e.g. GPT-4o voice, Moshi) achieves lower latency (200-300ms) and better naturalness/noise robustness but is 2-3x worse at structured slot-filling/reasoning, is much harder to safety-filter (no text intermediary), and is still research-grade maturity as of 2024-2025 — not viable as the sole architecture for a 50K-session production system.

**When to use:** Transactional, latency-critical spoken interactions (drive-thru, phone IVR/scheduling) where structured reasoning, auditability, and safety filtering matter. Recommended target architecture is pipeline-by-default with multimodal piloted only on low-risk subflows (greetings, FAQ) or as a fallback when STT confidence drops below 70%.

---

## Chapter 31 — Edge and On-Device LLM Deployment

**Problem:** Run an LLM directly on user devices (phone/laptop/embedded) under strict RAM/battery/thermal limits, keep user data on-device for privacy, and route only complex queries to the cloud.

**Core pattern:** Quantized on-device model + on-device routing classifier + confidence-gated cloud fallback, with delta model updates and thermal/battery-aware inference throttling.

- **Quantization** — INT4 (GGUF Q4_K_M, GPTQ, AWQ) is the default for mobile: a 7B model shrinks from 28GB (FP32) to 3.5GB (INT4), fitting a 6GB phone with ~2.5GB headroom. AWQ (activation-aware, protects the ~1% "salient" weights) edges out GPTQ for mobile quality (PPL delta ~0.2-0.3 vs 0.3-0.5). Importance-weighted quantization keeps embeddings, first/last transformer layers, and the LM head at higher precision (FP16/INT8) while quantizing FFN middle layers (60-70% of params) aggressively to INT4.
- **Inference runtime** — llama.cpp (portable, CPU/Metal/CUDA/Vulkan, 10-20 tok/s on mobile ARM) is the general default; Core ML routes to Apple Neural Engine for best iOS throughput (20-35 tok/s) but is iOS-only; MLC-LLM for best Android GPU throughput; ExecuTorch for Llama-family models on mobile. Most production deployments use a runtime adapter layer per platform.
- **On-Device Routing Classifier** — <5MB, <10ms inference (TF-IDF + logistic regression baseline, 80-87% routing accuracy; DistilBERT-tiny for 90-93% if needed). Computes token count, complexity score, document-reference count, estimated context length, and PII flags entirely locally (cannot call the network to decide whether to call the network). Outputs `LOCAL`, `CLOUD_WITH_CONSENT`, or `LOCAL_DEGRADED`.
- **Cloud Proxy** — consent-gated, PII-masking middleware; forwards only retrieved chunks + query (never raw documents or untouched history) to the cloud LLM.
- **Document Retrieval Layer** — on-device embedding model (all-MiniLM-L6-v2, 23MB) + FAISS/SQLite-vec for local RAG without any data leaving the device.
- **Model Update Daemon** — delta/LoRA-adapter updates (50-200MB monthly) instead of full re-downloads (2.3GB); SHA-256 verified, atomic rename swap, 7-day rollback window. On-device A/B testing uses deterministic `hash(device_id + experiment_id)` assignment (no network round-trip needed to pick a variant).
- **Thermal & Battery Monitor** — polls `ProcessInfo.thermalState` (iOS) / `PowerManager` thermal headroom (Android) every 2s; state machine throttles generation (inter-token delays, reduced max_tokens) as temperature rises, halting entirely above 40°C skin temp. Battery <20% reduces max_tokens and disables streaming; <10% routes to cloud or cached responses.

**Pros:**
- Zero-network operation for in-capability queries: true offline mode and no per-query network round-trip (150-300ms saved vs cloud).
- Privacy-by-construction — patient notes / documents never leave the device unless the user explicitly consents per query.
- Delta updates keep monthly bandwidth to 50-200MB instead of multi-GB full re-downloads.
- Hybrid routing captures both the reasoning quality of large cloud models (for complex queries) and the latency/privacy of local inference (for simple ones), without forcing an all-or-nothing choice.
- Concrete example: Phi-3-mini INT4 (2.2-2.4GB) hits 12-20 tok/s on iPhone A17 via Core ML/ANE with full HIPAA-safe on-device operation.

**Cons / failure modes:**
- Quantization is a hard compression/quality tradeoff — Q4_K_M costs +0.25-0.40 perplexity vs FP16; going to Q2_K (+2.0-4.0 PPL) should be avoided except under extreme RAM constraints.
- KV cache grows fast with context: doubling context from 2K to 4K roughly doubles KV cache size (~384MB → ~768MB for Phi-3-mini), a large chunk of a mobile RAM budget; requires INT8 KV cache quantization to control.
- Thermal throttling is a real, user-visible failure mode: sustained inference above 38-40°C forces reduced max_tokens, added inter-token delay, or a full halt mid-generation with a truncated response.
- iOS background execution is essentially disallowed (process killed in ~30s), forcing all inference to foreground and complicating any "continue processing after app switch" UX.
- Runtime choice is a deep platform commitment — switching from llama.cpp to Core ML requires a new conversion pipeline and iOS-only artifacts, creating Android/iOS parity and CI/CD burden.
- Routing misclassification risk: the classifier itself must run in <10ms and <5MB, which caps its accuracy (rule-based: 70-80%) unless a larger on-device classifier (DistilBERT-tiny, 90-93%) is affordable within the RAM budget.

**When to use:** Privacy-sensitive (healthcare, legal, enterprise-restricted-network) or connectivity-constrained (offline, in-flight) use cases, or where sub-100ms first-token latency is required and network round-trip alone would blow the budget. Not suited to workloads needing large-context multi-document reasoning or maximum output quality — those should route to cloud.

---

## Cross-Cutting Themes

- **Per-stage latency budgeting in milliseconds.** All three chapters decompose a hard end-to-end latency target into named stage budgets (Ch.14: 2s STT / 30s summary cycle / 10s final summary; Ch.18: 500ms split across VAD/STT/LLM/TTS/network; Ch.31: 500ms first-token, 200ms for short queries) and engineer each component (chunk size, model size, quantization) to fit its slice.
- **Streaming/incremental processing over batch everywhere on the critical path.** Streaming STT with partial hypotheses (Ch.14, Ch.18), streaming LLM token output (Ch.14, Ch.18), streaming TTS from sentence fragments (Ch.18) — all trade a small amount of quality/coherence for large latency wins, with batch/offline variants reserved for non-real-time re-processing (Ch.14's post-meeting re-diarization; Ch.18's batch pipeline mode; Ch.31's cloud fallback for complex queries).
- **VAD (Voice Activity Detection) as a shared building block.** Silero VAD appears in both Ch.14 (filtering ~40% of STT GPU load) and Ch.18 (50ms-budget end-of-speech and barge-in detection) — same model, same rationale (CPU-only, robust to noise vs WebRTC/energy-only VAD).
- **Small/quantized models on the hot path, larger models off it.** Ch.14 uses a 7B quantized model for 30s incremental updates but a 13B model for the non-time-critical final summary; Ch.18 uses an 8B INT4 model for the 150ms-budget turn response; Ch.31 uses INT4 quantization (Q4_K_M/AWQ) specifically to fit RAM-constrained devices, reserving full-size cloud models for complex fallback queries.
- **Explicit fallback/degradation paths.** Ch.14: stateless STT workers as overflow/recovery fallback for stateful workers; managed STT API as burst overflow. Ch.18: multi-provider STT failover circuit breaker; hybrid pipeline+multimodal fallback keyed on STT confidence. Ch.31: `LOCAL_DEGRADED` and `CLOUD_WITH_CONSENT` routing when on-device capability is insufficient. All three treat graceful degradation as a first-class design requirement, not an afterthought.
- **Cost asymmetry between self-hosted and managed/API options at scale.** Ch.14 (~$0.15/hr self-hosted STT vs $0.90-1.44/hr managed) and Ch.18 ($33K/day self-hosted vs $760K/day managed, 23x) both conclude self-hosting wins decisively once concurrency crosses roughly 5K-10K sessions, with managed APIs reserved for cold-start or low-scale phases.
