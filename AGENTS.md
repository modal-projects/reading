# Reading Repo Instructions

This repository is an agent-native workspace for researching and publishing reading spikes. The site is meant for engineers working in the `modal-labs` Modal workspace.

## Workflow

- Use `jj` or `git` for version control.
- Use the repo-local Nix shell for tooling. Prefer `nix develop -c ...` for one-off commands. If `nix` is unavailable on your machine, `uv` and `npm` work directly as long as the versions roughly match `flake.nix` and `.nvmrc`.
- Use `uv` for Python dependency management and keep `uv.lock` checked in.
- Do not rely on the system Node/npm/Python toolchain when repo-local alternatives exist.
- The site is deployed from the `modal-labs` Modal workspace. Confirm `modal profile current` returns `modal-labs` before running any `modal` commands, and use `modal profile activate modal-labs` if it does not.

## Spike authoring contract

- If the user asks for a new spike, use the repo-local skills under `.agents/skills/` (`spike-planner`, `spike-researcher`, `spike-generator`, `site-steward`).
- Start by scaffolding the spike with `uv run reading spike create "<topic>"`.
- **Ground framing in Modal internals via the Notion MCP server.** Before writing `whyItMatters`, the spike overview, or any `whyRelevant` entry, search Modal's Notion for the topic and adjacent terms. Pull planning docs, roadmap pages, design notes, and customer asks. Use that context to write the framing; do not fall back to generic industry claims.
- If the Notion MCP server is not configured, pause and ask the user for internal context rather than inventing a Modal priority.
- Never paste internal Notion content verbatim into published spike files. Translate it into public-safe framing that still names the concrete Modal priority.
- Research on the open web using primary sources when possible.
- Prefer papers, official docs, and strong engineering blogs over secondary summaries.
- Mirror canonical PDFs into `public/spikes/<slug>/assets/` when possible.
- Keep spike URLs stable. Refresh existing spikes in place instead of creating duplicate topics.

## Signing

- Every spike and every source entry carries an `addedBy` field with the Modal username (e.g. `alessio-modal-labs`) of the person who curated it. This is the same handle that shows up in `modal app history`.
- Resolve the signer with `uv run python scripts/modal_identity.py`. Use its output verbatim; never guess a handle.
- Set `addedBy` on the spike frontmatter when creating a new spike, and on each new entry in `sources.json` when adding sources.
- Do not modify existing `addedBy` values. If you refresh someone else's spike or source, leave their signature in place.
- If `scripts/modal_identity.py` fails, pause and ask the user to authenticate to the `modal-labs` workspace before writing anything that would need a signature.

## Topic selection

- Favor topics that help Modal engineers and customers reason about the systems they build on or around, with an emphasis on training, inference, and platform infrastructure.
- Prefer systems and implementation angles over generic literature reviews.
- When a spike could be written generically or with concrete product context, choose the version that names the real tradeoff a Modal reader will face.

## Content bar

- Every spike should explain why the topic matters.
- Every spike should include a theme, a concise overview, and a suggested reading order.
- Every source entry should have a summary and a clear note about why it matters.
- Do not pad the page with low-signal sources just to increase count.

## Validation and deploy

- Run `uv run reading site validate` before building.
- Run `npm run build` before deploying (optional smoke test; the Modal image rebuilds from scratch on deploy).
- Deploy with `uv run modal deploy modal_app.py`. This publishes to the `reading-site` app in the `modal-labs` workspace and serves at `https://modal-labs--read.modal.run`.
- Deploys from a different Modal workspace will fork a new parallel deployment at a different URL rather than updating the shared site. Always confirm the active profile first.
