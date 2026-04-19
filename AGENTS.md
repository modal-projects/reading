# Reading Repo Instructions

This repository is an agent-native workspace for researching and publishing reading spikes. The site is meant for engineers working in the `modal-labs` Modal workspace.

## Workflow

- Use `jj` or `git` for version control.
- Use the repo-local Nix shell for tooling. Prefer `nix develop -c ...` for one-off commands. If `nix` is unavailable on your machine, `uv` and `npm` work directly as long as the versions roughly match `flake.nix` and `.nvmrc`.
- Use `uv` for Python dependency management and keep `uv.lock` checked in.
- Do not rely on the system Node/npm/Python toolchain when repo-local alternatives exist.
- The site is deployed from the `modal-labs` Modal workspace. Confirm `modal profile current` returns `modal-labs` before running any `modal` commands, and use `modal profile activate modal-labs` if it does not.

## Spike authoring contract

- If the user asks for a new spike, use the repo-local skills under `.agents/skills/`.
- Start by scaffolding the spike with `uv run reading spike create "<topic>"`.
- Research on the open web using primary sources when possible.
- Prefer papers, official docs, and strong engineering blogs over secondary summaries.
- Mirror canonical PDFs into `public/spikes/<slug>/assets/` when possible.
- Keep spike URLs stable. Refresh existing spikes in place instead of creating duplicate topics.

## Topic selection

- Favor topics that help Modal engineers and customers reason about the systems they build on or around, with an emphasis on training, inference, and platform infrastructure.
- Prefer systems and implementation angles over generic literature reviews.
- When a spike could be written generically or with concrete product context, choose the version that names the real tradeoff a reader will face.
- If prior internal context (planning docs, design notes, customer asks) is available, use it to sharpen the framing rather than defaulting to an outsider's take.

## Content bar

- Every spike should explain why the topic matters.
- Every spike should include a theme, a concise overview, and a suggested reading order.
- Every source entry should have a summary and a clear note about why it matters.
- Do not pad the page with low-signal sources just to increase count.

## Validation and deploy

- Run `uv run reading site validate` before building.
- Run `npm run build` before deploying (optional smoke test; the Modal image rebuilds from scratch on deploy).
- Deploy with `uv run modal deploy modal_app.py`. This publishes to the `reading-site` app in the `modal-labs` workspace and serves at `https://modal-labs--reading.modal.run`.
- Deploys from a different Modal workspace will fork a new parallel deployment at a different URL rather than updating the shared site. Always confirm the active profile first.
