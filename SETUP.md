# Setup

## What works immediately

The repository can be used immediately by ChatGPT/Claude as a shared project-memory layer. No secret is required for humans/agents that already have GitHub access.

## Optional automatic live-state sync

GitHub's normal `GITHUB_TOKEN` is scoped to this repository and cannot read other private repositories. To let a scheduled workflow refresh AIDY and Super Signals branch heads automatically, add one fine-grained GitHub token to the **Memory repository only** as:

`MEMORY_SYNC_TOKEN`

Minimum recommended access:

- repository access: only `Aidy-Gold-Signals` and `super-signals`;
- `Aidy-Gold-Signals`: Contents **Read-only**, Pull requests **Read-only**;
- `super-signals`: Contents **Read-only**, Pull requests **Read-only**.

The token does **not** need write access to `Memory`; the workflow's own repository-scoped `GITHUB_TOKEN` performs the Memory commit/push.

Do not paste the token into chat, files, commits, workflow logs or PR descriptions. Add it through GitHub repository settings as an Actions secret.

Once configured, `.github/workflows/sync-live-state.yml` refreshes observed source-repository branch heads and latest merged PR metadata every six hours. These observations do not claim that the same SHA is deployed in production; runtime/deploy verification remains mandatory.

## Claude usage

Best option: clone `Memory` beside your project repositories so Claude can read it locally.

Example layout:

```text
workspace/
  Memory/
  Aidy-Gold-Signals/
  super-signals/
```

At the start of an AIDY session tell Claude:

> Read ../Memory/AGENTS.md and the AIDY files under ../Memory/projects/aidy first. Then verify the live AIDY repo state before continuing the build.

For Super Signals substitute `projects/super-signals`.

You do not need to paste project history into Claude. The whole point of Memory is to keep the bootstrap compact and versioned.

## ChatGPT usage

When GitHub is connected, say:

> Read the Memory repo for AIDY first, verify the authoritative AIDY repo/runtime, then continue Day X.

or

> Read the Memory repo for Super Signals first, verify production, then investigate X.

## Updating Memory

A completed build should produce a concise handover containing:

- what changed;
- why;
- source repo/branch/SHA;
- acceptance/production evidence;
- safety state;
- unresolved issues;
- exact next step.

Do not turn handovers into full transcripts.
