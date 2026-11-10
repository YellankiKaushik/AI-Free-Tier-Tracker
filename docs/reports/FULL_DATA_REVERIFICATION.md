# Full Data Reverification

**Review date:** 2026-11-10
**Canonical records reviewed:** 43

## Review result

Official vendor pricing pages, documentation, announcements, or source repositories were checked for all 43 records. Forty records have a current verification date of 2026-11-10. Three records retain their prior date of 2026-08-27 because official sources disagree on material free-tier details. Their generated index entries preserve the old dates and continue to trigger the stale-data warning.

| Review state | Records |
| --- | --- |
| Reverified on 2026-11-10 (40) | aider; Atlassian Rovo Dev; Augment Code; Base44; Bolt.new; Cerebras Inference; Claude Code; Cline; Cloudflare Workers AI; CodeRabbit; Continue; Anything (formerly Create.xyz); Cursor; Dyad; Gemini API; GitHub Copilot Free; GitHub Models; GitHub Spark; Goose; Groq; Hugging Face Inference; JetBrains AI Assistant; Kilo Code; Kiro; Lovable; NVIDIA NIM; OpenAI Codex; OpenCode; OpenHands; OpenRouter; Qoder; Qwen Code; Replit; Roo Code; Sourcegraph Cody; SWE-agent; Tabby; v0; Devin Desktop (formerly Windsurf); Zed AI |
| Still stale (3) | Emergent; TRAE; Warp |

The 40 current entries are listed above so the audit scope is explicit. Each record's evidence URLs, retrieval dates, field support, and claims are stored in its canonical YAML under tools/.

## Material corrections and clarifications

- **NVIDIA NIM:** replaced the 404 reference with the verified official product page at https://docs.api.nvidia.com/nim/docs/product. The free-tier allowance remains unpublished; no quota was added.
- **Anything:** updated Create.xyz's current name, vendor, product URL, and pricing URL. Public pricing confirms Free but publishes no exact free allowance.
- **GitHub Copilot:** retained 2,000 monthly completions; the Free AI-credit amount remains undisclosed. The card requirement is unknown because the plan page does not state it.
- **Lovable:** kept build, Cloud, and in-app AI grants as separate pools. The record distinguishes the known daily build expiry from unclear expiry for its free monthly Cloud and AI grants.
- **OpenAI Codex:** confirmed inclusion with eligible ChatGPT Free access, left the exact allowance unpublished, and marked the card requirement unknown. Codex Cloud is not included on Free.
- **Sourcegraph Cody:** retained the historical 200 chats and commands per month as a legacy Free allowance. Free and Pro were discontinued in 2025; Sourcegraph separately announced Cody end of life for January 31, 2027.
- **TRAE:** the official site returned incompatible plan presentations. Its official blog supports a 14-day Pro trial with a payment method required within 48 hours, while the exact Free allowance remains unpublished. The record date remains stale.
- **Warp:** the current pricing and billing pages say Free has no bundled AI usage, while Warp's official FAQ still says 150 free requests per month. The exact allowance is omitted and the record date remains stale.
- **Zed:** captured 2,000 accepted edit predictions without inferring a reset period. The 14-day Pro trial is separate and its $5 balance is shared across Zed and Delta. The schema now allows an undisclosed quota period.

No record was given a new verification date solely because a URL was accessible. No undisclosed numeric allowance was fabricated. Conflicts and unknown card requirements remain explicit.

## Records still needing follow-up

- **Emergent:** official pricing says 10 free monthly credits; official help says 10 credits on the first day and does not clearly confirm that this Free grant recurs. The 10-credit amount is retained, but cadence and rollover are unknown.
- **TRAE:** current pricing responses differ on whether the Free row is shown and provide no exact free usage amount. Recheck the live pricing experience once the vendor's plan presentation is consistent.
- **Warp:** reconcile the 150-request FAQ with the newer pricing and billing documentation before recording an exact Free allowance.

The source-health scan is documented separately in SOURCE_HEALTH_AUDIT.md. It confirms URL accessibility on merged main, not claim accuracy for this follow-up branch.
