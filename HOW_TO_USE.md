# How to Use Memory

Think of this repository as a **shared notebook for the AI builders**.

It does not trade. It does not make AIDY smarter by itself. It remembers where the projects are, what was built, why decisions were made, what is dangerous to change, and exactly what should happen next.

## When working on AIDY

Tell Claude:

> Read the Memory repo for AIDY first. Then verify the real AIDY repo/runtime and continue from the latest handover.

The AI reads the compact AIDY memory, then checks the real AIDY repository before changing anything.

## When working on Super Signals

Tell Claude:

> Read the Memory repo for Super Signals first. Then verify the live Super Signals repo/Render state before changing anything.

## After a build

The AI should update Memory with a short handover:

- what was built;
- why;
- the verified SHA/PR/evidence;
- what is still unresolved;
- exactly what comes next.

You should not need to write these files yourself.

## Automatic sync

The repository can automatically check the AIDY and Super Signals GitHub branch heads every six hours.

For private repositories GitHub needs one narrowly scoped secret called `MEMORY_SYNC_TOKEN`. Until that is configured the sync simply skips safely; everything else still works.

See `SETUP.md` for the one-time setup.

## Important

Memory is a map, not the territory. The AI must always verify important live facts against AIDY, Super Signals, Render, D1/R2/BigQuery or other authoritative systems before claiming something is live or fixed.
