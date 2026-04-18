---
name: spike-generator
description: Generate or refresh a spike page from the planned topic and researched sources. Use when writing `index.mdx`, filling source summaries, and polishing a spike for publication.
---

# Spike Generator

## Goal

Turn the planned topic and researched sources into a clean spike page.

## Workflow

1. Import `sources.json` in the spike MDX file.
2. Fill:
   - overview,
   - key themes,
   - suggested reading order.
3. Keep the page narrative short and let `SourceList` carry the detailed annotations.
4. Run `uv run reading spike refresh <slug>` after editing so `updatedAt` and `sourceCount` are correct.

## Rules

- Avoid filler prose. The page should orient the reader, not duplicate all source summaries.
- Keep the “key themes” section to 3-5 bullets.
- Make the reading order opinionated.

## References

- See `references/spike-template.md` for the expected page pattern.
