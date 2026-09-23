# Claude bootstrap

This repository is the shared continuity layer for AIDY and Super Signals.

Before working on either project, follow `AGENTS.md` exactly.

## AIDY

Read:

1. `projects/aidy/CURRENT_STATE.md`
2. `projects/aidy/SAFETY_RULES.md`
3. `projects/aidy/LIVE_STATE.json`
4. latest `projects/aidy/handovers/*.md`

Then verify relevant facts against `dannythehat/Aidy-Gold-Signals` before changing code or making production claims.

## Super Signals

Read:

1. `projects/super-signals/CURRENT_STATE.md`
2. `projects/super-signals/SAFETY_RULES.md`
3. `projects/super-signals/LIVE_STATE.json`
4. latest `projects/super-signals/handovers/*.md`

Then verify relevant facts against `dannythehat/super-signals` and the live Render/database state before changing code or making production claims.

## Important

Memory can tell you where to look and why past decisions were made. It cannot replace source/runtime verification.

When finishing a material build, update Memory so the next Claude session starts from the verified endpoint instead of reconstructing the project from chat history.
