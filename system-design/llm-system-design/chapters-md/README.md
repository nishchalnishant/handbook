---
title: LLM System Design — Home
tags: [llm, system-design, index]
cssclass: llm-book-home
---

# LLM System Design: A Production-Focused Guide

This book is a practical, production-grade guide to designing LLM systems — covering both the foundations and the applied case studies that senior engineers and architects encounter in the real world. It is written for engineers preparing for LLM system design interviews at top-tier companies and for practitioners building or scaling production LLM systems who need a structured framework for making defensible architectural decisions.

## How to Use This Book

Every chapter follows the same **5-step framework**:

1. **Context** — problem statement, real-world motivating examples, and a Quick Reference box with scale, key techniques, and cross-references.
2. **Step 1: Understand the Problem and Establish Design Scope** — simulated interviewer dialogue, functional and non-functional requirements, and back-of-the-envelope estimation.
3. **Step 2: Propose High-Level Design and Get Buy-In** — core architecture components, pipeline descriptions, and a Mermaid architecture diagram.
4. **Step 3: Design Deep Dive** — focused deep dives on the two or three hardest sub-problems, with trade-off tables and production failure modes.
5. **Step 4: Wrap Up / Step 5: Interviewer Curveballs** — final design summary, wrap-around concerns, and a structured FAQ with ideal answers and interviewer rubrics.

This structure mirrors a real system design interview. Readers preparing for interviews can use the simulated dialogues and FAQ sections as drill material. Practitioners building systems can use the trade-off tables, estimation templates, and architecture diagrams as design checklists.

## Book Structure

### Part I: Foundations (Chapters 1–5)

The first five chapters establish the vocabulary, decision frameworks, and infrastructure components that every LLM system relies on. Read these in order before tackling Part II.

### Part II: Case Studies (Chapters 6–23)

Each chapter applies the Part I foundations to a specific production use case. Chapters are largely independent — readers can jump to whichever case study matches their current project or interview focus. The Quick Reference box at the top of each chapter lists relevant cross-references into Part I.

### Part III: Production Operations (Chapter 24)

This chapter consolidates lifecycle management across prompts, models, retrieval indexes, tools, evals, deployments, observability, and incident response.

### Part IV: Deep Foundations (Chapters 25–26)

These chapters go deeper on two foundations that recur across the case studies: production prompt engineering and model fine-tuning/adaptation. Read them when a case study's depth on prompting or fine-tuning is not enough for your target system.

### Part V: Advanced Operations (Chapters 27–31)

The final five chapters cover the operational concerns that turn a working prototype into a production service: evaluation at scale, cost optimization, observability and incident response, privacy and compliance, and edge/on-device deployment. Each is independent — read the ones that match your current constraints.

## Chapter List

### Part I: Foundations

- [[Chapter 1 - A Framework for LLM System Design Interviews|Chapter 1: A Framework for LLM System Design Interviews]] — A reusable 5-step interview response structure with estimation templates, trade-off tables, and production failure modes applicable to any LLM system design question.
- [[Chapter 2 - The LLM Stack and Core Patterns|Chapter 2: The LLM Stack and Core Patterns]] — Decision framework for choosing between prompt chaining, RAG, and agentic orchestration; covers intent routing, model tiering, and platform architecture.
- [[Chapter 3 - Data Pipelines and Vector Infrastructure|Chapter 3: Data Pipelines and Vector Infrastructure]] — End-to-end ingestion, chunking, embedding, and hybrid retrieval design with ACL enforcement, index lifecycle management, and recall optimization.
- [[Chapter 4 - Serving, Scaling, and Optimizing LLMs|Chapter 4: Serving, Scaling, and Optimizing LLMs]] — Multi-tier LLM serving infrastructure covering continuous batching, speculative decoding, KV/prefix caching, quantization, and autoscaling under latency SLOs.
- [[Chapter 5 - Evaluation, Guardrails, and Safety|Chapter 5: Evaluation, Guardrails, and Safety]] — Layered guardrail architecture with input/output classifiers, LLM-as-judge pipelines, red-teaming, and risk-tiered depth calibration.

### Part II: Case Studies

- [[Chapter 6 - Design a Customer Support Chatbot|Chapter 6: Design a Customer Support Chatbot]] — Multi-tier deflection and escalation pipeline with intent classification, RAG-grounded responses, and human handoff logic.
- [[Chapter 7 - Design an Enterprise Semantic Search Engine|Chapter 7: Design an Enterprise Semantic Search Engine]] — Hybrid BM25 + dense retrieval at enterprise scale with ACL-aware ranking, multi-tenant index management, and relevance evaluation.
- [[Chapter 8 - Design an AI Coding Assistant|Chapter 8: Design an AI Coding Assistant]] — Low-latency code completion and generation with context-aware retrieval, speculative decoding, and IDE integration constraints.
- [[Chapter 9 - Design an Autonomous Research Agent|Chapter 9: Design an Autonomous Research Agent]] — Multi-step agentic planning with tool use, memory management, loop detection, and bounded execution under cost and latency budgets.
- [[Chapter 10 - Design an Automated Content Generation Pipeline|Chapter 10: Design an Automated Content Generation Pipeline]] — Batch and streaming content generation with quality gates, brand safety guardrails, and human-in-the-loop review workflows.
- [[Chapter 11 - Design a Financial Document Extraction System|Chapter 11: Design a Financial Document Extraction System]] — High-accuracy structured extraction from financial filings with citation grounding, confidence scoring, and audit trail requirements.
- [[Chapter 12 - Design a Personalized E-commerce Shopping Assistant|Chapter 12: Design a Personalized E-commerce Shopping Assistant]] — Real-time personalization with catalog retrieval, user preference modeling, and recommendation safety under inventory constraints.
- [[Chapter 13 - Design an AI Tutor for Education|Chapter 13: Design an AI Tutor for Education]] — Adaptive instruction with knowledge state tracking, hint generation, and content safety controls appropriate for student populations.
- [[Chapter 14 - Design a Real-Time Meeting Summarizer|Chapter 14: Design a Real-Time Meeting Summarizer]] — Low-latency streaming transcription, incremental summarization, and action item extraction with speaker attribution.
- [[Chapter 15 - Design a Multimodal Asset Search System|Chapter 15: Design a Multimodal Asset Search System]] — Cross-modal retrieval over images, video, and text with joint embedding spaces, metadata filtering, and relevance ranking.
- [[Chapter 16 - Design an AI Data Analyst (Text-to-SQL and Insights)|Chapter 16: Design an AI Data Analyst (Text-to-SQL and Insights)]] — Natural language to SQL translation with schema-aware grounding, query validation, result interpretation, and hallucination guards.
- [[Chapter 17 - Design a Legal Contract Review System|Chapter 17: Design a Legal Contract Review System]] — Clause extraction, risk identification, and comparison against playbooks with high-precision requirements and audit-complete traceability.
- [[Chapter 18 - Design a Voice-First Real-Time Agent|Chapter 18: Design a Voice-First Real-Time Agent]] — End-to-end voice pipeline with ASR, LLM inference, and TTS under strict end-to-end latency budgets and interruption handling.
- [[Chapter 19 - Design an AI NPC Engine for Multiplayer Games|Chapter 19: Design an AI NPC Engine for Multiplayer Games]] — Real-time character dialogue generation with persona consistency, player context, content moderation, and high-concurrency serving.
- [[Chapter 20 - Design a Healthcare Triage and Diagnostic Assistant|Chapter 20: Design a Healthcare Triage and Diagnostic Assistant]] — Safety-first triage system with abstention logic, escalation protocols, regulatory compliance, and conservative guardrail calibration.
- [[Chapter 21 - Design an Advanced RAG Platform|Chapter 21: Design an Advanced RAG Platform]] — Production RAG architecture with query planning, hybrid retrieval, GraphRAG, reranking, context packing, grounding verification, and RAG observability.
- [[Chapter 22 - Design a Multi-Agent Workflow Orchestrator|Chapter 22: Design a Multi-Agent Workflow Orchestrator]] — Supervisor-worker and DAG-based multi-agent orchestration with typed state, tool budgets, approval gates, and trace replay.
- [[Chapter 23 - Design an MCP-Based Tool Integration Platform|Chapter 23: Design an MCP-Based Tool Integration Platform]] — Model Context Protocol platform design covering server registry, tools/resources/prompts, permissions, approval UX, and MCP security controls.

### Part III: Production Operations

- [[Chapter 24 - LLMOps and Production Lifecycle Management|Chapter 24: LLMOps and Production Lifecycle Management]] — Operational lifecycle for prompts, models, retrieval indexes, tools, eval gates, shadow deployments, monitoring, rollback, and governance.

### Part IV: Deep Foundations

- [[Chapter 25 - Prompt Engineering in Depth|Chapter 25: Prompt Engineering in Depth]] — Production-grade prompt pipeline design with dynamic few-shot selection, chain-of-thought, structured output framing, prompt versioning, A/B testing, and injection defense.
- [[Chapter 26 - Fine-Tuning and Adaptation|Chapter 26: Fine-Tuning and Adaptation]] — Decision framework for fine-tuning vs. RAG vs. prompting; LoRA/QLoRA mechanics, instruction dataset curation, DPO vs. RLHF vs. ORPO, adapter multiplexing, and continual learning.

### Part V: Advanced Operations

- [[Chapter 27 - Evaluation at Scale|Chapter 27: Evaluation at Scale]] — Automated eval pipeline with LLM-as-judge design, benchmark curation, regression detection, A/B testing, CI/CD integration, and multi-dimensional scoring.
- [[Chapter 28 - Cost Optimization as a Design Concern|Chapter 28: Cost Optimization as a Design Concern]] — Semantic caching, model routing/cascading, prompt compression, batching strategies, quantization economics, and GPU right-sizing for cost-per-quality targets.
- [[Chapter 29 - Observability and Incident Response for LLM Systems|Chapter 29: Observability and Incident Response for LLM Systems]] — Distributed tracing for LLM pipelines, SLO burn-rate alerting, prompt/response sampling, PII-safe logging, incident runbooks, and LLM-specific post-mortems.
- [[Chapter 30 - Privacy, Compliance, and Data Governance for LLM Systems|Chapter 30: Privacy, Compliance, and Data Governance]] — PII detection and de-identification, GDPR/HIPAA/CCPA requirements for LLM systems, ACL-aware retrieval, right to deletion, vendor DPAs, and audit logging.
- [[Chapter 31 - Edge and On-Device LLM Deployment|Chapter 31: Edge and On-Device LLM Deployment]] — Quantization for edge (GGUF INT4/INT8), inference runtime selection, hybrid edge-cloud routing, model update delivery, and battery/thermal constraint management.

## Recommended Reading Paths

### Path 1: Interview Prep (Quick Path)

For engineers with 1–2 weeks before an LLM system design interview. Read [[Chapter 1 - A Framework for LLM System Design Interviews|Chapter 1]]–[[Chapter 2 - The LLM Stack and Core Patterns|Chapter 2]] in full, skim [[Chapter 3 - Data Pipelines and Vector Infrastructure|Chapter 3]]–[[Chapter 5 - Evaluation, Guardrails, and Safety|Chapter 5]] for the trade-off tables and FAQ sections, then work through 2–3 case study chapters in areas relevant to the target company. Use the Step 5 curveball FAQs as active drill questions.

### Path 2: Building a RAG System

For practitioners designing or improving a retrieval-augmented generation system. Read [[Chapter 3 - Data Pipelines and Vector Infrastructure|Chapter 3]] (data pipelines and retrieval) in full, [[Chapter 21 - Design an Advanced RAG Platform|Chapter 21]] (advanced RAG platform) for the end-to-end production architecture, [[Chapter 2 - The LLM Stack and Core Patterns|Chapter 2]] (pattern selection) for routing context, [[Chapter 5 - Evaluation, Guardrails, and Safety|Chapter 5]] (evaluation) for recall and quality measurement, and [[Chapter 7 - Design an Enterprise Semantic Search Engine|Chapter 7]] (enterprise search) or [[Chapter 11 - Design a Financial Document Extraction System|Chapter 11]] (financial extraction) as domain-specific applied examples.

### Path 3: Production Deployment

For engineers operationalizing an LLM system at scale. Read [[Chapter 4 - Serving, Scaling, and Optimizing LLMs|Chapter 4]] (serving and optimization), [[Chapter 5 - Evaluation, Guardrails, and Safety|Chapter 5]] (guardrails and evaluation), and [[Chapter 24 - LLMOps and Production Lifecycle Management|Chapter 24]] (LLMOps lifecycle) in full, then [[Chapter 1 - A Framework for LLM System Design Interviews|Chapter 1]] for the cost-latency-safety trade-off framework. Follow with case studies matching your deployment context — [[Chapter 8 - Design an AI Coding Assistant|Chapter 8]] for coding tools, [[Chapter 18 - Design a Voice-First Real-Time Agent|Chapter 18]] for latency-critical voice, or [[Chapter 20 - Design a Healthcare Triage and Diagnostic Assistant|Chapter 20]] for high-stakes regulated domains.

### Path 4: Agents and Tool Integration

For engineers building tool-using assistants or agentic systems. Read [[Chapter 2 - The LLM Stack and Core Patterns|Chapter 2]] for core patterns, [[Chapter 9 - Design an Autonomous Research Agent|Chapter 9]] for a single autonomous research agent, [[Chapter 22 - Design a Multi-Agent Workflow Orchestrator|Chapter 22]] for multi-agent orchestration, [[Chapter 23 - Design an MCP-Based Tool Integration Platform|Chapter 23]] for MCP-based integration, and [[Chapter 5 - Evaluation, Guardrails, and Safety|Chapter 5]] for agent safety and guardrails.

### Path 5: Learning Guide (Deep Understanding)

For engineers who want to understand the *why* behind every architectural decision, not just what to say in an interview. Start with [[Chapter 25 - Prompt Engineering in Depth|Chapter 25]] (prompt engineering) and [[Chapter 26 - Fine-Tuning and Adaptation|Chapter 26]] (fine-tuning) as the adaptation layer, then [[Chapter 27 - Evaluation at Scale|Chapter 27]] (evaluation) to understand how to measure quality, [[Chapter 28 - Cost Optimization as a Design Concern|Chapter 28]] (cost optimization) to understand economic constraints, [[Chapter 29 - Observability and Incident Response for LLM Systems|Chapter 29]] (observability) for production operation, and [[Chapter 30 - Privacy, Compliance, and Data Governance for LLM Systems|Chapter 30]]–[[Chapter 31 - Edge and On-Device LLM Deployment|Chapter 31]] for compliance and edge deployment. The `> **Why:**` decision reasoning blocks throughout every chapter explain the reasoning behind each threshold, technology choice, and trade-off.

> **Picking case studies:** The paths above name representative case studies, but Chapters 6–23 are independent and chosen by domain. Match your target to the closest case study: conversational/support ([[Chapter 6 - Design a Customer Support Chatbot|6]], [[Chapter 13 - Design an AI Tutor for Education|13]]), search/retrieval ([[Chapter 7 - Design an Enterprise Semantic Search Engine|7]], [[Chapter 15 - Design a Multimodal Asset Search System|15]], [[Chapter 16 - Design an AI Data Analyst (Text-to-SQL and Insights)|16]], [[Chapter 17 - Design a Legal Contract Review System|17]]), content/generation ([[Chapter 10 - Design an Automated Content Generation Pipeline|10]], [[Chapter 12 - Design a Personalized E-commerce Shopping Assistant|12]]), real-time/latency-critical ([[Chapter 14 - Design a Real-Time Meeting Summarizer|14]], [[Chapter 18 - Design a Voice-First Real-Time Agent|18]], [[Chapter 19 - Design an AI NPC Engine for Multiplayer Games|19]]), or high-stakes/regulated ([[Chapter 11 - Design a Financial Document Extraction System|11]], [[Chapter 20 - Design a Healthcare Triage and Diagnostic Assistant|20]]).
