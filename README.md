# Memory

Private shared project-memory repository for **AIDY** and **Super Signals**.

This repository is a continuity layer for Claude and other development agents. It records what has been built, why decisions were made, what is live, what is unsafe to change casually, and the exact next starting point.

> **2026-09-23 — owner decision: ChatGPT is removed as a development agent.** Claude is
> the only AI assistant that changes these repositories or production. Do not "ask ChatGPT",
> relay prompts to it, or treat a ChatGPT-authored change as reviewed.
>
> **This is NOT the OpenAI API.** Super Signals calls OpenAI models inside the live product
> to read provider Telegram messages and turn them into trades (`ai_message_decisions`:
> 2,413 decisions in the 24h to 2026-09-23 14:12Z). **Never remove, rotate or disable the
> OpenAI API key in Render as part of "removing ChatGPT"** — it would stop signal
> ingestion. Only the ChatGPT GitHub connection is being revoked.
>
> ChatGPT committed as the owner (`dannythehat`), so older commits cannot be told apart by
> author. Historical notes below that mention ChatGPT are kept as history.

## Authority rule

Memory is **not** the production source of truth.

When facts conflict, use this order:

1. live production/runtime evidence and authoritative data stores;
2. source repository code and deployed/accepted commit evidence;
3. acceptance evidence in the source repositories;
4. this Memory repository;
5. chat recollection or model memory.

An agent must verify live facts against the real project repository/data before claiming something is deployed, fixed, GREEN, profitable, current, or safe.

## Projects

- [`projects/aidy/`](projects/aidy/) — AIDY Gold Signals / intelligence system.
- [`projects/super-signals/`](projects/super-signals/) — Super Signals private app and Provider Lab.

## Start here

For any project session, read in this order:

1. `AGENTS.md`
2. the project's `CURRENT_STATE.md`
3. the project's `SAFETY_RULES.md`
4. the project's `LIVE_STATE.json`
5. the latest file in the project's `handovers/` directory
6. only then inspect the authoritative source repo/runtime and begin work.

## Design

Adapted from the useful part of Memspan's three-tier model:

- **Tier 1 — Current state:** small files that should be cheap to load every session.
- **Tier 2 — Project memory:** architecture, roadmap, decisions and known issues loaded when relevant.
- **Tier 3 — Historical archive:** dated handovers/evidence retrieved only when needed.

We deliberately do **not** store giant conversation dumps, personal psychological profiles, credentials, API tokens, broker secrets or other secret material here.

## Automation

`Memory` includes validation and live-state sync tooling. Cross-private-repository GitHub Actions need a narrowly scoped repository secret named `MEMORY_SYNC_TOKEN`; see [`SETUP.md`](SETUP.md). Until that secret is configured, Claude can still use the repository normally and update verified state during development sessions.
