---
name: spike-researcher
description: Research sources for a spike. Use when a spike needs papers, blogs, docs, citations, PDF URLs, and source selection.
---

# Spike Researcher

## Goal

Gather a compact, high-signal reading list for a spike and populate `sources.json`.

## Workflow

1. Read the relevant Training team pages in Notion first and extract the internal frame for the topic.
2. Prefer primary or official sources:
   - papers,
   - official docs,
   - engineering blogs from the team that built the system.
3. Select 4-8 sources maximum.
4. For each source, capture:
   - title,
   - kind,
   - canonical URL,
   - authors if known,
   - publication date if known,
   - concise summary,
   - why it matters.
5. Mirror canonical PDFs into `public/spikes/<slug>/assets/` when available.
6. Update `src/content/spikes/<slug>/sources.json`.

## Rules

- Do not use low-signal summary sites if the original source exists.
- Use blogs to explain implementation tradeoffs, not as a substitute for papers.
- If a source has no PDF, keep the link and skip the embed.
- Use the Notion MCP server as the source of truth for team priorities, preferred terminology, and what the spike should optimize for.
- When writing `whyRelevant`, connect the source back to the Training team’s active goals rather than keeping the annotation generic.

## References

- See `references/source-rubric.md` for the source scoring rubric.
