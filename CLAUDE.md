# Claude bootstrap

This repository is the shared continuity layer for AIDY and Super Signals.

Before working on either project, follow `AGENTS.md` exactly, then read `NETWORK.md` for the
whole-estate map (what each repository is, what runs where, and how the systems interlink).

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

**The deployed branch is `feature/day-10-shared-telegram-sources`, not `main`.** `main` is well
behind it and a branch named `production` is not deployed. Always confirm the deployed branch
head before reasoning about production behaviour.

**That branch auto-deploys to live real-money trading.** A push to it is a production release with
no manual gate, so never push to it without an explicit go-ahead from the owner, and never close
to the Monday 01:01 Europe/Sofia market open. Work on a separate branch and merge deliberately.
Repointing Render at `main`, or merging `main` into the deploy branch, would roll production back
141 commits instantly. (The committed `render.yaml` says `autoDeployTrigger: off`; that is
misleading — the live dashboard setting is ON and governs behaviour.)

## Important

Memory can tell you where to look and why past decisions were made. It cannot replace source/runtime verification.

When finishing a material build, update Memory so the next ChatGPT/Claude session starts from the verified endpoint instead of reconstructing the project from chat history.
