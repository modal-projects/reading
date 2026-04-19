---
name: spike-researcher
description: Research sources for a spike. Use when a spike needs papers, blogs, docs, citations, PDF URLs, and source selection.
---

# Spike Researcher

## Goal

Gather a compact, high-signal reading list for a spike and populate `sources.json` with `whyRelevant` annotations that connect each source back to a real Modal priority.

## Workflow

1. **Pull internal context first via the Notion MCP server.** Search Modal's Notion for the spike topic, adjacent terms, and any customer or product names that show up in the planner's brief. Capture the internal framing — which problem Modal is solving, which customers care, which platform constraints matter — before reading external sources. This is what turns `whyRelevant` from a generic paragraph into a Modal-specific annotation.
2. Prefer primary or official sources on the open web:
   - papers,
   - official docs,
   - engineering blogs from the team that built the system.
3. Select 4-8 sources maximum.
4. **Resolve the signer once.** Run `uv run python scripts/modal_identity.py` and capture the output (e.g. `alessio-modal-labs`). This is the Modal user running the agent and will be attached to every new source entry as `addedBy`.
5. For each source, capture:
   - title,
   - kind,
   - canonical URL,
   - authors if known,
   - publication date if known,
   - a concise `summary` of what the source actually contains,
   - a `whyRelevant` that ties the source to the Modal priority you found in step 1 (e.g. "this is the closest public analogue to the Perplexity/Tinker workstream" rather than "this is a good paper about X"),
   - an `addedBy` set to the signer from step 4.
6. Mirror canonical PDFs into `public/spikes/<slug>/assets/` when available.
7. Update `src/content/spikes/<slug>/sources.json`. Only touch existing entries if the user asked you to — otherwise leave their `addedBy` untouched.

## Rules

- If the Notion MCP server is not configured or returns nothing for the topic, **pause and ask the user** for internal context. Do not invent a Modal priority, and do not silently fall back to a generic `whyRelevant`.
- If `scripts/modal_identity.py` fails (no Modal auth, wrong workspace), **pause and ask the user** to authenticate instead of writing a source without an `addedBy` or guessing a handle. Every new source entry must carry a real signature.
- Do not use low-signal summary sites if the original source exists.
- Use blogs to explain implementation tradeoffs, not as a substitute for papers.
- If a source has no PDF, keep the link and skip the embed.
- Do not paste internal Notion content into `summary` or `whyRelevant`. Translate it into public-safe framing that still names the concrete Modal priority.

## References

- See `references/source-rubric.md` for the source scoring rubric.
