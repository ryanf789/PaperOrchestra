# Halt Rules

Source: arXiv:2604.05018, §4 Step 5 ("Iterative Content Refinement"):

> After modifying the LaTeX source to address weaknesses, revisions are
> accepted if the overall score increases, or if it ties when net sub-axis
> gains are non-negative. The agent immediately reverts to the previous
> version and halts upon any overall score decrease, negative tie-breaker,
> or reaching the iteration limit.

Encoded as deterministic logic in `scripts/score_delta.py`. This file is the
human-readable specification.

## Definitions

Let:

- `prev` = score JSON from the previous accepted iteration
- `curr` = score JSON from the just-completed iteration
- `prev.overall` = `prev.overall_score`
- `curr.overall` = `curr.overall_score`
- `subaxis_delta(axis)` = `curr.axis_scores[axis].score - prev.axis_scores[axis].score`
- `net_subaxis_delta` = `sum(subaxis_delta(a) for a in 6 axes)`

## Decision rules (in order)

```
if curr.overall > prev.overall:
    DECISION = ACCEPT_IMPROVED

elif curr.overall == prev.overall:
    if net_subaxis_delta >= 0:
        DECISION = ACCEPT_TIED_NON_NEGATIVE
    else:
        DECISION = REVERT_TIED_NEGATIVE_SUBAXIS

else:  # curr.overall < prev.overall
    DECISION = REVERT_OVERALL_DECREASED
```

The script exits with:

| Exit code | Meaning | Loop action |
|---|---|---|
| 0 | ACCEPT_IMPROVED | keep new draft, continue loop |
| 0 | ACCEPT_TIED_NON_NEGATIVE | keep new draft, continue loop |
| 1 | REVERT_OVERALL_DECREASED | rollback to prev, halt loop |
| 2 | REVERT_TIED_NEGATIVE_SUBAXIS | rollback to prev, halt loop |

The script also prints a one-line decision string and a JSON object on
stdout for the host agent to log.

## Loop-level halt conditions

In addition to the per-iteration accept/revert decision, the loop halts
when ANY of these is true:

1. **Iteration cap reached.** Default 3 (configurable via env var
   `PO_REFINE_MAX_ITER`). Per the paper Table 7, the typical
   refinement count is "3× content refinement loop".
2. **REVERT decision** from `score_delta.py` (exit code 1 or 2).
3. **Empty weaknesses list.** If the simulated reviewer's `weaknesses`
   array is empty, there is nothing to fix — halt.
4. **Diminishing returns.** Three consecutive ACCEPT_IMPROVED iterations
   each with `overall_delta < 1.0` → halt to save wall-time. (Soft rule;
   the paper does not specify it but it matches the cost budget of
   ~5-7 LLM calls.)

## Promoting the best snapshot

After halt, identify the iteration with the highest `accepted` overall
score:

```python
accepted_iters = [it for it in worklog.iterations if it.decision.startswith("ACCEPT")]
best = max(accepted_iters, key=lambda it: it.score.overall_score)
```

If the loop halted on REVERT, `best` is the iteration immediately *before*
the reverted one. Copy its `paper.tex` and `paper.pdf` to
`workspace/final/`.

## Worked example

Suppose:

| iter | overall | depth | exec | flow | clarity | evidence | style | decision |
|---|---|---|---|---|---|---|---|---|
| 0 | 64.5 | 65 | 70 | 60 | 55 | 72 | 68 | (baseline) |
| 1 | 67.3 | 68 | 73 | 64 | 58 | 74 | 70 | ACCEPT_IMPROVED |
| 2 | 67.3 | 70 | 73 | 64 | 58 | 73 | 71 | ACCEPT_TIED_NON_NEGATIVE (Σdelta = +2) |
| 3 | 66.0 | 70 | 70 | 62 | 56 | 73 | 71 | REVERT_OVERALL_DECREASED, HALT |

Promoted: iter 2 (`final/paper.tex` ← `iter2/paper.tex`).
Score trajectory in the run report:
```
64.5 → 67.3 (accept) → 67.3 (accept tied) → 66.0 (revert, halt)
```
