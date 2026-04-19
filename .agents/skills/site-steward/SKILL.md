---
name: site-steward
description: Validate, build, and deploy the reading site after content changes. Use when a spike is done and the site needs verification or Modal deployment.
---

# Site Steward

## Goal

Keep the site coherent and deployable, and push updates to the shared Modal deployment in the `modal-labs` workspace.

## Workflow

1. Run `uv sync` if the Python environment is not ready. Prefer `nix develop -c uv sync` when `nix` is available; fall back to `uv sync` directly otherwise.
2. Run `npm ci` if `node_modules/` is missing (same Nix preference).
3. Run `uv run reading site validate`. Fix all errors before continuing.
4. Run `npm run build` as a local smoke test (the Modal image rebuilds from scratch on deploy, but a failing local build means a failing deploy).
5. **Deploy to Modal.** Always verify the active workspace first:
   - Run `uv run modal profile current`.
   - If the output is exactly `modal-labs`, continue: `uv run modal deploy modal_app.py`.
   - If the output is anything else, **do not deploy.** Stop and tell the user which workspace is active and ask them to confirm or run `modal profile activate modal-labs` before you retry. Deploying from the wrong workspace forks a parallel deployment at a different URL instead of updating the shared site.
6. After a successful deploy, report the URL that `modal deploy` printed (expected: `https://modal-labs--reading.modal.run`) and the dashboard link so the user can verify the new revision landed.

## Rules

- Validate before building.
- Build before deploying.
- Never run `modal deploy` without first confirming `modal profile current` returns `modal-labs`.
- Do not attempt to change the user's Modal profile yourself. If the active profile is wrong, ask — do not silently switch it.
- If a PDF path is missing, fix it or remove the embed path from `sources.json`.
- Always run `modal deploy` from the repo root so the `add_local_dir` in `modal_app.py` picks up the right tree.

## References

- See `references/deploy-checklist.md` for the final pre-deploy checklist.
