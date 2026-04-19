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
6. **Evict the warm container.** A fresh deploy creates a new image revision, but any warm container from the previous revision keeps serving stale HTML until it scales down on its own. Always force the flip after deploy:
   - Run `uv run modal container list` and find the task whose app is `reading-site` (rows look like `ta-<id> │ ap-<id> │ reading-site`).
   - Run `uv run modal container stop --yes <task-id>` for that task. If there are multiple `reading-site` tasks, stop all of them.
   - If there are no `reading-site` tasks listed, skip this step — the site has already scaled to zero and the next request will cold-start on the new image.
7. **Verify the live URL.** Wait a few seconds for a new container to start, then `curl -sI https://modal-labs--read.modal.run/` and `curl -s https://modal-labs--read.modal.run/ | rg -o "<spike-slug>"` to confirm the new content is actually being served. If the old HTML is still coming back, re-run step 6 — sometimes a second container spins up during the eviction window.
8. Report the URL that `modal deploy` printed (expected: `https://modal-labs--read.modal.run`) and the dashboard link (`https://modal.com/apps/modal-labs/main/deployed/reading-site`) so the user can verify the new revision landed.

## Rules

- Validate before building.
- Build before deploying.
- Never run `modal deploy` without first confirming `modal profile current` returns `modal-labs`.
- Do not attempt to change the user's Modal profile yourself. If the active profile is wrong, ask — do not silently switch it.
- If a PDF path is missing, fix it or remove the embed path from `sources.json`.
- Always run `modal deploy` from the repo root so the `add_local_dir` in `modal_app.py` picks up the right tree.
- A deploy is not done until step 7's `curl` shows the new content. Do not report success on `modal deploy` exit code alone — past deploys have returned 0 while a warm container from the previous revision kept serving stale HTML.

## References

- See `references/deploy-checklist.md` for the final pre-deploy checklist.
