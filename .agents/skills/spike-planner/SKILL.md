---
name: spike-planner
description: Plan a new reading spike before research starts. Use when the user asks for a new spike or wants to reshape an existing topic into a better reading angle.
---

# Spike Planner

## Goal

Turn a broad topic into a decision-ready spike brief.

## Workflow

1. Read the relevant Training team pages in Notion before narrowing the topic.
2. Normalize the topic into a sharp title and slug.
3. Identify:
   - the main technical question,
   - why it matters to the team,
   - the likely source categories,
   - what should be ignored.
4. Run `uv run reading spike create "<topic>"` if the spike does not exist yet.
5. Fill the spike frontmatter and the top sections of `index.mdx` before deep research starts.

## Rules

- Keep the spike focused enough that 4-8 sources can cover it well.
- Prefer a systems or implementation angle over a generic literature review.
- Write the “why it matters” section in team-facing language, not academic language.
- Default to the Training team’s current goals from Notion: RLVR as wedge, repeatable golden paths, LoRA-friendly post-training frameworks, and platform-informed systems tradeoffs.

## References

- See `references/spike-brief.md` for the target brief structure.
