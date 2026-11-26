---
title: "Part 6 Cards — Regulated and Safety-Critical (Ch 13, 20, 30)"
tags: [cards, safety, compliance]
---

# Part 6 Cards — Regulated and Safety-Critical

Every card here is **P4 (layered guardrails) + P8 (verify)** with one rule: **the LLM advises, a deterministic system decides.** Name the regulation, name the audit trail, name the escalation path.

---

### Ch 13 — Design an AI Tutor for Education
**One line:** A tutor that guides students to answers instead of giving them away, safely for minors.
**Shape:** Student input (text/photo) → Age-tier safety → Learner model (what they know) → **Socratic engine** (hint ladder) → Answer-leak check → Response
**Patterns:** P4, P8

**3 ideas**
1. **Socratic prompting:** hint ladder (nudge → hint → worked step), never the final answer until earned. A checker catches answer leaks.
2. **Age-appropriate safety:** stricter policies for minors, COPPA/FERPA-style data limits, escalation to teacher/parent on risk signals.
3. **Multimodal input:** photo of homework → OCR/vision → parse the problem → verify the math with a solver, not the LLM.

**2 trade-offs**
- Helpfulness vs not giving answers away (students get frustrated).
- Rich learner profile (personalization) vs data minimization for minors.

**Numbers:** Math answers verified by a symbolic solver (P8), not trusted from the LLM.
**Soundbite:** *"The tutor knows the answer from a solver, and the LLM's job is to not say it yet."*

> [!question]- How do you stop the tutor giving away the answer?
> Solver computes the answer privately; output checker blocks responses containing it until the hint ladder is exhausted or the student solves it.

> [!question]- What changes when users are minors?
> Stricter content filters, minimal data retention, parental/school consent, no open-ended companionship, escalation for self-harm signals.

**Go deep:** [[Chapter 13 - Design an AI Tutor for Education]] → "Socratic Prompting Engine" and "Age-Appropriate Safety System".

---

### Ch 20 — Design a Healthcare Triage and Diagnostic Assistant
**One line:** Help patients/clinicians triage symptoms safely, with deterministic escalation for emergencies.
**Shape:** Input → **PHI protection** → **Red-flag rules engine** (deterministic) → LLM structured intake → Triage level from **protocol, not the LLM** → Clinician review → Audit log
**Patterns:** P4, P8, P10

**3 ideas**
1. **Deterministic escalation:** red-flag symptoms (chest pain, stroke signs, suicidal ideation) trigger rules **before and regardless of** the LLM.
2. **PHI pipeline:** detect/redact, BAA-covered vendors only, encryption, minimum necessary access.
3. **Audit trail:** every input, model version, prompt version, retrieved source and output is logged immutably for review.

**2 trade-offs**
- Sensitivity (catch every emergency, more false alarms) vs specificity. In triage, choose sensitivity.
- LLM flexibility in conversation vs protocol-bound decisions. LLM gathers info; protocol decides urgency.

**Numbers:** Emergency recall target ≈ 100% (rules, not ML, own it).
**Soundbite:** *"The LLM collects symptoms into a structured form. A validated clinical protocol, not the model, assigns urgency."*

> [!question]- Why must red-flag detection be rule-based?
> Missing an emergency is catastrophic and must be auditable and deterministic. LLMs are probabilistic and can be talked out of things.

> [!question]- What goes in the audit record?
> Timestamp, user/clinician, inputs (protected), model + prompt versions, retrieved guidelines, outputs, rule hits, final decision, reviewer.

> [!question]- What does HIPAA imply architecturally?
> BAAs with every vendor touching PHI, encryption at rest/in transit, access controls and logs, minimum necessary data, no PHI in general logs.

**Go deep:** [[Chapter 20 - Design a Healthcare Triage and Diagnostic Assistant]] → "Clinical Safety and Deterministic Escalation" and "Audit Trail and Compliance".

---

### Ch 30 — Privacy, Compliance, and Data Governance for LLM Systems
**One line:** Handle personal data correctly across prompts, logs, indexes, fine-tunes and vendors.
**Shape:** Data map → PII detect/redact at ingress → Residency-aware routing → ACL/consent-aware retrieval → Scrubbed logs → Deletion propagation (index, cache, logs, training sets)
**Patterns:** P2, P4, P10

**3 ideas**
1. **PII de-identification:** NER + regex + context; pseudonymize reversibly when the answer needs the real value later.
2. **Residency + vendors:** region-pinned endpoints, zero-data-retention agreements, DPAs; route EU data to EU regions.
3. **Right to deletion:** delete from source, vector index, caches, logs and eval sets. Fine-tuned weights are the hard part: retrain/unlearn or never train on personal data.

**2 trade-offs**
- Redact aggressively (safe) vs answer quality (lost context).
- Train on user data (better model) vs deletion and consent obligations.

**Numbers:** Deletion SLA from regulation (e.g. GDPR "without undue delay", ~30 days).
**Soundbite:** *"Deletion is easy in a database and hard in weights, so personal data stays in retrieval, where I can delete it, not in training."*

> [!question]- Where does personal data hide in an LLM system?
> Prompts/logs, vector index, semantic cache, eval/golden sets, fine-tuning data and weights, vendor-side retention, traces.

> [!question]- How do you honor deletion in a RAG system?
> Delete source → delete chunks by doc ID in the index → invalidate caches → purge logs/traces → verify. Track lineage so you know every copy.

> [!question]- What is data residency routing?
> Requests and stored data are kept in the user's legal region by routing to region-pinned model endpoints and storage.

**Go deep:** [[Chapter 30 - Privacy, Compliance, and Data Governance for LLM Systems]] → "Right to Deletion and Model Unlearning" and "Data Residency and Vendor Agreements".
