---
title: "N2 — Post-Training: DPO, GRPO, RLVR, Distillation"
tags: [new-topic, post-training, fine-tuning, rl]
---

# N2 — Post-Training: DPO, GRPO, RLVR, Distillation

## Card

**One line:** After pretraining, models are shaped by SFT, then preference or reward optimization; for interviews know which method fits which data and goal.
**Patterns:** P5 (eval loop), P6 (version + rollback)

**3 ideas**
1. **The pipeline:** pretrain → SFT (imitate good examples) → preference/RL (prefer better outputs) → eval gate. Each stage needs different data.
2. **DPO replaced PPO-RLHF for most teams.** Same preference pairs, no reward model, no online sampling, stable. **GRPO + verifiable rewards (RLVR)** is how reasoning is trained.
3. **Distillation is the practical win.** Use a big model to generate (and filter) data, train a small model to match it. Big quality per dollar.

**2 trade-offs**
- Offline preference methods (DPO: simple, cheap) vs online RL (PPO/GRPO: stronger, costly, reward hacking risk).
- Distill a small model (cheap, fast inference) vs keep calling the big one (no training, always latest).

**Soundbite:** *"If I have preference pairs I use DPO; if I can check answers automatically I use RL with verifiable rewards; if I want cheap inference I distill."*

---

## 1. The methods at a glance

| Method | Data needed | Mechanism | Use when |
|---|---|---|---|
| **SFT** | Prompt → ideal response | Next-token loss on responses | Teach format, style, task |
| **RLHF (PPO)** | Preference pairs → reward model | Online RL against reward model with KL penalty | Big labs; hard to run |
| **DPO** | (prompt, chosen, rejected) | Closed-form loss increases chosen vs rejected log-prob relative to a reference model | Default preference tuning |
| **KTO / ORPO / SimPO** | Thumbs up/down (KTO) or pairs | DPO variants: no reference model, or single-label data | Only binary feedback; simpler setup |
| **GRPO** | Prompts + a reward function | Sample a group per prompt, advantage = reward vs group mean; no value/critic model | RL for reasoning; cheaper than PPO |
| **RLVR** | Prompts with checkable answers | Reward = verifier (unit tests pass, math answer correct, schema valid) | Math, code, tool use, structured tasks |
| **RLAIF / Constitutional** | Principles + AI judge | AI labels preferences instead of humans | Scale preference data cheaply |
| **Distillation** | Teacher outputs (+ maybe logits) | Student trained on teacher outputs/reasoning traces | Cheap model with big-model behavior |

## 2. How to explain DPO in 20 seconds

"RLHF trains a reward model then does RL to maximize it with a KL leash. DPO shows the optimal policy for that objective can be written in terms of the policy itself, so you skip the reward model and train directly on chosen-vs-rejected pairs with a classification-style loss. A `β` parameter plays the role of the KL leash."

## 3. How to explain GRPO + RLVR in 20 seconds

"For each prompt, sample a group of, say, 8–16 answers. Score each with a verifier. Each answer's advantage is its reward minus the group average. Push up the above-average ones. No critic model, so it's cheaper than PPO. With verifiable rewards, the model learns to reason longer when it helps, which is how R1-style reasoning emerged."

## 4. Failure modes to name

- **Reward hacking:** model exploits the verifier (tests that don't cover the case, judge that likes length). Mitigate: stronger verifiers, held-out evals, length penalties.
- **Over-optimization / verbosity:** preference tuning drifts to long, sycophantic answers. Track length and refusal rate.
- **Catastrophic forgetting:** narrow tuning hurts general skills. Mix general data, LoRA, low LR (Ch 26).
- **Data contamination:** eval items leak into training. Hold out and dedupe first.

## 5. Distillation in practice (most likely in your job)

1. Collect real prompts from production (scrubbed, consented).
2. Generate teacher answers (optionally best-of-N with a verifier).
3. Filter: judge score, tests, dedupe, diversity.
4. SFT the student (often LoRA), optionally DPO with teacher-vs-student pairs.
5. Gate on the same eval suite as the teacher; canary; route easy traffic to the student (P1).

Check the provider's terms: some forbid training competing models on outputs.

## 6. Decision ladder (say it out loud)

prompt → few-shot → RAG → **SFT** → **DPO** → **RL with verifiable rewards**. Climb only when the rung below plateaus on your eval set.

---

## Recall

> [!question]- DPO vs PPO-based RLHF?
> Both use preference data. PPO-RLHF trains a separate reward model and runs online RL (complex, unstable). DPO optimizes directly on pairs with a reference model, offline and stable.

> [!question]- What makes GRPO cheaper than PPO?
> No learned value/critic model. The baseline is the mean reward of a group of samples for the same prompt.

> [!question]- What is RLVR and where does it apply?
> RL where the reward comes from a programmatic verifier: tests, exact answers, schema checks. Works for math, code, tool calls; not for open-ended writing.

> [!question]- What is reward hacking? Give an example.
> The model maximizes the reward without doing the task: e.g. editing tests to pass, or writing longer answers because the judge prefers length.

> [!question]- When would you distill rather than fine-tune from human data?
> When a big model already does the task well and you need lower cost/latency at volume. Teacher generates and filters data; student learns it.

**Related:** [[Chapter 26 - Fine-Tuning and Adaptation]] · [[Chapter 27 - Evaluation at Scale]] · [[N1 - Reasoning Models and Test-Time Compute]] · [[N8 - Evaluating Agents]]
