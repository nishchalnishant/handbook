---
title: "ML/DL/LLM Glossary"
tags: [llm, glossary, reference, ml, deep-learning]
---

# ML/DL/LLM Glossary (Detailed Reference)

Comprehensive A-Z glossary for machine learning, deep learning, and LLM systems.  
Each term is written for interview depth and production relevance.

---

## How to Read This Glossary

Each term uses this structure:
- **Definition**
- **Math / Formula**
- **How it works**
- **Why it matters**
- **Pitfalls**
- **Related**

---

## A

### Agentic Loop
- **Definition:** Repeated cycle where an LLM plans or reasons, takes an action, observes the result, and decides the next step.
- **Math / Formula:** Cost roughly grows with `steps * (model_cost + tool_cost + verification_cost)`.
- **How it works:** The system maintains state across iterations and stops when a goal, budget, or failure condition is reached.
- **Why it matters:** Core control pattern behind autonomous agents and multi-agent workflows.
- **Pitfalls:** Unbounded loops can create runaway cost, tool spam, and unsafe side effects.
- **Related:** [[glossary#Tool Use / Function Calling|Tool Use]], [[glossary#Multi-Agent Orchestration|Multi-Agent Orchestration]], Budget Controller, ReAct.

### Activation Function
- **Definition:** Non-linear transform applied to a neuron's pre-activation value.
- **Math / Formula:** Examples: `ReLU(x)=max(0,x)`, `GELU(x)=x*Phi(x)`.
- **How it works:** Adds non-linearity so stacked layers can represent complex functions beyond linear maps.
- **Why it matters:** Activation choice affects gradient flow, convergence speed, and final model quality.
- **Pitfalls:** Saturating functions (sigmoid/tanh) can cause vanishing gradients in deep networks.
- **Related:** [[glossary#Vanishing Gradient|Vanishing Gradient]], ReLU, BatchNorm, Residual Connections.

### Adam (Adaptive Moment Estimation)
- **Definition:** Optimizer that keeps exponential moving averages of gradients and squared gradients.
- **Math / Formula:** Parameter update scales learning rate by `m_t / (sqrt(v_t)+eps)` with bias correction.
- **How it works:** Combines momentum-like behavior with per-parameter adaptive step sizes.
- **Why it matters:** Strong default for many deep learning workloads, especially sparse/noisy gradients.
- **Pitfalls:** Can overfit or generalize worse than SGD+momentum in some fine-tuning regimes.
- **Related:** SGD, [[glossary#Learning Rate Schedule|Learning Rate Schedule]], [[glossary#Weight Decay|Weight Decay]], AdamW.

### Attention
- **Definition:** Mechanism that computes context-aware weighted combinations of token representations.
- **Math / Formula:** `Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V`.
- **How it works:** Query-key similarity determines weights over value vectors, producing dynamic context mixing.
- **Why it matters:** Core primitive behind Transformers and LLM quality.
- **Pitfalls:** Quadratic complexity in sequence length for standard self-attention.
- **Related:** [[glossary#Transformer|Transformer]], [[glossary#Multi-Head Attention|Multi-Head Attention]], [[glossary#KV Cache|KV Cache]], [[glossary#Context Window|Context Window]].

## B


### BM25 / Lexical Search
- **Definition:** A bag-of-words retrieval function that ranks documents based on term frequency and inverse document frequency.
- **Math / Formula:** Saturates term frequency impacts and penalizes overly long documents compared to raw TF-IDF.
- **How it works:** Matches exact keywords between the query and documents.
- **Why it matters:** Essential half of Hybrid Search. Dense embeddings miss exact IDs, product codes, and rare names that BM25 catches.
- **Pitfalls:** Cannot match synonyms or semantic intent (e.g., "laptop" vs "macbook").
- **Related:** [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], [[glossary#Reciprocal Rank Fusion (RRF)|Reciprocal Rank Fusion]], Sparse Retrieval.
## C

### Calibration
- **Definition:** Agreement between predicted probabilities and empirical outcome frequencies.
- **Math / Formula:** Expected Calibration Error (ECE) bins confidence and compares confidence vs accuracy.
- **How it works:** A well-calibrated model with 0.8 confidence should be correct about 80% of the time.
- **Why it matters:** Critical for risk-sensitive decisions and abstention thresholds.
- **Pitfalls:** High accuracy does not imply good calibration.
- **Related:** Brier Score, Temperature Scaling, Reliability Diagram.

### Context Window
- **Definition:** Maximum number of tokens a model can process at once (input plus sometimes output constraints by runtime).
- **Math / Formula:** Attention memory/time for vanilla attention scales roughly `O(n^2)` with sequence length `n`.
- **How it works:** Tokens beyond the limit are truncated, summarized, or moved to retrieval memory.
- **Why it matters:** Governs RAG chunking strategy, prompt packing, and latency/cost behavior.
- **Pitfalls:** Long context can degrade quality if relevant evidence is diluted.
- **Related:** [[glossary#Tokenization|Tokenization]], [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], [[glossary#Positional Encoding|Positional Encoding]], [[glossary#KV Cache|KV Cache]].

### Cross-Encoder Reranking
- **Definition:** Reranking retrieved candidates by scoring query-document pairs jointly in one model forward pass.
- **Math / Formula:** Score function `s(q,d)` learned via ranking/classification objective.
- **How it works:** Initial retriever returns top-K quickly; reranker reorders by deeper semantic matching.
- **Why it matters:** Strong quality boost for RAG answer grounding.
- **Pitfalls:** Computationally expensive; throughput bottleneck at high QPS.
- **Related:** Bi-Encoder [[glossary#Embedding|Embeddings]], Hybrid Retrieval, [[glossary#Recall|Recall@K]], MRR.

### Chain-of-Thought Prompting
- **Definition:** Prompting technique that instructs the model to produce explicit intermediate reasoning steps before the final answer.
- **Math / Formula:** No formula; realized through prompt templates like "Let's think step by step."
- **How it works:** Decomposing a problem into smaller steps improves multi-hop and arithmetic reasoning by making intermediate computations visible in the context window.
- **Why it matters:** Significantly improves accuracy on complex reasoning tasks; required technique for agentic planning and structured problem solving.
- **Pitfalls:** Verbose reasoning inflates token cost and latency; reasoning chains can be wrong while sounding confident.
- **Related:** [[glossary#In-Context Learning|In-Context Learning]], Agentic Orchestration, [[glossary#Structured Output / Constrained Decoding|Structured Output]], [[glossary#Zero-Shot / Few-Shot Prompting|Few-Shot Prompting]].

### Continuous Batching
- **Definition:** Serving strategy that continuously merges arriving decode requests into active batches.
- **Math / Formula:** Effective throughput improves by raising average GPU occupancy while keeping queue time bounded.
- **How it works:** Scheduler interleaves prefill/decode work and admits new requests without waiting for full batch boundaries.
- **Why it matters:** Major production optimization for LLM latency-throughput trade-offs.
- **Pitfalls:** Poor scheduler tuning can increase tail latency or starve long prompts.
- **Related:** [[glossary#KV Cache|KV Cache]], [[glossary#Throughput|Throughput]], Queueing, [[glossary#TTFT (Time To First Token)|TTFT]], [[glossary#TPOT (Time Per Output Token)|TPOT]].

---


### Chunking
- **Definition:** The process of splitting large documents into smaller text segments before embedding them for vector storage.
- **Math / Formula:** Controlled by `chunk_size` (e.g., 500 tokens) and `overlap` (e.g., 50 tokens).
- **How it works:** Documents are split at fixed token counts, sentence boundaries, or structural elements (paragraphs, markdown headers).
- **Why it matters:** LLMs have limited context windows and attention degrades on long inputs. Chunking ensures only relevant context is retrieved.
- **Pitfalls:** Arbitrary splitting can cut sentences in half or separate a question from its answer.
- **Related:** [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], [[glossary#Embedding|Embedding]], Document Parsing.

### Cosine Similarity
- **Definition:** A mathematical measure of similarity between two non-zero vectors based on the angle between them.
- **Math / Formula:** `cos(θ) = (A · B) / (||A|| ||B||)`
- **How it works:** Ranges from -1 (opposite) to 1 (identical). In embedding spaces, 1 means highly semantically similar.
- **Why it matters:** The primary distance metric used in vector databases to find the most relevant chunks for a user's query.
- **Pitfalls:** Requires vectors to be normalized. Not sensitive to vector magnitude, only direction.
- **Related:** [[glossary#Embedding|Embedding]], [[glossary#Vector Database / ANN Index|Vector Database]], Dot Product.
## D

### DPO (Direct Preference Optimization)
- **Definition:** Preference-learning objective for aligning LLM outputs to human/chosen preferences without full RL loop.
- **Math / Formula:** Optimizes preference probability between chosen vs rejected responses under a reference model.
- **How it works:** Uses pairwise preference data to directly shift policy toward preferred responses.
- **Why it matters:** Lower operational complexity than PPO-based RLHF for many alignment tasks.
- **Pitfalls:** Highly sensitive to preference data quality and diversity.
- **Related:** [[glossary#RLHF (Reinforcement Learning from Human Feedback)|RLHF]], [[glossary#SFT (Supervised Fine-Tuning)|SFT]], Reward Modeling, Alignment.

---

## E

### Embedding
- **Definition:** Dense vector representation of items (tokens, sentences, documents, users, products).
- **Math / Formula:** Similarity often measured via cosine `u·v/(||u|| ||v||)`.
- **How it works:** Learned so semantically related items are geometrically close in vector space.
- **Why it matters:** Foundation of retrieval, recommendation, clustering, and semantic search.
- **Pitfalls:** Embedding drift after model upgrades can break nearest-neighbor assumptions.
- **Related:** Vector Index, ANN Search, [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], Bi-Encoder.

## F

### Fine-tuning
- **Definition:** Continued training of a pretrained model on a target dataset/task.
- **Math / Formula:** Minimize task/alignment objective with small learning rate and often selective parameter updates.
- **How it works:** Reuses broad representations from pretraining and adapts to domain/task style.
- **Why it matters:** Faster and cheaper than full pretraining with strong downstream gains.
- **Pitfalls:** Catastrophic forgetting and overfitting with narrow or low-quality data.
- **Related:** Transfer Learning, [[glossary#LoRA (Low-Rank Adaptation)|LoRA]], [[glossary#SFT (Supervised Fine-Tuning)|SFT]], Domain Adaptation.

### Foundation Model
- **Definition:** Large pretrained model broadly reusable across tasks via prompting or adaptation.
- **Math / Formula:** Trained with self-supervised objectives over massive corpora.
- **How it works:** Learns general-purpose representations before specialization.
- **Why it matters:** Core platform primitive behind modern LLM products.
- **Pitfalls:** Hidden biases and capability gaps outside training distribution.
- **Related:** [[glossary#Pretraining|Pretraining]], [[glossary#Fine-tuning|Fine-tuning]], Prompting, Alignment.

### Flash Attention
- **Definition:** Memory-efficient attention algorithm that avoids materializing the full N×N attention matrix by tiling operations in SRAM.
- **Math / Formula:** Equivalent to standard `softmax(QK^T/sqrt(d_k))V` but computed in blocks to reduce HBM reads/writes.
- **How it works:** Tiles Q, K, V into SRAM blocks; computes attention incrementally without storing the full intermediate matrix.
- **Why it matters:** Reduces attention memory from O(N²) to O(N) for activations; enables longer contexts and higher throughput at the same VRAM budget.
- **Pitfalls:** Requires specialized CUDA kernels; compatibility depends on hardware and model architecture.
- **Related:** [[glossary#Attention|Attention]], [[glossary#Context Window|Context Window]], [[glossary#KV Cache|KV Cache]], [[glossary#Transformer|Transformer]].

---

## G

### GraphRAG
- **Definition:** Retrieval-augmented generation that uses an entity or knowledge graph alongside text/vector retrieval.
- **Math / Formula:** Often combines graph traversal scores with lexical/vector scores during candidate fusion.
- **How it works:** Extract entities and relationships from documents, retrieve graph neighborhoods, then pack supporting text evidence for generation.
- **Why it matters:** Improves multi-hop questions where answers depend on relationships across documents.
- **Pitfalls:** Poor entity resolution or stale graph edges can produce confident but wrong context.
- **Related:** [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], Entity Extraction, Hybrid Retrieval, Multi-Hop Retrieval.

## H

### Hallucination (LLM)
- **Definition:** Confident but unsupported or false model output.
- **Math / Formula:** Measured via unsupported-claim rate, factuality metrics, citation precision.
- **How it works:** Arises from weak grounding, distribution mismatch, or decoding behavior.
- **Why it matters:** Primary trust and safety failure mode in LLM applications.
- **Pitfalls:** Treating hallucination as purely model issue; often retrieval/prompt/orchestration failures.
- **Related:** [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], Groundedness, [[glossary#Safety Filter / Guardrails|Guardrails]], Verification.

## I

### In-Context Learning
- **Definition:** Model adapts behavior from prompt examples without weight updates.
- **Math / Formula:** No parameter update; behavior changes through conditioning on token sequence.
- **How it works:** Prompt demonstrations induce task pattern following during inference.
- **Why it matters:** Enables rapid iteration without retraining.
- **Pitfalls:** Prompt sensitivity and context-length limitations.
- **Related:** [[glossary#Zero-Shot / Few-Shot Prompting|Few-Shot Prompting]], [[glossary#Context Window|Context Window]], Prompt Engineering.

### Inference-Time Compute
- **Definition:** Compute budget spent at serving time (sampling params, reranking, self-consistency, tool calls).
- **Math / Formula:** Latency roughly `TTFT + output_tokens * TPOT + downstream_overheads`.
- **How it works:** Additional reasoning/verification can improve quality at higher cost and latency.
- **Why it matters:** Key lever for quality-latency-cost trade-offs.
- **Pitfalls:** Unbounded agent loops can blow SLO and budget.
- **Related:** [[glossary#TTFT (Time To First Token)|TTFT]], [[glossary#TPOT (Time Per Output Token)|TPOT]], Rate Limiting, Budget Policies.

---

## K

### KV Cache
- **Definition:** Cached key/value attention states from prior tokens used during autoregressive decoding.
- **Math / Formula:** Per-layer cache memory grows roughly with sequence length and hidden dimensions.
- **How it works:** Reuses prior attention states so each new token avoids recomputing full prefix.
- **Why it matters:** Major throughput and latency optimization for long generations.
- **Pitfalls:** Large contexts can exhaust GPU memory and reduce batch capacity.
- **Related:** [[glossary#Attention|Attention]], [[glossary#Continuous Batching|Continuous Batching]], [[glossary#Context Window|Context Window]], [[glossary#Quantization|Quantization]].

---

## L

### LLMOps
- **Definition:** Operational discipline for versioning, evaluating, deploying, monitoring, and rolling back LLM system artifacts.
- **Math / Formula:** No single formula; key metrics include quality, safety, latency, and cost by artifact version.
- **How it works:** Treats prompts, models, retrieval indexes, tools, policies, and inference configs as governed production artifacts.
- **Why it matters:** Prevents silent regressions and makes LLM behavior reproducible under audit.
- **Pitfalls:** Monitoring only model metrics while ignoring prompt, tool, and retrieval changes.
- **Related:** MLOps, [[glossary#Prompt Registry|Prompt Registry]], Eval Gates, [[glossary#Trace Replay|Trace Replay]], Model Registry.

### Latency (TTFT, TPOT, Tail)
- **Definition:** Response-time profile for generation systems.
- **Math / Formula:** `E2E ~= queue_wait + TTFT + output_tokens*TPOT + postproc`.
- **How it works:** TTFT captures first token delay; TPOT captures steady-state generation speed.
- **Why it matters:** User experience and SLOs depend heavily on p95/p99 tail latency.
- **Pitfalls:** Optimizing average latency while ignoring tail behavior under burst traffic.
- **Related:** [[glossary#Throughput|Throughput]], Rate Limiting, Batching, Autoscaling.

### LoRA (Low-Rank Adaptation)
- **Definition:** Parameter-efficient fine-tuning that learns low-rank update matrices on frozen base weights.
- **Math / Formula:** `W' = W + BA`, with low rank `r << d`.
- **How it works:** Trains small adapter parameters while keeping most model parameters fixed.
- **Why it matters:** Reduces VRAM, storage, and serving complexity for many domain adaptations.
- **Pitfalls:** Poor rank/target-module choices can bottleneck quality.
- **Related:** PEFT, [[glossary#Fine-tuning|Fine-tuning]], Adapters, Quantized Training.

---


### LLM-as-a-Judge
- **Definition:** An evaluation pattern where a strong LLM (like GPT-4) is prompted to grade the output of another model against a specific rubric.
- **Math / Formula:** Often calibrated against human raters using Cohen's Kappa score.
- **How it works:** The judge model evaluates faithfulness, relevance, or safety, returning a numeric score and reasoning.
- **Why it matters:** Traditional metrics like ROUGE/BLEU fail to capture semantic correctness in generative tasks.
- **Pitfalls:** Judge models suffer from position bias, verbosity bias, and drift (if the provider updates the model behind the API).
- **Related:** [[glossary#Evaluation at Scale|Evaluation]], [[glossary#RAG Evaluation|RAG Evaluation]], Ground Truth.
## M

### Multi-Agent Orchestration
- **Definition:** Coordination of multiple specialized agents through a shared workflow, state model, and control plane.
- **Math / Formula:** Workflow cost is approximately the sum of agent step costs, tool costs, verifier costs, and retry costs.
- **How it works:** A supervisor, DAG scheduler, or workflow engine assigns tasks, manages dependencies, validates outputs, and resolves conflicts.
- **Why it matters:** Enables complex work while keeping autonomy bounded and auditable.
- **Pitfalls:** Free-form agent chat without typed state leads to conflicts, loops, and hard-to-debug behavior.
- **Related:** [[glossary#Agentic Loop|Agentic Loop]], [[glossary#Tool Use / Function Calling|Tool Use]], Shared State, Human Approval.

### Multi-Head Attention
- **Definition:** Parallel attention heads learn different relational subspaces.
- **Math / Formula:** Concatenate head outputs then project: `MHA(Q,K,V)=Concat(head_i)W_O`.
- **How it works:** Multiple heads attend to different patterns (syntax, coreference, locality).
- **Why it matters:** Increases representational flexibility without serial depth increase.
- **Pitfalls:** Head redundancy can emerge; more heads do not guarantee better quality.
- **Related:** [[glossary#Attention|Attention]], [[glossary#Transformer|Transformer]], [[glossary#Positional Encoding|Positional Encoding]].

### Model Drift
- **Definition:** Declining production performance due to changing data/task conditions.
- **Math / Formula:** Tracked through rolling metrics, population stability, and distribution divergence.
- **How it works:** Drift appears gradually or abruptly as user behavior/content changes.
- **Why it matters:** Requires monitoring, retraining triggers, and safe rollback workflows.
- **Pitfalls:** Monitoring only one global metric misses important cohort failures.
- **Related:** [[glossary#Distribution Shift|Distribution Shift]], Monitoring, Shadow Evaluation.

### Model Context Protocol (MCP)
- **Definition:** Open protocol for connecting AI applications to external tools, resources, and prompt workflows through a host-client-server architecture.
- **Math / Formula:** No formula; it is an integration protocol and control-plane concern.
- **How it works:** An AI host creates MCP clients that connect to MCP servers exposing capabilities such as tools, resources, and prompts.
- **Why it matters:** Standardizes tool/data integration for agentic systems while allowing centralized governance.
- **Pitfalls:** MCP does not replace permissioning, approval UX, result sanitization, or audit logging.
- **Related:** [[glossary#Tool Use / Function Calling|Tool Use]], Resources, [[glossary#Prompt Registry|Prompt Registry]], [[glossary#Agentic Loop|Agentic Loop]], [[glossary#MCP Server|MCP Server]].

### MCP Server
- **Definition:** Service that exposes MCP capabilities such as tools, resources, and prompts to an AI host.
- **Math / Formula:** No formula; capacity planning uses tool-call QPS, timeout, and result-size budgets.
- **How it works:** The host connects through an MCP client, discovers capabilities, and invokes approved operations.
- **Why it matters:** Encapsulates integrations in reusable, discoverable components.
- **Pitfalls:** Unreviewed servers can introduce tool poisoning, data exfiltration, or prompt-injection risks.
- **Related:** [[glossary#Model Context Protocol (MCP)|Model Context Protocol]], Tool Gateway, Resources, OAuth.

### Mixture of Experts (MoE)
- **Definition:** Model architecture where each input token is routed to a sparse subset of "expert" feed-forward networks rather than a single dense FFN.
- **Math / Formula:** Router selects top-k experts: `output = sum_i gate_i * FFN_i(x)` where `gate_i` is sparse (typically k=1 or k=2 out of E experts).
- **How it works:** A learned router dispatches tokens to the most relevant experts; only a fraction of parameters activate per token.
- **Why it matters:** Scales model parameter count without proportional compute increase; models like Mixtral and GPT-4 use MoE for efficiency.
- **Pitfalls:** Load imbalance across experts; complex to serve efficiently; router collapse is a training failure mode.
- **Related:** [[glossary#Transformer|Transformer]], [[glossary#Quantization|Quantization]], [[glossary#Throughput|Throughput]], [[glossary#Fine-tuning|Fine-tuning]].

---


### Model Routing
- **Definition:** Dynamically dispatching user queries to different LLMs (e.g., small vs. large) based on query complexity or intent.
- **Math / Formula:** Routing threshold optimized for `Cost = %_small * C_small + %_large * C_large` while maintaining quality.
- **How it works:** A fast, cheap classifier (or rule engine) determines if a query is simple enough for a small model (e.g., Llama 3 8B) or requires a frontier model (e.g., GPT-4).
- **Why it matters:** Can reduce production inference costs by 5-20x without noticeable quality degradation on simple tasks.
- **Pitfalls:** If the router is slow, it negates the latency benefits of the smaller model.
- **Related:** Intent Classification, [[glossary#Cost Optimization as a Design Concern|Cost Optimization]], [[glossary#Throughput|Throughput]].
## N


### nDCG (Normalized Discounted Cumulative Gain)
- **Definition:** A metric for evaluating ranking quality that heavily penalizes highly relevant documents appearing lower in the search results.
- **Math / Formula:** `DCG = Σ (rel_i / log2(i + 1))`; nDCG is DCG divided by ideal DCG.
- **How it works:** Measures both presence and position of relevant documents in the top-K retrieved chunks.
- **Why it matters:** The gold standard metric for evaluating RAG retrieval pipelines.
- **Pitfalls:** Requires graded relevance judgments (0-3 scale) rather than simple binary (relevant/not relevant).
- **Related:** [[glossary#Recall|Recall@K]], MRR, [[glossary#Cross-Encoder Reranking|Cross-Encoder Reranking]].
## P

### Perplexity
- **Definition:** Exponential of average token-level negative log-likelihood in language modeling.
- **Math / Formula:** `PPL = exp( (1/N) * sum_t -log p(w_t|w_<t) )`.
- **How it works:** Measures how surprised a model is by true token sequence.
- **Why it matters:** Useful intrinsic metric for next-token prediction quality.
- **Pitfalls:** Poor proxy for task-specific usefulness and factual correctness.
- **Related:** [[glossary#Negative Log-Likelihood (NLL)|NLL]], Cross-Entropy, Task Evaluation.

### Prompt Registry
- **Definition:** Versioned store for prompt templates, variables, examples, owners, and deployment metadata.
- **Math / Formula:** No formula; each prompt version should map to quality, cost, latency, and safety metrics.
- **How it works:** Applications reference immutable prompt versions rather than editing live prompt strings directly.
- **Why it matters:** Makes prompt changes reviewable, testable, reversible, and auditable.
- **Pitfalls:** Treating prompts as informal config causes untraceable behavior changes.
- **Related:** [[glossary#LLMOps|LLMOps]], Eval Gates, [[glossary#Trace Replay|Trace Replay]], Prompt Engineering.

### Positional Encoding
- **Definition:** Mechanism that injects token order information into attention-based models.
- **Math / Formula:** Absolute sinusoidal or learned embeddings; relative/rotary variants.
- **How it works:** Distinguishes permutations of identical token sets by encoding position.
- **Why it matters:** Sequence order is critical for language understanding and generation.
- **Pitfalls:** Position extrapolation issues beyond training lengths.
- **Related:** [[glossary#Transformer|Transformer]], [[glossary#Context Window|Context Window]], RoPE.

### Precision
- **Definition:** Fraction of predicted positives that are true positives.
- **Math / Formula:** `TP / (TP + FP)`.
- **How it works:** Captures false-positive control.
- **Why it matters:** Important when false alarms are expensive.
- **Pitfalls:** Can look high while recall is poor.
- **Related:** [[glossary#Recall|Recall]], F1, PR Curve.

### Pretraining
- **Definition:** Large-scale self-supervised training stage before task-specific adaptation.
- **Math / Formula:** Language models optimize next-token or masked-token objectives at scale.
- **How it works:** Learns broad linguistic/world priors from massive corpora.
- **Why it matters:** Determines baseline capability ceiling for downstream adaptation.
- **Pitfalls:** Data contamination, licensing risk, and inherited biases.
- **Related:** [[glossary#Fine-tuning|Fine-tuning]], [[glossary#SFT (Supervised Fine-Tuning)|SFT]], [[glossary#Foundation Model|Foundation Model]].

### Prompt Injection
- **Definition:** Adversarial input that manipulates LLM instructions or tool behavior.
- **Math / Formula:** No canonical formula; mitigated through policy filters, instruction hierarchy, and tool constraints.
- **How it works:** Malicious tokens exploit model tendency to follow latest/local instructions.
- **Why it matters:** Critical security risk in agentic and tool-using systems.
- **Pitfalls:** Assuming system prompts alone provide complete protection.
- **Related:** [[glossary#Safety Filter / Guardrails|Guardrails]], Tool Sandboxing, Policy Enforcement.

---


### Prefix Caching
- **Definition:** Caching the KV states for long, static prompt prefixes (like system instructions or few-shot examples) so they aren't recomputed on every request.
- **Math / Formula:** Reduces Time To First Token (TTFT) by skipping the prefill computation for the cached prefix.
- **How it works:** The inference server (e.g., vLLM) recognizes shared prompt prefixes across different user requests and loads their KV matrices directly from GPU memory.
- **Why it matters:** Drastically reduces latency and compute cost for applications with massive system prompts.
- **Pitfalls:** Cache misses trigger full recomputation; requires a server that supports it natively.
- **Related:** [[glossary#KV Cache|KV Cache]], [[glossary#TTFT (Time To First Token)|TTFT]], [[glossary#Context Window|Context Window]].
## Q

### Quantization
- **Definition:** Representing model weights/activations with lower precision (for example INT8, INT4).
- **Math / Formula:** Map float ranges to discrete integer levels via scale and zero-point.
- **How it works:** Reduces memory bandwidth and storage; may improve inference throughput.
- **Why it matters:** Key for cost-efficient LLM serving under VRAM constraints.
- **Pitfalls:** Accuracy degradation if calibration/quantization scheme is poor.
- **Related:** [[glossary#KV Cache|KV Cache]], [[glossary#Throughput|Throughput]], Memory Bandwidth, QLoRA.

---

## R

### RAG (Retrieval-Augmented Generation)
- **Definition:** Pipeline that retrieves external evidence and conditions generation on it.
- **Math / Formula:** Typical objective combines retrieval quality and generation quality, not a single metric.
- **How it works:** Query rewrite -> retrieval -> reranking -> context packing -> generation -> citation/verification.
- **Why it matters:** Improves grounding, freshness, and domain specificity without full model retraining.
- **Pitfalls:** Low recall retrieval or poor chunking causes confident but unsupported answers.
- **Related:** [[glossary#Embedding|Embeddings]], Hybrid Search, [[glossary#Cross-Encoder Reranking|Cross-Encoder]], Groundedness.

### RAG Evaluation
- **Definition:** Measurement framework for retrieval, context quality, generation faithfulness, and citation correctness.
- **Math / Formula:** Common metrics include recall@K, MRR, NDCG, unsupported-claim rate, and citation accuracy.
- **How it works:** Evaluates each stage separately so wrong answers can be traced to ingestion, retrieval, packing, generation, or verification.
- **Why it matters:** End-to-end answer quality alone does not reveal which subsystem failed.
- **Pitfalls:** Measuring only final answer preference hides low recall and bad citations.
- **Related:** [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], Recall@K, LLM-as-Judge, Groundedness.

### Recall
- **Definition:** Fraction of true positives captured among all actual positives.
- **Math / Formula:** `TP / (TP + FN)`.
- **How it works:** Captures false-negative control.
- **Why it matters:** Vital when misses are costly.
- **Pitfalls:** High recall can come with unacceptable false-positive volume.
- **Related:** [[glossary#Precision|Precision]], F1, ROC/PR Curves.

### RLHF (Reinforcement Learning from Human Feedback)
- **Definition:** Alignment approach using human preference data and RL optimization.
- **Math / Formula:** Policy optimized against learned reward model with KL regularization to reference policy.
- **How it works:** Collect preferences -> train reward model -> optimize policy.
- **Why it matters:** Improves helpfulness/harmlessness relative to pure SFT in many settings.
- **Pitfalls:** Reward hacking and preference dataset bias.
- **Related:** [[glossary#DPO (Direct Preference Optimization)|DPO]], [[glossary#SFT (Supervised Fine-Tuning)|SFT]], Alignment, Reward Model.

---


### Reciprocal Rank Fusion (RRF)
- **Definition:** An algorithm to combine ranked lists from multiple search algorithms into a single unified ranking.
- **Math / Formula:** `RRF Score = Σ (1 / (k + rank_i))`, usually k=60.
- **How it works:** It takes the rank position from a dense retriever and a BM25 retriever, calculates a score, and sorts the combined list.
- **Why it matters:** The standard, parameter-free way to merge hybrid search results because it doesn't require normalizing vastly different scoring scales.
- **Pitfalls:** Can dilute strong signals from one retriever if the other brings in excessive noise.
- **Related:** [[glossary#BM25 / Lexical Search|BM25]], Hybrid Search, [[glossary#RAG (Retrieval-Augmented Generation)|RAG]].
## S

### Safety Filter / Guardrails
- **Definition:** Policy enforcement layers before and after model generation.
- **Math / Formula:** Typically classifier/rule ensembles with thresholding and action policies.
- **How it works:** Input moderation, tool-use constraints, output checks, and refusal/rewrite flows.
- **Why it matters:** Reduces policy violations and operational risk.
- **Pitfalls:** Over-blocking harms utility; under-blocking harms trust/compliance.
- **Related:** [[glossary#Prompt Injection|Prompt Injection]], Red Teaming, Policy Engine.

### Sampling Parameters
- **Definition:** Decoding controls such as temperature, top-k, top-p, repetition penalties.
- **Math / Formula:** Temperature rescales logits: `p_i = softmax(z_i / T)`.
- **How it works:** Shape randomness/diversity vs determinism in generated text.
- **Why it matters:** Large effect on creativity, factuality, and consistency.
- **Pitfalls:** Aggressive randomness increases hallucinations and unstable outputs.
- **Related:** Beam Search, Deterministic Decoding, [[glossary#Hallucination (LLM)|Hallucination]].

### SFT (Supervised Fine-Tuning)
- **Definition:** Fine-tuning on labeled prompt-response pairs to teach desired behavior.
- **Math / Formula:** Minimize token-level supervised loss on curated instruction data.
- **How it works:** Conditions base model toward task style and response format.
- **Why it matters:** Usually first alignment stage before preference optimization.
- **Pitfalls:** Narrow data causes over-specialization and brittle behavior.
- **Related:** [[glossary#Pretraining|Pretraining]], [[glossary#RLHF (Reinforcement Learning from Human Feedback)|RLHF]], [[glossary#DPO (Direct Preference Optimization)|DPO]], Instruction Tuning.

### Structured Output / Constrained Decoding
- **Definition:** Technique that restricts model token generation to comply with a predefined schema (JSON, regex, grammar, FSM).
- **Math / Formula:** At each decoding step, invalid token logits are masked to -inf before sampling, ensuring only schema-valid tokens are sampled.
- **How it works:** A grammar or schema is compiled into token-level masks applied during greedy/sampling decoding.
- **Why it matters:** Eliminates JSON parsing errors, format inconsistencies, and hallucinated field names in extraction pipelines.
- **Pitfalls:** Overly strict schemas can force incorrect completions; grammar compilation overhead at high QPS.
- **Related:** [[glossary#Hallucination (LLM)|Hallucination]], [[glossary#Safety Filter / Guardrails|Guardrails]], [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], [[glossary#Fine-tuning|Fine-tuning]], Constrained Generation.

### Speculative Decoding
- **Definition:** Inference acceleration where a small draft model proposes tokens and a larger model verifies them.
- **Math / Formula:** Speedup depends on acceptance rate and draft/target model throughput ratio.
- **How it works:** Accept verified token blocks; reject and backtrack when mismatch occurs.
- **Why it matters:** Can significantly improve latency without equivalent quality loss.
- **Pitfalls:** Low acceptance rates can erase benefits.
- **Related:** [[glossary#TTFT (Time To First Token)|TTFT]], [[glossary#TPOT (Time Per Output Token)|TPOT]], [[glossary#Continuous Batching|Continuous Batching]], Model Cascades.

---


### Semantic Caching
- **Definition:** Caching LLM responses based on the semantic similarity of the query, rather than an exact string match.
- **Math / Formula:** Cache hit if `cosine_similarity(query_emb, cached_emb) > threshold`.
- **How it works:** When a new query arrives, it is embedded. If it is highly similar to a previous query (e.g., "how do I reset password" vs "password reset instructions"), the cached response is served instantly.
- **Why it matters:** Reduces API costs by up to 40% for FAQ-like workloads and provides sub-100ms latency on hits.
- **Pitfalls:** Setting the threshold too low causes false hits (serving the wrong answer to a superficially similar question).
- **Related:** [[glossary#Cosine Similarity|Cosine Similarity]], [[glossary#Embedding|Embedding]], [[glossary#Cost Optimization as a Design Concern|Cost Optimization]].

### System Prompt
- **Definition:** The metaprompt or instruction set that defines the core persona, boundaries, and rules of engagement for an LLM application.
- **Math / Formula:** Often consumes 10-50% of the input token budget on small queries.
- **How it works:** Injected into the model's context as the highest-privilege instruction before the user's input.
- **Why it matters:** The primary defense mechanism against prompt injection and the main driver of application behavior.
- **Pitfalls:** Long system prompts dilute attention; contradictory instructions cause erratic behavior.
- **Related:** [[glossary#Prompt Injection|Prompt Injection]], [[glossary#Safety Filter / Guardrails|Guardrails]], [[glossary#Prefix Caching|Prefix Caching]].
## T

### Temperature
- **Definition:** Decoding parameter controlling entropy of token distribution.
- **Math / Formula:** Lower `T` sharpens distribution; higher `T` flattens it.
- **How it works:** Rescales logits before sampling.
- **Why it matters:** Directly affects output diversity and determinism.
- **Pitfalls:** High temperature can introduce incoherence in high-stakes tasks.
- **Related:** Top-p, Top-k, [[glossary#Sampling Parameters|Sampling Parameters]].

### Throughput
- **Definition:** Work completed per unit time (for example requests/sec or tokens/sec).
- **Math / Formula:** `Throughput = completed_work / time`.
- **How it works:** Influenced by batching, model size, hardware, sequence lengths, and queueing.
- **Why it matters:** Core capacity planning metric for SLA and cost.
- **Pitfalls:** Maximizing throughput can degrade per-request latency.
- **Related:** [[glossary#Latency (TTFT, TPOT, Tail)|Latency]], QPS, Autoscaling, Queueing.

### Tokenization
- **Definition:** Process of splitting text into model-recognized token units.
- **Math / Formula:** No universal formula; token count depends on tokenizer vocabulary and encoding scheme.
- **How it works:** Maps raw text to token IDs consumed by model embeddings.
- **Why it matters:** Drives context usage, latency, and billing in LLM APIs.
- **Pitfalls:** Different tokenizers produce materially different token counts and costs.
- **Related:** [[glossary#Context Window|Context Window]], Prompt Budgeting, BPE.

### Tool Use / Function Calling
- **Definition:** Model capability to emit structured calls to external tools (APIs, databases, code interpreters) as part of generation.
- **Math / Formula:** No formula; implemented via special tokens or JSON output schema that the runtime parses and dispatches.
- **How it works:** The model generates a structured tool invocation; the runtime executes it and feeds the result back as context for the next generation step.
- **Why it matters:** Enables agentic workflows: web search, code execution, database queries, and API orchestration without retrieval-only architectures.
- **Pitfalls:** Hallucinated tool names or arguments; unbounded tool call loops; sandbox escapes in code execution.
- **Related:** Agentic Orchestration, [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], [[glossary#Prompt Injection|Prompt Injection]], [[glossary#Structured Output / Constrained Decoding|Structured Output]], Sandboxing.

### Trace Replay
- **Definition:** Re-running historical requests or workflows using stored inputs, artifact versions, retrieved context, and tool outputs.
- **Math / Formula:** No formula; compare old vs new outputs with fixed or controlled context.
- **How it works:** Uses production traces to test prompt/model/index/policy changes before rollout or during incident analysis.
- **Why it matters:** Makes regressions reproducible and supports audit investigations.
- **Pitfalls:** Re-executing real side-effecting tools during replay unless tool outputs are mocked or frozen.
- **Related:** [[glossary#LLMOps|LLMOps]], Observability, Eval Gates, Incident Response.

### TPOT (Time Per Output Token)
- **Definition:** Average latency to generate each token after first token.
- **Math / Formula:** `TPOT ~= (generation_time_after_first_token) / output_tokens`.
- **How it works:** Reflects steady-state decode efficiency.
- **Why it matters:** Strong predictor of perceived streaming speed.
- **Pitfalls:** Ignoring TPOT while optimizing only TTFT yields poor long-answer UX.
- **Related:** [[glossary#TTFT (Time To First Token)|TTFT]], [[glossary#Latency (TTFT, TPOT, Tail)|Latency]], [[glossary#Throughput|Throughput]].

### TTFT (Time To First Token)
- **Definition:** Latency from request acceptance to first generated token.
- **Math / Formula:** Includes queueing, preprocessing, retrieval/tool setup, and first decode step.
- **How it works:** Captures startup overhead before user sees model response.
- **Why it matters:** Primary driver of perceived responsiveness.
- **Pitfalls:** Hidden queue time can dominate TTFT under burst load.
- **Related:** [[glossary#TPOT (Time Per Output Token)|TPOT]], Queueing, Batching, Autoscaling.

### Transformer
- **Definition:** Neural architecture built around attention, feed-forward blocks, residual paths, and normalization.
- **Math / Formula:** Stacked blocks: `x <- x + Attention(LN(x))`, `x <- x + MLP(LN(x))`.
- **How it works:** Self-attention mixes token context globally; MLP layers transform features per position.
- **Why it matters:** Foundation of modern LLMs and many state-of-the-art sequence models.
- **Pitfalls:** Quadratic attention costs and memory pressure at long context lengths.
- **Related:** [[glossary#Attention|Attention]], [[glossary#Multi-Head Attention|Multi-Head Attention]], [[glossary#Positional Encoding|Positional Encoding]], [[glossary#KV Cache|KV Cache]].

---

## V

### Vector Database / ANN Index
- **Definition:** System optimized for approximate nearest-neighbor search over embedding vectors.
- **Math / Formula:** Similarity via cosine/dot/L2; ANN trades exactness for speed and scale.
- **How it works:** Index structures (HNSW, IVF-PQ, etc.) accelerate top-k vector retrieval.
- **Why it matters:** Backbone of semantic retrieval and RAG at production scale.
- **Pitfalls:** Stale embeddings and poor filtering/ACL integration degrade relevance and safety.
- **Related:** Embeddings, Hybrid Search, [[glossary#RAG (Retrieval-Augmented Generation)|RAG]], Index Refresh.

### Vanishing Gradient
- **Definition:** Gradients shrink as they backpropagate through many layers/time steps.
- **Math / Formula:** Repeated multiplication by derivatives with magnitude < 1 drives gradients toward 0.
- **How it works:** Early layers receive weak learning signal.
- **Why it matters:** Slows or stalls training in deep/recurrent networks.
- **Pitfalls:** Often masked until late when optimization appears stuck.
- **Related:** Residual Connections, Normalization, Activation Choice.

---

## Z

### Zero-Shot / Few-Shot Prompting
- **Definition:** Solving tasks with zero or a few demonstrations in the prompt.
- **Math / Formula:** No weight update; relies on in-context conditioning.
- **How it works:** Task instructions and exemplars steer output behavior.
- **Why it matters:** Fastest way to ship prototypes and baseline capabilities.
- **Pitfalls:** Brittle formatting and instruction ambiguity can cause high variance outputs.
- **Related:** [[glossary#In-Context Learning|In-Context Learning]], Prompt Engineering, Instruction Following.

---

## Interview High-Yield Terms (Must Know)

1. Bias-Variance Trade-off  
2. Precision vs Recall vs F1  
3. Cross-Validation and Data Leakage  
4. Regularization (L1/L2, Dropout, Weight Decay, Early Stopping)  
5. Transformer, Attention, Context Window  
6. TTFT, TPOT, Throughput, Tail Latency  
7. Tokenization and Prompt Budgeting  
8. RAG (retrieval, reranking, grounding, evaluation)
9. Hallucination, Guardrails, and Agent/MCP Security
10. KV Cache, Quantization, Continuous/Server-Side Batching
11. Agentic Loops and Multi-Agent Orchestration
12. MCP, Tool Use, Prompt Registry, and Trace Replay

## Quick Self-Check for Interviews

- Can you define each term in one sentence?
- Can you write the core formula when applicable?
- Can you explain one production failure mode?
- Can you compare it with one adjacent concept?
- Can you state one practical mitigation or tuning lever?
