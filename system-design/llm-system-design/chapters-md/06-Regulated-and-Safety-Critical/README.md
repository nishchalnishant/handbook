# 06 — Regulated and Safety-Critical Systems

This folder covers LLM system design in domains where mistakes have outsized, non-reversible real-world consequences: education (minors, COPPA/FERPA), healthcare (patient safety, HIPAA), and cross-domain privacy/data governance (GDPR/CCPA/HIPAA). Unlike consumer LLM products where a bad response is a UX annoyance, here a bad response can mean a missed heart attack, an inappropriate response to a 9-year-old, or a six-figure regulatory fine. The common thread across all three case studies:

- **Heavy, layered guardrails** — no single classifier or prompt instruction is trusted; safety is enforced by stacking independent, differently-failing layers.
- **Deterministic overrides of probabilistic systems** — the LLM proposes, a non-LLM (rule engine, validator, symbolic solver) decides on anything safety-critical.
- **Human-in-the-loop escalation** — automated systems are conservative by design and route uncertainty/high-risk cases to humans on tight SLAs.
- **Immutable audit trails** — every decision is logged, cryptographically chained, and retained for years to survive regulatory review.
- **Explicit tolerance for false positives over false negatives** — all three chapters accept degraded UX/efficiency in exchange for near-zero missed-harm rates.

---

## Chapter 13 — Design an AI Tutor for Education

**Problem:** Build a K-12/college AI tutor that teaches via Socratic questioning (never giving direct answers) while enforcing zero-tolerance safety guardrails for minors and handling multimodal homework photos, at 5M users / ~33K peak QPS.

**Core pattern — Pedagogical Socratic tutoring system:**
- **Pedagogical Engine + state machine**: externalizes tutoring logic outside the LLM's stochastic output — `PROBLEM_PRESENTED → INITIAL_PROBE → HINT_LEVEL_1 → HINT_LEVEL_2 → SCAFFOLD → GUIDED_SOLUTION → REFLECTION`. State transitions are deterministic and auditable; the LLM only generates text within the state chosen for it.
- **Answer-withholding enforcement stack**: system prompt rules → few-shot Socratic exemplars → post-generation "answer-giving" classifier (fine-tuned BERT, regenerate if P(gives_answer) > 0.7) → state machine barrier (can't jump to SCAFFOLD/GUIDED_SOLUTION prematurely). Combined approach reaches 99%+ withholding success vs. 80-85% for prompting alone.
- **Bayesian Knowledge Tracing (BKT)**: per-skill mastery estimate (4 latent params: P(initial), P(learn), P(slip), P(guess)) drives adaptive difficulty; targets Zone of Proximal Development (~65-70% success probability) rather than fixed grade-level difficulty.
- **Defense-in-depth safety stack (4 layers)**: (1) input pre-filter — keyword blocklist + jailbreak/intent classifier + PII detector + self-harm crisis detector (15-min human escalation SLA); (2) prompt-level age-gating (content detail scales by grade band 5-8 / 9-12 / 13-17 / 18+); (3) output post-filter — content safety classifier + toxicity detector + answer-giving detector + math fact-checking; (4) human moderation queue with tiered SLAs (self-harm 15 min, jailbreak 2 hr, quality flags 24 hr) plus 0.1% random audit sampling.
- **Math Verification Service**: independent SymPy symbolic solver pre-solves the problem before the LLM responds; verified solution is injected into hidden LLM context to anchor hints, and cross-checked post-hoc — discrepancies trigger regeneration rather than surfacing a wrong hint.
- **Multimodal pipeline**: image preprocessing → CNN content classifier → specialized TrOCR-math OCR (CROHME-tuned) for the primary path, with VLM fallback only for low-confidence (<0.7) cases — hybrid achieves ~93%/87% (printed/handwritten) accuracy at ~$12K/day vs. $48-144K/day for all-VLM.
- **COPPA compliance architecture**: verifiable parental consent (email + payment) for under-13 signup, data minimization, parent dashboard with full transcript access and one-click deletion, 30-day cascade deletion on account closure, zero third-party data sharing (all inference on platform-owned infra).

**Pros:**
- Full defense-in-depth reaches <0.1% combined false-negative rate on harmful content (vs. 20-30% for keyword-only blocklists).
- State-machine pedagogy demonstrably improves outcomes: real-world example shows exam scores recovering after switching from freeform chat to Socratic state machine.
- Cost-efficient multimodal design (hybrid OCR) is 4-12x cheaper than pure VLM at comparable accuracy.
- Pre-solving math with SymPy eliminates an entire class of hint errors for ~100ms latency cost.

**Cons / failure modes:**
- Determined students still bypass answer-withholding via adversarial phrasing ("confirm my answer is 42") — requires monthly red-teaming and an evolving adversarial dataset even at 99%+ enforcement.
- Full defense-in-depth carries a 3-5% false-positive rate (blocking safe content) — deliberately accepted as the cost of <0.1% false negatives.
- 10-15x traffic spike concentrated in a 3-hour homework window (3-6 PM) requires aggressive autoscaling (2,000 → 14,000 GPUs) and graceful degradation (routing K-5 to a faster 7B model under extreme peak).
- Image upload quality varies wildly (30% of photos partially obscured/blurry/poorly lit) — pipeline must communicate uncertainty ("Is that what you wrote?") rather than silently guessing.
- High engineering cost: state machine + BKT integration is rated "4-8 weeks of engineering effort" vs. hours for a system-prompt-only approach.

**When to use:** Any tutoring/pedagogical product for minors where direct-answer leakage undermines the product's value proposition and where regulatory exposure (COPPA/FERPA) is real. Not needed for adult-facing Q&A tools with no pedagogical withholding requirement.

---

## Chapter 20 — Design a Healthcare Triage and Diagnostic Assistant

**Problem:** Build an LLM-powered triage system that interviews patients, assigns ESI acuity levels, and gives preliminary diagnostic guidance — with zero tolerance for missed critical (ESI 1-2) symptoms, PHI that must never reach external LLM APIs, deterministic escalation, and a full regulatory audit trail, at 1M sessions/day.

**Core pattern — Safety-critical healthcare triage with HIPAA compliance ("the LLM advises, the deterministic system decides"):**
- **2-pass PHI de-identification pipeline**: Pass 1 — fine-tuned clinical NER (BioBERT-large, 400M params, F1=97.8%/recall=98.9% on i2b2/2014); Pass 2 — regex + 50K-name dictionary for structured/edge-case patterns. Combined recall >99.5%. Typed placeholders (`[NAME_1]`, `[DATE_1]`) preserve entity-type context for coherent LLM follow-ups, vs. generic `[REDACTED]` which reduces question quality ~18%. Re-identification only replaces placeholders present in the session's mapping table — hallucinated tokens are left untouched and flagged.
- **Deterministic red-flag detection engine, run in parallel with (never gated on) the LLM**: Layer 1 keyword/pattern rules (~500 rules, <5ms, e.g. "chest pain" + "arm/jaw/shortness of breath" → ESI 2); Layer 2 medical NER + clinical inference handles negation and temporal context. Combined sensitivity >99.9% on a 50K-case held-out set. If a red flag fires, LLM output is discarded entirely — safety overrides the LLM, not the reverse.
- **Clinical Safety Validator**: a separate 500M-param classifier (not the triage LLM) checks acuity consistency, dangerous-advice screening, and differential-diagnosis plausibility against a closed list of ~500 approved ICD-10 codes — LLM output outside that list is stripped.
- **Confidence-gated clinician handoff**: tiered logic table (clear emergency → bypass LLM entirely; ambiguous/low-confidence → default escalation; LLM under-triage vs. rule engine → override to higher ESI). Structured JSON handoff summary delivered to clinicians within a hard 30-second SLO via HL7 FHIR R4 integration with Epic/Cerner.
- **temperature=0** for all acuity classifications (deterministic, reproducible, auditable); temperature=0.3 only for cosmetic follow-up question phrasing.
- **WORM immutable audit trail**: every turn logs prompt, response, model/prompt version, safety-check results, and decision trace; SHA-256 hash-chained entries in S3 Object Lock (Compliance mode); 7-year retention (HIPAA minimum). Recommended stack: S3 Object Lock + Athena for query + DynamoDB for hot session state.
- **Mandatory 7-day shadow deployment** for any new model version before promotion, requiring no statistically significant sensitivity change, acuity distribution within 2% of production, and clinical review board sign-off.

**Pros:**
- LLM + deterministic-override architecture reaches >99.9% sensitivity on ESI 1-2 (vs. 95% rule-only, 98% LLM-only) — the chapter states LLM-only is "NEVER for production" because it has no deterministic failure bound and FDA SaMD reviewers will reject it.
- Real-world example: LLM-augmented triage with a red-flag layer cut urgent misclassification from 8% (rule-only) to 0.3%.
- Cost is trivial relative to risk: ~$0.0007/session, well under the $0.01 budget.
- On-premise deployment breaks even vs. cloud API at ~6 months for hospital-scale volume and gives zero (not "low") PHI exposure risk.
- Structured chain-of-thought clinical reasoning reduces ESI misclassification ~12% by forcing symptom evidence to be articulated before a level is committed.

**Cons / failure modes:**
- Two fully independent systems (rule engine + LLM + validator) triple maintenance burden — quarterly rule reviews and monthly model evaluations run on separate schedules.
- Accepted 15% over-triage rate (specificity 85%) is a deliberate tradeoff — unnecessary escalations cost clinician time but are "clinically acceptable" against the cost of one missed MI.
- Real-world cited failure: a hospital was fined $1.2M after patient names/DOBs leaked into a third-party LLM API in prompt text — a single missed de-identification layer is a compliance-ending event.
- Ensemble (second 70B "opinion" LLM) pushes p99 latency past the 2s SLO for the ~10% of cases that trigger it, despite reaching 99.95% sensitivity — a documented latency/safety tradeoff.
- PostgreSQL-only audit storage is explicitly called out as **insufficient for HIPAA** because a superuser can mutate rows — only WORM-enforced storage passes compliance review.

**When to use:** Any clinical decision-support or triage system where regulatory bodies (FDA SaMD, HIPAA) will audit outputs and where a missed detection has patient-safety consequences. Not appropriate to run LLM-only without a deterministic safety layer under any circumstance the chapter describes.

---

## Chapter 30 — Privacy, Compliance, and Data Governance for LLM Systems

**Problem:** Design a privacy/compliance layer for any production LLM system handling personal data (PHI/PII) — de-identifying data before it reaches external model APIs, enforcing per-user ACL on retrieval, supporting right-to-erasure (including in fine-tuned weights) within regulatory SLAs, and producing an audit trail sufficient for regulatory inquiry.

**Core pattern — Defense-in-depth privacy stack:**
- **PII Detection and De-identification Gateway** (boundary component, fail-closed if unavailable): two-pass regex (<5ms, structured PII: SSN/phone/email/DOB/MRN/NPI) + NER (spaCy clinical / Presidio, confidence threshold 0.85, <55ms) → **entity-consistent pseudonymization** ("John Smith" / "Mr. Smith" / "the patient" all map to the same `Patient_A7` token via canonicalization + coreference resolution) rather than generic redaction, which breaks coreference and produces incoherent LLM output. Pseudonym map lives only in server-side session state.
- **Indirect prompt-injection defense for RAG**: ingest-time scanning of documents for instruction-like patterns, XML-tag wrapping of retrieved context (`<retrieved_context>`) with explicit "never override instructions" system-prompt language, plus output anomaly monitoring (base64 blobs, unexpected URLs).
- **Data Residency Router**: routes by account-metadata jurisdiction (not IP geolocation) to fully isolated regional stacks (own endpoint, vector shard, audit log). Region-locked API endpoints (Azure OpenAI EU, Bedrock eu-west-1/eu-central-1, Vertex AI europe-west) are contractually the strongest external-API option; self-hosted-in-VPC and on-prem are stronger still but far higher cost/ops burden.
- **Vendor DPA/BAA Assessment Registry**: a CI-gate checklist (BAA signed, PHI-not-used-for-training confirmed in writing, encryption verified via SOC 2, retention/deletion mechanism specified, breach notification ≤ HIPAA's 60-day window; GDPR: Article 28 DPA elements, 2021 SCCs, Article 30 record, sub-processor equivalence; CCPA: no "sale," opt-out mechanism, 45-day deletion) gates any new external API/tool integration before it can receive user data.
- **Right-to-Erasure Orchestrator**: coordinated deletion across document store (hard delete, ms), vector index (tombstone immediately, ms; full physical rebuild monthly, ~4-5 hrs for 500K chunks), query logs (delete or filtered-manifest for write-once stores), and — hardest — fine-tuned model weights via **SISA training** (sharded/isolated/sliced/aggregated: retrain only the affected shard-slice, ~10% of original fine-tune compute) or **influence functions** (approximate, O(n·d) per deleted example) when SISA wasn't architected in from the start. Audit logs themselves are never deleted — they record that deletion occurred, not the personal data itself.
- **ACL-aware retrieval**: query-time metadata pre-filter (index-time tagging, ~2-5ms overhead) is the production default — evaluated against per-user index (too costly, O(users×docs)), post-retrieval filtering (unauthorized docs enter memory before being discarded — race-condition risk), and LLM-based access decisions (explicitly called "catastrophic" / must never be primary enforcement). Nightly audit-log reconciliation retroactively detects ACL bypass (cache staleness, filter bugs, missing ACL tags).
- **Consent management**: explicit opt-in required for model-training use of queries (`not_set` defaults to `false`) per GDPR Article 6.

**Pros:**
- De-identification stays well within latency budget (~55ms vs. 200ms budget) and is cheap relative to LLM inference time.
- Tombstoning gives millisecond logical deletion, meeting 30-day GDPR/45-day CCPA SLAs without requiring an immediate expensive full rebuild.
- SISA reduces unlearning retraining cost to ~10% of full fine-tune compute (vs. full retrain from scratch) — practical at 7B model scale (~50 min shard retrain vs. 8 GPU-hours full).
- Region-locked API endpoints add only 80-150ms vs. US endpoints — data residency compliance is nearly free on the latency budget.
- Query-time ACL filtering adds only ~2-5ms and is independent of index size, unlike per-user indexes which don't scale.

**Cons / failure modes / tradeoffs:**
- A signed DPA/BAA is "necessary but not sufficient" — real example: a provider's abuse-monitoring logging (permitted under general terms even after a signed DPA) retained PHI outside any BAA-covered pipeline after a policy change.
- Tombstoning is only *logical* deletion — embeddings remain on disk/in the ANN structure until a full rebuild; a sophisticated attacker with direct index access could reconstruct proximity information. Must be disclosed in the DPIA.
- Machine unlearning (SISA/influence functions) is explicitly "approximate" — neither guarantees zero memorization; residual risk is typically <5% and requires post-hoc membership-inference-attack testing to bound.
- Retrofitting SISA to a model not originally partitioned for it requires full retraining from scratch — this must be architected before the first fine-tune, not after.
- Post-retrieval filtering is a common but weak pattern: unauthorized documents enter application memory/logging paths before being discarded, creating leak risk if any downstream step runs first.
- Real example: RAG retrieval filtered on file extension but not document-level ACL, surfacing a third party's HR disciplinary records to an unauthorized user — an Article 17 violation caused purely by wrong-layer enforcement (post-retrieval instead of index/query-time).

**When to use:** Required from day one for any regulated-industry LLM system (healthcare, finance, legal) or any system processing GDPR/CCPA-covered personal data; complexity compounds specifically when using external API providers rather than self-hosted models. LLM-based ACL decisions should never be used as primary enforcement in any context.

---

## Cross-Cutting Themes

- **Deterministic layer overrides the LLM on anything safety-critical.** Chapter 20's red-flag engine and safety validator can override/discard LLM output outright; Chapter 13's pedagogical state machine and answer-giving detector block the LLM from reaching disallowed states; Chapter 30's ACL filter and PII gateway sit structurally in front of the LLM rather than relying on prompted self-restraint.
- **Conservative-by-default / false-positive-over-false-negative tuning.** All three chapters explicitly accept a higher false-positive rate to drive false negatives toward zero: Ch.13 tunes safety thresholds to minimize missed unsafe content even at 3-5% over-blocking; Ch.20 accepts a 15% over-triage rate to guarantee >99.9% sensitivity on ESI 1-2; Ch.30 fails closed (rejects requests) if the de-identification pipeline is unavailable rather than passing raw PII through.
- **Human-in-the-loop escalation on tight, tiered SLAs.** Ch.13: self-harm 15 min / jailbreak 2 hr / quality 24 hr, plus 0.1% random audit. Ch.20: ESI 1 <30s, ESI 2 <2 min, low-confidence cases default to clinician escalation. Ch.30: verified deletion requests and DPA/BAA gates require documented human/compliance sign-off before data flows to a new vendor.
- **Immutable, cryptographically-chained audit trails with multi-year retention.** Ch.20 mandates 7-year WORM (S3 Object Lock Compliance mode) retention with SHA-256 hash chaining; Ch.30 requires ≥6-year append-only chained logs and explicitly states audit logs are the one thing *never* deleted, even under right-to-erasure. Both chapters call out that a standard mutable relational database (plain Postgres) is insufficient for compliance regardless of access controls.
- **Regulatory/compliance requirements are engineered as architecture, not policy.** COPPA (Ch.13), HIPAA (Ch.20), and GDPR/CCPA (Ch.30) obligations are each translated into concrete pipeline components (parental-consent gating, PHI de-identification gateways, SISA-partitioned fine-tuning) rather than left as legal-team documentation — and each chapter notes that policy-only controls (a signed BAA/DPA, a stated retention policy) are insufficient without a technical enforcement mechanism.
- **Latency/cost is a secondary constraint that safety budgets absorb.** Each chapter reserves latency headroom or accepts added cost for safety steps: Ch.13's math verification adds ~100ms to prevent bad hints; Ch.20 reserves 800ms of explicit "headroom" in its 2s budget "never trade safety for speed"; Ch.30's de-identification and ACL filtering are engineered to stay under 200ms/5ms specifically so they don't force safety shortcuts under load.
