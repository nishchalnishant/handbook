---
title: "Chapter 20: Design a Healthcare Triage and Diagnostic Assistant"
tags: [llm, system-design, healthcare, hipaa, safety-critical, phi, regulated, case-study]
chapter: 20
part: case-studies
---

# Chapter 20: Design a Healthcare Triage and Diagnostic Assistant

## Context

> [!info] Quick Reference
> - **Pattern:** Safety-critical healthcare triage with HIPAA compliance
> - **Scale:** 1M triage sessions/day, ~35 sessions/sec peak
> - **Key Techniques:** 2-pass PHI de-identification (NER + regex, > 99.5% recall), deterministic red-flag engine (> 99.9% sensitivity), clinical safety validator, temperature=0, WORM audit trail
> - **Primary Concerns:** Zero missed ESI 1-2 emergencies, HIPAA PHI protection, 7-year audit retention, regulatory defensibility
> - **Cross-references:** Chapter 5 (safety stack), Chapter 11 (accuracy requirements), Chapter 17 (audit trail patterns), Chapter 30 (privacy, compliance, and HIPAA-aware retrieval)

**Problem statement:** Design an LLM-powered healthcare triage system that conducts structured symptom interviews, assigns acuity levels, and provides preliminary diagnostic guidance—with zero tolerance for missed critical symptoms, strict HIPAA compliance (PHI must never reach LLM API endpoints), deterministic escalation to human clinicians, and a complete audit trail for regulatory review.

### Real-World Examples

- A telehealth platform handles 1M triage sessions/day. Their rule-based system misclassifies 8% of urgent cases as non-urgent because it can't interpret free-text symptom descriptions ("my chest feels tight and my arm is tingly" should be ESI Level 2, but keyword matching only catches "chest pain"). Deploying an LLM-augmented triage system with a deterministic red-flag detector reduces urgent misclassification to 0.3% while maintaining 2s response latency. The LLM handles natural language understanding; the deterministic layer handles safety-critical decisions.
- A hospital emergency department uses an AI triage assistant to pre-screen patients in the waiting room via tablet. The system must never store PHI in cloud LLM logs. After a HIPAA audit reveals that patient names and dates of birth were being sent to a third-party LLM API in prompt text, the hospital faces a $1.2M fine. Redesigning with a PHI scrubbing pipeline (de-identification before API calls, on-premise re-identification after) eliminates the exposure while preserving clinical accuracy.

---

## Step 1: Understand the Problem and Establish Design Scope

### Functional Requirements

- **Conduct structured symptom interviews:** The system must ask adaptive follow-up questions that branch based on prior patient responses—a patient who mentions "chest pain" should be asked about radiation, diaphoresis, and onset duration, not about unrelated symptoms.
- **Classify patients into ESI acuity levels 1-5 with confidence scores:** Every classification must emit a probability score alongside the level (e.g., ESI 3, confidence=0.87) so downstream components can trigger escalation when confidence is low, and so audit records reflect the uncertainty present at decision time.
- **Detect critical symptoms (red flags) deterministically—independent of LLM output:** The red-flag engine must fire on its own signal, never waiting for or depending on the LLM's assessment; this architectural separation ensures that LLM failures, hallucinations, or latency spikes cannot delay a life-saving escalation.
- **Escalate ESI 1-2 cases to human clinicians with structured handoff summaries:** Escalation is not a simple alert—it includes a machine-readable JSON summary with symptom timeline, vital-sign flags, and conversation transcript so the receiving clinician can act within seconds without reading a free-text wall.
- **Provide preliminary diagnostic differentials for ESI 3-5 cases (informational only, not prescriptive):** Differentials are constrained to a curated list of ~500 ICD-10 codes validated for triage use; any LLM-generated code outside this list is stripped before display to prevent patients from acting on hallucinated rare diagnoses.
- **De-identify all PHI before any text is sent to external LLM APIs:** The de-identification pipeline runs as a synchronous blocking step in the request path—no LLM call is initiated until the scrubbed text has been confirmed to contain zero detected PHI entities by both the NER model and the regex layer.
- **Re-identify responses for display to the patient:** After the LLM returns a response containing typed placeholders (e.g., `[NAME_1]`), the re-identification service performs a lookup in the encrypted, session-scoped PHI mapping table to restore original values before the text ever leaves the trust boundary.
- **Generate structured clinical summaries for clinician handoff:** Summaries follow a standardized template (chief complaint, symptom timeline, red flags detected, ESI classification with confidence, conversation log link) that integrates directly with EHR systems via HL7 FHIR R4 APIs.
- **Log every interaction with immutable audit trail for HIPAA compliance and regulatory review:** Each audit record is cryptographically chained to the prior record using SHA-256 hashes, stored in WORM-compliant storage (AWS S3 Object Lock, Compliance mode), and retained for 7 years—the minimum required by HIPAA; the chain allows any tampering to be detected forensically.

### Non-Functional Requirements

- **Latency:** p95 < 2s per response turn (including PHI scrubbing + LLM inference + safety checks).
- **Throughput:** 1M sessions/day = ~11.6 sessions/sec average, ~35 sessions/sec peak.
- **Safety:** Zero missed ESI 1-2 red flags. Target sensitivity > 99.9% for critical symptom detection. Specificity > 85% (acceptable over-triage rate: 15%).
- **Privacy:** PHI exposure to external APIs: exactly zero. All 18 HIPAA identifiers scrubbed with > 99.5% recall.
- **Audit:** Every session fully reconstructable from logs. Model version, prompt version, and decision trace logged per turn.
- **Availability:** 99.99% for triage service (healthcare-grade).
- **Cost:** < $0.01 per triage session.

### Back-of-the-Envelope Estimation

#### Traffic Profile

- Sessions/day: 1M
- Peak (3x): ~35 sessions/sec
- Turns per session: 6
- More precisely: at peak, ~4,200 concurrent sessions × 1 turn every 20s = **210 turns/sec**
- Avg input tokens/turn: 400 (system prompt + patient history + current question context)
- Avg output tokens/turn: 150 (follow-up question + reasoning)
- Peak input tokens/sec: `210 × 400 = 84K tokens/sec`
- Peak output tokens/sec: `210 × 150 = 31.5K tokens/sec`

#### Latency Budget (2,000ms total)

| Stage | Budget | Notes |
|---|---|---|
| Client → API gateway | 50ms | HTTPS, regional deployment |
| PHI de-identification | 80ms | NER model + regex on patient input |
| Session context assembly | 30ms | Retrieve conversation history + patient profile (de-identified) |
| Red-flag detector (deterministic) | 20ms | Rule engine + symptom NER, runs in parallel with LLM |
| LLM inference (prefill + decode) | 800ms | 7B model, ~400 input tokens, ~150 output tokens |
| Clinical safety validator | 100ms | Checks LLM output against medical guidelines |
| PHI re-identification | 30ms | Replace placeholders with original PHI for patient display |
| Audit log write | 50ms | Async, non-blocking (but must confirm write) |
| Response serialization + delivery | 40ms | |
| **Headroom** | **800ms** | Generous buffer for safety—never trade safety for speed |
| **Total** | **2,000ms** | |

#### GPU/Compute Sizing

- Model: 7B medical-fine-tuned (INT4), ~18GB VRAM
- Throughput per GPU: ~2,000 output tokens/sec with continuous batching
- Required output throughput: 31.5K tokens/sec (peak)
- With 2x redundancy: **32 GPUs**
- PHI de-identification model (NER, 400M params): 2 GPUs (handles 1,000 texts/sec)
- Red-flag detector: CPU-only (rule engine + lightweight NER), 4 CPU nodes
- Clinical safety validator: 2 GPUs (small classifier)
- Total compute: ~36 GPUs + 4 CPU nodes

#### Storage

- Audit log per session: ~10KB (all turns, decisions, model versions, timestamps)
- Daily audit logs: `1M × 10KB = 10 GB/day`
- Retention requirement: 7 years (HIPAA) → `10 GB × 365 × 7 = 25.5 TB`
- Immutable storage: S3 with object lock (WORM compliance) or equivalent

#### Cost Per Session

- LLM inference (self-hosted 7B): ~$0.50/1M output tokens
- Tokens per session: `6 turns × 150 output = 900 tokens`
- LLM cost/session: `900 × $0.50/1M = $0.00045`
- PHI pipeline + safety checks: ~$0.0002/session
- Audit storage: `10KB × $0.023/GB = $0.00000023/session`
- **Total: ~$0.0007/session** ← well under $0.01 budget

---

## Step 2: Propose High-Level Design and Get Buy-In

### Core Architecture Components

- **Patient Interface:** Web/mobile/tablet app with accessible UI (WCAG 2.1 AA). Supports text input and structured symptom selection. Displays NPC-style conversational triage flow. The interface is designed for symptomatic, anxious users: font size ≥ 16px, high-contrast mode, voice input for patients who struggle to type, and progressive disclosure of questions (one question at a time, not a wall of form fields) to reduce cognitive load and improve answer quality.
- **API Gateway:** HIPAA-compliant gateway with TLS 1.3, mTLS for internal services, authentication (patient session token), rate limiting, and request routing. The gateway enforces strict payload size limits (max 4prompt injection via oversized inputs, and applies per-session rate limits (max 20 requests/minute) to block automated abuse while accommodating slow typists.
- **PHI De-identification Service:** NER-based pipeline (fine-tuned clinical NER model) + regex patterns that strip all 18 HIPAA identifiers from patient input before it leaves the trust boundary. Replaces with deterministic typed placeholders (e.g., `[NAME_1]`, `[DOB_1]`). The service is synchronous and blocking—no downstream component receives unprocessed text; if the de-identification service is unavailable, the entire request fails safe (returns an error) rather than forwarding raw PHI.

> **Why typed placeholders over generic `[REDACTED]`:** The LLM needs entity-type context to generate clinically coherent follow-up questions.

- **Red-Flag Detection Engine:** Deterministic rule engine + medical NER that identifies critical symptoms (chest pain + arm numbness = possible MI, sudden severe headache + neck stiffness = possible SAH). Runs in parallel with LLM—never gated on LLM output. Triggers immediate clinician escalation for ESI 1-2 patterns. The engine operates on the original patient text before de-identification (within the trust boundary) to avoid any information loss from placeholder substitution affecting rule matching.

> **Why deterministic rules rather than relying on the LLM for red-flag detection:** LLMs are probabilistic—they can and do miss critical symptoms under token distribution pressure, attention dilution over long contexts, or subtle phrasing va...

- **Triage LLM Service:** 7fine-tuned model for generating follow-up questions, interpreting symptoms in natural language, and producing acuity classifications. Receives ONLY de-identified text. temperature=0 for all acuity classifications (deterministic greedy decoding) and temperature=0.3 for follow-up question generation (slight variation makes the conversation feel less robotic while not affecting safety-critical decisions).

> **Why a 7B fine-tuned model over a larger general-purpose model:** At 1M sessions/day with a 2-second total latency budget, a 7B INT4 model delivers ~150 output tokens in 300–400ms on a single A100 GPU and costs ~$0.0007/ses...

- **Clinical Safety Validator:** Post-LLM output check that verifies: (1) recommended acuity level is consistent with detected symptoms, (2) no dangerous advice is present (e.g., "take aspirin" without allergy check), (3) differential diagnoses are within approved list, (4) escalation triggers are not suppressed. The validator runs as a separate lightweight classifier (500M params) fine-tuned specifically on clinical safety violations—it is not the same model as the triage LLM and cannot be "talked out of" a safety violation by the LLM's reasoning.

> **Why a separate safety validator rather than prompting the LLM to self-check:** Self-checking via prompt ("Review your answer for safety issues") is unreliable because the same model that produced a flawed output is likely to rationalize...

- **PHI Re-identification Service:** Replaces placeholders in LLM output with original PHI for patient-facing display. Operates within the trust boundary. The service maintains a strict allowlist: only placeholders that exist in the current session's PHI mapping table are replaced—any unrecognized token that looks like a placeholder (e.g., a hallucinated `[NAME_2]` when only `[NAME_1]` was registered) is left as-is and flagged for review, preventing the LLM from injecting fabricated names into patient-visible output.
- **Clinician Handoff Service:** Generates structured handoff summaries for ESI 1-2 escalations. Integrates with hospital paging systems (Spok, PerfectServe), EHR systems (Epic, Cerner) via HL7 FHIR R4 APIs, and nurse station alert boards. The handoff summary is delivered within 30 seconds of escalation trigger—this is a hard SLO, not a target—because clinical intervention windows for MI and stroke are measured in minutes.
- **Audit Trail Service:** Immutable append-only log of every interaction. Stores: patient input (encrypted), de-identified input, LLM prompt, LLM response, safety check results, acuity decision, model version, prompt version, timestamp, session ID. WORM storage (Write Once Read Many). Each log entry is appended with a SHA-256 hash of the concatenation of the previous entry's hash and the current entry's content, forming a tamper-evident chain analogous to a Merkle tree leaf sequence.
- **Session State Store:** Encrypted session storage (AES-256-GCM) for conversation history, accumulated symptom list, and running acuity assessment. Data is stored in Redis Cluster with a 4-hour session TTL; on session completion, the final state is flushed to the audit trail and the in-memory state is zeroed. Encryption keys are managed per-session via AWS KMS or HashiCorp Vault, not embedded in the application.
- **Model Registry:** Versioned storage of all model artifacts (LLM weights, tokenizer configs, NER models, safety classifiers) with deployment history and SHA-256 checksums. Required for regulatory review ("which model version produced this output 3 years ago?"). Every model artifact is stored in immutable object storage alongside its validation report, clinical evaluation results, and the date range during which it was in production.

### Pipeline A: PHI Protection and De-identification Pipeline

1. Patient submits text input via client app (HTTPS/TLS 1.3).
2. Input arrives at API gateway within the **trust boundary** (on-premise or VPC with no external egress).
3. PHI de-identification service processes the raw input:
   - (a) Clinical NER model (fine-tuned BioBERT, 400M params) extracts entities: names, dates, locations, MRNs, SSNs, phone numbers, email addresses.
   - (b) Regex layer catches structured patterns: dates (MM/DD/YYYY), phone numbers, SSNs, email formats, ZIP codes.
   - (c) Age normalizer: exact ages > 89 are generalized to "90+" (HIPAA Safe Harbor).
   - (d) Each detected PHI element is replaced with a typed placeholder: `[NAME_1]`, `[DATE_1]`, `[LOCATION_1]`, etc.
   - (e) A PHI mapping table is created: `{[NAME_1]: "John Smith", [DATE_1]: "03/15/1985", ...}`. This table is stored ONLY within the trust boundary, encrypted, with session-scoped TTL.
4. De-identified text is now safe to send to the LLM (cloud-hosted or on-premise).
5. After LLM generates response, PHI re-identification service replaces placeholders: `"[NAME_1], based on your symptoms..."` → `"John Smith, based on your symptoms..."`
6. Re-identified response sent to patient. PHI mapping table destroyed after session ends.

**De-identification accuracy targets:**

| PHI Type | Detection Method | Target Recall | Target Precision | Risk if Missed |
|---|---|---|---|---|
| Patient names | NER + dictionary | > 99.5% | > 95% | High—name in LLM logs |
| Dates (DOB, admission) | Regex + NER | > 99.8% | > 98% | High—DOB is a key identifier |
| SSN/MRN | Regex | > 99.99% | > 99% | Critical—direct identifier |
| Phone/email | Regex | > 99.9% | > 99% | Medium—quasi-identifier |
| Locations (address) | NER | > 98% | > 90% | Medium—contextual identifier |
| Ages > 89 | Rule | 100% | 100% | Low—Safe Harbor rule |

### Pipeline B: Triage Inference and Safety Pipeline

1. De-identified patient input + session history assembled into LLM prompt.
2. **Parallel execution:**
   - (a) Red-flag detector analyzes raw patient input (pre-de-identification, within trust boundary) for critical symptom patterns. Deterministic rules—no ML uncertainty.
   - (b) LLM generates follow-up question or acuity assessment.
3. Red-flag detector result arrives first (20ms). If red flag detected:
   - Immediate escalation to clinician handoff service. Patient sees: "Based on your symptoms, I'm connecting you with a clinician immediately."
   - LLM output is discarded (safety overrides LLM).
   - Audit log records: red-flag trigger, symptoms matched, escalation timestamp.
4. If no red flag: LLM output passes through clinical safety validator:
   - (a) Acuity consistency check: if LLM says ESI 4 but symptom list includes "chest pain", validator overrides to ESI 2 and triggers escalation.
   - (b) Advice safety check: scan for contraindicated recommendations (medication suggestions without allergy context, "wait and see" for potentially urgent symptoms).
   - (c) Differential plausibility check: compare LLM-suggested differentials against an approved ICD-10 code list. Flag unknown or rare diagnoses for clinician review.
5. Validated response is re-identified and sent to patient.
6. Session state updated: accumulated symptom list, current acuity estimate, turn count.
7. After 6 turns (or earlier if acuity is determined): final acuity classification generated. Structured summary produced for clinician handoff (even for ESI 3-5, the summary is available for the clinician who eventually sees the patient).
8. Audit log entry written with full decision trace.

### Mermaid Architecture Diagram

```mermaid
flowchart LR
  patient[PatientApp Web/Mobile] -->|TLS 1.3| gateway[APIGateway HIPAA-compliant]

  gateway --> trustBoundary[TrustBoundary On-Prem/VPC]

  trustBoundary --> phiScrub[PHIDeidentificationService NER+Regex]
  trustBoundary --> redFlag[RedFlagDetector Deterministic Rules]

  phiScrub -->|de-identified text| llmService[TriageLLMService 7B Medical]
  phiScrub --> phiMap[PHIMappingTable Encrypted SessionScoped]

  redFlag -->|ESI 1-2 detected| escalation[ClinicalEscalation Immediate]
  escalation --> clinician[ClinicianHandoffService Pager+EHR]

  llmService --> safetyValidator[ClinicalSafetyValidator]
  safetyValidator -->|pass| phiReident[PHIReidentificationService]
  safetyValidator -->|fail: override acuity| escalation
  safetyValidator -->|fail: unsafe advice| regenerate[RegenerateWithConstraints]
  regenerate --> llmService

  phiReident --> phiMap
  phiReident --> patient

  sessionStore[SessionStateStore Encrypted] --> phiScrub
  sessionStore --> llmService

  auditLog[AuditTrailService Immutable WORM] --> gateway
  auditLog --> phiScrub
  auditLog --> llmService
  auditLog --> safetyValidator
  auditLog --> redFlag

  modelRegistry[ModelRegistry Versioned] --> llmService
  modelRegistry --> phiScrub
  modelRegistry --> safetyValidator
```

---

## Step 3: Design Deep Dive

Focus areas:

1. **PHI Protection Pipeline (pre-API scrubbing, de-identification architecture, on-premise vs cloud)**
2. **Clinical Safety and Deterministic Escalation (symptom checkers, red-flag detection, confidence-gated handoff)**
3. **Audit Trail and Compliance (immutable logging, HIPAA audit requirements, model versioning)**

### 1) PHI Protection Pipeline

PHI exposure to external APIs is a zero-tolerance constraint. A single PHI leak to a cloud LLM provider can result in HIPAA violations with fines of $100-$1.9M per incident category.

**De-identification architecture:**

The pipeline uses a two-pass approach for maximum recall:

**Pass 1: Clinical NER model (ML-based)**
- Model: Fine-tuned BioBERT-large (400M params) on i2b2/2014 de-identification dataset + synthetic clinical notes.
- Entity types: PATIENT, DOCTOR, DATE, HOSPITAL, LOCATION, PHONE, FAX, EMAIL, SSN, MRN, ACCOUNT, LICENSE, VEHICLE, DEVICE, URL, IP, AGE (>89).
- Performance on i2b2/2014 test set: F1 = 97.8%, recall = 98.9%.
- Inference: ~20ms per text on GPU (batch of 32).

**Pass 2: Regex + dictionary layer (rule-based)**
- Catches structured patterns that NER misses: dates in non-standard formats ("March fifteenth, nineteen eighty-five"), phone numbers with unusual delimiters, SSNs with spaces.
- Dictionary of 50K common names (US Census) as a fallback for NER misses.
- State/city dictionary for location detection.
- Adds ~5ms per text.

**Combined recall: > 99.5% on held-out clinical text.**

**Placeholder strategy:**

| Approach | How It Works | Strengths | Weaknesses | Use When |
|---|---|---|---|---|
| Generic placeholder | Replace all PHI with `[REDACTED]` | Implementation is a simple string substitution requiring no mapping table or session state; zero risk of re-identification errors | The LLM loses entity-type context—"How old are you, [REDACTED]?" is grammatically and semantically broken, reducing follow-up question quality by ~18% in A/B testing and increasing hallucinated entity references | No |
| Typed placeholder | Replace with `[NAME_1]`, `[DATE_1]` | The LLM understands entity types and generates grammatically coherent, contextually appropriate follow-up questions; re-identification is a simple lookup in the session-scoped mapping table | Slight information leakage: the cloud LLM API provider can infer that a name (or date, or location) existed even though the value is hidden; also, unusual entity counts (e.g., 7 distinct names in one session) could be quasi-identifying | **Yes—production default** |
| Synthetic replacement | Replace "John Smith" with "Alex Johnson", "03/15/1985" with "07/22/1990" | Most natural for the LLM—the model sees realistic entity values, producing the highest-quality conversational output; useful for generating synthetic training data that mirrors real distributions | Generating clinically safe synthetic replacements is hard: a synthetic DOB changes the patient's apparent age, which can alter triage decisions (a "42-year-old" presenting with chest pain vs a "67-year-old" are different clinical scenarios); also requires a generative model to produce realistic values, adding latency and cost | For research and training data generation only |
| Token-level masking | Replace each PHI token with `[MASK]` (BERT-style) | Fine-grained control at the sub-word token level, preserving as much non-PHI context as possible | Masking multiple adjacent tokens (e.g., a full name or address) fragments sentence structure in ways that confuse the LLM, producing incoherent follow-up questions and elevated hallucination rates in ~30% of affected turns | No |

**On-premise vs cloud LLM deployment:**

| Architecture | PHI Exposure Risk | Latency | Cost | Scalability | Regulatory Comfort |
|---|---|---|---|---|---|
| Cloud LLM API (with de-identification) | Low but non-zero—residual exposure depends on de-identification recall; at 99.5% recall and 1M sessions/day, up to 5,000 sessions/day may contain quasi-identifiers in API logs | 200–500ms round-trip API latency adds ~200ms vs self-hosted; acceptable within the 800ms LLM budget but subject to provider network conditions | Pay-per-token with zero fixed hardware cost; at 1M sessions/day the LLM cost is approximately $700/day using a self-hosted-equivalent API, scaling linearly with volume | High—cloud providers offer elastic autoscaling that handles 3x peak surges without pre-provisioning | Moderate—requires a signed Business Associate Agreement (BAA) with the provider (Azure OpenAI offers HIPAA BAAs; raw OpenAI API does not) |
| On-premise LLM (no external calls) | Zero—PHI physically cannot leave the hospital data center; this is the strongest possible privacy guarantee and eliminates the de-identification recall gap entirely | 300–800ms for self-hosted 7B on A100 GPUs; p99 latency is more predictable than cloud APIs because there is no shared-provider queue or network variability | High fixed cost: approximately $120K hardware (4× A100 GPUs) plus $30K/year operations; break-even vs cloud API at this volume occurs at approximately 6 months | Limited by physical GPU inventory; requires pre-provisioning 2x redundancy for the ~35 sessions/sec peak, meaning idle capacity during off-peak hours | **Highest—preferred by academic medical centers, VA hospitals, and any deployment subject to state-level data residency laws** |
| Hybrid (on-prem for PHI-heavy, cloud for general) | Minimal—PHI-sensitive turns (containing direct identifiers) route to on-prem; general reasoning turns can use cloud with de-identification; routing logic itself is a potential failure point | Mixed latency: on-prem turns take 300–800ms, cloud turns take 200–500ms; session consistency requires that all turns for a single session use the same model to avoid acuity drift | Medium—on-prem hardware is sized for peak PHI-intensive traffic only, reducing hardware cost by 30–40% vs full on-prem | Medium—cloud path scales elastically; on-prem path is capacity-capped | Good—the hybrid routing logic must itself be validated and audited; regulators may question how "PHI-heavy" turns are classified |
| **De-identified cloud with on-prem fallback** | Near-zero—de-identification scrubs PHI before any cloud API call; on-prem fallback activates automatically when the cloud provider is unavailable or when de-identification confidence falls below threshold (e.g., NER uncertainty > 0.2) | 300–600ms in the normal cloud path; on-prem fallback adds ~100ms switching latency on the first turn of a failover; subsequent turns on fallback match on-prem baseline | Medium—cloud API for 90% of traffic at low variable cost; on-prem hardware sized for 100% fallback capacity but normally idle; total cost approximately 40% less than full on-prem | High with fallback—cloud path handles elastic scaling; on-prem fallback guarantees availability during cloud outages | **Recommended for most production deployments**—defense in depth: de-identification + BAA + structural failover |

**On-premise deployment specifics:**

For maximum-privacy deployments (academic medical centers, VA hospitals):
- Deploy 7B model on 4× A100 GPUs in hospital data center.
- No external network calls. All inference is local.
- Model updates delivered via air-gapped media or secure SFTP, validated by checksum.
- Cost: ~$120K hardware (one-time) + $30K/year operations vs ~$250K/year for cloud API at 1M sessions/day.
- Break-even: ~6 months. On-premise is cheaper at this scale.

**PHI re-identification edge cases:**

- The LLM generates text that includes a placeholder in an unexpected position: "Your symptoms, [NAME_1], suggest..." → re-identification must handle arbitrary placeholder positions.
- The LLM generates a new name not in the mapping (hallucination): "Dr. Johnson recommends..." where Dr. Johnson is generated, not from PHI. Re-identification service must NOT map this—only replace known placeholders.
- Patient mentions another person's name in their input: "My mother Sarah also had these symptoms." Sarah must be de-identified too (PHI by association).

### 2) Clinical Safety and Deterministic Escalation

The cardinal rule: **the LLM advises, the deterministic system decides.** No LLM output can override a deterministic safety rule. The LLM is a text-understanding and question-generation engine; the safety layer is a hard-coded clinical decision support system.

**ESI (Emergency Severity Index) classification:**

| ESI Level | Description | Example | System Action | Target Detection Sensitivity |
|---|---|---|---|---|
| ESI 1 | Immediate life threat | Cardiac arrest, respiratory failure, anaphylaxis | Instant escalation (< 30s). Bypass all LLM processing. | > 99.99% |
| ESI 2 | High risk / confused / severe pain | MI symptoms, stroke signs, severe hemorrhage, altered mental status | Escalation within 2 minutes. LLM may ask 1 clarifying question. | > 99.9% |
| ESI 3 | Two or more resources needed | Laceration needing sutures + tetanus, abdominal pain + labs | Full triage session. Clinician handoff summary generated. | > 99% |
| ESI 4 | One resource needed | Simple laceration, UTI symptoms, minor sprain | Full triage session. Self-care guidance + appointment recommendation. | > 95% |
| ESI 5 | No resources needed | Cold symptoms, minor rash, prescription refill | Self-care guidance. No clinician escalation unless patient requests. | > 90% |

**Red-flag detection engine:**

The engine operates on two layers:

**Layer 1: Keyword/pattern matching (< 5ms)**
- Hard-coded rules mapping symptom phrases to ESI levels.
- Examples:
  - "chest pain" + ("arm" OR "jaw" OR "shortness of breath") → ESI 2 (possible MI)
  - "worst headache of my life" OR "thunderclap headache" → ESI 2 (possible SAH)
  - "can't breathe" OR "struggling to breathe" → ESI 2 (respiratory emergency)
  - "not responsive" OR "unconscious" → ESI 1
  - "severe bleeding" + "won't stop" → ESI 2
- ~500 rules covering major emergency presentations.
- Limitation: brittle to phrasing variation ("my chest is tight and my left arm is tingling" might miss keyword rules).

**Layer 2: Medical NER + clinical inference (< 15ms)**
- Fine-tuned medical NER model extracts structured symptoms: {body_part: "chest", symptom: "pain", radiation: "left arm", severity: "moderate"}.
- Structured symptoms are matched against clinical decision rules (more robust than keyword matching).
- Handles negation: "I do NOT have chest pain" correctly negates the symptom.
- Handles temporal context: "chest pain that started 2 hours ago" is more urgent than "chest pain I had last month."

**Combined sensitivity: > 99.9% for ESI 1-2 detection on a held-out test set of 50K emergency presentations.**

**Confidence-gated clinician handoff:**

The system uses a tiered escalation model based on acuity classification confidence:

| Scenario | LLM Acuity | Red-Flag Engine | Safety Validator | Action |
|---|---|---|---|---|
| Clear emergency | N/A (bypassed) | ESI 1-2 detected | N/A | Immediate escalation. LLM not consulted. |
| Ambiguous emergency | ESI 2 (confidence: 0.7) | No red flag | Flags inconsistency | Escalation with note: "LLM flagged possible ESI 2 but deterministic rules did not confirm. Recommend clinician review." |
| LLM under-triages | ESI 4 (confidence: 0.9) | No red flag | Symptom list inconsistent with ESI 4 | Override to ESI 3. Escalation with full symptom log. |
| LLM over-triages | ESI 2 (confidence: 0.6) | No red flag | Symptoms consistent with ESI 3-4 | Accept clinician escalation (over-triage is safe). Flag for calibration review. |
| Clear non-emergency | ESI 4 (confidence: 0.95) | No red flag | Consistent | Self-care guidance. No escalation. |
| Low confidence | ESI 3 (confidence: 0.4) | No red flag | Can't determine | Default escalation to clinician. "Insufficient confidence for automated triage." |

**Clinician handoff summary format:**

```text
TRIAGE SUMMARY — Session ID: [SESSION_ID]
Generated: [TIMESTAMP] | Model: triage-7b-v2.3 | Prompt: v1.7

PATIENT: [NAME], [AGE], [SEX]
CHIEF COMPLAINT: [FREE TEXT FROM PATIENT]

SYMPTOM TIMELINE:
- [TIMESTAMP] [SYMPTOM_1]: [DESCRIPTION], Onset: [TIME], Severity: [1-10]
- [TIMESTAMP] [SYMPTOM_2]: [DESCRIPTION], Onset: [TIME], Severity: [1-10]

RED FLAGS DETECTED: [LIST OR "None"]
ACUITY CLASSIFICATION: ESI [LEVEL] (Confidence: [0.0-1.0])
ESCALATION REASON: [REASON]

DIFFERENTIAL CONSIDERATIONS (informational):
1. [DIAGNOSIS_1] — ICD-10: [CODE] — Likelihood: [HIGH/MEDIUM/LOW]
2. [DIAGNOSIS_2] — ICD-10: [CODE] — Likelihood: [HIGH/MEDIUM/LOW]

CONVERSATION LOG: [LINK TO FULL AUDIT TRAIL]
```

#### Clinical Safety Trade-off Table

| Approach | Sensitivity (ESI 1-2) | Specificity | Latency | Maintenance Burden | Best For |
|---|---|---|---|---|---|
| Rule-based only (no LLM) | 95%—rule engines excel on canonical presentations ("crushing chest pain radiating to the left arm") but miss 5% of ESI 1-2 cases expressed in non-standard phrasing ("my chest feels like it's being squeezed and my left side is tingling"), which at 1M sessions/day translates to 50,000 missed critical cases | 90%—over-triage rate is 10%; false positive escalations consume clinician time but never result in patient harm | < 20ms total, running entirely on CPU with ~500 compiled regex/pattern rules; can handle 35 sessions/sec on 4 standard CPU cores with no GPU dependency | Low—rules are static text files updated quarterly by clinicians; no model retraining, no GPU infrastructure, no ML pipeline maintenance | Legacy hospital intake systems, low-volume urgent care clinics, fallback mode when ML infrastructure is unavailable |
| LLM-only (no deterministic layer) | 98%—the LLM's natural language understanding catches phrasing variations that rule engines miss, but the 2% miss rate represents ~20,000 critical cases/day at 1M sessions; and unlike rule-based misses, LLM misses are non-deterministic, meaning the same input may be triaged differently on different runs | 80%—the LLM tends to over-triage (generating unnecessary escalations) due to clinical uncertainty in training data; 20% over-triage means 200,000 unnecessary escalations/day, overwhelming clinical staff | 800ms LLM inference dominates; no rule-engine parallelism possible since all decisions go through the LLM | Medium—model updates require clinical re-validation, prompt regression testing, and shadow deployment; but there is only one system to maintain | **NEVER for production**—a purely probabilistic safety-critical system has no deterministic failure bound; regulatory bodies (FDA for SaMD) will not approve a system without a deterministic safety layer |
| LLM + deterministic override | > 99.9%—the combination exceeds either component alone: the rule engine catches clear-cut cases in < 20ms (providing a hard lower bound), and the LLM catches the phrasing variations the rules miss; the deterministic override ensures any rule-engine ESI 1-2 detection immediately escalates regardless of LLM output | 85%—combined over-triage rate of 15% is clinically acceptable because the cost of one missed MI (mortality, liability) exceeds the cost of 10,000 unnecessary escalations (clinician time) by orders of magnitude | 800ms dominated by LLM inference; the rule engine runs in parallel so it adds zero latency to the critical path; clinical safety validator adds 100ms post-LLM for a total of ~900ms in the LLM stage | High—two separate systems (rule engine + LLM) require independent maintenance, separate validation pipelines, and coordinated deployment; quarterly rule reviews and monthly model evaluations run on separate schedules | **Production default**—the only architecture that satisfies both the > 99.9% sensitivity requirement and the deterministic safety guarantee required by healthcare regulators |
| Ensemble (LLM + rule engine + second LLM) | > 99.95%—the second LLM (typically a larger, slower model like a 70B) acts as a "second opinion" for cases where the primary LLM and rule engine disagree; on a held-out evaluation set of 50K emergency presentations, this ensemble reduces ESI 1-2 miss rate to 2.5 per 100K sessions | 88%—the second LLM is more conservative and tends to escalate ambiguous cases that the primary model might have passed; the 3% improvement in over-triage rate vs the LLM+rules baseline is a modest benefit given the latency cost | 1,400ms total—primary LLM (800ms) + second LLM consulted only on disagreements (~10% of cases, 2,400ms for 70B); weighted average adds ~160ms to the median case; p99 latency exceeds the 2s SLO for cases that hit the second LLM | Very high—three separate systems (rule engine + two LLMs) require independent validation; the ensemble logic itself (how to arbitrate disagreements) must be validated and versioned as a separate component | High-liability ER triage deployments, academic medical centers, or deployments seeking FDA 510(k) clearance where maximum documented sensitivity is required for the regulatory submission |

### 3) Audit Trail and Compliance

Healthcare AI systems are subject to HIPAA, FDA (if classified as SaMD—Software as Medical Device), and state-level medical practice regulations. The audit trail is not optional—it's a legal requirement.

**What must be logged (per turn):**

| Field | Content | Storage | Retention |
|---|---|---|---|
| session_id | Unique session identifier | Plaintext | 7 years |
| turn_id | Sequential turn number within session | Plaintext | 7 years |
| timestamp | ISO 8601 with timezone | Plaintext | 7 years |
| patient_input_raw | Original patient text (with PHI) | Encrypted (AES-256-GCM) | 7 years |
| patient_input_deidentified | Scrubbed text sent to LLM | Plaintext | 7 years |
| phi_mapping | Placeholder → PHI mapping for this turn | Encrypted, separate key | 7 years |
| llm_prompt_full | Complete prompt sent to LLM (de-identified) | Plaintext | 7 years |
| llm_response_raw | Raw LLM output | Plaintext | 7 years |
| llm_model_version | Exact model version hash | Plaintext | 7 years |
| llm_prompt_template_version | Prompt template version | Plaintext | 7 years |
| red_flag_result | Red-flag detector output (flags, confidence) | Plaintext | 7 years |
| safety_validator_result | Validator output (pass/fail, reasons) | Plaintext | 7 years |
| acuity_classification | ESI level + confidence | Plaintext | 7 years |
| escalation_decision | Escalated? Reason? Clinician notified? | Plaintext | 7 years |
| response_sent_to_patient | Final re-identified text shown to patient | Encrypted (contains PHI) | 7 years |
| latency_breakdown | Per-stage latency in ms | Plaintext | 7 years |

**Immutability requirements:**

- Audit logs must be written to WORM (Write Once Read Many) storage.
- AWS: S3 with Object Lock in Compliance mode (cannot be deleted, even by root account, until retention expires).
- On-premise: NetApp SnapLock or similar WORM-compliant storage.
- Tamper detection: each log entry includes a SHA-256 hash of the previous entry (blockchain-style chain). Any tampering breaks the hash chain.
- Access controls: audit logs readable only by compliance officers and authorized auditors. Not accessible to engineering teams without compliance approval.

**Model versioning for regulatory review:**

A regulator may ask: "Three years ago, a patient was misclassified as ESI 4. What model made that decision, and can you reproduce the output?"

Requirements:
1. **Model artifact storage:** every deployed model version is stored permanently (weights, tokenizer, config). Storage cost: ~20GB per model version × 12 versions/year × 7 years = ~1.7 TB. Trivial.
2. **Prompt template versioning:** every prompt template is stored in version control with deployment timestamps.
3. **Reproducibility:** given a session_id, retrieve the exact prompt, model version, and inference configuration used. Re-run inference to reproduce the output. Note: LLM outputs are non-deterministic due to sampling—store the random seed or use temperature=0 for triage (deterministic greedy decoding).
4. **Model deployment log:** timestamp, model version, deployment scope (canary %, full rollout), rollback history.

**Temperature=0 for clinical decisions:**

Unlike creative applications, triage requires deterministic outputs. Use temperature=0 (greedy decoding) for all acuity classifications and clinical recommendations. This ensures:
- Reproducibility: same input → same output.
- Auditability: regulators can verify outputs.
- Safety: no random sampling that might produce unsafe outliers.

Follow-up questions (less safety-critical) can use temperature=0.3 for slight variation to feel more natural.

**HIPAA audit readiness:**

HIPAA requires covered entities to:
1. Conduct risk assessments annually.
2. Maintain access logs for 6 years (the system logs for 7).
3. Respond to breach notifications within 60 days.
4. Provide patients with access to their health records (including AI triage records) within 30 days of request.

The audit trail system supports all of these:
- Risk assessment: the decision trace shows exactly how acuity was determined.
- Access logs: who accessed which audit records, when, from where.
- Breach investigation: if PHI is suspected to have leaked, the PHI mapping table and de-identification logs show exactly what was sent to the LLM.
- Patient data request: reconstruct the full session from audit logs, including all questions, answers, and decisions.

#### Audit Trail Architecture Trade-off Table

| Storage Architecture | Immutability | Query Performance | Cost | Compliance Level |
|---|---|---|---|---|
| Relational DB (PostgreSQL) | No native WORM—a DBA with superuser access can UPDATE or DELETE any row; row-level triggers and access controls reduce but do not eliminate the mutation risk; a determined insider or a compromised account can falsify records | High—SQL queries over indexed columns return session history in < 100ms even at 10M rows; PostgreSQL full-text search supports compliance team ad-hoc investigation without data exports | Low—commodity hardware or RDS at ~$0.10/GB/month; at 25.5 TB over 7 years the storage cost is approximately $2,500/month | Insufficient for HIPAA audit requirements—HIPAA requires that audit records cannot be altered or deleted; PostgreSQL's mutable architecture fails this requirement regardless of access controls; any compliance auditor will flag it |
| S3 with Object Lock (Compliance mode) | Hardware-enforced WORM—in Compliance mode, no IAM policy, no AWS root account, and no AWS support ticket can delete or overwrite an object before the retention period expires; this is the strongest immutability guarantee available in cloud storage | Low for querying—S3 does not support SQL; audit investigation requires downloading log files and parsing them locally or exporting to an analytics tool; at 10 GB/day this means investigators download potentially gigabytes of gzip-compressed JSON to answer a single question | Low—S3 Standard at $0.023/GB/month; transition logs older than 90 days to S3 Glacier at $0.004/GB/month; at 25.5 TB total, steady-state cost is approximately $100/month | **HIPAA-compliant**—the Compliance mode Object Lock satisfies HIPAA's requirement that audit records cannot be tampered with; AWS offers HIPAA BAAs covering S3 |
| S3 + Athena (query layer) | WORM storage (S3 Object Lock) with SQL query access layered on top via Athena—Athena reads Parquet-formatted logs directly from S3 without moving data; the underlying storage immutability is unaffected by query access | Medium—Athena queries on partitioned Parquet files return results in 5–30 seconds for typical session lookups; complex aggregations across 7 years of data may take 2–5 minutes but are infrequent | Medium—Athena charges $5/TB scanned; partition pruning (by session_date and session_id prefix) ensures most queries scan < 1 GB for point lookups, costing < $0.005 per investigation; S3 storage cost unchanged from the baseline | **Production default**—combines S3's WORM compliance with SQL query capability that compliance officers can use without engineering support; Athena's serverless model means no query infrastructure to maintain |
| Blockchain (Hyperledger Fabric) | Cryptographic immutability—each audit record is a transaction committed to an append-only distributed ledger; altering any record requires re-mining all subsequent blocks, which is computationally infeasible; this provides mathematical proof of non-tampering | Low—blockchain query performance is fundamentally limited by the ledger's sequential read model; point lookups require traversing the block chain or maintaining an off-chain index; Hyperledger Fabric achieves ~2,000 TPS but query latency is 500ms–5s | High—Hyperledger requires operating a distributed validator network (typically 3–7 nodes) each running on dedicated VMs; infrastructure cost is 5–10x the equivalent S3 solution; engineering complexity is disproportionate | Overkill for most healthcare deployments—blockchain immutability is not meaningfully stronger than S3 Object Lock in Compliance mode for audit purposes, yet the operational complexity is 10x higher; appropriate only for multi-institution audit sharing where no single party is trusted to operate storage |
| On-prem WORM + ELK stack | Hardware WORM (NetApp SnapLock or EMC Isilon with WORM) enforces immutability at the storage controller level; Elasticsearch provides full-text search and structured query capabilities over the WORM-stored logs without requiring data export | High—Elasticsearch full-text search returns results in < 500ms even over 25 TB of indexed log data; Kibana dashboards provide compliance officers with self-service investigation without engineering involvement | High—NetApp SnapLock licensing and hardware costs approximately $200K upfront plus $40K/year; Elasticsearch cluster requires 6–8 nodes at $30K/year infrastructure; total 7-year TCO approximately $500K vs ~$50K for S3+Athena | Maximum control for on-prem hospitals—appropriate when hospital policy prohibits cloud storage of PHI-adjacent audit data, when state data residency laws require on-prem storage, or when the hospital's existing NetApp infrastructure makes the marginal cost of adding SnapLock low |

**Recommended:** S3 with Object Lock (Compliance mode) for long-term storage + Athena for ad-hoc queries + DynamoDB for real-time session state. Daily export of DynamoDB session records to S3 after session completion.

### Production Bottlenecks and Mitigations

- **PHI de-identification false negatives**
  - Symptom: audit review discovers patient name in LLM API logs (for cloud deployment).
  - Mitigation: monthly adversarial testing with synthetic PHI in unusual formats. Red-team the NER model with edge cases: non-English names, names that are also common words ("May", "Grace"), dates written as prose ("the fifteenth of March"). Maintain a continuously updated test suite of 10K adversarial examples. Target: zero escapes on adversarial set.

- **LLM hallucinating diagnoses not in the approved list**
  - Symptom: LLM suggests "chronic fatigue syndrome" for a patient presenting with acute symptoms—plausible-sounding but clinically inappropriate for a triage context.
  - Mitigation: constrain LLM output to a closed vocabulary of approved ICD-10 codes for triage differentials (~500 codes). Implement structured output (JSON mode) with schema validation: `{"differentials": [{"code": "I21.9", "name": "Acute MI, unspecified", "likelihood": "HIGH"}]}`. Reject any output that doesn't conform to schema.

- **Red-flag detector rule maintenance**
  - Symptom: new clinical guidelines identify a symptom pattern as urgent that the rule engine doesn't cover.
  - Mitigation: quarterly rule review with emergency medicine physicians. Automated pipeline: monitor LLM escalation recommendations that the rule engine missed—these are candidate new rules. Clinical review board approves before deployment.

- **Audit log storage growth**
  - Symptom: 10 GB/day × 7 years = 25.5 TB; query performance degrades.
  - Mitigation: partition by month. Compress logs older than 90 days (gzip reduces 10x). Athena queries on partitioned Parquet files. Hot tier (last 90 days) in DynamoDB for fast access; cold tier in S3 Glacier for cost reduction.

- **Model update deployment risk**
  - Symptom: new model version subtly changes acuity classification behavior, causing a spike in ESI 3→4 downgrades that goes unnoticed for 2 weeks.
  - Mitigation: mandatory shadow deployment for 7 days. New model runs in parallel with production model on 100% of traffic. Both outputs logged; only production model's output is served. Statistical comparison of acuity distributions, escalation rates, and red-flag agreement. Promotion requires: (1) no statistically significant change in ESI 1-2 sensitivity, (2) acuity distribution within 2% of production model, (3) clinical review board sign-off.

### Advanced Techniques

- **Structured clinical reasoning chains:** Instead of freeform LLM output, force the model to generate intermediate clinical reasoning steps before the final classification: "Patient reports chest pain radiating to left arm, onset 2 hours ago, with diaphoresis. This pattern is consistent with acute coronary syndrome. ESI classification: 2." The reasoning chain serves as both an audit artifact and a quality signal—incoherent reasoning (e.g., "Patient has a cold, ESI classification: 1") triggers automatic regeneration or escalation to a clinician for review. In production evaluations, enforcing a structured reasoning chain reduces ESI misclassification rate by ~12% compared to direct classification prompts, because the model is forced to articulate the symptom evidence before committing to a level.

> **Why structured reasoning chains improve safety:** Chain-of-thought prompting forces the model to surface latent symptom associations that direct classification can miss.

- **Multi-turn symptom extraction with ontology grounding:** Map free-text symptoms to SNOMED CT terms at each turn using a dedicated medical NLP pipeline (e.g., QuickUMLS or MetaMap). Maintain a structured symptom graph (nodes = symptoms, edges = temporal and severity relationships) that grows over the session. Feed the structured symptom graph (serialized as JSON) alongside the raw conversation history to the LLM. This dual-input approach reduces hallucination by anchoring the model's reasoning in standardized clinical terminology—a model that sees `{"symptom": "chest pain", "snomed_ct": "29857009", "severity": 7, "onset": "2h ago"}` is less likely to invent a different symptom than one seeing only the raw text "my chest hurts a bit."

> **Why SNOMED CT grounding reduces hallucination:** LLMs hallucinate most frequently when forced to recall specific facts from parametric memory.

- **Active learning for rare conditions:** Flag sessions where the LLM's confidence is low (< 0.5 for the top differential) AND the deterministic system has no matching rules—these are cases at the intersection of model uncertainty and rule-engine blindness, representing the highest-risk undetected edge cases. Queue these sessions for expert emergency medicine physician review within 24 hours. Use clinician annotations (corrected acuity, correct differential, reasoning) to expand both the rule engine (new rule candidates) and the LLM fine-tuning dataset. Target: 100 expert-reviewed cases per week, yielding approximately 5,200 annotated edge cases per year—enough to materially expand the tail coverage of both the rule engine and the fine-tuned model.

> **Why active learning targets low-confidence AND rule-engine misses simultaneously:** Routing all low-confidence cases to clinicians would overwhelm the review queue (at 1M sessions/day, even 5% low-confidence cases is 50,000 sessions/day).

- **Federated fine-tuning across hospital systems:** Multiple hospitals contribute to model improvement without sharing PHI. Each hospital fine-tunes a local copy of the base model on their patient population data, then shares only the gradient updates (parameter differentials) with the central aggregation server. The central server applies federated averaging (FedAvg) to merge gradient contributions from all participating hospitals, producing an improved global model that incorporates the diverse demographics and disease presentations of all participating institutions. The PHI-carrying training data never leaves each hospital's local infrastructure. Differential privacy (DP-SGD with ε=1.0) can be applied to the gradient updates to provide a mathematical bound on the information leakage about individual patients from the gradients themselves.

---

## Step 5: Interviewer Curveballs

### Interviewer Follow-ups & Frequently Asked Questions (FAQ)

Q: A patient types "I've been having chest pains for the last week but they seem to be getting better." Your system escalates this as ESI 2. The patient is frustrated by the over-triage. How do you handle this?

**The Ideal Answer:** Over-triage is by design. "Chest pain" triggers a red flag regardless of temporal modifiers or improving trajectory, because patients are unreliable self-assessors of cardiac risk—a patient who says "it's getting better" could still be having unstable angina. The system's response should acknowledge the patient's perspective while explaining the escalation: "I understand your symptoms seem to be improving. Because chest pain can indicate serious conditions, I want to have a clinician review your case to be safe. This is a precaution, not a diagnosis." Post-escalation, the clinician can downgrade if appropriate. The false positive rate for chest pain escalation is ~40%—clinically acceptable because the cost of missing one MI far exceeds the cost of 10 unnecessary escalations.

**Deep Dive & Trade-offs:**
- Over-triage wastes clinician time. At 1M sessions/day, even 5% over-triage = 50K unnecessary escalations/day. This is managed by the ESI 3+ tier handling most of the load—most chest pain escalations are ESI 2 routing to nurses who can quickly validate and downgrade, not physicians. The system routes these to a triage nurse queue, not the emergency physician queue directly, reducing the clinical cost of each false positive.
- Under-triage kills patients. The asymmetry is absolute. A missed MI has a mortality rate of 8–12% per hour without intervention; a false-positive escalation wastes ~10 minutes of clinician time. The expected value calculation is not close: accepting 1,000 false positives per day to avoid one missed MI per day is not a trade-off—it is the correct operating point.
- User experience: frustrated patients may abandon the system entirely and seek no care, which is worse than over-triage. Mitigation: empathetic escalation messaging ("I want to make sure you're safe—let me connect you with a clinician who can evaluate this more thoroughly") reduces abandonment by ~25% compared to clinical/robotic messaging ("Symptom pattern detected: chest pain. Escalating to ESI 2.").
- Some systems allow "soft escalation" (ESI 2 with a 30-minute callback instead of immediate paging) for improving-symptom cases. This is a clinical policy decision, not a system architecture decision—the architecture must support both modes, with the soft/hard distinction configurable per deployment site based on their clinical protocols.

**The Interviewer's Rubric:** The interviewer is checking (1) understanding of the fundamental asymmetry between false positives and false negatives in medical triage, (2) ability to quantify the trade-off with concrete numbers rather than vague statements, (3) awareness that user experience and clinical safety must both be managed—not traded against each other—and (4) understanding of where clinical policy decisions end and engineering decisions begin.

---

Q: Your PHI de-identification pipeline has a 99.5% recall rate. That means at 1M sessions/day, 5,000 sessions may have PHI leakage. Is this acceptable?

**The Ideal Answer:** No, 5,000 PHI leaks/day is not acceptable, and the 99.5% figure requires context. The 0.5% miss rate is across all PHI types—most misses are quasi-identifiers (unusual location formats, ambiguous age references), not direct identifiers (names, SSNs). For direct identifiers (names, SSNs, MRNs), the recall target is > 99.99% (< 100 misses/day). Mitigation layers: (1) The cloud LLM provider has a BAA that covers incidental PHI—legally, this limits liability. (2) LLM API request logs are disabled (zero-retention agreement with provider). (3) Monthly adversarial testing identifies new miss patterns. (4) For the highest-risk deployments, use on-premise LLM where PHI leakage to external APIs is structurally impossible. The goal is defense in depth: even if de-identification misses something, no downstream system stores or exposes it.

**Deep Dive & Trade-offs:**
- 99.5% recall sounds high but is insufficient for direct identifiers. Stratify by PHI type.
- Zero-retention API agreements with LLM providers (e.g., Azure OpenAI with data processing agreements) mean that even leaked PHI is not persisted.
- On-premise deployment eliminates the problem entirely but increases operational cost.
- The strongest defense is architectural: if PHI never leaves the trust boundary, de-identification recall is irrelevant. This is why on-premise is preferred for sensitive deployments.

**The Interviewer's Rubric:** The interviewer is checking (1) the ability to decompose a single aggregate accuracy number into per-risk-class rates and identify where it is insufficient, (2) understanding that PHI types carry different risk levels and require different detection thresholds, (3) knowledge of defense-in-depth (de-identification + BAA + zero-retention + on-prem fallback) rather than reliance on a single control, and (4) willingness to acknowledge that 99.5% is not good enough for direct identifiers and to propose a concrete path to higher recall.

---

Q: A new variant of a disease emerges (like COVID-19 in early 2020). Your system has never seen these symptoms. How do you handle novel disease presentations?

**The Ideal Answer:** The system will under-triage novel diseases because neither the rule engine nor the LLM have been trained on them. Mitigations: (1) The LLM's general medical knowledge provides some zero-shot capability—"severe respiratory distress with fever" will trigger ESI 2 escalation regardless of the specific disease. (2) The red-flag engine is symptom-based, not disease-based—it detects dangerous symptom combinations, not specific diagnoses. This provides partial coverage. (3) Emergency rule updates: the rule engine supports hot-reload of new rules without deployment. A clinician can add a new rule ("cough + fever + travel to affected region → ESI 2") and deploy it within hours. (4) The LLM's prompt can be updated with a clinical advisory: "Note: novel respiratory illness reported in [region]. Patients with cough + fever + travel history should be classified ESI 2 minimum." Prompt updates deploy in minutes. (5) Long-term: fine-tune on new clinical data as it becomes available. Fast-adaptation via LoRA: < 24 hours from data to deployed adapter.

**Deep Dive & Trade-offs:**
- Novel diseases expose the fundamental limitation of AI triage: models are retrospective. They know what they were trained on.
- Symptom-based (not disease-based) rule engines are more robust to novel presentations.
- The prompt update path is the fastest response mechanism—deploy new clinical advisories in the system prompt within minutes.
- Regulatory risk: if the system fails to triage a novel disease, is the vendor liable? This depends on FDA classification and the system's labeling (CDS exemption requires "clinician in the loop").

**The Interviewer's Rubric:** The interviewer is checking (1) clear acknowledgment that AI systems are retrospective and will fail on genuinely novel presentations—avoiding overconfidence is important, (2) understanding that symptom-based detection is more robust to novel diseases than disease-based detection, (3) knowledge of the different adaptation pathways sorted by speed (prompt update: minutes, rule update: hours, LoRA fine-tune: < 24 hours, full fine-tune: days) and when each is appropriate, and (4) awareness of the regulatory and liability implications of AI failure on novel inputs and how system design (CDS framing, clinician-in-the-loop) mitigates them.

---

Q: The hospital IT team wants to use GPT-4 via API for the triage system instead of your self-hosted 7B model. What are the trade-offs?

**The Ideal Answer:** GPT-4 offers higher reasoning quality (better symptom interpretation, more nuanced follow-up questions) but introduces critical compliance risks. Trade-off analysis:

| Dimension | Self-hosted 7B | GPT-4 API |
|---|---|---|
| Clinical reasoning quality | Good (after medical fine-tuning) | Excellent (broader knowledge) |
| PHI exposure risk | Zero (no external calls) | Non-zero (depends on de-identification + BAA) |
| Latency | 300-800ms (local inference) | 500-3,000ms (API latency + queue) |
| Cost per session | ~$0.0007 | ~$0.15 (at 6 turns × 550 tokens × $0.03/1K) |
| Availability dependency | Self-controlled | Depends on OpenAI uptime + rate limits |
| Auditability | Full control over model weights, versioning | Black box—model may change without notice |
| Reproducibility | temperature=0, deterministic | temperature=0, but model updates may change behavior |
| Regulatory | Full control for FDA submission | Third-party dependency complicates regulatory narrative |

Recommendation: use GPT-4 for offline evaluation, training data generation (synthetic clinical scenarios), and as a "second opinion" model in shadow mode. Use self-hosted 7B for production serving. If GPT-4 is used in production, it MUST be behind the de-identification pipeline with a zero-retention BAA, and the system must handle API outages gracefully (fall back to self-hosted 7B).

**Deep Dive & Trade-offs:**
- Cost is 200x higher with GPT-4. At 1M sessions/day, that's $150K/day vs $700/day.
- Model versioning: OpenAI may update GPT-4 without notice, changing clinical behavior. This is a regulatory nightmare for SaMD.
- BAA: Azure OpenAI offers HIPAA-compliant configurations with BAA. Raw OpenAI API does not.
- The strongest argument for self-hosted: you control the model, the versioning, and the infrastructure. In healthcare, control equals compliance.

**The Interviewer's Rubric:** The interviewer is checking (1) the ability to translate technical trade-offs (latency, cost, availability) into healthcare-specific risk dimensions (PHI exposure, regulatory compliance, auditability), (2) quantitative cost analysis—candidates who know that GPT-4 at 1M sessions/day costs ~$150K/day vs $700/day self-hosted demonstrate depth, (3) knowledge that regulatory compliance (model versioning, BAA requirements, auditability) is a first-class constraint, not an afterthought, and (4) the pragmatic recommendation to use GPT-4 offline for evaluation and training data while keeping self-hosted in the production critical path.

---

Q: A patient provides a symptom in a language you don't support (e.g., Tagalog). Your system is English-only. What happens?

**The Ideal Answer:** Unsafe failure mode: the system might misinterpret Tagalog text as English nonsense and triage incorrectly. Detection: language identification model (fasttext-lid, < 1ms) runs on every patient input. If detected language is not supported, the system should: (1) immediately respond in English: "I detected that your message may be in a language I don't currently support. For your safety, I'm connecting you with a human clinician who can assist in your language." (2) Escalate to clinician with note: "Patient input in unsupported language (detected: Tagalog). Unable to perform automated triage." (3) Never attempt to triage in an unsupported language—the risk of misinterpretation is too high. Long-term: add multilingual support via translation pipeline (NLLB-200) for high-demand languages. Clinical validation required per-language before deployment.

**Deep Dive & Trade-offs:**
- Machine translation introduces clinical risk: medical terminology may be mistranslated ("I have pressure in my chest" → "I have stress in my chest" in some MT systems—changing the clinical meaning).
- Per-language clinical validation is expensive: require physician review of 1,000 translated triage sessions per language before go-live.
- Language identification is cheap and fast—there's no reason not to run it on every input.
- For multilingual deployments: maintain language-specific red-flag rules (symptom keywords in each supported language).

**The Interviewer's Rubric:** The interviewer is checking (1) proactive identification of the unsafe failure mode (attempting triage in an unsupported language) before being prompted, (2) knowledge of a concrete detection mechanism (fasttext-lid language identification, < 1ms) rather than vague language about "detecting language," (3) understanding that the safe failure for language detection is conservative escalation—not a degraded attempt at triage—and (4) awareness that adding multilingual support is not just a translation problem but a clinical validation problem requiring per-language physician review before deployment.

---

Q: Your system has been deployed for 6 months. A malpractice lawsuit alleges that your system misclassified a patient as ESI 4 who later had a heart attack. How does your audit trail help defend this case?

**The Ideal Answer:** The audit trail provides complete reconstruction: (1) Pull the exact session by session_id. (2) Retrieve every turn: patient inputs, LLM prompts, LLM responses, red-flag detector outputs, safety validator outputs, final acuity classification with confidence score. (3) Retrieve the exact model version (weights hash) and prompt template version used during that session. (4) Reproduce the inference: load the archived model version, replay the exact prompts, verify the output matches (temperature=0 ensures determinism). (5) Show the decision trace: "Red-flag detector did not trigger because the patient's description did not match any ESI 1-2 rule patterns. The LLM classified ESI 4 with 0.82 confidence. The safety validator found no inconsistency." (6) Demonstrate that the system performed within its validated specifications—sensitivity for cardiac presentations was validated at 99.9% on a test set of 50K cases. (7) Show the disclaimer displayed to the patient: "This is a preliminary assessment. Please seek emergency care if symptoms worsen."

**Deep Dive & Trade-offs:**
- The audit trail is the primary legal defense. Without it, the vendor has no way to prove the system behaved correctly.
- Reproducibility (temperature=0) is critical—if you can't reproduce the output, the defense weakens significantly.
- Model versioning means you can prove exactly which model was running. If the model has since been updated (improving cardiac detection), this shows continuous improvement—not negligence.
- The disclaimer and "clinician in the loop" design are legal shields: the system never claims to diagnose, only to assist.
- Expert witness can testify that the system's sensitivity (99.9%) exceeds typical human triage nurse performance (~95% for cardiac presentations).

**The Interviewer's Rubric:** The interviewer is checking (1) the ability to walk through an audit trail reconstruction step by step—session ID lookup, model version retrieval, prompt replay, output reproduction—not just assert that the audit trail "helps," (2) understanding that temperature=0 is an engineering decision with direct legal consequences (reproducibility), (3) awareness that the disclaimer and "clinician in the loop" design are legal shields that must be designed in from the start, not added as an afterthought, and (4) knowing that expert witness testimony comparing AI sensitivity (99.9%) to human triage nurse baseline (~95% for cardiac presentations) is a concrete defense argument, not a hand-wave.

---

Q: You need to support pediatric patients. A parent is entering symptoms on behalf of their 3-year-old. What changes?

**The Ideal Answer:** Pediatric triage has fundamentally different clinical rules. Changes required: (1) **Separate red-flag rule set:** pediatric vital sign thresholds differ dramatically (a heart rate of 150 bpm is normal for a 1-year-old but alarming for an adult). Fever thresholds differ (38°C in a neonate < 28 days is an emergency; in an adult, it's not). (2) **Age-adjusted ESI classification:** the LLM must receive the patient's age and apply pediatric-specific reasoning. The prompt includes: "This patient is 3 years old. Apply pediatric clinical guidelines." (3) **Proxy communication handling:** the system is talking to a parent, not the patient. Questions must be phrased for a caregiver: "Is your child having difficulty breathing?" not "Are you having difficulty breathing?" (4) **Lower escalation threshold:** for pediatric patients under 2 years, any uncertain classification defaults to clinician escalation. (5) **Separate model fine-tuning:** pediatric presentations are clinically distinct. The model should be fine-tuned on pediatric triage data (PedsCases, pediatric EM datasets). (6) **PHI handling:** pediatric patients have additional privacy protections (COPPA in addition to HIPAA). Parental consent is required for AI triage.

**Deep Dive & Trade-offs:**
- Pediatric triage is harder: children can't describe symptoms, vital sign norms vary by age, and disease progression is faster. Over-triage is even more appropriate.
- Separate model or LoRA adapter for pediatric vs adult? LoRA adapter is more cost-efficient (one base model, two adapters). But clinical validation must be separate—FDA would require independent validation for each patient population.
- Age detection from input: if the parent doesn't mention age, the system MUST ask before proceeding. Age determines which rule set applies.
- COPPA compliance: additional consent flows for data collection on minors.

**The Interviewer's Rubric:** The interviewer is checking (1) the ability to identify concrete clinical differences between pediatric and adult triage—vital sign thresholds, fever standards, proxy communication—not just generic statements about pediatric patients being "different," (2) knowledge that LoRA adapters can support population-specific models without doubling the base model footprint, (3) awareness that FDA validation must be performed separately for each patient population subgroup (pediatric vs adult is a well-established boundary), and (4) recognition that COPPA adds a second compliance framework on top of HIPAA for patients under 13, requiring additional consent and data handling controls.

---

Q: Your system currently uses a 7B model. A new 70B medical model achieves 15% better diagnostic accuracy on benchmarks. Should you upgrade?

**The Ideal Answer:** Not automatically. The decision framework: (1) **Latency impact:** 70B at INT4 requires ~40GB VRAM and ~2,400ms for 150 output tokens—exceeding the 800ms LLM budget. Either accept higher latency (violates SLO) or use tensor parallelism across 2 GPUs (doubles GPU cost). (2) **Cost impact:** 10x more compute per inference. Cost/session jumps from $0.0007 to ~$0.007. Still under budget, but 10x increase. (3) **Benchmark vs production gap:** 15% better on academic benchmarks (MedQA, USMLE) doesn't guarantee 15% better triage accuracy. Triage is a narrow task; a fine-tuned 7B may match or exceed a general 70B on triage-specific evaluation. (4) **Regulatory impact:** new model requires re-validation. Shadow deployment for 7+ days, clinical review, updated documentation. (5) **Recommendation:** run a controlled evaluation: deploy 70B in shadow mode on 100% of traffic for 14 days. Compare acuity classification agreement with production 7B. If the 70B catches ESI 1-2 cases that the 7B misses (even 1 case), the upgrade is justified regardless of cost. If acuity distributions are identical, the upgrade is not worth the latency and cost penalty.

**Deep Dive & Trade-offs:**
- In healthcare, the question is not "is the new model better?" but "does it catch cases the old model misses, and does it introduce new failure modes?"
- Shadow deployment is non-negotiable. No healthcare AI model goes to production without parallel evaluation.
- Benchmark scores are necessary but not sufficient evidence. Production evaluation on your specific population is the gold standard.
- A practical middle ground: use the 70B model as an "escalation oracle"—when the 7B has low confidence (< 0.5), route to the 70B for a second opinion. This uses the 70B for only ~10% of traffic, keeping costs manageable.

**The Interviewer's Rubric:** The interviewer is checking (1) the ability to translate a benchmark improvement ("15% better on MedQA") into production-relevant metrics ("does it catch ESI 1-2 cases the 7B misses?"), (2) knowledge that shadow deployment is non-negotiable and the ability to specify what metrics to monitor during shadow (acuity distribution, escalation rate, ESI 1-2 agreement with rule engine), (3) quantitative cost and latency analysis demonstrating that a 70B model violates the 800ms LLM budget unless additional GPU infrastructure is added, and (4) the creative solution of using the 70B as an escalation oracle for low-confidence cases (~10% of traffic) to get most of the benefit at a fraction of the cost.

---

