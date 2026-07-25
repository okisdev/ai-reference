# Verification rounds

Exact ledger format and verification angles for the sweep, referenced from SKILL.md steps 2 and 3. Every finding carries file and line evidence; an angle that cannot produce evidence reports nothing rather than a guess.

## Ledger format

`fix.md` opens with a header block, then one numbered entry per finding.

```markdown
# fix.md

Scope: <scope>
Started: <date>
Round: <current round>

## Findings

1. [open] <one-line finding> (<file>:<line>) - evidence: <one line> - round <r>
2. [fixed] <one-line finding> (<file>:<line>) - evidence: <one line> - round <r>
3. [rejected] <one-line finding> (<file>:<line>) - evidence: <one line> - round <r> - reason: <one line>
```

Status is always `open`, `fixed`, or `rejected`. A rejected entry always carries its reason; an open or fixed entry states only its evidence.

## Angle menu

| Angle | What it checks | Evidence it must return |
| --- | --- | --- |
| Functional correctness | Behavior against the original ask | Repro steps or test output |
| Convention conformance | Alignment with the repo's own precedents | Paired file:line of the change and the neighbor it should match |
| Rendered UI | The UI as it actually renders, not merely as it reads in source | A screenshot or DOM assertion from a real browser |
| Tests and types | Whether a suite or typecheck actually covers the change | Suite and typecheck run results, naming which checks cover the change |
| Docs and dead surface | Docs invalidated by the change, and files or exports left unused | The stale doc passage or the unreferenced file or export |
| Security and input handling | Injection, leakage, or unchecked input on the touched surface; in scope only when the change touches auth, input parsing, or secrets | The specific input or path that breaks handling, with file:line |

## Round discipline

Each round draws on fresh angles or a fresh emphasis on a prior angle; repeating the same angle unchanged wastes a round. Any finding that would trigger a rework needs two independent verifiers before it counts as confirmed, because a single verifier's confirmation is unreliable. A round converges once it returns zero new confirmed findings; typical audits settle in 3 to 5 rounds.

## Dispatch note

Verifiers run as parallel subagents launched in one batch per round, never sequentially. Each brief carries the scope, its assigned angle, the evidence contract from the angle menu above, and an explicit instruction to return findings rather than fix anything; a verifier that starts editing the codebase has stopped verifying.
