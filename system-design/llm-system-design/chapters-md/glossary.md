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

### Accuracy
- **Definition:** Fraction of predictions that are correct over all predictions.
- **Math / Formula:** `(TP + TN) / (TP + TN + FP + FN)`.
- **How it works:** Compares predicted labels against ground truth and counts exact matches.
- **Why it matters:** Useful as a quick baseline when classes are balanced and misclassification costs are symmetric.
- **Pitfalls:** Can be dangerously misleading on imbalanced datasets (for example, 99% negative class).
- **Related:** Precision, Recall, F1, PR-AUC, Confusion Matrix.

### Activation Function
- **Definition:** Non-linear transform applied to a neuron's pre-activation value.
- **Math / Formula:** Examples: `ReLU(x)=max(0,x)`, `GELU(x)=x*Phi(x)`.
- **How it works:** Adds non-linearity so stacked layers can represent complex functions beyond linear maps.
- **Why it matters:** Activation choice affects gradient flow, convergence speed, and final model quality.
- **Pitfalls:** Saturating functions (sigmoid/tanh) can cause vanishing gradients in deep networks.
- **Related:** Vanishing Gradient, ReLU, BatchNorm, Residual Connections.

### Adam (Adaptive Moment Estimation)
- **Definition:** Optimizer that keeps exponential moving averages of gradients and squared gradients.
- **Math / Formula:** Parameter update scales learning rate by `m_t / (sqrt(v_t)+eps)` with bias correction.
- **How it works:** Combines momentum-like behavior with per-parameter adaptive step sizes.
- **Why it matters:** Strong default for many deep learning workloads, especially sparse/noisy gradients.
- **Pitfalls:** Can overfit or generalize worse than SGD+momentum in some fine-tuning regimes.
- **Related:** SGD, Learning Rate Schedule, Weight Decay, AdamW.

### Attention
- **Definition:** Mechanism that computes context-aware weighted combinations of token representations.
- **Math / Formula:** `Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V`.
- **How it works:** Query-key similarity determines weights over value vectors, producing dynamic context mixing.
- **Why it matters:** Core primitive behind Transformers and LLM quality.
- **Pitfalls:** Quadratic complexity in sequence length for standard self-attention.
- **Related:** Transformer, Multi-Head Attention, KV Cache, Context Window.

### AUC (ROC-AUC)
- **Definition:** Area under ROC curve (TPR vs FPR across thresholds).
- **Math / Formula:** Probability that a random positive is ranked above a random negative.
- **How it works:** Threshold-independent ranking metric for binary classifiers.
- **Why it matters:** Useful when class threshold is undecided and ranking quality is primary.
- **Pitfalls:** Overly optimistic under heavy class imbalance compared with PR-AUC.
- **Related:** ROC, PR-AUC, Precision, Recall.

---

## B

### Backpropagation
- **Definition:** Algorithm to compute gradients of loss with respect to model parameters via chain rule.
- **Math / Formula:** For each layer, `dL/dW = dL/dz * dz/dW`.
- **How it works:** Forward pass computes activations and loss; backward pass propagates gradients layer-by-layer.
- **Why it matters:** Makes training deep networks computationally tractable.
- **Pitfalls:** Gradient explosion/vanishing without careful architecture and normalization choices.
- **Related:** Gradient Descent, Autodiff, Vanishing Gradient, Gradient Clipping.

### Batch Normalization
- **Definition:** Normalizes intermediate activations within mini-batches during training.
- **Math / Formula:** `x_hat=(x-mu_batch)/sqrt(var_batch+eps)`, then affine transform with learnable `gamma, beta`.
- **How it works:** Reduces internal covariate shift and stabilizes optimization.
- **Why it matters:** Enables higher learning rates and faster convergence in many CNN/MLP settings.
- **Pitfalls:** Train/inference mismatch and weaker behavior with very small batch sizes.
- **Related:** LayerNorm, Residual Networks, Learning Rate Warmup.

### Bias-Variance Trade-off
- **Definition:** Decomposition intuition of prediction error into underfitting vs overfitting effects.
- **Math / Formula:** `Expected Error = Bias^2 + Variance + Irreducible Noise`.
- **How it works:** Simpler models reduce variance but increase bias; complex models do the opposite.
- **Why it matters:** Guides model capacity, regularization strength, and dataset size decisions.
- **Pitfalls:** Treated as a slogan rather than measured with proper validation strategy.
- **Related:** Regularization, Cross-Validation, Overfitting, Underfitting.

---

## C

### Calibration
- **Definition:** Agreement between predicted probabilities and empirical outcome frequencies.
- **Math / Formula:** Expected Calibration Error (ECE) bins confidence and compares confidence vs accuracy.
- **How it works:** A well-calibrated model with 0.8 confidence should be correct about 80% of the time.
- **Why it matters:** Critical for risk-sensitive decisions and abstention thresholds.
- **Pitfalls:** High accuracy does not imply good calibration.
- **Related:** Brier Score, Temperature Scaling, Reliability Diagram.

### Categorical Cross-Entropy
- **Definition:** Standard loss for multi-class classification.
- **Math / Formula:** `L = -sum_i y_i * log(p_i)`.
- **How it works:** Penalizes low predicted probability assigned to true class.
- **Why it matters:** Optimizes probabilistic discrimination and pairs naturally with softmax outputs.
- **Pitfalls:** Sensitive to mislabeled data; can encourage overconfident outputs.
- **Related:** Softmax, Label Smoothing, NLL.

### Context Window
- **Definition:** Maximum number of tokens a model can process at once (input plus sometimes output constraints by runtime).
- **Math / Formula:** Attention memory/time for vanilla attention scales roughly `O(n^2)` with sequence length `n`.
- **How it works:** Tokens beyond the limit are truncated, summarized, or moved to retrieval memory.
- **Why it matters:** Governs RAG chunking strategy, prompt packing, and latency/cost behavior.
- **Pitfalls:** Long context can degrade quality if relevant evidence is diluted.
- **Related:** Tokenization, RAG, Positional Encoding, KV Cache.

### Cross-Validation
- **Definition:** Resampling method to estimate model generalization using repeated train/validation splits.
- **Math / Formula:** K-fold average metric across `k` held-out folds.
- **How it works:** Rotate validation fold; train `k` models; aggregate mean and variance.
- **Why it matters:** More robust estimate than a single split for limited data.
- **Pitfalls:** Leakage if preprocessing is fit on full data instead of per-fold training data.
- **Related:** Data Leakage, Stratification, Hyperparameter Tuning.

### Cross-Encoder Reranking
- **Definition:** Reranking retrieved candidates by scoring query-document pairs jointly in one model forward pass.
- **Math / Formula:** Score function `s(q,d)` learned via ranking/classification objective.
- **How it works:** Initial retriever returns top-K quickly; reranker reorders by deeper semantic matching.
- **Why it matters:** Strong quality boost for RAG answer grounding.
- **Pitfalls:** Computationally expensive; throughput bottleneck at high QPS.
- **Related:** Bi-Encoder Embeddings, Hybrid Retrieval, Recall@K, MRR.

### Chain-of-Thought Prompting
- **Definition:** Prompting technique that instructs the model to produce explicit intermediate reasoning steps before the final answer.
- **Math / Formula:** No formula; realized through prompt templates like "Let's think step by step."
- **How it works:** Decomposing a problem into smaller steps improves multi-hop and arithmetic reasoning by making intermediate computations visible in the context window.
- **Why it matters:** Significantly improves accuracy on complex reasoning tasks; required technique for agentic planning and structured problem solving.
- **Pitfalls:** Verbose reasoning inflates token cost and latency; reasoning chains can be wrong while sounding confident.
- **Related:** In-Context Learning, Agentic Orchestration, Structured Output, Few-Shot Prompting.

### Continuous Batching
- **Definition:** Serving strategy that continuously merges arriving decode requests into active batches.
- **Math / Formula:** Effective throughput improves by raising average GPU occupancy while keeping queue time bounded.
- **How it works:** Scheduler interleaves prefill/decode work and admits new requests without waiting for full batch boundaries.
- **Why it matters:** Major production optimization for LLM latency-throughput trade-offs.
- **Pitfalls:** Poor scheduler tuning can increase tail latency or starve long prompts.
- **Related:** KV Cache, Throughput, Queueing, TTFT, TPOT.

---

## D

### Data Leakage
- **Definition:** Train-time access to information unavailable at inference time.
- **Math / Formula:** No single formula; detected via suspiciously high validation metrics that collapse in production.
- **How it works:** Common sources include target leakage, temporal leakage, and split contamination.
- **Why it matters:** Produces brittle models and false confidence.
- **Pitfalls:** Leakage hidden in feature engineering or preprocessing pipelines.
- **Related:** Cross-Validation, Time-Series Split, Feature Store.

### Distribution Shift
- **Definition:** Difference between training data distribution and real-world serving distribution.
- **Math / Formula:** Conceptualized as `P_train(X,Y) != P_prod(X,Y)`.
- **How it works:** Can be covariate shift, label shift, concept drift, or abrupt regime change.
- **Why it matters:** Main cause of silent performance decay after deployment.
- **Pitfalls:** Monitoring only aggregate accuracy misses segment-level drift.
- **Related:** Drift Detection, Monitoring, Retraining Strategy.

### Dropout
- **Definition:** Regularization that randomly masks activations during training.
- **Math / Formula:** `h' = m * h`, where `m ~ Bernoulli(1-p)` and activations are scaled accordingly.
- **How it works:** Prevents co-adaptation and encourages redundant robust feature learning.
- **Why it matters:** Helps generalization in over-parameterized networks.
- **Pitfalls:** Excessive dropout can underfit; interacts with normalization and architecture choices.
- **Related:** Regularization, Early Stopping, Weight Decay.

### DPO (Direct Preference Optimization)
- **Definition:** Preference-learning objective for aligning LLM outputs to human/chosen preferences without full RL loop.
- **Math / Formula:** Optimizes preference probability between chosen vs rejected responses under a reference model.
- **How it works:** Uses pairwise preference data to directly shift policy toward preferred responses.
- **Why it matters:** Lower operational complexity than PPO-based RLHF for many alignment tasks.
- **Pitfalls:** Highly sensitive to preference data quality and diversity.
- **Related:** RLHF, SFT, Reward Modeling, Alignment.

---

## E

### Early Stopping
- **Definition:** Stop training when validation metric fails to improve after a patience window.
- **Math / Formula:** Trigger when `best_metric` unchanged for `patience` epochs.
- **How it works:** Prevents overfitting by halting before memorization dominates.
- **Why it matters:** Cheap and effective regularizer in practical pipelines.
- **Pitfalls:** Noisy validation metrics can trigger premature stopping without smoothing.
- **Related:** Regularization, Checkpointing, Learning Curves.

### Embedding
- **Definition:** Dense vector representation of items (tokens, sentences, documents, users, products).
- **Math / Formula:** Similarity often measured via cosine `u·v/(||u|| ||v||)`.
- **How it works:** Learned so semantically related items are geometrically close in vector space.
- **Why it matters:** Foundation of retrieval, recommendation, clustering, and semantic search.
- **Pitfalls:** Embedding drift after model upgrades can break nearest-neighbor assumptions.
- **Related:** Vector Index, ANN Search, RAG, Bi-Encoder.

### Epoch
- **Definition:** One full pass through the training dataset.
- **Math / Formula:** Steps per epoch roughly `ceil(num_samples / batch_size)`.
- **How it works:** Multiple epochs iteratively update parameters until convergence or stopping criteria.
- **Why it matters:** Helps reason about optimization progress and compute budget.
- **Pitfalls:** More epochs are not always better; can overfit if validation degrades.
- **Related:** Batch Size, Iteration, Early Stopping.

---

## F

### F1 Score
- **Definition:** Harmonic mean of precision and recall.
- **Math / Formula:** `F1 = 2PR/(P+R)`.
- **How it works:** Penalizes extreme imbalance between precision and recall.
- **Why it matters:** Better summary metric than accuracy under class imbalance.
- **Pitfalls:** Hides calibration quality and business-specific error asymmetry.
- **Related:** Precision, Recall, PR-AUC.

### Feature Engineering
- **Definition:** Transforming raw data into informative model inputs.
- **Math / Formula:** Includes interactions, log transforms, aggregations, temporal windows.
- **How it works:** Encodes domain structure and signal into model-friendly features.
- **Why it matters:** Still decisive in classical ML and tabular systems.
- **Pitfalls:** Leakage through future information or post-outcome fields.
- **Related:** Data Leakage, Feature Store, Model Explainability.

### Fine-tuning
- **Definition:** Continued training of a pretrained model on a target dataset/task.
- **Math / Formula:** Minimize task/alignment objective with small learning rate and often selective parameter updates.
- **How it works:** Reuses broad representations from pretraining and adapts to domain/task style.
- **Why it matters:** Faster and cheaper than full pretraining with strong downstream gains.
- **Pitfalls:** Catastrophic forgetting and overfitting with narrow or low-quality data.
- **Related:** Transfer Learning, LoRA, SFT, Domain Adaptation.

### Foundation Model
- **Definition:** Large pretrained model broadly reusable across tasks via prompting or adaptation.
- **Math / Formula:** Trained with self-supervised objectives over massive corpora.
- **How it works:** Learns general-purpose representations before specialization.
- **Why it matters:** Core platform primitive behind modern LLM products.
- **Pitfalls:** Hidden biases and capability gaps outside training distribution.
- **Related:** Pretraining, Fine-tuning, Prompting, Alignment.

### Flash Attention
- **Definition:** Memory-efficient attention algorithm that avoids materializing the full N×N attention matrix by tiling operations in SRAM.
- **Math / Formula:** Equivalent to standard `softmax(QK^T/sqrt(d_k))V` but computed in blocks to reduce HBM reads/writes.
- **How it works:** Tiles Q, K, V into SRAM blocks; computes attention incrementally without storing the full intermediate matrix.
- **Why it matters:** Reduces attention memory from O(N²) to O(N) for activations; enables longer contexts and higher throughput at the same VRAM budget.
- **Pitfalls:** Requires specialized CUDA kernels; compatibility depends on hardware and model architecture.
- **Related:** Attention, Context Window, KV Cache, Transformer.

---

## G

### Generalization
- **Definition:** Ability to perform well on unseen data from target distribution.
- **Math / Formula:** Generalization gap = train metric - validation/test metric.
- **How it works:** Emerges from fit quality, regularization, data coverage, and optimization dynamics.
- **Why it matters:** Production value comes from generalization, not memorized training performance.
- **Pitfalls:** Benchmark overfitting via repeated evaluation on same test sets.
- **Related:** Cross-Validation, Overfitting, Distribution Shift.

### Gradient Clipping
- **Definition:** Restricts gradient magnitude to improve numerical stability.
- **Math / Formula:** Commonly clip global norm: `g <- g * min(1, c/||g||)`.
- **How it works:** Prevents rare large updates from destabilizing training.
- **Why it matters:** Especially useful in long-sequence models and recurrent architectures.
- **Pitfalls:** Over-clipping slows convergence and can mask poor hyperparameters.
- **Related:** Learning Rate, Exploding Gradient, Optimizer Stability.

---

## H

### Hallucination (LLM)
- **Definition:** Confident but unsupported or false model output.
- **Math / Formula:** Measured via unsupported-claim rate, factuality metrics, citation precision.
- **How it works:** Arises from weak grounding, distribution mismatch, or decoding behavior.
- **Why it matters:** Primary trust and safety failure mode in LLM applications.
- **Pitfalls:** Treating hallucination as purely model issue; often retrieval/prompt/orchestration failures.
- **Related:** RAG, Groundedness, Guardrails, Verification.

### Hyperparameter
- **Definition:** Configuration value set before training (not directly learned).
- **Math / Formula:** Examples: learning rate, weight decay, depth, batch size, dropout.
- **How it works:** Controls optimization behavior, model capacity, and regularization.
- **Why it matters:** Often dominates final performance.
- **Pitfalls:** Tuning on test set leaks information and inflates reported metrics.
- **Related:** Cross-Validation, Bayesian Optimization, Reproducibility.

---

## I

### In-Context Learning
- **Definition:** Model adapts behavior from prompt examples without weight updates.
- **Math / Formula:** No parameter update; behavior changes through conditioning on token sequence.
- **How it works:** Prompt demonstrations induce task pattern following during inference.
- **Why it matters:** Enables rapid iteration without retraining.
- **Pitfalls:** Prompt sensitivity and context-length limitations.
- **Related:** Few-Shot Prompting, Context Window, Prompt Engineering.

### Inference-Time Compute
- **Definition:** Compute budget spent at serving time (sampling params, reranking, self-consistency, tool calls).
- **Math / Formula:** Latency roughly `TTFT + output_tokens * TPOT + downstream_overheads`.
- **How it works:** Additional reasoning/verification can improve quality at higher cost and latency.
- **Why it matters:** Key lever for quality-latency-cost trade-offs.
- **Pitfalls:** Unbounded agent loops can blow SLO and budget.
- **Related:** TTFT, TPOT, Rate Limiting, Budget Policies.

---

## K

### KV Cache
- **Definition:** Cached key/value attention states from prior tokens used during autoregressive decoding.
- **Math / Formula:** Per-layer cache memory grows roughly with sequence length and hidden dimensions.
- **How it works:** Reuses prior attention states so each new token avoids recomputing full prefix.
- **Why it matters:** Major throughput and latency optimization for long generations.
- **Pitfalls:** Large contexts can exhaust GPU memory and reduce batch capacity.
- **Related:** Attention, Continuous Batching, Context Window, Quantization.

---

## L

### Label Smoothing
- **Definition:** Replaces hard one-hot labels with softened targets.
- **Math / Formula:** `y_smooth = (1-eps)*y + eps/K`.
- **How it works:** Prevents overconfident logits and improves calibration/generalization.
- **Why it matters:** Useful stabilization trick in classification and seq2seq training.
- **Pitfalls:** Too much smoothing can hurt separability and confidence where needed.
- **Related:** Cross-Entropy, Calibration, Overconfidence.

### Latency (TTFT, TPOT, Tail)
- **Definition:** Response-time profile for generation systems.
- **Math / Formula:** `E2E ~= queue_wait + TTFT + output_tokens*TPOT + postproc`.
- **How it works:** TTFT captures first token delay; TPOT captures steady-state generation speed.
- **Why it matters:** User experience and SLOs depend heavily on p95/p99 tail latency.
- **Pitfalls:** Optimizing average latency while ignoring tail behavior under burst traffic.
- **Related:** Throughput, Rate Limiting, Batching, Autoscaling.

### Learning Rate Schedule
- **Definition:** Time-varying policy for optimizer step size.
- **Math / Formula:** Common patterns: warmup + cosine decay, linear decay, step decay.
- **How it works:** Larger early steps accelerate progress; smaller late steps refine minima.
- **Why it matters:** Strongly influences convergence and final quality.
- **Pitfalls:** No warmup in large models can cause unstable early training.
- **Related:** AdamW, SGD, Gradient Noise Scale.

### LoRA (Low-Rank Adaptation)
- **Definition:** Parameter-efficient fine-tuning that learns low-rank update matrices on frozen base weights.
- **Math / Formula:** `W' = W + BA`, with low rank `r << d`.
- **How it works:** Trains small adapter parameters while keeping most model parameters fixed.
- **Why it matters:** Reduces VRAM, storage, and serving complexity for many domain adaptations.
- **Pitfalls:** Poor rank/target-module choices can bottleneck quality.
- **Related:** PEFT, Fine-tuning, Adapters, Quantized Training.

---

## M

### Multi-Head Attention
- **Definition:** Parallel attention heads learn different relational subspaces.
- **Math / Formula:** Concatenate head outputs then project: `MHA(Q,K,V)=Concat(head_i)W_O`.
- **How it works:** Multiple heads attend to different patterns (syntax, coreference, locality).
- **Why it matters:** Increases representational flexibility without serial depth increase.
- **Pitfalls:** Head redundancy can emerge; more heads do not guarantee better quality.
- **Related:** Attention, Transformer, Positional Encoding.

### Model Drift
- **Definition:** Declining production performance due to changing data/task conditions.
- **Math / Formula:** Tracked through rolling metrics, population stability, and distribution divergence.
- **How it works:** Drift appears gradually or abruptly as user behavior/content changes.
- **Why it matters:** Requires monitoring, retraining triggers, and safe rollback workflows.
- **Pitfalls:** Monitoring only one global metric misses important cohort failures.
- **Related:** Distribution Shift, Monitoring, Shadow Evaluation.

### Mixture of Experts (MoE)
- **Definition:** Model architecture where each input token is routed to a sparse subset of "expert" feed-forward networks rather than a single dense FFN.
- **Math / Formula:** Router selects top-k experts: `output = sum_i gate_i * FFN_i(x)` where `gate_i` is sparse (typically k=1 or k=2 out of E experts).
- **How it works:** A learned router dispatches tokens to the most relevant experts; only a fraction of parameters activate per token.
- **Why it matters:** Scales model parameter count without proportional compute increase; models like Mixtral and GPT-4 use MoE for efficiency.
- **Pitfalls:** Load imbalance across experts; complex to serve efficiently; router collapse is a training failure mode.
- **Related:** Transformer, Quantization, Throughput, Fine-tuning.

---

## N

### Negative Log-Likelihood (NLL)
- **Definition:** Loss based on log probability assigned to true targets.
- **Math / Formula:** `NLL = -sum log p(y_true | x)`.
- **How it works:** Encourages assigning higher probability to correct outputs.
- **Why it matters:** Core objective in language modeling and many probabilistic models.
- **Pitfalls:** Lower NLL does not always correlate with downstream task utility.
- **Related:** Cross-Entropy, Perplexity, Calibration.

### Normalization Layers
- **Definition:** Layers that normalize activations to stabilize optimization.
- **Math / Formula:** BatchNorm (batch stats), LayerNorm (feature stats per token/sample), RMSNorm.
- **How it works:** Controls activation scale and gradient behavior through depth.
- **Why it matters:** Essential for deep Transformer training stability.
- **Pitfalls:** Wrong normalization choice can degrade throughput or quality.
- **Related:** BatchNorm, LayerNorm, Residual Connections.

---

## O

### Overfitting
- **Definition:** Model captures training idiosyncrasies/noise rather than general patterns.
- **Math / Formula:** Characterized by widening train-vs-validation gap.
- **How it works:** Excess capacity or training duration without adequate regularization/data diversity.
- **Why it matters:** Leads to poor real-world performance despite high train metrics.
- **Pitfalls:** Mistaking data leakage or shift for pure overfitting.
- **Related:** Regularization, Early Stopping, Data Augmentation.

---

## P

### Perplexity
- **Definition:** Exponential of average token-level negative log-likelihood in language modeling.
- **Math / Formula:** `PPL = exp( (1/N) * sum_t -log p(w_t|w_<t) )`.
- **How it works:** Measures how surprised a model is by true token sequence.
- **Why it matters:** Useful intrinsic metric for next-token prediction quality.
- **Pitfalls:** Poor proxy for task-specific usefulness and factual correctness.
- **Related:** NLL, Cross-Entropy, Task Evaluation.

### Positional Encoding
- **Definition:** Mechanism that injects token order information into attention-based models.
- **Math / Formula:** Absolute sinusoidal or learned embeddings; relative/rotary variants.
- **How it works:** Distinguishes permutations of identical token sets by encoding position.
- **Why it matters:** Sequence order is critical for language understanding and generation.
- **Pitfalls:** Position extrapolation issues beyond training lengths.
- **Related:** Transformer, Context Window, RoPE.

### Precision
- **Definition:** Fraction of predicted positives that are true positives.
- **Math / Formula:** `TP / (TP + FP)`.
- **How it works:** Captures false-positive control.
- **Why it matters:** Important when false alarms are expensive.
- **Pitfalls:** Can look high while recall is poor.
- **Related:** Recall, F1, PR Curve.

### Pretraining
- **Definition:** Large-scale self-supervised training stage before task-specific adaptation.
- **Math / Formula:** Language models optimize next-token or masked-token objectives at scale.
- **How it works:** Learns broad linguistic/world priors from massive corpora.
- **Why it matters:** Determines baseline capability ceiling for downstream adaptation.
- **Pitfalls:** Data contamination, licensing risk, and inherited biases.
- **Related:** Fine-tuning, SFT, Foundation Model.

### Prompt Injection
- **Definition:** Adversarial input that manipulates LLM instructions or tool behavior.
- **Math / Formula:** No canonical formula; mitigated through policy filters, instruction hierarchy, and tool constraints.
- **How it works:** Malicious tokens exploit model tendency to follow latest/local instructions.
- **Why it matters:** Critical security risk in agentic and tool-using systems.
- **Pitfalls:** Assuming system prompts alone provide complete protection.
- **Related:** Guardrails, Tool Sandboxing, Policy Enforcement.

---

## Q

### Quantization
- **Definition:** Representing model weights/activations with lower precision (for example INT8, INT4).
- **Math / Formula:** Map float ranges to discrete integer levels via scale and zero-point.
- **How it works:** Reduces memory bandwidth and storage; may improve inference throughput.
- **Why it matters:** Key for cost-efficient LLM serving under VRAM constraints.
- **Pitfalls:** Accuracy degradation if calibration/quantization scheme is poor.
- **Related:** KV Cache, Throughput, Memory Bandwidth, QLoRA.

---

## R

### RAG (Retrieval-Augmented Generation)
- **Definition:** Pipeline that retrieves external evidence and conditions generation on it.
- **Math / Formula:** Typical objective combines retrieval quality and generation quality, not a single metric.
- **How it works:** Query rewrite -> retrieval -> reranking -> context packing -> generation -> citation/verification.
- **Why it matters:** Improves grounding, freshness, and domain specificity without full model retraining.
- **Pitfalls:** Low recall retrieval or poor chunking causes confident but unsupported answers.
- **Related:** Embeddings, Hybrid Search, Cross-Encoder, Groundedness.

### Recall
- **Definition:** Fraction of true positives captured among all actual positives.
- **Math / Formula:** `TP / (TP + FN)`.
- **How it works:** Captures false-negative control.
- **Why it matters:** Vital when misses are costly.
- **Pitfalls:** High recall can come with unacceptable false-positive volume.
- **Related:** Precision, F1, ROC/PR Curves.

### Regularization
- **Definition:** Techniques that reduce overfitting by constraining effective model complexity.
- **Math / Formula:** Examples include `L2: Loss + lambda||w||^2`, dropout, label smoothing.
- **How it works:** Penalizes unstable or overly specific solutions.
- **Why it matters:** Improves robustness and out-of-sample performance.
- **Pitfalls:** Over-regularization can underfit and suppress useful signal.
- **Related:** Bias-Variance Trade-off, Early Stopping, Weight Decay.

### RLHF (Reinforcement Learning from Human Feedback)
- **Definition:** Alignment approach using human preference data and RL optimization.
- **Math / Formula:** Policy optimized against learned reward model with KL regularization to reference policy.
- **How it works:** Collect preferences -> train reward model -> optimize policy.
- **Why it matters:** Improves helpfulness/harmlessness relative to pure SFT in many settings.
- **Pitfalls:** Reward hacking and preference dataset bias.
- **Related:** DPO, SFT, Alignment, Reward Model.

---

## S

### Safety Filter / Guardrails
- **Definition:** Policy enforcement layers before and after model generation.
- **Math / Formula:** Typically classifier/rule ensembles with thresholding and action policies.
- **How it works:** Input moderation, tool-use constraints, output checks, and refusal/rewrite flows.
- **Why it matters:** Reduces policy violations and operational risk.
- **Pitfalls:** Over-blocking harms utility; under-blocking harms trust/compliance.
- **Related:** Prompt Injection, Red Teaming, Policy Engine.

### Sampling Parameters
- **Definition:** Decoding controls such as temperature, top-k, top-p, repetition penalties.
- **Math / Formula:** Temperature rescales logits: `p_i = softmax(z_i / T)`.
- **How it works:** Shape randomness/diversity vs determinism in generated text.
- **Why it matters:** Large effect on creativity, factuality, and consistency.
- **Pitfalls:** Aggressive randomness increases hallucinations and unstable outputs.
- **Related:** Beam Search, Deterministic Decoding, Hallucination.

### SFT (Supervised Fine-Tuning)
- **Definition:** Fine-tuning on labeled prompt-response pairs to teach desired behavior.
- **Math / Formula:** Minimize token-level supervised loss on curated instruction data.
- **How it works:** Conditions base model toward task style and response format.
- **Why it matters:** Usually first alignment stage before preference optimization.
- **Pitfalls:** Narrow data causes over-specialization and brittle behavior.
- **Related:** Pretraining, RLHF, DPO, Instruction Tuning.

### Structured Output / Constrained Decoding
- **Definition:** Technique that restricts model token generation to comply with a predefined schema (JSON, regex, grammar, FSM).
- **Math / Formula:** At each decoding step, invalid token logits are masked to -inf before sampling, ensuring only schema-valid tokens are sampled.
- **How it works:** A grammar or schema is compiled into token-level masks applied during greedy/sampling decoding.
- **Why it matters:** Eliminates JSON parsing errors, format inconsistencies, and hallucinated field names in extraction pipelines.
- **Pitfalls:** Overly strict schemas can force incorrect completions; grammar compilation overhead at high QPS.
- **Related:** Hallucination, Guardrails, RAG, Fine-tuning, Constrained Generation.

### Speculative Decoding
- **Definition:** Inference acceleration where a small draft model proposes tokens and a larger model verifies them.
- **Math / Formula:** Speedup depends on acceptance rate and draft/target model throughput ratio.
- **How it works:** Accept verified token blocks; reject and backtrack when mismatch occurs.
- **Why it matters:** Can significantly improve latency without equivalent quality loss.
- **Pitfalls:** Low acceptance rates can erase benefits.
- **Related:** TTFT, TPOT, Continuous Batching, Model Cascades.

---

## T

### Temperature
- **Definition:** Decoding parameter controlling entropy of token distribution.
- **Math / Formula:** Lower `T` sharpens distribution; higher `T` flattens it.
- **How it works:** Rescales logits before sampling.
- **Why it matters:** Directly affects output diversity and determinism.
- **Pitfalls:** High temperature can introduce incoherence in high-stakes tasks.
- **Related:** Top-p, Top-k, Sampling Parameters.

### Throughput
- **Definition:** Work completed per unit time (for example requests/sec or tokens/sec).
- **Math / Formula:** `Throughput = completed_work / time`.
- **How it works:** Influenced by batching, model size, hardware, sequence lengths, and queueing.
- **Why it matters:** Core capacity planning metric for SLA and cost.
- **Pitfalls:** Maximizing throughput can degrade per-request latency.
- **Related:** Latency, QPS, Autoscaling, Queueing.

### Tokenization
- **Definition:** Process of splitting text into model-recognized token units.
- **Math / Formula:** No universal formula; token count depends on tokenizer vocabulary and encoding scheme.
- **How it works:** Maps raw text to token IDs consumed by model embeddings.
- **Why it matters:** Drives context usage, latency, and billing in LLM APIs.
- **Pitfalls:** Different tokenizers produce materially different token counts and costs.
- **Related:** Context Window, Prompt Budgeting, BPE.

### Tool Use / Function Calling
- **Definition:** Model capability to emit structured calls to external tools (APIs, databases, code interpreters) as part of generation.
- **Math / Formula:** No formula; implemented via special tokens or JSON output schema that the runtime parses and dispatches.
- **How it works:** The model generates a structured tool invocation; the runtime executes it and feeds the result back as context for the next generation step.
- **Why it matters:** Enables agentic workflows: web search, code execution, database queries, and API orchestration without retrieval-only architectures.
- **Pitfalls:** Hallucinated tool names or arguments; unbounded tool call loops; sandbox escapes in code execution.
- **Related:** Agentic Orchestration, RAG, Prompt Injection, Structured Output, Sandboxing.

### TPOT (Time Per Output Token)
- **Definition:** Average latency to generate each token after first token.
- **Math / Formula:** `TPOT ~= (generation_time_after_first_token) / output_tokens`.
- **How it works:** Reflects steady-state decode efficiency.
- **Why it matters:** Strong predictor of perceived streaming speed.
- **Pitfalls:** Ignoring TPOT while optimizing only TTFT yields poor long-answer UX.
- **Related:** TTFT, Latency, Throughput.

### TTFT (Time To First Token)
- **Definition:** Latency from request acceptance to first generated token.
- **Math / Formula:** Includes queueing, preprocessing, retrieval/tool setup, and first decode step.
- **How it works:** Captures startup overhead before user sees model response.
- **Why it matters:** Primary driver of perceived responsiveness.
- **Pitfalls:** Hidden queue time can dominate TTFT under burst load.
- **Related:** TPOT, Queueing, Batching, Autoscaling.

### Transformer
- **Definition:** Neural architecture built around attention, feed-forward blocks, residual paths, and normalization.
- **Math / Formula:** Stacked blocks: `x <- x + Attention(LN(x))`, `x <- x + MLP(LN(x))`.
- **How it works:** Self-attention mixes token context globally; MLP layers transform features per position.
- **Why it matters:** Foundation of modern LLMs and many state-of-the-art sequence models.
- **Pitfalls:** Quadratic attention costs and memory pressure at long context lengths.
- **Related:** Attention, Multi-Head Attention, Positional Encoding, KV Cache.

---

## U

### Underfitting
- **Definition:** Model fails to capture signal in training data due to insufficient capacity or training.
- **Math / Formula:** Both training and validation performance remain poor.
- **How it works:** Model class or optimization budget is too weak for task complexity.
- **Why it matters:** Wastes data and compute while delivering weak accuracy.
- **Pitfalls:** Misdiagnosed as data-quality issue when model capacity is the root cause.
- **Related:** Bias-Variance Trade-off, Model Capacity, Learning Curves.

---

## V

### Vector Database / ANN Index
- **Definition:** System optimized for approximate nearest-neighbor search over embedding vectors.
- **Math / Formula:** Similarity via cosine/dot/L2; ANN trades exactness for speed and scale.
- **How it works:** Index structures (HNSW, IVF-PQ, etc.) accelerate top-k vector retrieval.
- **Why it matters:** Backbone of semantic retrieval and RAG at production scale.
- **Pitfalls:** Stale embeddings and poor filtering/ACL integration degrade relevance and safety.
- **Related:** Embeddings, Hybrid Search, RAG, Index Refresh.

### Vanishing Gradient
- **Definition:** Gradients shrink as they backpropagate through many layers/time steps.
- **Math / Formula:** Repeated multiplication by derivatives with magnitude < 1 drives gradients toward 0.
- **How it works:** Early layers receive weak learning signal.
- **Why it matters:** Slows or stalls training in deep/recurrent networks.
- **Pitfalls:** Often masked until late when optimization appears stuck.
- **Related:** Residual Connections, Normalization, Activation Choice.

---

## W

### Weight Decay
- **Definition:** Parameter shrinkage regularization applied during optimization (often decoupled in AdamW).
- **Math / Formula:** Parameter update includes `-lr * wd * w`.
- **How it works:** Discourages large weights and improves generalization.
- **Why it matters:** Standard default in modern deep learning training recipes.
- **Pitfalls:** Confusing classic L2 penalty with decoupled weight decay in adaptive optimizers.
- **Related:** Regularization, AdamW, Overfitting.

---

## Z

### Zero-Shot / Few-Shot Prompting
- **Definition:** Solving tasks with zero or a few demonstrations in the prompt.
- **Math / Formula:** No weight update; relies on in-context conditioning.
- **How it works:** Task instructions and exemplars steer output behavior.
- **Why it matters:** Fastest way to ship prototypes and baseline capabilities.
- **Pitfalls:** Brittle formatting and instruction ambiguity can cause high variance outputs.
- **Related:** In-Context Learning, Prompt Engineering, Instruction Following.

---

## Interview High-Yield Terms (Must Know)

1. Bias-Variance Trade-off  
2. Precision vs Recall vs F1  
3. Cross-Validation and Data Leakage  
4. Regularization (L1/L2, Dropout, Weight Decay, Early Stopping)  
5. Transformer, Attention, Context Window  
6. TTFT, TPOT, Throughput, Tail Latency  
7. Tokenization and Prompt Budgeting  
8. RAG (retrieval, reranking, grounding)  
9. Hallucination and Guardrails  
10. KV Cache, Quantization, Continuous/Server-Side Batching  

## Quick Self-Check for Interviews

- Can you define each term in one sentence?
- Can you write the core formula when applicable?
- Can you explain one production failure mode?
- Can you compare it with one adjacent concept?
- Can you state one practical mitigation or tuning lever?
