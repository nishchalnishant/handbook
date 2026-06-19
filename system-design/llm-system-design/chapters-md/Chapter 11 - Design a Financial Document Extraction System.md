---
title: "Chapter 11: Design a Financial Document Extraction System"
tags: [llm, system-design, document-extraction, ocr, structured-output, hallucination, finance, case-study]
chapter: 11
part: case-studies
---

# Chapter 11: Design a Financial Document Extraction System

## Context

> [!info] Quick Reference
> - **Pattern:** OCR-to-LLM document extraction pipeline
> - **Scale:** 2M documents/day, < 5s latency, 99.5%+ per-field accuracy
> - **Key Techniques:** Layout detection (DETR), table structure recognition, constrained decoding, 5-layer hallucination prevention
> - **Primary Concerns:** Digit transposition errors, cross-document bleed, arithmetic consistency, compliance audit trail
> - **Cross-references:** [[chapter-07|Chapter 7]] (document parsing), [[chapter-17|Chapter 17]] (legal contracts), [[chapter-05|Chapter 5]] (guardrails)

**Problem statement:** Design a production system that ingests millions of financial documents (invoices, bank statements, contracts, tax forms), extracts structured fields with >99.5% per-field accuracy, and outputs validated JSON—where a single [[glossary#Hallucination (LLM)|hallucinated]] number can trigger regulatory violations or erroneous payments.

### Real-World Examples

- A payments company processes 3M vendor invoices/day. Their regex-based extraction fails on 40% of non-standard layouts. An OCR-to-LLM pipeline with layout-aware table extraction and [[glossary#Structured Output / Constrained Decoding|constrained JSON decoding]] achieves 99.7% field accuracy, reducing manual review from 45% to 3% of documents.
- A bank's loan processing system extracts income figures from scanned tax returns. The LLM hallucinates "$85,000" as "$850,000" on a blurred document, approving a loan that defaults. Adding cross-field verification (income × tax rate ≈ reported tax) and confidence-gated human review catches the error class entirely.

---

## Step 1: Understand the Problem and Establish Design Scope

### Simulated Dialogue

**Interviewer:** Design a system to extract structured data from financial documents at scale.  
**Candidate:** Financial extraction is an accuracy-critical domain. I need to understand document types, field schemas, volume, accuracy targets, and what happens when the system is wrong before proposing anything.

**Candidate:** What document types and volumes?  
**Interviewer:** Invoices, bank statements, loan contracts, tax forms. 2M documents/day. Mix of digital-native PDFs (60%) and scanned images (40%).

**Candidate:** What fields need extraction, and what accuracy is required?  
**Interviewer:** Average 15 fields per document—amounts, dates, account numbers, party names, line items. Target 99.5%+ per-field accuracy. Errors in monetary fields are especially costly.

**Candidate:** What's the latency budget?  
**Interviewer:** Under 5 seconds per document for the full pipeline. Some documents go through batch processing overnight, but real-time extraction for incoming invoices must meet the SLO.

**Candidate:** What happens when the system is wrong?  
**Interviewer:** Incorrect amounts can trigger erroneous payments or regulatory flags. We need confidence scoring and human-in-the-loop routing for low-confidence extractions.

### Functional Requirements

- Ingest PDFs (digital-native and scanned), images (TIFF, JPEG, PNG), and structured electronic formats (EDI, XML).
- Extract document-type-specific fields into a predefined JSON schema per document class.
- Detect and extract tables (line items, transaction histories) preserving row-column relationships.
- Assign per-field confidence scores; route low-confidence documents to human review.
- Support 50+ document templates with [[glossary#Zero-Shot / Few-Shot Prompting|zero-shot]] generalization to unseen layouts.

### Non-Functional Requirements

- **[[glossary#Accuracy|Accuracy]]:** 99.5%+ per-field extraction accuracy across all document types. 99.9%+ for monetary fields after validation.
- **Latency:** End-to-end <5s per document (OCR + classification + extraction + validation).
- **Throughput:** Sustain 2M documents/day (~23 docs/sec average, 100 docs/sec peak).
- **Auditability:** Full provenance trail—every extracted value links to bounding box coordinates in the source document.
- **Availability:** 99.9% uptime with queue-based decoupling (documents never lost).

### Back-of-the-Envelope Estimation

#### Traffic Profile

- Documents/day: 2M
- Average docs/sec: `2M / 86,400 ≈ 23`
- Peak docs/sec (4x): `~92`
- Fields/day: `2M × 15 = 30M field extractions`
- Digital-native PDFs: 1.2M/day (text-layer extraction, no OCR needed)
- Scanned documents: 800K/day (require full OCR pipeline)

#### Compute Budget per Document (5s SLO)

| Stage | Budget | Notes |
|---|---|---|
| Document ingestion + classification | 200ms | Page count detection, format conversion, doc-type classifier |
| OCR (scanned only, 40% of docs) | 1,500ms | Layout-aware OCR (Tesseract/PaddleOCR), multi-page |
| Text extraction (digital PDFs) | 100ms | PDF text layer + coordinate extraction |
| Layout detection + table parsing | 800ms | Object detection model for tables, headers, footers |
| LLM extraction (field mapping) | 1,800ms | ~2K input tokens, ~500 output tokens, 7B model |
| JSON validation + cross-field checks | 200ms | Schema validation, arithmetic checks, format verification |
| Confidence scoring + routing | 100ms | Per-field confidence aggregation, threshold check |
| **Total (scanned)** | **~4,700ms** | Within 5s SLO |
| **Total (digital)** | **~3,200ms** | Comfortable margin |

#### GPU Fleet Sizing

- LLM extraction: 7B [[glossary#Quantization|quantized]] model (INT4), ~120 tokens/sec/GPU
- Output tokens/doc: ~500
- Time per doc per GPU: `500 / 120 ≈ 4.2s`
- With [[glossary#Continuous Batching|continuous batching]] (6x efficiency): `~0.7s effective per doc`
- Peak demand: 92 docs/sec → `92 × 0.7 / 1 ≈ 65 GPU-equivalents`
- Layout detection model: ~10 GPUs (lightweight object detection)
- OCR: CPU-bound, ~200 CPU cores for peak scanned volume
- Total GPU fleet: **~80 GPUs** (steady-state ~35 with autoscaling)

#### Storage

- Average document size: 2MB (PDF/image)
- Daily ingestion: `2M × 2MB = 4TB/day`
- 90-day retention (regulatory): ~360TB
- Extracted JSON: ~2KB/doc → 4GB/day → negligible
- Audit trail (bounding boxes + provenance): ~10KB/doc → 20GB/day

---

## Step 2: Propose High-Level Design and Get Buy-In

### Core Architecture Components

- **Document Ingestion Service:** Accepts uploads (API, SFTP, email), normalizes format, assigns document ID, and queues for processing. This service is the sole entry point and must be idempotent—if a document is submitted twice (network retry, duplicate upload), exactly one processing job should be created, enforced via a content hash deduplication check before enqueue.

> **Why a single ingestion service fronted by a message queue:** Placing all ingestion behind a single service with a message queue decouples the upload rate from the processing rate. During invoice batch uploads at month-end, the queue absorbs spikes without back-pressure reaching the client; documents are never lost even if downstream workers restart.

- **Document Classifier:** A lightweight CNN or vision transformer (e.g., LayoutLMv3 [[glossary#Fine-tuning|fine-tuned]] on 50+ document classes) classifies each document as invoice, bank statement, loan contract, or tax form, then selects the appropriate extraction schema for that class. Classification accuracy matters because schema mismatch causes all downstream field mappings to fail—a misclassified tax form treated as an invoice will produce zero valid fields.

> **Why a dedicated document classifier rather than prompting the LLM to infer document type:** Using a dedicated classifier rather than prompting the LLM to infer document type separates concerns and saves tokens. A small vision classifier runs in <50ms and achieves >99% accuracy on trained classes; asking the LLM to classify adds ~200ms and consumes prompt budget that could be used for field extraction.

- **OCR Engine:** Layout-aware OCR (PaddleOCR or Tesseract with preprocessing) processes scanned documents and produces text tokens plus their bounding box coordinates (x, y, width, height) on the page. This stage is bypassed entirely for digital-native PDFs, where pdfplumber or PyMuPDF extracts the text layer and character-level coordinates directly from the PDF's internal structure at ~100ms per document.

> **Why OCR must emit bounding box coordinates, not just text:** Bounding box coordinates are not optional metadata—they are the foundation of source grounding (Layer 1 of hallucination prevention). Without knowing precisely where on the page a value came from, you cannot re-verify it independently, and you cannot present it to a human reviewer with a visual highlight.

- **Layout Analyzer:** An object detection model (DETR or Faster R-CNN fine-tuned on financial document layouts) identifies structural regions—tables, key-value blocks, headers, footers, logos, and signature zones—and outputs their bounding boxes and semantic labels. The model is fine-tuned on a corpus of at least 100K annotated financial document pages to handle the wide variation in vendor templates.

> **Why a dedicated layout analyzer on top of OCR:** Raw OCR text loses spatial structure. A list of words in reading order cannot distinguish between a table cell containing "$1,250" in the "Total" column from the same number appearing in free text. Layout analysis recovers the two-dimensional structure that gives financial numbers their meaning.

- **Table Extractor:** A specialized Table Structure Recognition (TSR) module processes the regions flagged as tables by the layout analyzer, predicting row separators, column separators, and cell boundaries to reconstruct the full row-column grid. It handles complex layouts including merged header cells, borderless tables (where whitespace defines structure), multi-line cell content, and tables that span page boundaries.

> **Why a specialized Table Structure Recognition model rather than OCR alone:** General OCR reads text in a single left-to-right, top-to-bottom pass and cannot reconstruct table structure. A dedicated TSR model—trained specifically on the two-dimensional prediction task—achieves 95%+ cell-level accuracy on financial tables, compared to 60-70% for naive spatial clustering of OCR words.

- **LLM Extraction Engine:** Takes the assembled prompt (OCR text, layout structure as serialized key-value and table blocks, and the target JSON schema) and generates structured JSON with per-field values. Inference uses a 7B quantized model with grammar-constrained decoding to guarantee that every token produced continues a parse-valid JSON sequence matching the schema, eliminating the possibility of malformed output.

> **Why an LLM for field extraction rather than template or regex rules:** The LLM is the only component capable of zero-shot generalization to unseen vendor templates. Template-based or regex extraction requires a handcrafted rule per layout; the LLM's language understanding maps semantically equivalent labels ("Invoice Total", "Amount Due", "Grand Total") to the same schema field without explicit programming.

- **Validation Engine:** Applies three independent validation passes after extraction: (1) JSON schema conformance using jsonschema; (2) cross-field arithmetic checks (line item totals must sum to subtotal; subtotal plus tax must equal invoice total within rounding tolerance); (3) format and business-rule checks (dates must be parseable and logically ordered, account numbers must pass checksum algorithms, currencies must be in the allowed enum). Fields that fail validation are flagged with specific failure codes before confidence routing.

> **Why a separate validation engine with cross-field arithmetic checks:** Even with constrained decoding guaranteeing structural validity, a model can produce a structurally valid but arithmetically impossible output—a total that doesn't match its components. Independent arithmetic verification catches the entire class of digit transposition errors (~2-3% of monetary fields) that look syntactically correct but are semantically wrong.

- **Confidence Router:** Aggregates per-field confidence scores (combining LLM token log-probabilities, OCR word confidence, and validation pass/fail signals) into a document-level confidence score, then routes each document to one of three queues: auto-accept (>0.95), human review (0.80–0.95), or full manual extraction (<0.80). The router also performs per-field routing for high-value documents—even a high-confidence document goes to human review if any monetary field has confidence below 0.90.

> **Why three-way confidence routing rather than a binary accept/reject:** A binary accept/reject decision is wasteful. At a 0.95 document-level threshold, approximately 85% of documents auto-accept—routing all of them to human review would require 10x the reviewer headcount. The routing triage concentrates human attention on the 12-15% of documents where it has the highest impact on accuracy.

- **Human Review UI:** Displays the source document with bounding box overlays highlighted for every extracted field, shows the extracted value alongside the raw OCR text for that region, and indicates the confidence score and any validation failures per field. Reviewers correct individual fields without re-extracting the entire document, and corrections are stored with reviewer ID and timestamp for downstream fine-tuning.

> **Why the review UI overlays bounding boxes on the source document:** Showing reviewers only the extracted fields without the source document context forces them to mentally re-read the document to verify values—increasing review time from ~30 seconds to 3+ minutes per document. The bounding box overlay collapses verification to a glance, enabling reviewers to process 6-8x more documents per hour.

- **Audit & Provenance Store:** An append-only store that links every extracted field value to its source bounding box coordinates, OCR confidence score, LLM model version, extraction timestamp, and (if applicable) the reviewer ID who confirmed or corrected the value. No records are ever deleted or modified; corrections are stored as new entries linked to the original extraction event.

> **Why an append-only audit and provenance store:** Financial regulators (e.g., under Sarbanes-Oxley, PSD2, or Basel III requirements) require complete audit trails for any automated financial data processing. The immutable provenance record answers the question "why did the system extract this specific value" in a way that can be presented to auditors—without it, the organization cannot demonstrate compliance with automated processing rules.

### Pipeline A: Document Processing Pipeline

1. Document arrives via API/SFTP/email → ingestion service assigns a UUID, deduplicates via content hash, stores the original binary in blob storage (S3/GCS), and places a processing job on the queue with the blob reference and detected MIME type.
2. Document classifier reads the first page as an image (for visual classification) and the MIME type, determines document type (invoice, statement, contract, tax form) and page count, and attaches the appropriate JSON schema definition to the job.
3. For scanned docs: OCR engine applies preprocessing (deskew, denoise, binarize) then runs PaddleOCR to produce a word-level list of `{text, confidence, bbox}` tuples. For digital PDFs: pdfplumber extracts text tokens with character-level bounding boxes directly from the PDF object tree, bypassing OCR entirely.
4. Layout analyzer runs the DETR-based detection model on each page image and produces a list of region annotations: `{region_type, page, bbox, confidence}` covering tables, key-value blocks, headers, footers, and signature zones.
5. Table extractor runs TSR on each region annotated as a table, produces a structured grid of `{row, col, content, bbox}` tuples, merges multi-page table continuations by matching column headers, and serializes each table into markdown for prompt injection.
6. Prompt assembler combines the OCR key-value pairs, serialized tables, remaining free text, document type, and target schema into the structured extraction prompt format, keeping total prompt length under the model's 8K token context window by truncating low-priority free text last.
7. LLM extraction engine runs grammar-constrained inference, producing a JSON object guaranteed to conform to the target schema. Token log-probabilities for each field value are captured alongside the output for confidence scoring.
8. Validation engine runs three passes: JSON schema conformance, cross-field arithmetic checks with a 0.5% rounding tolerance, and format/business-rule checks. Each failing check attaches a failure code and the specific field(s) implicated.
9. Confidence router computes the document-level confidence score and per-field confidence scores, then routes to auto-accept (>0.95), human review (0.80–0.95), or full manual extraction (<0.80). High-value documents (total amount >$10K) apply a stricter monetary-field threshold of 0.92 regardless of document-level score.
10. Results are written to the output store with full provenance: every field value links to its source bounding box, OCR confidence, LLM model version, and extraction timestamp. An event is published to downstream consumers (payment systems, accounting APIs) only after successful provenance write.

### Pipeline B: Model Training & Improvement Pipeline

1. Human review corrections are collected in a corrections database with the original extraction, the reviewer-supplied correct value, and the field-level diff. Each correction is tagged with the document type and the specific failure mode (wrong value, hallucinated value, missed field, format error) to enable targeted analysis.
2. Corrections are joined with the original document image and OCR output to form training tuples: `(document_image, ocr_text, layout_regions, correct_json)`. Tuples where the correction was a reviewer error (caught by subsequent audit) are excluded from training data.
3. A weekly LoRA fine-tuning run on the extraction model processes all corrections accumulated since the last run. The LoRA adapter targets the attention and MLP layers most responsible for value extraction (identified via activation analysis), leaving the model's general language understanding intact.
4. A quality gate compares the new model checkpoint against the frozen baseline on a held-out test set stratified by document type. The new checkpoint must show ≥0.2% improvement in per-field exact-match accuracy with no regression on any individual document class before promotion.
5. Canary deployment routes 5% of live traffic to the new model while the baseline handles the remaining 95%. Field-level accuracy is measured against human review outcomes for 24 hours; the deployment is promoted if accuracy meets or exceeds the baseline and rolled back automatically if any accuracy metric drops more than 0.1%.
6. Gradual rollout advances in 10% increments every 4 hours, with continuous monitoring of the per-field accuracy, human review routing rate, and arithmetic validation failure rate. A drop in any metric triggers an automatic halt and Slack alert to the ML engineering on-call.

### Mermaid Architecture Diagram

```mermaid
flowchart LR
  input[Document Input API/SFTP/Email] --> ingest[IngestionService]
  ingest --> blob[BlobStorage]
  ingest --> classifier[DocumentClassifier]

  classifier --> ocrBranch{Scanned?}
  ocrBranch -->|Yes| ocr[OCR Engine]
  ocrBranch -->|No| textExtract[PDF Text Extractor]

  ocr --> layout[LayoutAnalyzer]
  textExtract --> layout

  layout --> tableExtract[TableExtractor]
  tableExtract --> promptAssembly[PromptAssembler]
  layout --> promptAssembly

  promptAssembly --> llm[LLM Extraction Engine]
  llm --> validator[ValidationEngine]
  validator --> confidence[ConfidenceRouter]

  confidence -->|High| autoAccept[AutoAccept Store]
  confidence -->|Medium| humanReview[Human Review UI]
  confidence -->|Low| autoReject[AutoReject + Alert]

  humanReview --> corrections[Corrections DB]
  corrections --> finetune[Fine-Tuning Pipeline]
  finetune --> llm

  autoAccept --> audit[Audit & Provenance Store]
  humanReview --> audit
```

---

## Step 3: Design Deep Dive

Focus areas:

1. **OCR-to-LLM Pipeline (Layout Detection, Table Extraction, Field Mapping)**
2. **Structured Output Enforcement (JSON Schema, Constrained Decoding, Validation)**
3. **Hallucination Prevention for Financial Data**

### 1) OCR-to-LLM Pipeline

The pipeline must bridge the gap between raw pixels and structured financial data. Each stage introduces potential error that compounds downstream.

**OCR strategy by document type:**

| Document Source | OCR Approach | Word-Level Accuracy | Notes |
|---|---|---|---|
| Digital-native PDF | Direct text extraction (pdfplumber/PyMuPDF) | 99.9%+ | No OCR needed; extract coordinates from PDF internals |
| Clean scan (300+ DPI) | Tesseract/PaddleOCR with preprocessing | 98-99% | Deskew, binarize, denoise before OCR |
| Low-quality scan (<200 DPI) | PaddleOCR + super-resolution preprocessing | 94-97% | Upscale with ESRGAN before OCR; flag for human review |
| Photographed documents | Document-specific model (DocTR/TrOCR) | 90-95% | Perspective correction, shadow removal required |
| Handwritten fields | TrOCR fine-tuned on financial handwriting | 85-92% | Always route to human review for monetary amounts |

**Layout detection architecture:**

The layout analyzer uses an object detection model (Faster R-CNN or DETR fine-tuned on financial documents) to identify structural regions:

- **Key-value blocks:** "Invoice Number: INV-2024-001" → detect label-value pairs using spatial proximity heuristics; labels and values within ~20px vertical alignment and <200px horizontal separation are grouped. This structured representation prevents the LLM from needing to parse free text to find field associations.
- **Tables:** Detect the outer bounding box of tables, then apply a secondary TSR model for internal row/column segmentation. The two-model approach lets each model specialize: the detector handles "is this a table?" while the TSR model handles the finer "where are the rows and columns?"
- **Headers/footers:** Identify recurring text blocks that appear at the same vertical position across multiple pages (company name, page numbers, document title), enabling template matching for known vendor layouts and cross-page context stitching.
- **Signatures/stamps:** Detect but do not extract content from signature and stamp regions. Their presence is recorded as a boolean completeness signal (e.g., `signature_present: true`) required by some compliance workflows to confirm a document is fully executed.

**Table extraction pipeline:**

Tables are the hardest structural element. Financial documents contain line items, transaction histories, and amortization schedules with complex layouts.

1. **Table detection:** Object detection model identifies table bounding boxes.
2. **Row/column segmentation:** TSR (Table Structure Recognition) model predicts row and column separators. Handles borderless tables using whitespace analysis.
3. **Cell content extraction:** Map OCR words to cells using spatial overlap with predicted cell boundaries.
4. **Header association:** Classify first row(s) as headers; map column semantics (Description, Quantity, Unit Price, Total).
5. **Multi-page table merging:** Detect continuation tables across pages using header matching and column alignment.

**Prompt assembly for LLM extraction:**

The prompt must convey document structure, not just raw text. The format:

```text
Document Type: Invoice
Schema: {invoice_number: string, date: date, vendor_name: string, ...}

=== KEY-VALUE PAIRS ===
[Label: "Invoice Number", Value: "INV-2024-001", Position: (120, 45)]
[Label: "Date", Value: "March 15, 2024", Position: (120, 72)]
...

=== TABLE: Line Items ===
| Description | Qty | Unit Price | Total |
|---|---|---|---|
| Widget A | 100 | $12.50 | $1,250.00 |
| Widget B | 50 | $8.75 | $437.50 |

=== RAW TEXT (remaining) ===
Payment Terms: Net 30 ...

Extract all fields matching the schema as JSON.
```

#### OCR-to-LLM Trade-off Table

| Approach | Accuracy | Latency | Generalization | Complexity |
|---|---|---|---|---|
| OCR → regex/template matching | 85-92% per field; fails completely on any layout not in the template library, requiring weeks of engineering per new vendor | <500ms; purely deterministic, no model inference | None — a new vendor layout breaks the system entirely until a template is hand-coded | Low to build; high to maintain as the template library grows to hundreds of rules |
| OCR → LLM (text only, no layout) | 93-96% per field; table cell values are frequently misattributed to the wrong column because spatial structure is lost in linearization | ~2s; one LLM inference call with ~2K tokens, no object detection overhead | Good for simple key-value documents; degrades significantly on multi-column tables and complex invoices | Medium; OCR pipeline plus LLM, but no layout detection or TSR models to build and maintain |
| OCR → layout-aware LLM (structured prompt) | 97-99% per field; table structure preserved in the prompt eliminates most cross-column confusion; source grounding enables error detection | ~3s; adds ~800ms for layout detection and TSR on top of OCR and LLM inference | Strong; the LLM maps semantically equivalent labels across layouts, handling ~80% of novel vendor templates without retraining | High; three additional ML models (layout detector, TSR, OCR) each requiring monitoring, retraining, and versioning |
| Vision-Language Model (end-to-end, no OCR) | 95-98% on clean documents; degrades to 85-90% on low-quality scans, and below 80% on dense multi-page tables — the model loses positional precision at scale | 3-5s; requires processing full-resolution page images through a large vision encoder (typically 7B-72B parameters) | Best zero-shot on novel layouts; VLMs generalize visual patterns without needing document-type-specific training | High computational cost; VLMs are 5-10x more expensive per document than a 7B text model; no bounding box provenance without additional grounding heads |
| Hybrid: OCR + layout + LLM + VLM fallback | 99%+ per field; OCR pipeline handles 90% of documents reliably, VLM catches the 10% where layout parsing fails; combining both verification channels catches nearly all error types | 4-5s for the VLM fallback path; the majority of documents complete on the 3s OCR+LLM path | Best overall; each approach covers the other's blind spots, and the system degrades gracefully when one component fails | Very high; two complete pipeline paths to build, monitor, and maintain; requires routing logic to decide which path each document takes |

### 2) Structured Output Enforcement

Financial extraction demands perfectly structured output. A missing closing brace or a string where a number belongs is unacceptable.

**JSON schema enforcement layers:**

1. **Schema definition per document type:**

```json
{
  "type": "object",
  "properties": {
    "invoice_number": {"type": "string", "pattern": "^[A-Z]{2,4}-\\d{4,}$"},
    "total_amount": {"type": "number", "minimum": 0},
    "currency": {"type": "string", "enum": ["USD", "EUR", "GBP", "JPY"]},
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": {"type": "string"},
          "quantity": {"type": "integer", "minimum": 1},
          "unit_price": {"type": "number", "minimum": 0},
          "total": {"type": "number", "minimum": 0}
        },
        "required": ["description", "quantity", "unit_price", "total"]
      }
    }
  },
  "required": ["invoice_number", "total_amount", "currency", "line_items"]
}
```

2. **Constrained decoding at inference time:**

Rather than hoping the LLM produces valid JSON, enforce it during generation:

- **Grammar-constrained decoding:** Use a context-free grammar (CFG) that mirrors the JSON schema. At each token position, mask logits to only allow tokens that continue a valid parse. Libraries: Outlines, llama.cpp grammar mode, vLLM guided decoding.
- **Finite-state machine (FSM) approach:** Track the parser state during decoding. When inside a string value for `total_amount`, only allow digit tokens, decimal points, and the closing quote.
- **Structured output APIs:** OpenAI/Anthropic structured output modes that guarantee schema conformance.

3. **Post-generation validation pipeline:**

Even with constrained decoding, validate:

- JSON schema conformance (jsonschema library).
- Type coercion: parse "$1,250.00" → 1250.00 (strip currency symbols, commas).
- Date normalization: "03/15/2024", "March 15, 2024", "15-Mar-24" → ISO 8601.
- Enum matching: fuzzy-match extracted values to allowed enum sets.

#### Structured Output Trade-off Table

| Technique | Conformance Rate | Latency Overhead | Quality Impact | Complexity |
|---|---|---|---|---|
| Free-form generation + regex parsing | 70-85% conformance; models frequently add markdown fences, prose explanations, or trailing commas that break JSON parsers, especially on edge cases with unusual field values | None at inference time; all cost is paid in regex maintenance and error-handling code for the 15-30% of responses that fail | High failure rate in production; every parse failure requires a retry or fallback, adding latency variance and compute cost unpredictably | Low to start; rapidly grows complex as more edge cases require special-casing in the parsing layer |
| Prompt engineering ("output valid JSON") | 85-95% conformance; reliability depends heavily on model size and instruction-following capability — a 7B model may achieve only 85%, while a 70B model reaches 95% | None; the instruction consumes ~10 tokens of prompt budget but adds zero inference overhead | Model-dependent and inconsistent; the same prompt may fail 5% of the time in one model version and 15% after a model update, creating silent regressions | Low; just a prompt addition, but requires careful monitoring as model versions change |
| Constrained decoding (grammar/FSM) | 99.9%+ conformance by construction; the FSM makes it physically impossible to generate a token that would violate the grammar, so invalid output cannot occur | 5-15% slower decoding throughput due to logit masking at each step — masking eliminates ~90% of the vocabulary at most positions, requiring an extra matrix operation per token | Slight reduction in field value accuracy (~0.5-1%) because the most probable token is sometimes masked; the model is forced to the second-best token, which may be a valid format but a slightly less confident value | Medium; requires integrating a grammar library (Outlines, llama.cpp grammar mode) with the inference server and defining a CFG per schema |
| Function calling / tool use API | 98-99% conformance; cloud provider APIs (OpenAI, Anthropic) enforce schema server-side, so clients receive only valid responses or explicit errors | Minimal — typically <50ms additional latency over standard generation; schema enforcement is handled inside the provider's inference stack | Good quality; the model is trained specifically for structured output, so function-calling-tuned models often produce higher-quality field values than grammar-constrained open models | Low on the client side; providers handle the complexity, but you're locked into their API and schema language capabilities |
| Constrained decoding + post-validation | 100% structural conformance; arithmetic and semantic validation is layered on top of structural guarantees, catching the errors constrained decoding cannot prevent (valid structure, wrong value) | 10-20% slower total pipeline; 5-15% from constrained decoding plus ~10ms for arithmetic checks and format validation | Best overall; structural guarantees eliminate parse failures, and semantic validation catches the remaining error classes | High; requires constrained decoding infrastructure, per-schema grammar definitions, and a validation rule engine with domain-specific arithmetic and format rules |

### 3) Hallucination Prevention for Financial Data

In financial extraction, a hallucinated digit is not a minor quality issue—it's a potential compliance violation or erroneous payment. The system must treat hallucination as a safety problem.

**Hallucination taxonomy for document extraction:**

| Hallucination Type | Example | Frequency | Severity |
|---|---|---|---|
| Digit transposition | "$1,250" → "$1,520" | 2-3% of fields | Critical for amounts |
| Fabricated field | Model invents an invoice number not present in document | 1-2% | High |
| Cross-document bleed | Value from a previous document in batch appears in current extraction | <0.5% | Critical |
| OCR error propagation | OCR reads "8" as "6" → LLM faithfully extracts wrong value | 3-5% on low-quality scans | High |
| Normalization error | "$1,250.00" parsed as "$125,000" (misplaced decimal) | 1-2% | Critical for amounts |

**Multi-layer hallucination prevention:**

**Layer 1 — Source grounding:**
- Every extracted value must trace to specific bounding box coordinates in the source document.
- During extraction, require the LLM to output both the value and its source location: `{"total_amount": 1250.00, "total_amount_source": "page1, bbox(320, 415, 420, 435)"}`.
- Post-extraction: OCR the specific bounding box region independently and compare against extracted value. Mismatch → flag for review.

**Layer 2 — Cross-field verification:**
- Arithmetic checks: `sum(line_item.total) == subtotal`, `subtotal + tax == total_amount`.
- Rate checks: `tax_amount / subtotal ≈ expected_tax_rate ± 1%`.
- Date logic: `due_date > invoice_date`, `payment_terms_days == due_date - invoice_date`.
- Relationship checks: `vendor_name` in extracted text must appear in raw OCR output (not fabricated).

**Layer 3 — Confidence scoring:**
- Per-field confidence derived from:
  - LLM token-level log-probabilities (average log-prob of tokens comprising the field value).
  - OCR confidence for the source bounding box region.
  - Validation pass/fail signals (arithmetic check passed → boost confidence).
- Composite confidence: `conf = 0.4 × llm_logprob + 0.3 × ocr_confidence + 0.3 × validation_score`.

**Layer 4 — Human review routing:**

| Confidence Band | Action | Expected Volume |
|---|---|---|
| > 0.95 | Auto-accept | 85% of documents |
| 0.80 – 0.95 | Human review (reviewer sees flagged fields only) | 12% of documents |
| < 0.80 | Full manual extraction | 3% of documents |

**Layer 5 — Batch-level anomaly detection:**
- Track field value distributions per vendor/document type.
- Flag statistical outliers: invoice total 10x historical average for that vendor → review.
- Detect cross-document bleed: if same unique identifier (invoice number) appears in two consecutive extractions → flag.

#### Hallucination Prevention Trade-off Table

| Technique | Error Reduction | Latency Cost | Human Review Load | Implementation Effort |
|---|---|---|---|---|
| Source grounding (bbox verification) | 40-50% reduction in hallucinated values; the technique specifically catches cases where the LLM generates a value that does not appear anywhere in the OCR output — i.e., pure fabrication rather than OCR-error propagation | +200ms to re-OCR the specific bounding box region at higher resolution for comparison; this can be parallelized with the validation pipeline to minimize wall-clock impact | Reduces review load by converting vague "low confidence" flags into specific, actionable "extracted value does not match source text" flags, enabling reviewers to verify in seconds rather than re-reading the entire document | Medium; requires extracting and storing bounding box coordinates per field during LLM inference, implementing independent re-OCR logic, and building the character-level comparison pipeline |
| Cross-field arithmetic checks | 20-30% reduction in monetary field errors; catches all cases where individual line item errors propagate to totals, and all cases of digit transposition that change a sum — but cannot catch errors where both the line items and the total are consistently wrong (e.g., consistently off by 10x) | +10ms; purely computational, no model inference; arithmetic on ~15 fields per invoice is negligible | Eliminates the entire class of "total doesn't match line items" errors from human review — reviewers see only arithmetic failures where something is genuinely inconsistent, not marginal floating-point differences | Low; a straightforward rules engine with document-type-specific formulas (sum of line items = subtotal; subtotal + tax = total; tax / subtotal ≈ expected rate); requires only the extracted JSON, no additional ML |
| Confidence-gated routing | Not an error prevention mechanism — a detection and containment strategy; routes ~12-15% of documents to human review, where human accuracy is ~99.9%, effectively achieving that accuracy for the routed subset | +50ms for aggregating per-field confidence scores, computing composite scores, and evaluating routing thresholds across all fields; can be parallelized with provenance storage | Routes 12-15% of documents to human review; the key design choice is the threshold — lowering from 0.95 to 0.90 reduces review load by ~40% but allows ~0.5% more errors through to auto-accept | Medium; requires capturing and storing per-field token log-probabilities during LLM inference (not available in all inference frameworks), implementing OCR confidence aggregation, and calibrating thresholds empirically against held-out labeled data |
| Dual extraction (run twice, compare) | 60-70% reduction in field errors; when two independent extraction runs disagree on a value, one is almost certainly wrong — and the disagreement signal is highly correlated with actual errors (~85% precision for flagging) | +100% compute cost; each document requires two full LLM inference passes at the same latency as the original, effectively doubling the GPU fleet requirement and doubling per-document inference cost | Reduces human review to only the ~10-20% of documents where the two extraction runs disagree on at least one field, which is a much more targeted review queue than confidence-gated routing | Low implementation complexity (run the same pipeline twice with different temperature or prompt variations) but high infrastructure cost; rarely justified except for a subset of very high-value documents (e.g., invoices >$100K) |
| Ensemble (two models, majority vote) | 50-60% reduction in errors; two differently-trained models have largely independent error patterns — a digit transposition error in model A is unlikely to produce the same wrong digit in model B | +80% compute overhead rather than +100%; the two models can run concurrently if GPU capacity permits, adding only ~200ms for the slower model's completion rather than the full inference time of a second pass | Requires human review only for the ~15-25% of documents where models disagree, similar to dual extraction but with the additional benefit that agreement between two architecturally different models is a stronger quality signal | High; requires training and maintaining two separate extraction models with different architectures or training data, coordinating their deployment, and building a field-level comparison and merging layer |

### Production Bottlenecks and Mitigations

- **OCR quality variance across document sources**
  - Symptom: The same pipeline achieves 99% word-level accuracy on clean 300 DPI scans but drops to 88% on faxed documents or documents photographed with poor lighting — an 11-point gap that translates directly into extraction errors on monetary fields.
  - Mitigation: Assign a per-source quality score at ingestion by measuring the median OCR word confidence for a sample of that source's historical documents. Sources with median confidence below 0.85 automatically receive super-resolution preprocessing (Real-ESRGAN upscaling before OCR) and have all monetary fields routed to human review regardless of extraction confidence, effectively treating them as a lower-trust input class.

> **Why per-source OCR confidence calibration rather than a single global threshold:** A single OCR quality threshold applied uniformly to all sources either over-routes clean documents (expensive reviewer time) or under-routes degraded documents (accuracy violations). Per-source calibration adapts the confidence thresholds to the actual noise level of each input channel.

- **Table extraction failure on complex layouts**
  - Symptom: Merged header cells, nested tables within line items, or borderless tables that use only whitespace for column separation cause the TSR model to misalign rows and columns — a row of "$1,250 | 10 | $125" may be parsed as three separate single-cell rows, associating none of the values with the correct column header.
  - Mitigation: Ensemble two table detection approaches: the neural TSR model and a rule-based whitespace-alignment parser. When their outputs disagree on column count or cell boundaries, fall back to passing the table image directly to a VLM (e.g., GPT-4V) with a prompt asking for the table as a markdown grid. This fallback applies to fewer than 5% of tables but catches the cases where structural parsing fails most spectacularly.

> **Why ensemble TSR with a rule-based parser and VLM fallback:** A neural TSR model trained on well-structured tables generalizes poorly to the adversarial long tail of financial document formats. The rule-based parser is brittle but correct for borderless tables where whitespace is consistent. Combining them and falling back to a VLM covers all three cases — clean tables (TSR), borderless tables (rules), and complex tables (VLM) — without a single model needing to handle all cases.

- **LLM context window overflow on multi-page documents**
  - Symptom: A 20-page loan contract with 300 words per page contains approximately 90K characters or ~22K tokens — exceeding the 8K context window of a 7B model. Fields mentioned only in the appendix (e.g., prepayment penalty clauses on page 19) are never seen by the extraction model, resulting in silently missed fields with no error or confidence signal.
  - Mitigation: Implement a two-level extraction strategy. First, use the document classifier's page-level segmentation to identify which pages contain which schema fields (trained on 10K annotated contracts). Second, run extraction independently on each relevant page or section, using only the sub-schema for that section. Third, merge the per-section JSON extractions, resolving conflicts (e.g., an interest rate mentioned on page 3 and page 47 must match) using a lightweight reconciliation prompt with only the conflicting fields.

> **Why a segment-then-reconcile strategy for multi-page documents:** Naively chunking documents and running a single extraction pass per chunk loses cross-page field references and produces duplicate or conflicting values for fields mentioned in multiple sections. The segment-then-reconcile pattern preserves full-document coherence while respecting context window limits.

- **Cross-document contamination in batch processing**
  - Symptom: When multiple documents are processed in the same GPU worker process (a common optimization for throughput), the KV cache state from document N can influence the softmax attention weights for document N+1, particularly for rare tokens like specific account numbers or invoice IDs that appear in both documents' contexts — causing values from a previous document to appear in the current extraction.
  - Mitigation: Enforce document isolation at the inference level: clear the KV cache completely between documents and never include multiple documents in a single inference call. Use a dedicated process per document (process-level isolation) during high-accuracy mode, accepting the 15-20% throughput loss. Flag any extracted value (account number, invoice ID, vendor name) that also appears in the immediately preceding document's extraction as a potential contamination event for review.

> **Why enforce per-document KV cache isolation during batch processing:** KV cache contamination is insidious because it produces plausible-looking extractions — the contaminating values are real financial data from a real document, just the wrong one. Source grounding (Layer 1) partially catches this because the contaminated value may not appear in the current document's OCR output, but only if the contaminating value is textually distinct from any string in the current document.

- **Schema evolution when new document types appear**
  - Symptom: A new vendor begins submitting invoices in an EDI 810 format with vendor-specific extension fields (e.g., a `project_code` field not in the standard invoice schema). The extraction model correctly extracts all schema-defined fields but silently ignores the project code — which the downstream payment system requires for cost center allocation, causing payment rejections.
  - Mitigation: Run zero-shot discovery mode on the first 100 documents from each new vendor or format: prompt the LLM to extract both the schema-mandated fields AND any additional key-value pairs it detects that are not in the schema. Human reviewers confirm which discovered fields should be promoted to schema-level fields. Discovered fields accumulate in a "candidate fields" registry; any candidate that appears in >80% of documents from a vendor triggers a schema update proposal.

> **Why run zero-shot discovery mode on new document types:** Purely schema-driven extraction creates a closed-world assumption — the system can only find what it's looking for. Discovery mode turns unknown-unknowns into known-unknowns by surfacing fields the schema designers didn't anticipate, enabling proactive schema evolution rather than reactive debugging of silent extraction failures.

- **Confidence calibration drift**
  - Symptom: At launch, the 0.95 confidence threshold auto-accepts 85% of documents with a 0.3% error rate. After three months, the same threshold auto-accepts only 70% of documents — a 15% increase in human review load with no corresponding increase in error rate. The model's confidence distribution has shifted rightward (lower confidence on average) due to changes in document quality, vendor mix, or model fine-tuning.
  - Mitigation: Weekly calibration using human review outcomes as ground truth. For each document reviewed by a human, record whether the extracted fields were correct. Fit a Platt scaling logistic regression that maps raw composite confidence scores to calibrated probabilities that equal the empirical accuracy rate. Recalibrate thresholds so that the 0.95 tier corresponds to documents with measured 95%+ accuracy — which may require a raw score of 0.92 or 0.97 depending on the current distribution.

> **Why weekly Platt scaling recalibration of confidence thresholds:** Confidence scores from LLM token log-probabilities are not naturally calibrated to accuracy percentages. A model that assigns 0.95 confidence to 70% of its outputs (regardless of their accuracy) will systematically flood the human review queue. Platt scaling is a lightweight, interpretable calibration method that adjusts the score-to-accuracy mapping without retraining the underlying model.

---

## Practical Implementation

### Code Block 1: Grammar-Constrained LLM Extraction with Outlines

This implementation uses the Outlines library to enforce JSON schema conformance at the token level during inference, guaranteeing that every generated token continues a valid parse tree. The schema is compiled into a finite-state machine before inference begins, adding negligible per-document overhead after the one-time compilation cost.

```python
import json
import outlines
import outlines.models as models
import outlines.generate as generate
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date


class LineItem(BaseModel):
    description: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0.0)
    total: float = Field(ge=0.0)

    @field_validator("total")
    @classmethod
    def total_matches_product(cls, v: float, info) -> float:
        qty = info.data.get("quantity")
        price = info.data.get("unit_price")
        if qty is not None and price is not None:
            expected = round(qty * price, 2)
            if abs(v - expected) > 0.015:  # allow 1.5 cent rounding tolerance
                raise ValueError(
                    f"total {v} does not match quantity({qty}) × unit_price({price}) = {expected}"
                )
        return v


class InvoiceExtraction(BaseModel):
    invoice_number: str = Field(pattern=r"^[A-Z0-9\-]{4,20}$")
    invoice_date: str  # ISO 8601 date string; validated in post-processing
    vendor_name: str
    total_amount: float = Field(ge=0.0)
    currency: str = Field(pattern=r"^(USD|EUR|GBP|JPY|CAD|AUD)$")
    line_items: list[LineItem]
    tax_amount: Optional[float] = Field(default=None, ge=0.0)
    subtotal: Optional[float] = Field(default=None, ge=0.0)


def build_extraction_prompt(doc_text: str, layout_tables: list[str]) -> str:
    tables_section = "\n".join(
        [f"=== TABLE {i+1} ===\n{t}" for i, t in enumerate(layout_tables)]
    )
    return f"""Document Type: Invoice

=== DOCUMENT TEXT ===
{doc_text}

{tables_section if layout_tables else ""}

Extract all invoice fields as structured JSON matching the schema.
If a field is not present in the document, omit it from the output.
Extract monetary amounts as numbers without currency symbols."""


def extract_invoice(
    model_path: str,
    doc_text: str,
    layout_tables: list[str],
) -> InvoiceExtraction:
    """
    Run grammar-constrained LLM inference to extract invoice fields.
    Returns a validated Pydantic model or raises ValidationError.
    """
    # Load model once; in production, load at service startup and reuse
    llm = models.transformers(model_path, device="cuda")

    # Compile the JSON schema to an FSM; ~50ms one-time cost per schema
    generator = generate.json(llm, InvoiceExtraction)

    prompt = build_extraction_prompt(doc_text, layout_tables)

    # generate() guarantees the output is valid InvoiceExtraction JSON
    extraction: InvoiceExtraction = generator(prompt, max_tokens=1024)

    return extraction


def cross_field_validate(extraction: InvoiceExtraction) -> list[str]:
    """
    Post-extraction arithmetic validation.
    Returns a list of validation failure messages (empty = all checks passed).
    """
    failures = []
    computed_subtotal = sum(item.total for item in extraction.line_items)

    if extraction.subtotal is not None:
        if abs(extraction.subtotal - computed_subtotal) > 0.02:
            failures.append(
                f"subtotal mismatch: sum(line_items)={computed_subtotal:.2f}, "
                f"extracted subtotal={extraction.subtotal:.2f}"
            )

    if extraction.tax_amount is not None and extraction.subtotal is not None:
        expected_total = round(extraction.subtotal + extraction.tax_amount, 2)
        if abs(extraction.total_amount - expected_total) > 0.02:
            failures.append(
                f"total_amount mismatch: subtotal({extraction.subtotal:.2f}) + "
                f"tax({extraction.tax_amount:.2f}) = {expected_total:.2f}, "
                f"extracted total = {extraction.total_amount:.2f}"
            )

    return failures
```

### Code Block 2: Confidence Scoring and Routing

This implementation captures per-field token log-probabilities during LLM inference and combines them with OCR confidence scores to produce a calibrated routing decision. The composite score uses the weighted formula from the design: `0.4 × llm_logprob + 0.3 × ocr_confidence + 0.3 × validation_score`.

```python
import math
import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RoutingDecision(Enum):
    AUTO_ACCEPT = "auto_accept"
    HUMAN_REVIEW = "human_review"
    MANUAL_EXTRACTION = "manual_extraction"


@dataclass
class FieldConfidence:
    field_name: str
    extracted_value: str
    llm_log_prob: float       # Average log-probability of tokens in this field's value
    ocr_confidence: float     # Average OCR word confidence for the source bbox region (0-1)
    validation_passed: bool   # True if this field passed all applicable validation checks
    is_monetary: bool = False # Monetary fields apply a stricter routing threshold


@dataclass
class DocumentConfidence:
    doc_id: str
    total_amount_usd: float
    field_scores: list[FieldConfidence] = field(default_factory=list)

    def composite_score(self, fc: FieldConfidence) -> float:
        """
        Compute composite confidence for a single field.
        llm_log_prob is typically in range [-5, 0]; normalize to [0, 1].
        """
        # Clamp log-prob to a reasonable range before normalization
        log_prob_clamped = max(fc.llm_log_prob, -5.0)
        llm_normalized = (log_prob_clamped + 5.0) / 5.0  # maps [-5, 0] → [0, 1]

        validation_score = 1.0 if fc.validation_passed else 0.0

        return (
            0.4 * llm_normalized
            + 0.3 * fc.ocr_confidence
            + 0.3 * validation_score
        )

    def document_confidence(self) -> float:
        """Minimum composite score across all fields (weakest-link aggregation)."""
        if not self.field_scores:
            return 0.0
        return min(self.composite_score(fc) for fc in self.field_scores)

    def monetary_confidence(self) -> float:
        """Minimum composite score across monetary fields only."""
        monetary = [fc for fc in self.field_scores if fc.is_monetary]
        if not monetary:
            return 1.0
        return min(self.composite_score(fc) for fc in monetary)

    def route(
        self,
        auto_accept_threshold: float = 0.95,
        review_threshold: float = 0.80,
        monetary_threshold: float = 0.92,
        high_value_usd: float = 10_000.0,
    ) -> tuple[RoutingDecision, list[str]]:
        """
        Returns the routing decision and a list of reasons for non-auto-accept decisions.
        """
        reasons = []
        doc_conf = self.document_confidence()
        mon_conf = self.monetary_confidence()

        if doc_conf < review_threshold:
            reasons.append(
                f"document confidence {doc_conf:.3f} below manual extraction threshold {review_threshold}"
            )
            return RoutingDecision.MANUAL_EXTRACTION, reasons

        # High-value documents apply stricter monetary threshold
        effective_monetary_threshold = (
            monetary_threshold if self.total_amount_usd >= high_value_usd
            else auto_accept_threshold
        )

        if mon_conf < effective_monetary_threshold:
            reasons.append(
                f"monetary field confidence {mon_conf:.3f} below threshold "
                f"{effective_monetary_threshold:.2f} "
                f"(document amount ${self.total_amount_usd:,.2f})"
            )
            return RoutingDecision.HUMAN_REVIEW, reasons

        if doc_conf < auto_accept_threshold:
            reasons.append(
                f"document confidence {doc_conf:.3f} below auto-accept threshold {auto_accept_threshold}"
            )
            return RoutingDecision.HUMAN_REVIEW, reasons

        return RoutingDecision.AUTO_ACCEPT, []


def platt_scale_calibrate(
    raw_scores: list[float],
    ground_truth: list[bool],
) -> tuple[float, float]:
    """
    Fit Platt scaling parameters (A, B) such that:
        calibrated_prob = sigmoid(A * raw_score + B)
    approximates the empirical accuracy at each confidence level.

    Returns (A, B) for use in production confidence recalibration.
    """
    from scipy.optimize import minimize
    from scipy.special import expit  # sigmoid

    scores = np.array(raw_scores)
    labels = np.array(ground_truth, dtype=float)

    def neg_log_likelihood(params):
        a, b = params
        p = expit(a * scores + b)
        # Clip to avoid log(0)
        p = np.clip(p, 1e-7, 1 - 1e-7)
        return -np.mean(labels * np.log(p) + (1 - labels) * np.log(1 - p))

    result = minimize(neg_log_likelihood, x0=[1.0, 0.0], method="L-BFGS-B")
    a_opt, b_opt = result.x
    return float(a_opt), float(b_opt)
```

### Code Block 3: Source Grounding Verification

This implementation performs independent re-OCR of the specific bounding box region for each extracted field and compares the re-OCR output against the extracted value to detect hallucinated values that do not exist in the source document.

```python
import difflib
import pytesseract
from PIL import Image
from dataclasses import dataclass
from typing import Optional


@dataclass
class BoundingBox:
    page: int
    x: int      # left pixel coordinate
    y: int      # top pixel coordinate
    width: int
    height: int


@dataclass
class GroundingResult:
    field_name: str
    extracted_value: str
    reocr_text: str
    similarity: float       # character-level similarity ratio [0, 1]
    grounded: bool          # True if extracted value found in re-OCR output
    confidence_adjustment: float  # positive = boost, negative = penalty to apply


def reocr_region(
    page_image: Image.Image,
    bbox: BoundingBox,
    padding_px: int = 10,
) -> str:
    """
    Crop the bounding box region from the page image (with padding),
    run Tesseract at high DPI, and return the extracted text.
    """
    img_w, img_h = page_image.size
    x1 = max(0, bbox.x - padding_px)
    y1 = max(0, bbox.y - padding_px)
    x2 = min(img_w, bbox.x + bbox.width + padding_px)
    y2 = min(img_h, bbox.y + bbox.height + padding_px)

    region = page_image.crop((x1, y1, x2, y2))
    # Upscale 3x before Tesseract for better accuracy on small regions
    region = region.resize(
        (region.width * 3, region.height * 3), Image.LANCZOS
    )
    text = pytesseract.image_to_string(
        region,
        config="--psm 7 --oem 3",  # PSM 7: single text line
    )
    return text.strip()


def verify_field_grounding(
    field_name: str,
    extracted_value: str,
    page_image: Image.Image,
    bbox: BoundingBox,
    similarity_threshold: float = 0.85,
) -> GroundingResult:
    """
    Verify that the extracted value is present in the source document
    at the claimed bounding box location.
    """
    reocr_text = reocr_region(page_image, bbox)

    # Normalize both strings: strip whitespace, lowercase, remove punctuation
    def normalize(s: str) -> str:
        import re
        return re.sub(r"[^\w\d.]", "", s.lower().strip())

    norm_extracted = normalize(extracted_value)
    norm_reocr = normalize(reocr_text)

    # Character-level similarity (handles minor OCR variation between runs)
    similarity = difflib.SequenceMatcher(
        None, norm_extracted, norm_reocr
    ).ratio()

    grounded = similarity >= similarity_threshold

    # Confidence adjustment: boost if strongly grounded, penalize if not
    if similarity >= 0.95:
        adjustment = +0.05
    elif similarity >= similarity_threshold:
        adjustment = 0.0
    elif similarity >= 0.70:
        adjustment = -0.10
    else:
        # Value is likely hallucinated — severe confidence penalty
        adjustment = -0.30

    return GroundingResult(
        field_name=field_name,
        extracted_value=extracted_value,
        reocr_text=reocr_text,
        similarity=similarity,
        grounded=grounded,
        confidence_adjustment=adjustment,
    )


def verify_all_fields(
    extractions: dict[str, str],           # field_name → extracted_value
    bboxes: dict[str, BoundingBox],        # field_name → source bounding box
    page_images: dict[int, Image.Image],   # page_number → PIL image
) -> list[GroundingResult]:
    """
    Run source grounding verification for all extracted fields that have
    an associated bounding box. Fields without bboxes are skipped (they
    may have been inferred rather than directly extracted).
    """
    results = []
    for field_name, value in extractions.items():
        if field_name not in bboxes:
            continue  # No source location; cannot verify grounding
        bbox = bboxes[field_name]
        page_img = page_images.get(bbox.page)
        if page_img is None:
            continue

        result = verify_field_grounding(
            field_name=field_name,
            extracted_value=value,
            page_image=page_img,
            bbox=bbox,
        )
        results.append(result)

    return results
```

---


---

## Step 4: Wrap Up

### Final Design Summary

The system chains OCR, layout analysis, table extraction, and LLM-based field mapping into a pipeline that treats accuracy as a safety constraint. Constrained decoding guarantees structural validity. Multi-layer hallucination prevention—source grounding, cross-field verification, confidence routing, and anomaly detection—pushes effective per-field accuracy past 99.5% while keeping human review load under 15%.

### Wrap-Around Concerns

- **Risk:** OCR errors on degraded scans propagate through the entire pipeline undetected. Mitigation: Per-source quality scoring, automatic re-OCR with enhanced preprocessing, confidence penalties for low-quality sources.
- **Risk:** Constrained decoding forces structurally valid but semantically wrong output (model "guesses" a number that fits the schema when uncertain). Mitigation: Prefer high-entropy "null" fields over low-confidence guesses; route nulls to human review.
- **Risk:** Adversarial documents (deliberately manipulated invoices) exploit the system's trust in OCR output. Mitigation: Tamper detection layer (check for pixel-level edits near amount fields), cross-reference against vendor master data.
- **Risk:** Regulatory requirements vary by jurisdiction (EU invoicing directives vs US standards). Mitigation: Per-jurisdiction schema variants with region-specific validation rules.
- **Risk:** Human reviewer fatigue degrades correction quality during high-volume periods. Mitigation: Review prioritization by dollar amount at risk; auto-distribute review load; quality audits on reviewer corrections.

---

## Step 5: Interviewer Curveballs

### Interviewer Follow-ups & Frequently Asked Questions (FAQ)

Q: The system extracts "$12,500" from an invoice but the actual amount is "$1,250.00"—an extra zero. How does your system catch this?

**The Ideal Answer:** Three independent checks fire. First, source grounding: re-OCR the bounding box region for the total amount field and compare character-by-character against the extracted value. Second, cross-field arithmetic: sum the line item totals and compare against the extracted total—if line items sum to $1,250 but the total says $12,500, flag the discrepancy. Third, statistical anomaly detection: compare against historical invoice totals from this vendor—a 10x deviation triggers review.

**Deep Dive & Trade-offs:**
- Source grounding catches OCR propagation errors but not cases where the source document itself is wrong.
- Arithmetic checks catch ~80% of amount errors on invoices with line items but fail on single-total invoices.
- Vendor history checks require sufficient historical data (cold-start problem for new vendors).

**The Interviewer's Rubric:** Checking multi-layered defense thinking for financial data integrity.

---

Q: A vendor sends invoices as photographed images taken with a phone camera. Quality is terrible. What do you do?

**The Ideal Answer:** Apply a specialized pre-processing pipeline before any OCR: (1) perspective correction — detect the document's four corners using a document detection model (DocSeg or MobileNet-based), then apply a projective transform to warp the image to a rectangle with consistent margins; (2) shadow removal — apply a homomorphic filter or background subtraction to normalize uneven lighting across the document surface; (3) super-resolution upscaling — run Real-ESRGAN to upscale from an effective ~150 DPI to 300 DPI, recovering character edge detail needed for OCR; (4) adaptive binarization (Sauvola thresholding) — convert to black-and-white with locally adaptive thresholds that handle regions of different brightness in the same image. After preprocessing, route through TrOCR (a transformer-based OCR model) rather than Tesseract, because TrOCR's attention mechanism handles irregular character spacing and residual distortion far better than Tesseract's line-segmentation approach. Regardless of the resulting extraction confidence, automatically flag all monetary fields for human review — no matter how good the preprocessing, a photographed document is a lower-trust input class.

**Deep Dive & Trade-offs:**
- Super-resolution adds ~500ms to the preprocessing pipeline but improves TrOCR word accuracy from ~88% to ~94% on low-quality phone photographs, which translates directly to fewer OCR error propagations into field extraction.
- TrOCR is approximately 2x slower than Tesseract per page (~1.5s vs ~0.7s), but TrOCR's per-word error rate on degraded input is approximately half of Tesseract's — the latency trade-off is strongly justified for monetary documents where an OCR error means a wrong payment.
- The business decision is whether to absorb the extra per-document cost of preprocessing + human review (typically $0.50–$2.00 per document) or require the vendor to submit higher-quality scans, potentially with a contractual SLA for submission quality. Both are valid; the technical system must support the human review path regardless.

**The Interviewer's Rubric:** Checking practical image preprocessing knowledge and graceful degradation strategy. Strong candidates mention specific preprocessing steps (not just "enhance the image") and explain why each step addresses a specific failure mode. Top candidates also address the business dimension — what to do when preprocessing is not enough.

---

Q: How do you handle a 50-page loan contract where you need to extract fields scattered across different sections?

**The Ideal Answer:** Three-phase approach. Phase 1: Document segmentation—classify each page into sections (terms, signatures, schedules, amendments) using a page-level classifier. Phase 2: Per-section extraction—run the LLM on each relevant section independently with section-specific schemas. Phase 3: Cross-section reconciliation—merge extracted fields, resolve conflicts (e.g., interest rate mentioned on page 3 and page 47 must match), and validate cross-references.

**Deep Dive & Trade-offs:**
- Per-page extraction avoids context window limits but loses cross-page references.
- Full-document extraction with a 128K context model preserves references but is expensive (~15s for 50 pages) and accuracy degrades on long contexts.
- Hybrid: extract per-section, then run a lightweight verification pass with key fields from all sections in a single prompt.

**The Interviewer's Rubric:** Checking ability to decompose long-document problems without losing cross-document coherence. Strong candidates identify the two competing concerns (context window limits vs. cross-page references) and propose an architecture that addresses both. Top candidates quantify the costs of each approach — processing a 50-page contract as a single 22K-token prompt costs ~$0.30 per document at GPT-4 pricing vs. ~$0.08 for the segmented approach — and explain when the cost difference justifies each approach.

---

Q: You need to support a new document type (e.g., customs declarations) with zero training data. How?

**The Ideal Answer:** Zero-shot extraction using schema-driven prompting. Define the JSON schema for customs declarations (declaration number, HS codes, country of origin, declared value, etc.). Provide the schema and 2-3 synthetic examples in the system prompt. The LLM's general knowledge of financial document structure handles most field types. Monitor accuracy on the first 500 documents with 100% human review. Use corrections as few-shot examples, then fine-tune a LoRA adapter after accumulating 2K+ labeled documents.

**Deep Dive & Trade-offs:**
- Zero-shot accuracy for new doc types: typically 85-92% (sufficient for human-review-assisted launch).
- Few-shot (5-10 examples in prompt): jumps to 92-96%.
- Fine-tuned (2K+ examples): reaches 98%+ parity with established document types.
- Cold-start cost: 100% human review for ~2 weeks → expensive but necessary for accuracy guarantees.

**The Interviewer's Rubric:** Checking cold-start strategy and understanding of the accuracy-data flywheel. Strong candidates distinguish between zero-shot (schema only), few-shot (examples in prompt), and fine-tuned (LoRA) modes and know approximately when each is appropriate based on labeled data volume. Top candidates acknowledge the business cost of the cold-start period — 100% human review for 2 weeks on 2,000 documents per day means 28,000 manual reviews, roughly $14,000–$28,000 in reviewer cost — and frame this as an investment that enables a scalable, high-accuracy system rather than just a technical bootstrap problem.

---

Q: Constrained decoding guarantees valid JSON, but the model fills in a plausible-looking but wrong account number. How do you detect this?

**The Ideal Answer:** Constrained decoding only enforces structure, not semantics. Semantic correctness requires: (1) source grounding—verify the account number exists in the OCR text at the claimed bounding box; (2) format validation—check against known account number formats (routing numbers are 9 digits with a specific checksum algorithm, IBANs have country-specific formats with check digits); (3) entity resolution—if the vendor is known, check against the vendor master database for expected account numbers; (4) confidence thresholding—if the LLM's token log-probabilities for the account number tokens are low, route to review.

**Deep Dive & Trade-offs:**
- Checksum validation catches ~60% of fabricated account numbers (only works for formats with built-in checksums).
- Vendor master lookup catches ~90% for known vendors but requires maintained database.
- Source grounding is the strongest signal—if the value doesn't exist in the source text, it's hallucinated by definition.

**The Interviewer's Rubric:** Checking understanding that structural validity and semantic correctness are orthogonal properties. Strong candidates immediately identify source grounding as the definitive check — a value that doesn't appear in the OCR text is, by construction, hallucinated. Top candidates layer at least two additional independent checks (checksum validation + vendor master lookup) and explain that no single check achieves complete coverage — checksums only work for formats with built-in verification, vendor master lookup only works for known vendors — so defense depth across multiple independent signals is necessary to approach 99.9% accuracy on account number fields.

---

Q: How do you handle documents in 20 different languages?

**The Ideal Answer:** Multilingual OCR (PaddleOCR supports 80+ languages). Language detection at the OCR stage (or from document metadata). LLM extraction uses a multilingual model (or language-specific LoRA adapters on a multilingual base). JSON schema field names remain in English (canonical); extracted values retain original language. Date and number format normalization is locale-aware (e.g., "1.250,00" in German = "1,250.00" in US format). Monetary amounts always normalize to a canonical (amount, currency) tuple.

**Deep Dive & Trade-offs:**
- Multilingual base model (e.g., Qwen2 series): good across languages but slightly weaker per-language than specialized models.
- Per-language LoRA adapters: best accuracy but 20 adapters to maintain.
- Number format ambiguity: "1,250" could be 1250 (US) or 1.25 (EU). Must resolve using document language and currency context.

**The Interviewer's Rubric:** Checking awareness of locale-specific formatting challenges in financial data. Strong candidates immediately identify number format ambiguity (comma vs. period as decimal separator) as the most dangerous issue — silently misinterpreting "1,250" as 1.25 instead of 1250 introduces a 1000x error with no visible signal. Top candidates explain the resolution strategy: use the document's detected language and currency to select the locale, then apply locale-aware parsing. They also mention that when language detection is uncertain (e.g., a mixed-language document), the safest fallback is to route all monetary fields to human review rather than guess the locale and risk a catastrophic misparse.

---

Q: Your human review queue is growing faster than reviewers can process it. What do you do?

**The Ideal Answer:** Triage by business impact: prioritize documents by monetary amount × confidence gap (low confidence on a $500K invoice before high confidence on a $50 invoice). Reduce review scope: show reviewers only the flagged fields, not the entire document (reduces review time from 3 min to 30 sec). Active learning: use reviewer corrections to fine-tune the model weekly—each correction should reduce future review load. Adjust confidence thresholds: if the auto-accept threshold is too conservative, analyze the error rate in the 0.90-0.95 band—if errors are <0.1%, safely lower the review threshold to 0.90.

**Deep Dive & Trade-offs:**
- Lowering the review threshold increases auto-accept rate but increases undetected errors.
- Quantify: at 0.95 threshold, 85% auto-accept with 0.3% error rate. At 0.90, 92% auto-accept with 0.8% error rate. Business decides acceptable error rate.
- Long-term: model improvement should move the confidence distribution rightward, naturally reducing review volume.

**The Interviewer's Rubric:** Checking operational maturity thinking — the human-in-the-loop system is itself a system that needs optimization, not just a safety valve. Strong candidates identify triage by business impact (dollar value × confidence gap) as the highest-leverage action — it reduces queue depth while protecting the highest-risk extractions. Top candidates close the active learning loop: they explain that every reviewer correction is a training signal that should reduce future review load, and they quantify the flywheel — 500 corrections per week feeding weekly fine-tuning should reduce the review routing rate by 1-2 percentage points per cycle, eventually stabilizing at a lower steady-state review volume. Weak candidates propose only "hire more reviewers," which scales cost linearly without addressing the root cause.

---

Q: A competitor claims their end-to-end vision-language model (no OCR step) achieves 99% accuracy. Should you drop your OCR pipeline?

**The Ideal Answer:** Not yet—and probably never fully. End-to-end VLMs (e.g., GPT-4V, Qwen-VL) achieve strong results on clean documents but degrade on low-quality scans, complex tables, and dense multi-page documents. The OCR pipeline provides: (1) explicit bounding box provenance (required for audit compliance); (2) deterministic text extraction for digital PDFs (why run a vision model on a text document?); (3) modular error isolation (you can identify whether an error is OCR-stage or extraction-stage). Best approach: use VLM as a fallback for documents where layout-based extraction fails, and as a verification channel for high-value documents.

**Deep Dive & Trade-offs:**
- VLMs: simpler pipeline, fewer error propagation points, but opaque (no bounding box provenance without extra work).
- OCR pipeline: explicit provenance, modular debugging, but more moving parts.
- Hybrid wins: OCR pipeline for 90% of documents (reliable, auditable), VLM for the 10% that defeat layout analysis (complex or unusual formats).
- Cost: VLMs are 5-10x more expensive per document than OCR + 7B extraction model.

**The Interviewer's Rubric:** Checking ability to evaluate pipeline architecture trade-offs against end-to-end alternatives without dogma in either direction. Strong candidates recognize the competitor's claim at face value — 99% on a benchmark does not mean 99% in production on the full document quality distribution — and identify specific failure modes for VLMs (low-quality scans, complex tables, provenance gaps) rather than dismissing the approach outright. Top candidates articulate a concrete hybrid strategy with a routing decision rule (e.g., "use OCR pipeline by default; fall back to VLM when layout confidence is below 0.7 or when the document fails structural validation") and acknowledge the 5-10x cost difference, framing VLM usage as a targeted fallback for the 10% of documents where it adds value, not a wholesale replacement.

## Exercises

### Design Exercises

**Exercise 1 (Design):** A healthcare billing company wants to adapt this financial document extraction pipeline for medical claims (CMS-1500 forms and UB-04 hospital bills). These forms have rigid government-mandated layouts but contain highly sensitive PHI (Protected Health Information). Design the changes needed to the pipeline: which components can be reused unchanged, which require modification (and why), and what new components must be added to handle PHI handling requirements under HIPAA. Address specifically: how to prevent PHI from appearing in LLM training data derived from corrections, how to enforce data residency requirements, and how to produce the compliance audit trail required under HIPAA's Security Rule.

**Exercise 2 (Design):** The system currently processes documents synchronously within a 5-second SLO. A new client submits 500-page PDF prospectuses (SEC filings) that take 45 seconds to process with the current pipeline. They need extracted data within 2 minutes of submission. Design a new processing mode for long documents: specify the queue and worker architecture, how to parallelize processing across pages or sections, how to merge per-section extractions into a coherent final output, and how to handle the case where one page's processing fails mid-document. Draw the modified architecture diagram and identify which components from the existing design can be reused.

### Implementation Exercises

**Exercise 3 (Implementation):** Implement a `TableMerger` class that takes two `list[list[str]]` grids (representing the same logical table split across two pages) and merges them into a single grid. The merger must: (1) detect whether the second page's table is a continuation of the first by comparing column headers; (2) handle the case where the continuation page repeats the header row vs. continues without headers; (3) handle mismatched column counts (a continuation page may have fewer columns if some columns were empty and suppressed). Write unit tests covering at least three cases: clean continuation, header-repeated continuation, and mismatched column count.

**Exercise 4 (Implementation):** Implement a `VendorAnomalyDetector` that maintains a rolling 90-day history of invoice totals per vendor and flags statistical outliers. The detector should: (1) use a robust outlier detection method that handles the long-tailed distribution of invoice amounts (log-normal is a reasonable model); (2) return a normalized anomaly score (0-1) rather than a binary flag; (3) handle the cold-start case for vendors with fewer than 10 historical invoices; (4) expose a `calibrate(new_invoice_total)` method that updates the vendor's history. Write a test demonstrating that a $500K invoice from a vendor whose historical average is $5K is correctly flagged, while a $12K invoice from the same vendor is not.

### Debug Exercise

**Exercise 5 (Debug):** The following Python function is intended to compute the arithmetic validation score for an invoice, returning 1.0 if all checks pass and a value between 0 and 1 based on how many checks pass. Identify all bugs, explain why each is a bug (not just a style issue), and provide the corrected implementation.

```python
def arithmetic_validation_score(invoice: dict) -> float:
    checks_passed = 0
    total_checks = 0

    line_items = invoice.get("line_items", [])
    subtotal = invoice.get("subtotal")
    tax = invoice.get("tax_amount")
    total = invoice.get("total_amount")

    # Check 1: line item totals sum to subtotal
    if subtotal:
        total_checks += 1
        computed = sum(item["total"] for item in line_items)
        if computed == subtotal:
            checks_passed += 1

    # Check 2: subtotal + tax == total
    if tax and total:
        total_checks += 1
        if subtotal + tax == total:
            checks_passed += 1

    # Check 3: each line item total == quantity * unit_price
    for item in line_items:
        total_checks += 1
        if item["total"] == item["quantity"] * item["unit_price"]:
            checks_passed += 1

    return checks_passed / total_checks
```

**Expected findings:** The function contains at least four distinct bugs:

1. **`if subtotal:` falsy check on a numeric field** — a subtotal of `0.0` (a legitimate value for a zero-amount invoice) evaluates to `False`, silently skipping the check. The correct guard is `if subtotal is not None:`.
2. **Exact floating-point equality `computed == subtotal`** — floating-point arithmetic means `sum([1.10, 1.10, 1.10])` may equal `3.3000000000000003`, not `3.30`. The check must use `abs(computed - subtotal) <= tolerance` with a tolerance of 0.02 (2 cents) to account for rounding at the currency level.
3. **`if tax and total:` silently skips Check 2 when `subtotal` is `None`** — the expression `subtotal + tax` will raise `TypeError: unsupported operand type(s) for +: 'NoneType' and 'float'` if `subtotal` is not in the invoice, but only when `tax` and `total` are both present. The guard must also check `if subtotal is not None and tax is not None and total is not None:`.
4. **`ZeroDivisionError` when `total_checks == 0`** — if the invoice has no line items and neither `subtotal`, `tax`, nor `total` is present (e.g., a bare-minimum invoice with only `invoice_number` and `total_amount`), `total_checks` remains 0 and `checks_passed / total_checks` raises `ZeroDivisionError`. The function must return `1.0` (no checks applicable, no failures) when `total_checks == 0`.

---

## End of Chapter

- **Key takeaway:** Financial document extraction is an accuracy-critical pipeline where hallucination is a safety hazard. Multi-layer defense—source grounding, cross-field verification, constrained decoding, confidence routing—is non-negotiable. No single technique achieves 99.5%; the combination does.
- **What to practice:** Trace a single document through the full pipeline (ingestion → OCR → layout → LLM → validation → routing) and identify where each error type is caught.
- **Interview drill:** Given a hallucinated monetary amount, explain every layer of defense that should have caught it and why each layer alone is insufficient.

---

<!-- nav-footer -->
[[chapter-10|← Chapter 10]] | [[README|Contents]] | [[chapter-12|Chapter 12 →]]
