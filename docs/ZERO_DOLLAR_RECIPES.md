# Zero-dollar workflow recipes

These are workflow patterns, not promises that a complete production app will always fit inside free quotas.

## Existing repository work

1. Use GitHub Copilot Free for lightweight autocomplete.
2. Use Codex/Cursor/Kiro for discrete agent tasks while their free allowance is available.
3. Fall back to Cline/Aider/Roo Code with a local model when hosted quota is exhausted.

## New full-stack prototype

1. Use v0 for UI exploration.
2. Use Lovable/Base44/Bolt/Emergent for a first full-stack skeleton where useful.
3. Export/sync code as early as the product allows.
4. Move normal iteration to repository-based coding agents instead of consuming expensive app-builder prompts for trivial edits.

## Rule of thumb

Use metered app-builder credits for high-leverage generation. Use local/open-source agents for routine refactors, tests, docs, and repetitive repository work.

Do not create multiple accounts to evade vendor limits. This project tracks legitimate published free access, not circumvention tactics.

## UI prototype

```text
v0 / Lovable / Bolt / Base44
  -> export or connect GitHub
  -> Cline / Aider / Roo Code / Codex for repo-level refinement
  -> GitHub pull request
```

Respect each builder's own unit system. Do not add credits across vendors.

## Local-first agent workflow

```text
Cline / Aider / Roo Code / Continue
  +
local Ollama model
  +
GitHub repository
```

This is the most predictable zero-dollar path when local hardware is available. The free part is the client and local inference; cloud model/API use may cost money unless a verified free API tier applies.

## Free API plus open-source agent

Use this only when the API provider publishes a legitimate free allocation:

```text
Open-source agent
  +
Cloudflare Workers AI / Gemini API / Groq / OpenRouter / Hugging Face
  +
small scoped coding task
```

Watch provider-specific rate limits and after-exhaustion behavior. Many API free tiers are dynamic or model-specific.
