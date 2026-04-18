# Reading Repo Instructions

This repository is an agent-native workspace for researching and publishing reading spikes.

## Workflow

- Use `jj` for version control.
- Use the repo-local Nix shell for tooling. Prefer `nix develop -c ...` for one-off commands.
- Use `uv` for Python dependency management and keep `uv.lock` checked in.
- Do not rely on the system Node/npm/Python toolchain when repo-local alternatives exist.
- When interacting with Modal, source credentials from `~/.codex/modal.env` and target the `peyton-agents` workspace.

## Spike authoring contract

- If the user asks for a new spike, use the repo-local skills under `.agents/skills/`.
- Start by scaffolding the spike with `uv run reading spike create "<topic>"`.
- Use the Notion MCP server to read relevant pages in the Training team area before finalizing spike framing or source selection.
- Treat the Training pages as product context, not just background reading. In particular, anchor spikes to the team’s current goals, roadmap, and golden-path priorities.
- Research on the open web using primary sources when possible.
- Prefer papers, official docs, and strong engineering blogs over secondary summaries.
- Mirror canonical PDFs into `public/spikes/<slug>/assets/` when possible.
- Keep spike URLs stable. Refresh existing spikes in place instead of creating duplicate topics.

## Training team priorities

- Default assumption: this repo exists to help the Training team think more clearly about its current work.
- Favor topics that map to the Training team charter and planning docs, especially:
  - RLVR / post-training as the first wedge,
  - repeatable golden-path workloads rather than exotic one-offs,
  - Miles, LoRA, Tinker, SGLang, and non-Ray orchestration,
  - disaggregated rollout inference and delta-compressed weight sync,
  - capacity, storage, RDMA, and other platform constraints that affect training viability.
- When a spike could be written generically or in a team-specific way, choose the team-specific framing.

## Content bar

- Every spike should explain why the topic matters to the team.
- Every spike should include a theme, a concise overview, and a suggested reading order.
- Every source entry should have a summary and a clear note about why it matters.
- Do not pad the page with low-signal sources just to increase count.

## Validation and deploy

- Run `uv run reading site validate` before building.
- Run `npm run build` before deploying.
- Deploy with `uv run modal deploy modal_app.py` from inside the Nix shell after sourcing Modal credentials.
