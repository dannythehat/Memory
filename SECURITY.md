# Security

`Memory` is private but must still be treated as non-secret project documentation.

## Never store

- API keys or bearer tokens
- GitHub PATs
- broker/MT5 credentials
- Telegram session strings
- Cloudflare credentials
- passwords/private keys
- raw browser cookies/cURL authentication exports

## Allowed

- repository names, branches and commit SHAs
- PR/workflow/run IDs
- architecture and decisions
- non-secret production service names/URLs
- counts and operational evidence that do not expose credentials

## Secret setup

If automatic cross-repository sync is enabled, put the fine-grained token only in the Memory repository's GitHub Actions secret named `MEMORY_SYNC_TOKEN`.

Never write its value into a file, workflow YAML, issue, PR, log or chat.
