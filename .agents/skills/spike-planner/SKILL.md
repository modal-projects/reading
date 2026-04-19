---
name: spike-planner
description: Plan a new reading spike before research starts. Use when the user asks for a new spike or wants to reshape an existing topic into a better reading angle.
---

# Spike Planner

## Goal

Turn a broad topic into a decision-ready spike brief that is clearly grounded in what Modal actually cares about right now.

## Workflow

1. **Search Modal's Notion via the Notion MCP server first.** Query by the topic keywords and adjacent terms. Read planning docs, roadmap pages, design notes, customer asks, and team charters that mention the topic. Capture:
   - the concrete problem Modal is trying to solve,
   - which product surfaces or customers it affects,
   - the internal terminology Modal uses for it,
   - any explicit decisions, bets, or non-goals already in writing.
2. Normalize the topic into a sharp title and slug.
3. Identify:
   - the main technical question,
   - **why it matters to Modal specifically** (cite the Notion context you found in step 1, not generic industry framing),
   - the likely source categories,
   - what should be ignored.
4. Run `uv run reading spike create "<topic>"` if the spike does not exist yet.
5. Fill the spike frontmatter and the top sections of `index.mdx` before deep research starts. The `whyItMatters` frontmatter field should name a concrete Modal priority the spike maps onto.

## Rules

- If the Notion MCP server is not configured or returns nothing for the topic, **pause and ask the user** for internal context before writing `whyItMatters`. Do not fall back to a generic industry claim.
- Keep the spike focused enough that 4-8 sources can cover it well.
- Prefer a systems or implementation angle over a generic literature review.
- Write the "why it matters" section in Modal-facing language (products, customers, platform constraints), not academic language.
- Do not quote Notion pages verbatim in published output. Translate internal framing into a public-safe description of the Modal priority.

## References

- See `references/spike-brief.md` for the target brief structure.
