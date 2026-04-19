---
name: spike-generator
description: Generate or refresh a spike page from the planned topic and researched sources. Use when writing `index.mdx`, filling source summaries, and polishing a spike for publication.
---

# Spike Generator

## Goal

Turn the planned topic and researched sources into a clean spike page whose narrative actually explains why Modal cares about the topic.

## Workflow

1. **Re-check Modal's Notion via the Notion MCP server** before writing the overview. Confirm the Modal priority surfaced by `spike-planner`/`spike-researcher` is still current, and pull any additional context that sharpens the framing (customer asks, roadmap bets, platform constraints). This is what makes the overview and `whyItMatters` grounded instead of generic.
2. Import `sources.json` in the spike MDX file.
3. Fill:
   - **overview** — open with the Modal-specific reason the topic matters right now, then state the narrow question the spike is trying to answer,
   - **key themes** — 3 to 5 bullets that name the real tradeoffs, not a list of topics,
   - **suggested reading order** — opinionated, tied to what the reader should take away.
4. Keep the page narrative short and let `SourceList` carry the detailed annotations.
5. Verify signatures: every entry in `sources.json` should carry an `addedBy` (the Modal user who curated it). If a new entry is missing one, run `uv run python scripts/modal_identity.py` and set it before publishing. Never overwrite someone else's `addedBy`.
6. Run `uv run reading spike refresh <slug>` after editing so `updatedAt` and `sourceCount` are correct.

## Rules

- Avoid filler prose. The page should orient the reader, not duplicate all source summaries.
- `whyItMatters` frontmatter and the overview should both name a concrete Modal priority the spike maps onto. If the Notion MCP server is not available and the user did not provide internal context, **pause and ask** rather than writing a generic framing.
- Keep the "key themes" section to 3-5 bullets.
- Make the reading order opinionated.
- Do not paste internal Notion content into the published page. Translate it into public-safe framing that still names the concrete priority.

## References

- See `references/spike-template.md` for the expected page pattern.
