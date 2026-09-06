# AGENTS.md

These rules apply to ChatGPT, Claude and any other agent using this repository.

## Purpose

`Memory` exists to preserve project continuity. It is not allowed to become a competing production database or an excuse to skip verification.

## Mandatory session bootstrap

Before changing AIDY or Super Signals:

1. identify the project;
2. read that project's `CURRENT_STATE.md`, `SAFETY_RULES.md`, `LIVE_STATE.json`, and latest handover;
3. inspect the authoritative source repository and any live/runtime evidence needed for the task;
4. reconcile differences explicitly — source/runtime truth wins over Memory;
5. only then make changes.

Do not mix AIDY and Super Signals state. They interact, but they are separate systems with different repositories and production boundaries.

## Evidence language

Never say `fixed`, `live`, `deployed`, `GREEN`, `complete`, `profitable`, or `production verified` unless the relevant evidence was actually checked.

Use these statuses consistently:

- `BUILT` — code/config exists.
- `ENGINEERING PROVEN` — tests/acceptance prove the implementation.
- `PRODUCTION VERIFIED` — the exact production/runtime state was checked after deployment/merge.
- `STATISTICALLY VALIDATED` — sufficient forward evidence exists for the stated statistical claim.
- `WAITING` — the required real-world evidence cannot exist yet.
- `RED` — an acceptance condition is failing.

## Build-day completion gate

A build day or major milestone is **not complete** until all of the following are true:

1. the authoritative repository/runtime acceptance evidence has been checked;
2. `CURRENT_STATE.md` and `LIVE_STATE.json` reflect the verified state;
3. a dated handover records the completed work and exact next step;
4. `DECISIONS.jsonl` is updated when an architectural/product/safety decision changed;
5. the Memory validation workflow/script passes; and
6. the merged Memory `main` state is re-read to confirm the update landed.

An agent must not call a day `GREEN`, `complete`, or `finished` before this gate is satisfied. If a previous agent forgot to update Memory, repair Memory from the real repositories/runtime first; never alter production merely to make it match stale Memory.

## Production safety

- Protect live Super Signals real-money execution above research convenience.
- AIDY formal-forward authority remains OFF unless an explicit owner decision changes it and the production evidence supports that change.
- Research/shadow systems must not silently acquire broker authority.
- Never deploy a risky auth/credential change immediately before a market open unless the owner explicitly authorizes that exact production change with rollback ready.
- Never expose secrets in logs, evidence, Memory files, PR descriptions or chat.

## Memory hygiene

After a material completed change:

1. update `LIVE_STATE.json` only with verified repository/runtime facts;
2. update `CURRENT_STATE.md` with the new concise state;
3. append a decision to `DECISIONS.jsonl` if a real architectural/product/safety decision changed;
4. add a dated handover for completed build days or major incidents;
5. move superseded detail into handovers/archive rather than endlessly expanding `CURRENT_STATE.md`.

Keep `CURRENT_STATE.md` short enough to load every session.

## Conflict resolution

Authoritative precedence:

1. production runtime / authoritative database evidence;
2. source repository deployed/protected branch and acceptance evidence;
3. source repository documentation;
4. Memory;
5. conversation summaries / model memory.

If Memory is stale, update it after verifying the real system. Do not alter production to make it match Memory.

## Prohibited content

Do not commit:

- API keys, bearer tokens, passwords, session cookies or private keys;
- broker credentials or account secrets;
- raw ChatGPT/Claude authentication exports;
- giant conversation exports by default;
- personal psychological/identity profiling unrelated to the projects.
