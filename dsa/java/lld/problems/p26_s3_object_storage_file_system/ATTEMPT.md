# Design S3 Object Storage / File System — my attempt

Procedure: `../../../notes/THE_SCRIPT.md`. Fill this in **before** opening the key.
Do not paste the answer here. If you looked, write "LOOKED" next to the phase —
an honest record is worth more than a clean one.

Date attempted: ________   Time taken: ______   Got to Phase: ___

---

## PHASE 1 — SCOPE (0:00–5:00)

**Restate / Cut / Aim** — three sentences, out loud:

> Restate:
>
> Cut:
>
> Aim:

**My clarifying questions** (aim for 5; mark the one you *planted*):

| # | Question | What I'm fishing for |
|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |

---

## PHASE 2 — NOUNS (5:00–10:00)

Nouns I underlined:

```

```

Merged or deferred, and why:

- 
- 

Survivors:

---

## PHASE 3 — DECIDE (10:00–15:00)

Run every survivor through THE BIG DECISION (`../../../notes/TEXT_TO_CODE.md`).
The **reason** column is the one being graded.

| Noun | Q1 data-only? | Q2 shared state? | Q3 capability? | Verdict | Reason I said out loud |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

Expected shape: 2–4 records, 1–3 enums, 2–4 classes, 1–3 interfaces, 0–1 abstract classes.
Mine: ___ records, ___ enums, ___ classes, ___ interfaces, ___ abstract.

If I have more than one abstract class, I should justify it or drop it.

---

## PHASE 4 — API (15:00–20:00)

Signatures only. No bodies. Java, not pseudocode.

```java

```

Ownership check — does any method reach into another object's fields?

Usability check — could someone use this without reading the implementation?

Checkpoint sentence I said before coding:

> "

---

## PHASE 5 — CODE (20:00–35:00)

What I implemented fully:

What I stubbed, **and said I was stubbing**:

Code lives in: `./`

---

## PHASE 6 — EXTEND (35:00–45:00)

The key covers 4 follow-ups. Predict them before you look, then fill in the rest.

| # | Follow-up | My answer | Cost (classes added / lines edited) |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

**The extension test:** did a new requirement cost **one new class, zero edits**?

**Concurrency, all three layers** (if asked):

1. In-process:
2. Time / timeout:
3. Multi-machine:

---

## Self-check (six is a pass)

- [ ] Scoped out loud before writing anything
- [ ] Asked ~5 questions, one of them planted
- [ ] Said the *reason* for every record / enum / interface choice
- [ ] Wrote signatures before bodies, and paused for agreement
- [ ] Stated what I was stubbing instead of going quiet
- [ ] Reached Phase 6 with time left
- [ ] Answered a "now add X" with one class and zero edits
- [ ] Gave all three layers on concurrency

## After comparing to the key

What the key did that I didn't:

What I did that I'd defend anyway:

**Goes in `../../../notes/error_log.md`:**
