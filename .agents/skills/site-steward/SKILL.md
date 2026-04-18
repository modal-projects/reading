---
name: site-steward
description: Validate, build, and deploy the reading site after content changes. Use when a spike is done and the site needs verification or Modal deployment.
---

# Site Steward

## Goal

Keep the site coherent and deployable.

## Workflow

1. Run `nix develop -c uv sync` if the Python environment is not ready.
2. Run `nix develop -c npm ci` if frontend dependencies are missing.
3. Run `nix develop -c uv run reading site validate`.
4. Run `nix develop -c npm run build`.
5. For deploys:
   - `source ~/.codex/modal.env`
   - `nix develop -c uv run modal deploy modal_app.py`

## Rules

- Validate before building.
- Build before deploy.
- If a PDF path is missing, fix it or remove the embed path from `sources.json`.

## References

- See `references/deploy-checklist.md` for the final pre-deploy checklist.
